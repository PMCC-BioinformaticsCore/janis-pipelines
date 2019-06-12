import unittest
from typing import List

from janis import Input, String, Step, Workflow, File, Array, Output, Float, CaptureType, CommandTool, ToolOutput, \
    ToolInput, ToolArgument, Stdout
from janis_bioinformatics.data_types import FastaWithDict, Fastq, VcfIdx, VcfTabix, Bed, Bam
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.common import AlignSortedBam

from janis_bioinformatics.tools.common.processbam import MergeAndMarkBams_4_0
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_0
from janis_bioinformatics.tools.pmac import CombineVariants_0_0_4
from janis_bioinformatics.tools.variantcallers.gatksomatic_variants import GatkSomaticVariantCaller
from janis_bioinformatics.tools.variantcallers.illuminasomatic_strelka import IlluminaSomaticVariantCaller
from janis_bioinformatics.tools.variantcallers.vardictsomatic_variants import VardictSomaticVariantCaller


ENVIRONMENT = "pmac"
CAPTURE_TYPE = CaptureType.CHROMOSOME

inputs_map = {
    CaptureType.TARGETED: {
        "local": {
            "normalInputs": [[
                "/Users/franklinmichael/Desktop/workflows-for-testing/wgs-somatic/inputs/brca1/BRCA1_R1.normal.fastq.gz",
                "/Users/franklinmichael/Desktop/workflows-for-testing/wgs-somatic/inputs/brca1/BRCA1_R2.normal.fastq.gz"
            ]],
            "tumorInputs": [[
                "/Users/franklinmichael/Desktop/workflows-for-testing/wgs-somatic/inputs/brca1/BRCA1_R1.tumor.fastq.gz",
                "/Users/franklinmichael/Desktop/workflows-for-testing/wgs-somatic/inputs/brca1/BRCA1_R2.tumor.fastq.gz"
            ]],
            "vardictHeaderLines": "/Users/franklinmichael/Desktop/workflows-for-testing/wgs-somatic/inputs/vardictHeader.txt",
            "vardictIntervals": [
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test5_BRCA1_30X/other_files/BRCA1.intersect.bed"
            ],

            "reference": "/Users/franklinmichael/reference/hg38/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/Users/franklinmichael/reference/hg38/dbsnp_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/Users/franklinmichael/reference/hg38/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/Users/franklinmichael/reference/hg38/known_indels_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/Users/franklinmichael/reference/hg38/mills_indels/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",

        },
        "pmac": {
            "normalInputs": [[
                "/researchers/jiaan.yu/WGS_pipeline/somatic/somatic-in-a-bottle/test_cases/test5_BRCA1_30X/BRCA1_R1.normal.fastq.gz",
                "/researchers/jiaan.yu/WGS_pipeline/somatic/somatic-in-a-bottle/test_cases/test5_BRCA1_30X/BRCA1_R2.normal.fastq.gz"
            ]],
            "tumorInputs": [[
                "/researchers/jiaan.yu/WGS_pipeline/somatic/somatic-in-a-bottle/test_cases/test5_BRCA1_30X/BRCA1_R1.tumor.fastq.gz",
                "/researchers/jiaan.yu/WGS_pipeline/somatic/somatic-in-a-bottle/test_cases/test5_BRCA1_30X/BRCA1_R2.tumor.fastq.gz"
            ]],

            "vardictIntervals": [
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test5_BRCA1_30X/BRCA1.bed"],
            "vardictHeaderLines": "/researchers/jiaan.yu/WGS_pipeline/header_added_to_vardict.txt",

            "reference": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        },
    },
    CaptureType.CHROMOSOME: {
        "pmac": {
            "normalInputs": [[
                "/researchers/jiaan.yu/WGS_pipeline/somatic/somatic-in-a-bottle/test_cases/test4_chr18_30X/chr18_R1.normal.fastq.gz",
                "/researchers/jiaan.yu/WGS_pipeline/somatic/somatic-in-a-bottle/test_cases/test4_chr18_30X/chr18_R2.normal.fastq.gz",
            ]],
            "tumorInputs": [[
                "/researchers/jiaan.yu/WGS_pipeline/somatic/somatic-in-a-bottle/test_cases/test4_chr18_30X/chr18_R1.tumor.fastq.gz",
                "/researchers/jiaan.yu/WGS_pipeline/somatic/somatic-in-a-bottle/test_cases/test4_chr18_30X/chr18_R2.tumor.fastq.gz",
            ]],

            "vardictIntervals": [
                "/researchers/jiaan.yu/WGS_pipeline/somatic/somatic-in-a-bottle/test_cases/test4_chr18_30X/chr18.bed"],
            "vardictHeaderLines": "/researchers/jiaan.yu/WGS_pipeline/header_added_to_vardict.txt",

            "reference": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        }
    },

    CaptureType.THIRTYX: {
        "pmac": {
            "normalInputs": [[
                "/researchers/jiaan.yu/WGS_pipeline/somatic/somatic-in-a-bottle/test_cases/test2_WGS_30X/WGS_30X_R1.normal.fastq.gz",
                "/researchers/jiaan.yu/WGS_pipeline/somatic/somatic-in-a-bottle/test_cases/test2_WGS_30X/WGS_30X_R2.normal.fastq.gz",
            ]],
            "tumorInputs": [[
                "/researchers/jiaan.yu/WGS_pipeline/somatic/somatic-in-a-bottle/test_cases/test2_WGS_30X/WGS_30X_R1.tumor.fastq.gz",
                "/researchers/jiaan.yu/WGS_pipeline/somatic/somatic-in-a-bottle/test_cases/test2_WGS_30X/WGS_30X_R2.tumor.fastq.gz",
            ]],

            "vardictIntervals": [
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr1.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr2.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr3.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr4.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr5.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr6.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr7.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr8.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr9.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr10.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr11.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr12.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr13.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr14.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr15.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr16.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr17.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr18.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr19.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr20.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr21.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr22.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chrX.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chrY.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chrM.bed"
            ],
            "gatkIntervals": [
                "/home/mfranklin/hg38_beds/1.bed",
                "/home/mfranklin/hg38_beds/2.bed",
                "/home/mfranklin/hg38_beds/3.bed",
                "/home/mfranklin/hg38_beds/4.bed",
                "/home/mfranklin/hg38_beds/5.bed",
                "/home/mfranklin/hg38_beds/6.bed",
                "/home/mfranklin/hg38_beds/7.bed",
                "/home/mfranklin/hg38_beds/8.bed",
                "/home/mfranklin/hg38_beds/9.bed",
                "/home/mfranklin/hg38_beds/10.bed",
                "/home/mfranklin/hg38_beds/11.bed",
                "/home/mfranklin/hg38_beds/12.bed",
                "/home/mfranklin/hg38_beds/13.bed",
                "/home/mfranklin/hg38_beds/14.bed",
                "/home/mfranklin/hg38_beds/15.bed",
                "/home/mfranklin/hg38_beds/16.bed",
                "/home/mfranklin/hg38_beds/17.bed",
                "/home/mfranklin/hg38_beds/18.bed",
                "/home/mfranklin/hg38_beds/19.bed",
                "/home/mfranklin/hg38_beds/20.bed",
                "/home/mfranklin/hg38_beds/21.bed",
                "/home/mfranklin/hg38_beds/22.bed",
                "/home/mfranklin/hg38_beds/X.bed",
                "/home/mfranklin/hg38_beds/Y.bed",
                "/home/mfranklin/hg38_beds/M.bed",
            ],
            "vardictHeaderLines": "/researchers/jiaan.yu/WGS_pipeline/header_added_to_vardict.txt",

            "reference": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",

        }
    }
}


class WholeGenomeSomaticWorkflow(Workflow):

    def __init__(self):
        super().__init__("WgSomatic")

        normalInputs = Input('normalInputs', Array(Fastq()))
        tumorInputs = Input('tumorInputs', Array(Fastq()))

        normalName = Input("normalName", String(), "NA24385_normal")
        tumorName = Input("tumorName", String(), "NA24385_tumour")

        normal_read_group_header_line = Input('normalReadGroupHeaderLine', String(), "'@RG\\tID:NA24385_normal\\tSM:NA24385_normal\\tLB:NA24385_normal\\tPL:ILLUMINA'")
        tumor_read_group_header_line = Input('tumorReadGroupHeaderLine', String(),   "'@RG\\tID:NA24385_tumour\\tSM:NA24385_tumour\\tLB:NA24385_tumour\\tPL:ILLUMINA'")

        gatk_intervals = Input("gatkIntervals", Array(Bed(optional=True)), default=[None],
                               include_in_inputs_file_if_none=False)

        vardict_intervals = Input("vardictIntervals", Array(Bed()))

        header_lines = Input("vardictHeaderLines", File())
        allele_freq_threshold = Input("allelFreqThreshold", Float(), 0.05)

        reference = Input('reference', FastaWithDict())
        snps_dbsnp = Input("snps_dbsnp", VcfTabix())
        snps_1000gp = Input("snps_1000gp", VcfTabix())
        known_indels = Input("known_indels", VcfTabix())
        mills_indels = Input("mills_1000gp_indels", VcfTabix())

        s_norm = Step("normal", self.process_subpipeline())
        s_tum = Step("tumor", self.process_subpipeline())

        vc_gatkVariantCaller = Step("GATK_VariantCaller", GatkSomaticVariantCaller())
        vc_strelkaVariantCaller = Step("Strelka_VariantCaller", IlluminaSomaticVariantCaller())
        # vc_vardictVariantcaller = Step("VarDict_VariantCaller", VardictSomaticVariantCaller())

        vc_merged_gatk = Step("variantCaller_merge_GATK", Gatk4GatherVcfs_4_0())
        # vc_merged_vardict = Step("variantCaller_merge_Vardict", Gatk4GatherVcfs_4_0())

        combine_vcs = Step("combineVariants", CombineVariants_0_0_4())
        sort_combined_vcfs = Step("sortCombined", BcfToolsSort_1_9())

        self.add_edges([
            (normalInputs, s_norm.inputs),
            (normal_read_group_header_line, s_norm.readGroupHeaderLine),
            (reference, s_norm.reference),
        ])

        self.add_edges([
            (tumorInputs, s_tum.inputs),
            (tumor_read_group_header_line, s_tum.readGroupHeaderLine),
            (reference, s_tum.reference),
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
        #
        # # Strelka VariantCaller
        #
        self.add_edges([
            (s_norm.out, vc_strelkaVariantCaller.normalBam),
            (s_tum.out, vc_strelkaVariantCaller.tumorBam),

            (reference, vc_strelkaVariantCaller.reference)
        ])

        # VarDict VariantCaller

        # self.add_edges([
        #     (s_norm.out, vc_vardictVariantcaller.normalBam),
        #     (s_tum.out, vc_vardictVariantcaller.tumorBam),
        #     (tumorName, vc_vardictVariantcaller.tumorName),
        #
        #     (header_lines, vc_vardictVariantcaller.headerLines),
        #     (vardict_intervals, vc_vardictVariantcaller.intervals),
        #     (reference, vc_vardictVariantcaller.reference),
        #     (allele_freq_threshold, vc_vardictVariantcaller.alleleFreqThreshold),
        #
        #     (vc_vardictVariantcaller.out, vc_merged_vardict.vcfs)
        # ])

        # Combine
        self.add_edges([
            (Input("variant_type", String(), default="somatic", include_in_inputs_file_if_none=False),
             combine_vcs.type),
            (Input("columns", Array(String()), default=["AD", "DP", "GT"],
                   include_in_inputs_file_if_none=False), combine_vcs.columns),
            (normalName, combine_vcs.normal),
            (tumorName, combine_vcs.tumor),

            (vc_merged_gatk.out, combine_vcs.vcfs),
            (vc_strelkaVariantCaller.out, combine_vcs.vcfs),
            # (vc_merged_vardict.out, combine_vcs.vcfs),


        ])
        self.add_edge(combine_vcs.vcf, sort_combined_vcfs.vcf)

        # Outputs

        self.add_edges([
            (s_norm.out, Output("normalBam")),
            (s_tum.out, Output("tumorBam")),

            (s_norm.fastq, Output("normalReport")),
            (s_tum.fastq, Output("tumorReport")),

            (vc_strelkaVariantCaller.out, Output("variants_strelka")),
            # (vc_merged_vardict.out, Output("variants_vardict")),
            (vc_merged_gatk.out, Output("variants_gatk")),

            (sort_combined_vcfs.out, Output("variants_combined"))
        ])

    @staticmethod
    def process_subpipeline():
        w = Workflow("somatic_subpipeline")

        # Declare inputs  Input("inputIdentifier", InputType())
        reference = Input('reference', FastaWithDict())
        inputs = Input('inputs', Array(Fastq()))

        # Declare steps   Step("stepIdentifier", Tool())
        rghl = Input('readGroupHeaderLine', String())

        s1_alignsort = Step('alignAndSort', AlignSortedBam())
        s2_process = Step('mergeAndMark', MergeAndMarkBams_4_0())
        fastqc = Step("fastqc", FastQC_0_11_5())

        w.add_edges([
            (inputs, s1_alignsort.fastq),
            (reference, s1_alignsort.reference),
            (rghl, s1_alignsort.readGroupHeaderLine),
        ])

        # step1 sidestep
        w.add_edge(inputs, fastqc.reads)

        # step2 - process bam files
        w.add_edge(s1_alignsort.out, s2_process.bams)

        w.add_edge(s2_process.out, Output("out"))
        w.add_edge(fastqc.out, Output("fastq"))

        return w


if __name__ == "__main__":
        w = WholeGenomeSomaticWorkflow()

        im = inputs_map[CAPTURE_TYPE][ENVIRONMENT]
        for inp in w._inputs:
            if inp.id() in im:
                inp.input.value = im[inp.id()]

        hints = {CaptureType.key(): CAPTURE_TYPE}

        w.translate("wdl", to_disk=True, should_validate=True, write_inputs_file=True)
        w.generate_resources_file("wdl", hints)

        if str(input(f"Run at {ENVIRONMENT} (Y/n)? ")).lower() == "y":
            import shepherd
            tid = shepherd.fromjanis(w, env=ENVIRONMENT, hints=hints, watch=False)
            print(tid)
