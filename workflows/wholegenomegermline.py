import unittest

from janis import Input, String, Step, Directory, Workflow, Array, Output, Logger, LogLevel, Float, File
import janis.bioinformatics as jb

# Logger.set_console_level(LogLevel.DEBUG)
from janis.hints import CaptureType

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

        fastqInputs = Input("fastqs", Array(Fastq()))
        bedIntervals = Input("bedIntervals", Bed())

        reference = Input("reference", FastaWithDict())

        s1_inp_header = Input("readGroupHeaderLine", String())
        snps_dbsnp = Input("snps_dbsnp", VcfTabix())
        snps_1000gp = Input("snps_1000gp", VcfTabix())
        known_indels = Input("known_indels", VcfTabix())
        mills_indels = Input("mills_1000gp_indels", VcfTabix())

        sample_name = Input("sampleName", String(), "NA12878")
        allele_freq_threshold = Input("allelFreqThreshold", Float(), 0.05)
        header_lines = Input("headerLines", File())

        s1_sw = Step("s1_alignSortedBam", AlignSortedBam())
        fastqc = Step("fastqc", FastQC_0_11_5())
        s2_process = Step("s2_processBamFiles", MergeAndMarkBams_4_0())

        vc_gatk = Step("variantCaller_GATK", GatkVariantCaller())
        vc_strelka = Step("variantCaller_Strelka", StrelkaVariantCaller())
        vc_vardict = Step("variantCaller_Vardict", VardictVariantCaller())

        combine_vcs = Step("combineVariants", CombineVariants_0_1_0())

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
            (reference, vc_strelka.reference)
        ])

        # Vardict VariantCaller
        self.add_edges([
            (bedIntervals, vc_vardict.bed),
            (s2_process.out, vc_vardict.bam),
            (reference, vc_vardict.reference),
            (sample_name, vc_vardict),
            (allele_freq_threshold, vc_vardict.allelFreqThreshold),
            (header_lines, vc_vardict.headerLines)
        ])

        # Output the Variants
        self.add_edges([
            (vc_gatk.out, Output("variants_gatk")),
            (vc_strelka.out, Output("variants_strelka")),
            (vc_vardict.out, Output("variants_vardict"))
        ])

        # Combine
        self.add_edges([
            (Input("variant_type", String(), default="germline"), combine_vcs.type),
            (Input("columns", String(), default="AC AN AF AD DP GT"), combine_vcs.columns),

            (vc_gatk.out, combine_vcs.vcfs),
            (vc_strelka.out, combine_vcs.vcfs),
            (vc_vardict.out, combine_vcs.vcfs)
        ])

        # Outputs

        self.add_edges([
            (s2_process.out, Output("bam")),
            (fastqc.out, Output("reports")),
            (combine_vcs.vcf, Output("combinedVariants"))
        ])


if __name__ == "__main__":
    import shepherd

    wf = WholeGenomeGermlineWorkflow()

    im = inputs_map[CAPTURE_TYPE][ENVIRONMENT]
    for inp in wf._inputs:
        if inp.id() in im:
            inp.input.value = im[inp.id()]
    wdl = wf.dump_translation("cwl", to_console=True,
                              to_disk=True, write_inputs_file=True,
                              with_resource_overrides=False, should_validate=True)

    # print(wf.generate_resources_file("wdl", {CaptureType.KEY: CaptureType.CHROMOSOME}))

    #
    # config = shepherd.CromwellConfiguration(
    #     database=shepherd.CromwellConfiguration.Database.mysql("cromwelluser", "cromwell-pass")
    # )
    #
    # task = shepherd.from_janis(wf, engine=shepherd.Cromwell(config=config))
    # # task = shepherd.from_janis(wf, engine=shepherd.CWLTool())
    #
    # print(task.outputs)
