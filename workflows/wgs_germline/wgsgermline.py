from janis_core import Input, String, Step, Array, Output, Float, File, Boolean, Int, CaptureType

from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.data_types import FastaWithDict, VcfTabix, Fastq, Bed, BedTabix
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.common import BwaAligner, MergeAndMarkBams_4_0
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_0
from janis_bioinformatics.tools.pmac import CombineVariants_0_0_4
from janis_bioinformatics.tools.variantcallers import GatkGermlineVariantCaller, IlluminaGermlineVariantCaller, \
    VardictGermlineVariantCaller


class WGSGermlineMultiCallers(BioinformaticsWorkflow):

    @staticmethod
    def version():
        return "1.0.0"

    def __init__(self):

        BioinformaticsWorkflow.__init__(self, "WGSGermlineMultiCallers", "WGS Germline (Multi callers)")

        fastqInputs = Input("fastqs", Array(Fastq()))
        reference = Input("reference", FastaWithDict())

        gatk_intervals = Input("gatkIntervals", Array(Bed()))
        vardict_intervals = Input("vardictIntervals", Array(Bed()))
        strelka_intervals = Input("strelkaIntervals", BedTabix())

        header_lines = Input("vardictHeaderLines", File())

        sample_name = Input("sampleName", String(), "NA12878")
        allele_freq_threshold = Input("allelFreqThreshold", Float(), 0.05)

        snps_dbsnp = Input("snps_dbsnp", VcfTabix())
        snps_1000gp = Input("snps_1000gp", VcfTabix())
        known_indels = Input("known_indels", VcfTabix())
        mills_indels = Input("mills_1000gp_indels", VcfTabix())

        s1_sw = Step("alignSortedBam", BwaAligner())
        fastqc = Step("fastqc", FastQC_0_11_5())
        s2_process = Step("processBamFiles", MergeAndMarkBams_4_0())

        vc_gatk = Step("variantCaller_GATK", GatkGermlineVariantCaller())
        vc_strelka = Step("variantCaller_Strelka", IlluminaGermlineVariantCaller())
        vc_vardict = Step("variantCaller_Vardict", VardictGermlineVariantCaller())

        vc_merge_gatk = Step("variantCaller_merge_GATK", Gatk4GatherVcfs_4_0())
        vc_merge_vardict = Step("variantCaller_merge_Vardict", Gatk4GatherVcfs_4_0())

        combine_vcs = Step("combineVariants", CombineVariants_0_0_4())
        sort_combined_vcfs = Step("sortCombined", BcfToolsSort_1_9())

        # step1
        self.add_edge(fastqInputs, s1_sw.fastq)
        self.add_edges([
            (reference, s1_sw.reference),
            (sample_name, s1_sw.sampleName),
            (Input("sortSamTmpdir", String(optional=True), default="./tmp"), s1_sw.sortSamTmpDir)
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

        # Strelka VariantCaller
        self.add_edges([
            (s2_process.out, vc_strelka.bam),
            (reference, vc_strelka.reference),
            (strelka_intervals, vc_strelka.intervals)
        ])

        # Vardict VariantCaller
        self.add_edges([
            (vardict_intervals, vc_vardict.intervals),
            (s2_process.out, vc_vardict.bam),
            (reference, vc_vardict.reference),
            (sample_name, vc_vardict),
            (allele_freq_threshold, vc_vardict.allelFreqThreshold),
            (header_lines, vc_vardict.headerLines),

            (vc_vardict.out, vc_merge_vardict.vcfs)
        ])

        # Output the Variants
        self.add_edges([
            (vc_gatk.out, Output("variants_gatk_split")),
            (vc_vardict.out, Output("variants_vardict_split")),

            (vc_strelka.out, Output("variants_strelka")),
            (vc_merge_gatk.out, Output("variants_gatk")),
            (vc_merge_vardict.out, Output("variants_vardict"))
        ])

        # Combine
        self.add_edges([
            (Input("variant_type", String(), default="germline", include_in_inputs_file_if_none=False),
             combine_vcs.type),
            (Input("columns", Array(String()), default=["AC", "AN", "AF", "AD", "DP", "GT"],
                   include_in_inputs_file_if_none=False), combine_vcs.columns),

            (vc_merge_gatk.out, combine_vcs.vcfs),
            (vc_strelka.out, combine_vcs.vcfs),
            (vc_merge_vardict.out, combine_vcs.vcfs),
        ])
        self.add_edge(combine_vcs.vcf, sort_combined_vcfs.vcf)

        # Additional default as Toil fails on intermediary defaults: https://github.com/DataBiosphere/toil/issues/2727

        # createIndex = Input("createIndex", Boolean(optional=True), default=True, include_in_inputs_file_if_none=False)
        # maxRecords = Input("maxRecordsInRam", Int(), default=5000000, include_in_inputs_file_if_none=False)
        # self.add_edges([
        #     (Input("qualityCutoff", Int(optional=True), default=15, include_in_inputs_file_if_none=False), s1_sw.qualityCutoff),
        #     (Input("minReadLength", Int(optional=True), default=50, include_in_inputs_file_if_none=False), s1_sw.minReadLength),
        #     (Input("sortOrder", String(), default="coordinate", include_in_inputs_file_if_none=False), s1_sw.sortOrder),
        #     (Input("sortSamTmpDir", String(), default="tmp/", include_in_inputs_file_if_none=False), s1_sw.sortSamTmpDir),
        #     (createIndex, s1_sw.createIndex),
        #     (Input("validationStringency", String(optional=True), default="SILENT", include_in_inputs_file_if_none=False), s1_sw.validationStringency),
        #     (maxRecords, s1_sw.maxRecordsInRam),
        #     (createIndex, s2_process.createIndex),
        #     (maxRecords, s2_process.maxRecordsInRam),
        #     (Input("filters", Array(String()), default=["PASS"], include_in_inputs_file_if_none=False), vc_strelka.filters),
        #     (Input("chromNamesAreNumbers", Boolean(), default=True, include_in_inputs_file_if_none=False), vc_vardict.chromNamesAreNumbers),
        #     (Input("vcfFormat", Boolean(), default=True, include_in_inputs_file_if_none=False), vc_vardict.vcfFormat),
        #     (Input("chromColumn", Int(), default=1, include_in_inputs_file_if_none=False), vc_vardict.chromColumn),
        #     (Input("regStartCol", Int(), default=2, include_in_inputs_file_if_none=False), vc_vardict.regStartCol),
        #     (Input("geneEndCol", Int(), default=3, include_in_inputs_file_if_none=False), vc_vardict.geneEndCol),
        # ])

        # Outputs

        self.add_edges([
            (s2_process.out, Output("bam")),
            (fastqc.out, Output("reports")),
            (sort_combined_vcfs.out, Output("combinedVariants"))
        ])


if __name__ == "__main__":
    w = WGSGermlineMultiCallers()
    w.translate("cwl", to_console=False, to_disk=True, export_path="{language}")
    w.translate("wdl", to_console=False, to_disk=True, export_path="{language}")
