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

from janis_bioinformatics.data_types import (
    CompressedVcf,
    Fasta,
    FastaWithDict,
    FastqGzPair,
)
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow

from janis_bioinformatics.tools.arriba import RunArriba_2_1_0, ArribaDrawFusions_2_1_0
from janis_bioinformatics.tools.bcftools import (
    BcfToolsFillFromFasta_1_12,
    BcfToolsSort_1_9,
)
from janis_bioinformatics.tools.gatk4 import Gatk4SortSam_4_1_2
from janis_bioinformatics.tools.pmac import MegaFusion_0_1_2, ReplaceNFusionVcf_0_1_2
from janis_bioinformatics.tools.rnaseqqc import RNASeqQC_2_3_5
from janis_bioinformatics.tools.star import StarAlignReads_2_7_8


class RNASeqFusion(BioinformaticsWorkflow):
    def id(self):
        return "RNASeqFusion"

    def friendly_name(self):
        return "RNASeq Fusion"

    def version(self):
        return "1.0.0"

    def constructor(self):

        # Inputs
        self.input("sample_name", String)
        self.input("fastqs", FastqGzPair)

        # References
        self.input("reference", FastaWithDict)
        self.input("annotation_gtf", File)
        self.input("star_ref_genome", Directory)
        self.input("arriba_blacklist", File)
        self.input("arriba_known_fusions", File)
        self.input("arriba_protein_domains_gff", File)
        self.input("arriba_cytobands", File)
        self.input("qc_annotation_gtf", File)

        # Internal
        self.input("fusion_tsv_json", File)
        self.input("reference_contig_file", File)
        self.input("column_name", String(optional=True), default="REF")
        self.input("tool_version", String(optional=True), default="2.1.0")

        # Configuration
        self.input("star_threads", Int, default=8)

        # Pipeline
        self.add_alignment_step()
        self.add_fusion_step()
        self.add_sort_and_index_step()
        self.add_rnaseq_qc_step()
        self.add_fusion_plot_step()
        self.add_fusion_tsv_to_vcf_step()

    # Steps
    def add_alignment_step(self):
        self.step(
            "star_alignment",
            StarAlignReads_2_7_8(
                runThreadN=self.star_threads,
                genomeDir=self.star_ref_genome,
                genomeLoad="NoSharedMemory",
                readFilesIn=self.fastqs,
                readFilesCommand="zcat",
                outSAMtype=["BAM", "Unsorted"],
                outSAMunmapped="Within",
                outBAMcompression=0,
                outFilterMultimapNmax=50,
                peOverlapNbasesMin=10,
                alignSplicedMateMapLminOverLmate=0.5,
                alignSJstitchMismatchNmax=[5, -1, 5, 5],
                chimSegmentMin=10,
                chimOutType=["WithinBAM", "HardClip"],
                chimJunctionOverhangMin=10,
                chimScoreDropMax=30,
                chimScoreJunctionNonGTAG=0,
                chimScoreSeparation=1,
                chimSegmentReadGapMax=3,
                chimMultimapNmax=50,
            ),
        )

    def add_fusion_step(self):
        self.step(
            "arriba",
            RunArriba_2_1_0(
                aligned_inp=self.star_alignment.out_unsorted_bam.assert_not_null(),
                reference=self.reference,
                gtf_file=self.annotation_gtf,
                blacklist=self.arriba_blacklist,
                known_fusions=self.arriba_known_fusions,
                tag_tsv=self.arriba_known_fusions,
                protein_domains_gff=self.arriba_protein_domains_gff,
            ),
        )
        self.output(
            "out",
            source=self.arriba.out,
            output_folder=[
                self.sample_name,
            ],
            output_name=StringFormatter(
                "{sample_name}_fusions", sample_name=self.sample_name
            ),
        )
        self.output(
            "out_discarded",
            source=self.arriba.out_discarded,
            output_folder=[
                self.sample_name,
            ],
            output_name=StringFormatter(
                "{sample_name}_fusions_discarded", sample_name=self.sample_name
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
            output_folder=[
                self.sample_name,
            ],
            output_name=self.sample_name,
        )

    def add_rnaseq_qc_step(self):
        self.step(
            "rnaseq_qc",
            RNASeqQC_2_3_5(
                gtf=self.qc_annotation_gtf,
                bam=self.sortsam.out,
                sample=self.sample_name,
                coverage=True,
                coverage_mask=0,
            ),
        )
        self.output(
            "out_gene_fragments",
            source=self.rnaseq_qc.out_gene_fragments,
            output_folder=[
                self.sample_name,
                "QC",
                "RNASeqQC",
            ],
            output_name=StringFormatter(
                "{sample}.gene_fragments",
                sample=self.sample_name,
            ),
        ),
        self.output(
            "out_gene_reads",
            source=self.rnaseq_qc.out_gene_reads,
            output_folder=[
                self.sample_name,
                "QC",
                "RNASeqQC",
            ],
            output_name=StringFormatter(
                "{sample}.gene_reads",
                sample=self.sample_name,
            ),
        ),
        self.output(
            "out_gene_tpm",
            source=self.rnaseq_qc.out_gene_tpm,
            output_folder=[
                self.sample_name,
                "QC",
                "RNASeqQC",
            ],
            output_name=StringFormatter(
                "{sample}.gene_tpm",
                sample=self.sample_name,
            ),
        ),
        self.output(
            "out_metrics",
            source=self.rnaseq_qc.out_metrics_tsv,
            output_folder=[
                self.sample_name,
                "QC",
                "RNASeqQC",
            ],
            output_name=StringFormatter(
                "{sample}_QC_metrics",
                sample=self.sample_name,
            ),
        )
        self.output(
            "out_coverage",
            source=self.rnaseq_qc.out_coverage_tsv,
            output_folder=[
                self.sample_name,
                "QC",
                "RNASeqQC",
            ],
            output_name=StringFormatter(
                "{sample}_gene_coverage",
                sample=self.sample_name,
            ),
        ),
        self.output(
            "out_exon_reads",
            source=self.rnaseq_qc.out_exon_reads,
            output_folder=[
                self.sample_name,
                "QC",
                "RNASeqQC",
            ],
            output_name=StringFormatter(
                "{sample}.exon_reads",
                sample=self.sample_name,
            ),
        ),

    def add_fusion_plot_step(self):
        self.step(
            "fusion_plot",
            ArribaDrawFusions_2_1_0(
                fusions=self.arriba.out,
                alignments=self.sortsam.out,
                annotation=self.annotation_gtf,
                cytobands=self.arriba_cytobands,
                proteinDomains=self.arriba_protein_domains_gff,
            ),
        )
        self.output(
            "out_plot",
            source=self.fusion_plot.out,
            output_folder=[
                self.sample_name,
            ],
            output_name=StringFormatter(
                "{sample_name}_fusions", sample_name=self.sample_name
            ),
        )

    def add_fusion_tsv_to_vcf_step(self):
        self.step(
            "megafusion",
            MegaFusion_0_1_2(
                sample=self.sample_name,
                json=self.fusion_tsv_json,
                fusion=self.arriba.out,
                contig=self.reference_contig_file,
                toolVersion=self.tool_version,
            ),
        )
        self.step("sort_vcf", BcfToolsSort_1_9(vcf=self.megafusion.out))
        self.step(
            "fill_from_fasta",
            BcfToolsFillFromFasta_1_12(
                fasta=self.reference.as_type(Fasta),
                column=self.column_name,
                vcf=self.sort_vcf.out.as_type(CompressedVcf),
            ),
        )
        self.step(
            "replace_n_fusion_vcf",
            ReplaceNFusionVcf_0_1_2(
                vcf=self.fill_from_fasta.out,
            ),
        )
        self.output(
            "vcf",
            source=self.replace_n_fusion_vcf.out,
            output_folder=[
                self.sample_name,
            ],
            output_name=StringFormatter(
                "{sample_name}_fusions", sample_name=self.sample_name
            ),
        )

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = [
            "rna-seq",
            "fusion",
            "star",
            "arriba",
        ]
        meta.contributors = ["Jiaan Yu"]

        meta.short_documentation = "A RNA-Seq fusion pipeline using STAR and Arriba."
        meta.documentation = """\
This workflow is a reference pipeline using the Janis Python framework (pipelines assistant).
- Alignment with STAR
- Fusion calling with Arriba
- Output the fusions in VCF and TSV format
"""


if __name__ == "__main__":
    RNASeqFusion().translate("wdl")
