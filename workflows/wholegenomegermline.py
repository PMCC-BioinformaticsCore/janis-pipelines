import unittest

from janis import Input, String, Step, Directory, Workflow, Array, Output
import janis.bioinformatics as jb

from janis_bioinformatics.data_types import FastaWithDict, Fastq, VcfIdx, VcfTabix, Fastq, VcfIdx, Vcf, Bed
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.common import AlignSortedBam
from janis_bioinformatics.tools.common.processbam import MergeAndMarkBams_4_0
from janis_bioinformatics.tools.pmac import CombineVariants_0_1_0

from janis_bioinformatics.tools.variantcallers import GatkVariantCaller, StrelkaVariantCaller, VardictVariantCaller

BcfToolsNorm = jb.tools.bcftools.BcfToolsNormLatest


class WholeGenomeGermlineWorkflow(Workflow):

    @staticmethod
    def version():
        return "1.0.0"

    def __init__(self):
        Workflow.__init__(self, "whole_genome_germline")


        fastqInputs = Input("fastqs", Array(Fastq()), [[
            "/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/BRCA1_R1.fastq.gz",
            "/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/BRCA1_R2.fastq.gz"
        ]])
        bedIntervals = Input("bedIntervals", Bed(), "/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/BRCA1.bed")

        reference = Input("reference", FastaWithDict(), "/Users/franklinmichael/reference/hg38/"
                                                        "assembly_contigs_renamed/Homo_sapiens_assembly38.fasta")

        s1_inp_header = Input("readGroupHeaderLine", String(),
                              "'@RG\\tID:NA12878\\tSM:NA12878\\tLB:NA12878\\tPL:ILLUMINA'")
        snps_dbsnp = Input("snps_dbsnp", VcfTabix(), "/Users/franklinmichael/reference/hg38/dbsnp_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz")
        snps_1000gp = Input("snps_1000gp", VcfTabix(), "/Users/franklinmichael/reference/hg38/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz")
        known_indels = Input("known_indels", VcfTabix(), "/Users/franklinmichael/reference/hg38/known_indels_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz")
        mills_indels = Input("mills_1000gp_indels", VcfTabix(), "/Users/franklinmichael/reference/hg38/mills_indels/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz")
        validator_truth = Input("truthVCF", VcfIdx(), "/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs//BRCA1.vcf")
        validator_intervals = Input("intervals", Array(Vcf()), ["/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs//BRCA1.interval_list"])


        s1_sw = Step("s1_alignSortedBam", AlignSortedBam())
        fastqc = Step("fastqc", FastQC_0_11_5())
        s2_process = Step("s2_processBamFiles", MergeAndMarkBams_4_0())

        vc_gatk = Step("variantCaller_GATK", GatkVariantCaller())
        vc_strelka = Step("variantCaller_Strelka", StrelkaVariantCaller())
        # vc_vardict = Step("variantCaller_Vardict", VardictVariantCaller())

        # combine_vcs = Step("combineVariants", CombineVariants_0_1_0())

        # step1
        self.add_edge(fastqInputs, s1_sw.fastq)
        self.add_edges([
            (reference, s1_sw.reference),
            (s1_inp_header, s1_sw.read_group_header_line),
        ])

        # step1 sidestep
        self.add_edge(fastqInputs, fastqc.reads)

        # step2 - process bam files
        self.add_edges([
            (s1_sw.out, s2_process.bams)
        ])

        # VARIANT CALLERS

        # GATK VariantCaller
        self.add_edges([
            (s2_process.out, vc_gatk.bam),
            (bedIntervals, vc_gatk.intervals),
            (reference, vc_gatk.reference),
            (snps_dbsnp, vc_gatk.snps_dbsnp),
            (snps_1000gp, vc_gatk.snps_1000gp),
            (known_indels, vc_gatk.knownIndels),
            (mills_indels, vc_gatk.millsIndels),
        ])

        # Strelka VariantCaller
        self.add_edges([
            (s2_process.out, vc_strelka),
            (reference, vc_strelka)
        ])


        # Output the Variants
        self.add_edges([
            (vc_gatk.out, Output("variants_gatk")),
            (vc_strelka.out, Output("variants_strelka"))
        ])

        # Combine
        self.add_edges([
            # (vc_gatk.out, combine_vcs.vcfs)
        ])

        # Outputs

        self.add_edges([
            (s2_process.out, Output("bam")),
            (fastqc.out, Output("reports")),
            (vc_gatk, Output("gatk_variants"))
        ])


if __name__ == "__main__":
    import shepherd

    wf = WholeGenomeGermlineWorkflow()
    wdl = wf.dump_translation("wdl", to_console=False, to_disk=True, write_inputs_file=True)
    #
    # config = shepherd.CromwellConfiguration(
    #     database=shepherd.CromwellConfiguration.Database.mysql("cromwelluser", "cromwell-pass")
    # )
    #
    # task = shepherd.from_janis(wf, engine=shepherd.Cromwell(config=config))
    # # task = shepherd.from_janis(wf, engine=shepherd.CWLTool())
    #
    # print(task.outputs)













