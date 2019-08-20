from janis_core import Input, String, Step, Array, Output

from janis_bioinformatics.data_types import FastaWithDict, VcfTabix, Fastq, Bed
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import AlignSortedBam, MergeAndMarkBams_4_0
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_0
from janis_bioinformatics.tools.variantcallers import GatkGermlineVariantCaller


class WGSGermlineGATK(BioinformaticsWorkflow):

    @staticmethod
    def version():
        return "1.0.0"

    def __init__(self):

        BioinformaticsWorkflow.__init__(self, "WGSGermlineGATK", "WGS Germline (GATK only)")

        fastqInputs = Input("fastqs", Array(Fastq()))
        reference = Input("reference", FastaWithDict())

        gatk_intervals = Input("gatkIntervals", Array(Bed()))

        sample_name = Input("sampleName", String(), "NA12878")

        snps_dbsnp = Input("snps_dbsnp", VcfTabix())
        snps_1000gp = Input("snps_1000gp", VcfTabix())
        known_indels = Input("known_indels", VcfTabix())
        mills_indels = Input("mills_1000gp_indels", VcfTabix())

        s1_sw = Step("alignSortedBam", AlignSortedBam())
        fastqc = Step("fastqc", FastQC_0_11_5())
        s2_process = Step("processBamFiles", MergeAndMarkBams_4_0())

        vc_gatk = Step("variantCaller_GATK", GatkGermlineVariantCaller())

        vc_merge_gatk = Step("variantCaller_merge_GATK", Gatk4GatherVcfs_4_0())
        sort_combined_vcfs = Step("sortCombined", BcfToolsSort_1_9())

        # step1
        self.add_edge(fastqInputs, s1_sw.fastq)
        self.add_edges([
            (reference, s1_sw.reference),
            (sample_name, s1_sw.sampleName),
        ])

        # step1 sidestep
        self.add_edge(fastqInputs, fastqc.reads)

        # step2 - process bam files
        self.add_edges([
            (s1_sw.out, s2_process.bams)
        ])

        # VARIANT CALLERS

        # GATK VariantCaller + Merge
        self.add_edges([
            (s2_process.out, vc_gatk.bam),
            (gatk_intervals, vc_gatk.intervals),
            (reference, vc_gatk.reference),
            (snps_dbsnp, vc_gatk.snps_dbsnp),
            (snps_1000gp, vc_gatk.snps_1000gp),
            (known_indels, vc_gatk.knownIndels),
            (mills_indels, vc_gatk.millsIndels),

            (vc_gatk.out, vc_merge_gatk.vcfs)
        ])

        # Sort variants
        self.add_edge(vc_merge_gatk.out, sort_combined_vcfs.vcf)

        # Outputs

        self.add_edges([
            (s2_process.out, Output("bam")),
            (fastqc.out, Output("reports")),
            (sort_combined_vcfs.out, Output("variants")),
            (vc_gatk.out, Output("scattered_variants")),
        ])


if __name__ == "__main__":
    w = WGSGermlineGATK()
    w.translate("cwl", to_console=False, to_disk=True, export_path="{language}")
    w.translate("wdl", to_console=False, to_disk=True, export_path="{language}")
