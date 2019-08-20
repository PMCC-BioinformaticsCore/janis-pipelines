from janis_bioinformatics.data_types import FastaWithDict, Fastq, VcfTabix, Bed
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import AlignSortedBam, MergeAndMarkBams_4_0
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_0
from janis_bioinformatics.tools.variantcallers.gatksomatic_variants import GatkSomaticVariantCaller
from janis_core import Input, String, Step, Workflow, Array, Output


class WGSSomaticGATK(BioinformaticsWorkflow):

    def __init__(self):
        BioinformaticsWorkflow.__init__(self, "WGSSomaticGATK", "WGS Somatic (GATK only)")

        normalInputs = Input('normalInputs', Array(Fastq()))
        tumorInputs = Input('tumorInputs', Array(Fastq()))

        normalName = Input("normalName", String(), "NA24385_normal")
        tumorName = Input("tumorName", String(), "NA24385_tumour")

        gatk_intervals = Input("gatkIntervals", Array(Bed()))

        reference = Input('reference', FastaWithDict())
        snps_dbsnp = Input("snps_dbsnp", VcfTabix())
        snps_1000gp = Input("snps_1000gp", VcfTabix())
        known_indels = Input("known_indels", VcfTabix())
        mills_indels = Input("mills_1000gp_indels", VcfTabix())

        s_norm = Step("normal", self.process_subpipeline())
        s_tum = Step("tumor", self.process_subpipeline())

        vc_gatkVariantCaller = Step("GATK_VariantCaller", GatkSomaticVariantCaller())

        vc_merged_gatk = Step("variantCaller_merge_GATK", Gatk4GatherVcfs_4_0())

        sort_combined_vcfs = Step("sortCombined", BcfToolsSort_1_9())
        sortsam_tmpdir = Input("sortSamTmpDir", String(optional=True), "/tmp")

        self.add_edges([
            (normalInputs, s_norm.inputs),
            (normalName, s_norm.sampleName),
            (reference, s_norm.reference),
            (sortsam_tmpdir, s_norm.sortSamTmpDir)
        ])

        self.add_edges([
            (tumorInputs, s_tum.inputs),
            (tumorName, s_tum.sampleName),
            (reference, s_tum.reference),
            (sortsam_tmpdir, s_tum.sortSamTmpDir)
        ])

        # GATK Variant Caller

        self.add_edges([
            (s_norm.out, vc_gatkVariantCaller.normalBam),
            (s_tum.out, vc_gatkVariantCaller.tumorBam),
            (normalName, vc_gatkVariantCaller.normalName),
            (tumorName, vc_gatkVariantCaller.tumorName),

            (gatk_intervals, vc_gatkVariantCaller.intervals),
            (reference, vc_gatkVariantCaller.reference),
            (snps_dbsnp, vc_gatkVariantCaller.snps_dbsnp),
            (snps_1000gp, vc_gatkVariantCaller.snps_1000gp),
            (known_indels, vc_gatkVariantCaller.knownIndels),
            (mills_indels, vc_gatkVariantCaller.millsIndels),

            (vc_gatkVariantCaller.out, vc_merged_gatk.vcfs)
        ])

        self.add_edge(vc_merged_gatk.out, sort_combined_vcfs.vcf)

        # Outputs

        self.add_edges([
            (s_norm.out, Output("normalBam")),
            (s_tum.out, Output("tumorBam")),

            (s_norm.fastq, Output("normalReport")),
            (s_tum.fastq, Output("tumorReport")),

            (sort_combined_vcfs.out, Output("variants")),

            (sort_combined_vcfs.out, Output("variants_combined"))
        ])

    @staticmethod
    def process_subpipeline():
        w = Workflow("somatic_subpipeline")

        reference = Input('reference', FastaWithDict())
        inputs = Input('inputs', Array(Fastq()))

        name = Input('sampleName', String())

        s1_alignsort = Step('alignAndSort', AlignSortedBam())
        s2_process = Step('mergeAndMark', MergeAndMarkBams_4_0())
        fastqc = Step("fastqc", FastQC_0_11_5())

        # Step 1, alignAndSort
        w.add_edges([
            (inputs, s1_alignsort.fastq),
            (reference, s1_alignsort.reference),
            (name, s1_alignsort.sampleName),
            (Input("sortSamTmpDir", String(optional=True)), s1_alignsort.sortSamTmpDir),
        ])

        # step1 sidestep
        w.add_edge(inputs, fastqc.reads)

        # step2 - process bam files
        w.add_edge(s1_alignsort.out, s2_process.bams)

        w.add_edge(s2_process.out, Output("out"))
        w.add_edge(fastqc.out, Output("fastq"))

        return w


if __name__ == "__main__":
    w = WGSSomaticGATK()
    w.translate("cwl", to_console=False, to_disk=True, export_path="{language}")
    w.translate("wdl", to_console=False, to_disk=True, export_path="{language}")