#         # AWS INPUTS
#         fastqInputs = Input("fastqs", Array(Fastq()), [[
#             "s3://pmac-cromwell/wgs/BRCA1_R1.fastq",
#             "s3://pmac-cromwell/wgs/BRCA1_R2.fastq"]])
#
#         s1_inp_header = Input("readGroupHeaderLine", String(),
#                               "'@RG\\tID:NA12878\\tSM:NA12878\\tLB:NA12878\\tPL:ILLUMINA'")
#         validator_truth = Input("truthVCF", VcfIdx(), "s3://pmac-cromwell/wgs/BRCA1.vcf")
#         validator_intervals = Input("intervals", Array(Vcf()), ["s3://pmac-cromwell/wgs/BRCA1.interval_list"])
#
#         reference = Input("reference", FastaWithDict(), "s3://pmac-cromwell/reference/Homo_sapiens_assembly38.fasta")
#
#         snps_dbsnp = Input("snps_dbsnp", VcfIdx(), "s3://pmac-cromwell/reference/Homo_sapiens_assembly38.dbsnp138.vcf")
#         snps_dbsnp_gz = Input("snps_dbsnp_gz", VcfTabix(),
#                               "s3://pmac-cromwell/reference/Homo_sapiens_assembly38.dbsnp138.vcf.gz")
#         snps_1000gp = Input("snps_1000gp", VcfTabix(),
#                             "s3://pmac-cromwell/reference/1000G_phase1.snps.high_confidence.hg38.vcf.gz")
#         omni = Input("omni", VcfTabix(), "s3://pmac-cromwell/reference/1000G_omni2.5.hg38.vcf.gz")
#         hapmap = Input("hapmap", VcfTabix(), "s3://pmac-cromwell/reference/hapmap_3.3.hg38.vcf.gz")
#
#
#         # GCP INPUTS
#         # fastqInputs = Input("fastqs", Array(Fastq()), [[
#         #     "gs://pmccromwelltests/wgs-inputs/BRCA1_R1.fastq",
#         #     "gs://pmccromwelltests/wgs-inputs/BRCA1_R2.fastq"]])
#         #
#         # s1_inp_header = Input("readGroupHeaderLine", String(),
#         #                       "'@RG\\tID:NA12878\\tSM:NA12878\\tLB:NA12878\\tPL:ILLUMINA'")
#         # validator_truth = Input("truthVCF", VcfIdx(), "gs://pmccromwelltests/wgs-inputs/BRCA1.vcf")
#         # validator_intervals = Input("intervals", Array(Vcf()), ["gs://pmccromwelltests/wgs-inputs/BRCA1.interval_list"])
#         #
#         # reference = Input("reference", FastaWithDict(), "gs://pmccromwelltests/reference/assembly/Homo_sapiens_assembly38.fasta")
#         #
#         # snps_dbsnp = Input("snps_dbsnp", VcfIdx(), "gs://pmccromwelltests/reference/snps_dbsnp/Homo_sapiens_assembly38.dbsnp138.vcf")
#         # snps_dbsnp_gz = Input("snps_dbsnp_gz", VcfTabix(),
#         #                       "gs://pmccromwelltests/reference/snps_dbsnp/Homo_sapiens_assembly38.dbsnp138.vcf.gz")
#         # snps_1000gp = Input("snps_1000gp", VcfTabix(),
#         #                     "gs://pmccromwelltests/reference/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz")
#         # omni = Input("omni", VcfTabix(), "gs://pmccromwelltests/reference/omni/1000G_omni2.5.hg38.vcf.gz")
#         # hapmap = Input("hapmap", VcfTabix(), "gs://pmccromwelltests/reference/hapmap/hapmap_3.3.hg38.vcf.gz")

# GCP INPUTS
# fastqInputs = Input("fastqs", Array(Fastq()), [[
#     "gs://pmccromwelltests/wgs-inputs/BRCA1_R1.fastq",
#     "gs://pmccromwelltests/wgs-inputs/BRCA1_R2.fastq"]])
#
# s1_inp_header = Input("readGroupHeaderLine", String(),
#                       "'@RG\\tID:NA12878\\tSM:NA12878\\tLB:NA12878\\tPL:ILLUMINA'")
# validator_truth = Input("truthVCF", VcfIdx(), "gs://pmccromwelltests/wgs-inputs/BRCA1.vcf")
# validator_intervals = Input("intervals", Array(Vcf()), ["gs://pmccromwelltests/wgs-inputs/BRCA1.interval_list"])
#
# reference = Input("reference", FastaWithDict(), "gs://pmccromwelltests/reference/assembly/Homo_sapiens_assembly38.fasta")
#
# snps_dbsnp = Input("snps_dbsnp", VcfIdx(), "gs://pmccromwelltests/reference/snps_dbsnp/Homo_sapiens_assembly38.dbsnp138.vcf")
# snps_dbsnp_gz = Input("snps_dbsnp_gz", VcfTabix(),
#                       "gs://pmccromwelltests/reference/snps_dbsnp/Homo_sapiens_assembly38.dbsnp138.vcf.gz")
# snps_1000gp = Input("snps_1000gp", VcfTabix(),
#                     "gs://pmccromwelltests/reference/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz")
# known_indels = Input("known_indels", VcfTabix(), "gs://pmccromwelltests/reference/known_indels/1000G_omni2.5.hg38.vcf.gz")
# mills_1000gp_indels = Input("mills_1000gp_indels", VcfTabix(), "gs://pmccromwelltests/reference/mills_1000gp_indels/hapmap_3.3.hg38.vcf.gz")
#
#
#
#
#
#
#         ## DEFAULTS
#
#         # reference = Input("reference", FastaWithDict())
#         # fastqInputs = Input("fastqs", Array(Fastq()))
#         #
#         # s1_inp_header = Input("readGroupHeaderLine", String())
#         # snps_dbsnp = Input("snps_dbsnp", VcfIdx())
#         # snps_dbsnp_gz = Input("snps_dbsnp_gz", VcfTabix())
#         # snps_1000gp = Input("snps_1000gp", VcfTabix())
#         # omni = Input("omni", VcfTabix())
#         # hapmap = Input("hapmap", VcfTabix())
#         # validator_truth = Input("truthVCF", VcfIdx())
#         # validator_intervals = Input("intervals", Array(Vcf()))
#         #
