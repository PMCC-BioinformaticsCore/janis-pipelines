from datetime import datetime
from janis_core import (
    Array,
    String,
    Int,
    StringFormatter,
    File,
    Directory,
    WorkflowMetadata,
    ScatterDescription,
    ScatterMethod,
    WorkflowBuilder,
)

from janis_bioinformatics.data_types import FastqGzPair
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow

# Tools
from janis_unix.tools.localisefolder import LocaliseFolder
from janis_bioinformatics.tools.gatk4 import Gatk4SortSam_4_1_2
from janis_bioinformatics.tools.htseq import HTSeqCount_1_99_2
from janis_bioinformatics.tools.star import StarAlignReads_2_7_8


class RNASeqGeneExpressionQuantificationByRun(BioinformaticsWorkflow):
    def id(self):
        return "RNASeqGeneExpressionQuantificationByRun"

    def friendly_name(self):
        return "RNASeq Gene Expression and Quantification (Per Run)"

    def version(self):
        return "1.0.0"

    def constructor(self):

        # Inputs
        self.input("fastqs_list", Array(FastqGzPair))
        self.input("sample_name_list", Array(String))

        # References
        self.input("gtf", File)
        self.input("star_ref_genome", Directory)

        # Configuration
        self.input("star_threads", Int, default=8)

        # Steps
        self.step(
            "localise_star_genome",
            LocaliseFolder(dir=self.star_ref_genome),
        )
        self.step(
            "single_sample_workflow",
            self.process_subpipeline(
                fastqs=self.fastqs_list,
                sample_name=self.sample_name_list,
                gtf=self.gtf,
                star_ref_genome=self.localise_star_genome.out,
                star_threads=self.star_threads,
            ),
            scatter=ScatterDescription(
                ["fastqs", "sample_name"],
                method=ScatterMethod.dot,
                labels=self.sample_name_list,
            ),
        )

    @staticmethod
    def process_subpipeline(**connections):
        w = WorkflowBuilder("sample_subpipeline")
        w.input("fastqs", FastqGzPair)
        w.input("sample_name", String)
        w.input("gtf", File)
        w.input("star_ref_genome", Directory)
        w.input("star_threads", Int, default=8)

        w.step(
            "star_alignment",
            StarAlignReads_2_7_8(
                readFilesIn=w.fastqs,
                outSAMattrRGline=[
                    StringFormatter("ID:{sample}", sample=w.sample_name),
                    StringFormatter("SM:{sample}", sample=w.sample_name),
                    StringFormatter("LB:{sample}", sample=w.sample_name),
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
                genomeDir=w.star_ref_genome,
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
                runThreadN=w.star_threads,
                twopassMode="Basic",
            ),
        )
        w.output(
            "out_transcriptome_bam",
            source=w.star_alignment.out_transcriptome_bam.assert_not_null(),
        )
        w.output(
            "out_chimeric_out_junction",
            source=w.star_alignment.out_chimeric_out_junction.assert_not_null(),
        )
        w.output(
            "out_chimeric_out_sam",
            source=w.star_alignment.out_chimeric_out_sam.assert_not_null(),
        )
        w.output(
            "out_gene_counts",
            source=w.star_alignment.out_gene_counts.assert_not_null(),
        )

        w.step(
            "sortsam",
            Gatk4SortSam_4_1_2(
                bam=w.star_alignment.out_unsorted_bam.assert_not_null(),
                sortOrder="coordinate",
                createIndex=True,
                validationStringency="SILENT",
                maxRecordsInRam=5000000,
                tmpDir=".",
            ),
        )
        w.output("out_bam", source=w.sortsam.out)

        w.step(
            "htseq_count",
            HTSeqCount_1_99_2(
                bams=[w.star_alignment.out_unsorted_bam.assert_not_null()],
                gff_file=w.gtf,
                format="bam",
                order="name",
                stranded="no",
                minaqual=10,
                type="exon",
                id="gene_id",
                mode="intersection-nonempty",
            ),
        )
        w.output("out_htseq_count", source=w.htseq_count.out)


if __name__ == "__main__":
    RNASeqGeneExpressionQuantificationByRun().translate(
        "wdl", allow_empty_container=True
    )
