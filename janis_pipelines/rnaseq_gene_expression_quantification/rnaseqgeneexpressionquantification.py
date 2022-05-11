from datetime import datetime
from janis_core import (
    Array,
    String,
    Int,
    StringFormatter,
    File,
    Directory,
    WorkflowMetadata,
)

from janis_bioinformatics.data_types import FastqGzPair
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow

# Tools
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_8
from janis_bioinformatics.tools.gatk4 import Gatk4SortSam_4_1_2
from janis_bioinformatics.tools.htseq import HTSeqCount_1_99_2
from janis_bioinformatics.tools.star import StarAlignReads_2_7_8
from janis_bioinformatics.tools.rnaseqqc import RNASeqQC_2_3_5


class RNASeqGeneExpressionQuantification(BioinformaticsWorkflow):
    def id(self):
        return "RNASeqGeneExpressionQuantification"

    def friendly_name(self):
        return "RNASeq Gene Expression and Quantification"

    def version(self):
        return "1.0.0"

    def constructor(self):

        # Inputs
        self.input("fastqs", FastqGzPair)
        self.input("sample_name", String)

        # References
        self.input("gtf", File)
        self.input("star_ref_genome", Directory)
        # self.input("qc_gtf", File)

        # Configuration
        self.input("star_threads", Int, default=8)

        # Pipeline
        self.add_fastqc_step()
        self.add_alignment_step()
        self.add_sort_and_index_step()
        # self.add_rnaseq_qc_step()
        self.add_counts_step()

    # Steps
    def add_fastqc_step(self):
        self.step("fastqc", FastQC_0_11_8(reads=self.fastqs))
        self.output(
            "out_fastqc_R1_reports",
            source=self.fastqc.out_R1,
            output_folder=[self.sample_name, "QC", "FASTQC"],
            doc="A zip file of the FastQC quality report.",
        )
        self.output(
            "out_fastqc_R2_reports",
            source=self.fastqc.out_R2,
            output_folder=[self.sample_name, "QC", "FASTQC"],
            doc="A zip file of the FastQC quality report.",
        )

    def add_alignment_step(self):
        self.step(
            "star_alignment",
            StarAlignReads_2_7_8(
                readFilesIn=self.fastqs,
                outSAMattrRGline=[
                    StringFormatter("ID:{sample_name}", sample_name=self.sample_name),
                    StringFormatter("SM:{sample_name}", sample_name=self.sample_name),
                    StringFormatter("LB:{sample_name}", sample_name=self.sample_name),
                    StringFormatter("PL:ILLUMINA"),
                ],
                alignIntronMax=1000000,
                alignIntronMin=20,
                alignMatesGapMax=1000000,
                alignSJDBoverhangMin=1,
                alignSJoverhangMin=8,
                alignSoftClipAtReferenceEnds="Yes",
                chimJunctionOverhangMin=15,
                chimMainSegmentMultNmax=1,
                # Some redundancy in output files, are they required?
                chimOutType=["Junctions", "SeparateSAMold", "WithinBAM", "SoftClip"],
                chimSegmentMin=15,
                genomeDir=self.star_ref_genome,
                genomeLoad="NoSharedMemory",
                limitSjdbInsertNsj=1200000,
                outFilterIntronMotifs="None",
                outFilterMatchNminOverLread=0.33,
                outFilterMismatchNmax=999,
                outFilterMismatchNoverLmax=0.1,
                outFilterMultimapNmax=20,
                outFilterScoreMinOverLread=0.33,
                outFilterType="BySJout",
                outSAMattributes=["NH", "HI", "AS", "nM", "NM", "ch"],
                outSAMstrandField="intronMotif",
                outSAMtype=["BAM", "Unsorted"],
                outSAMunmapped="Within",
                quantMode=["TranscriptomeSAM", "GeneCounts"],
                readFilesCommand="zcat",
                runThreadN=self.star_threads,
                twopassMode="Basic",
            ),
        )
        self.output(
            "transcriptome_bam",
            source=self.star_alignment.out_transcriptome_bam.assert_not_null(),
            output_folder=[self.sample_name],
            output_name=StringFormatter(
                "{sample_name}.toTranscriptome.out", sample_name=self.sample_name
            ),
        )
        self.output(
            "chimeric_out_junction",
            source=self.star_alignment.out_chimeric_out_junction.assert_not_null(),
            output_folder=[self.sample_name],
            output_name=StringFormatter(
                "{sample_name}.Chimeric.out", sample_name=self.sample_name
            ),
        )
        self.output(
            "chimeric_out_sam",
            source=self.star_alignment.out_chimeric_out_sam.assert_not_null(),
            output_folder=[self.sample_name],
            output_name=StringFormatter(
                "{sample_name}.Chimeric.out", sample_name=self.sample_name
            ),
        )
        self.output(
            "gene_counts",
            source=self.star_alignment.out_gene_counts.assert_not_null(),
            output_folder=[self.sample_name],
            output_name=StringFormatter(
                "{sample_name}.STAR.ReadsPerGene.out", sample_name=self.sample_name
            ),
        )

    def add_sort_and_index_step(self):
        self.step(
            "sortsam",
            Gatk4SortSam_4_1_2(
                bam=self.star_alignment.out_unsorted_bam.assert_not_null(),
                sortOrder="coordinate",
                createIndex=True,
                validationStringency="SILENT",
                maxRecordsInRam=5000000,
                tmpDir=".",
            ),
        )
        self.output(
            "bam",
            source=self.sortsam.out,
            output_folder=[self.sample_name],
            output_name=self.sample_name,
        )

    def add_rnaseq_qc_step(self):
        self.step(
            "rnaseq_qc",
            RNASeqQC_2_3_5(
                gtf=self.gtf,
                bam=self.sortsam.out,
                sample=self.sample_name,
                coverage=True,
                coverage_mask=0,
            ),
        )
        self.output(
            "out_gene_fragments",
            source=self.rnaseq_qc.out_gene_fragments,
            output_folder=[self.sample_name, "QC", "RNASeqQC"],
            output_name=StringFormatter(
                "{sample}.gene_fragments",
                sample=self.sample_name,
            ),
        ),
        self.output(
            "out_gene_reads",
            source=self.rnaseq_qc.out_gene_reads,
            output_folder=[self.sample_name, "QC", "RNASeqQC"],
            output_name=StringFormatter(
                "{sample}.gene_reads",
                sample=self.sample_name,
            ),
        ),
        self.output(
            "out_gene_tpm",
            source=self.rnaseq_qc.out_gene_tpm,
            output_folder=[self.sample_name, "QC", "RNASeqQC"],
            output_name=StringFormatter(
                "{sample}.gene_tpm",
                sample=self.sample_name,
            ),
        ),
        self.output(
            "out_metrics",
            source=self.rnaseq_qc.out_metrics_tsv,
            output_folder=[self.sample_name, "QC", "RNASeqQC"],
            output_name=StringFormatter(
                "{sample}_QC_metrics",
                sample=self.sample_name,
            ),
        )
        self.output(
            "out_coverage",
            source=self.rnaseq_qc.out_coverage_tsv,
            output_folder=[self.sample_name, "QC", "RNASeqQC"],
            output_name=StringFormatter(
                "{sample}_gene_coverage",
                sample=self.sample_name,
            ),
        ),
        self.output(
            "out_exon_reads",
            source=self.rnaseq_qc.out_exon_reads,
            output_folder=[self.sample_name, "QC", "RNASeqQC"],
            output_name=StringFormatter(
                "{sample}.exon_reads",
                sample=self.sample_name,
            ),
        ),

    def add_counts_step(self):
        self.step(
            "htseq_count",
            HTSeqCount_1_99_2(
                bams=[self.star_alignment.out_unsorted_bam.assert_not_null()],
                gff_file=self.gtf,
                format="bam",
                order="name",
                stranded="no",
                minaqual=10,
                type="exon",
                id="gene_id",
                mode="intersection-nonempty",
            ),
        )
        self.output(
            "out_htseq_count",
            source=self.htseq_count.out,
            output_folder=[self.sample_name],
            output_name=StringFormatter(
                "{sample_name}.htseq.counts", sample_name=self.sample_name
            ),
        )

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = ["rna-seq", "star", "htseq-count", "expression"]
        meta.contributors = ["Jiaan Yu"]

        meta.short_documentation = (
            "mRNA Analysis Pipeline for Gene Expression and Quantification (GDC)"
        )
        meta.documentation = """\
This workflow is based on GDC. 
- Alignment with STAR
- Gene counts with htseq-count
- Normalised counts: FPKM and FPKM-UQ
https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/
"""


if __name__ == "__main__":
    RNASeqGeneExpressionQuantification().translate("wdl")
