from datetime import date

from janis_bioinformatics.data_types import (
    FastaWithDict,
    VcfTabix,
    FastqGzPair,
    Bed,
    BedTabix,
)

from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import MergeAndMarkBams_4_1_3
from janis_bioinformatics.tools.common.bwaaligner import BwaAligner
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_1_3
from janis_bioinformatics.tools.pmac import CombineVariants_0_0_4
from janis_bioinformatics.tools.variantcallers import (
    GatkGermlineVariantCaller_4_1_3,
    IlluminaGermlineVariantCaller,
    VardictGermlineVariantCaller,
)
from janis_bioinformatics.tools.variantcallers.gridssgermline import (
    GridssGermlineVariantCaller,
)
from janis_bioinformatics.tools.pmac import ParseFastqcAdaptors

from janis_core import Array, File, String, Float, WorkflowMetadata


class WGSGermlineMultiCallers(BioinformaticsWorkflow):
    def id(self):
        return "WGSGermlineMultiCallers"

    def friendly_name(self):
        return "WGS Germline (Multi callers)"

    @staticmethod
    def version():
        return "1.2.0"

    def constructor(self):

        self.input("fastqs", Array(FastqGzPair))
        self.input("reference", FastaWithDict)

        self.input("cutadapt_adapters", File)

        self.input("gatk_intervals", Array(Bed))
        self.input("vardict_intervals", Array(Bed))
        self.input("strelkaIntervals", BedTabix)

        self.input("header_lines", File)

        self.input("sample_name", String, default="NA12878")
        self.input("allele_freq_threshold", Float, default=0.05)

        # self.input("gridssBlacklist", Bed)

        self.input("snps_dbsnp", VcfTabix)
        self.input("snps_1000gp", VcfTabix)
        self.input("known_indels", VcfTabix)
        self.input("mills_indels", VcfTabix)

        # STEPS

        self.step("fastqc", FastQC_0_11_5(reads=self.fastqs), scatter="reads"),

        self.step(
            "getfastqc_adapters",
            ParseFastqcAdaptors(
                fastqc_datafiles=self.fastqc.datafile,
                cutadapt_adaptors_lookup=self.cutadapt_adapters,
            ),
            scatter="fastqc_datafiles",
        )

        self.step(
            "align_and_sort",
            BwaAligner(
                fastq=self.fastqs,
                reference=self.reference,
                sample_name=self.sample_name,
                sortsam_tmpDir="./tmp",
                cutadapt_adapter=self.getfastqc_adapters,
                cutadapt_removeMiddle3Adapter=self.getfastqc_adapters,
            ),
            scatter=["fastq", "cutadapt_adapter", "cutadapt_removeMiddle3Adapter"],
        )
        self.step(
            "merge_and_mark", MergeAndMarkBams_4_1_3(bams=self.align_and_sort.out)
        )

        # VARIANT CALLERS

        # GATK
        self.step(
            "vc_gatk",
            GatkGermlineVariantCaller_4_1_3(
                bam=self.merge_and_mark.out,
                intervals=self.gatk_intervals,
                reference=self.reference,
                snps_dbsnp=self.snps_dbsnp,
                snps_1000gp=self.snps_1000gp,
                known_indels=self.known_indels,
                mills_indels=self.mills_indels,
            ),
            scatter="intervals",
        )

        self.step("vc_gatk_merge", Gatk4GatherVcfs_4_1_3(vcfs=self.vc_gatk.out))

        # Strelka
        self.step(
            "vc_strelka",
            IlluminaGermlineVariantCaller(
                bam=self.merge_and_mark.out,
                reference=self.reference,
                intervals=self.strelkaIntervals,
            ),
        )

        # Vardict
        self.step(
            "vc_vardict",
            VardictGermlineVariantCaller(
                bam=self.merge_and_mark.out,
                reference=self.reference,
                intervals=self.vardict_intervals,
                sample_name=self.sample_name,
                allele_freq_threshold=self.allele_freq_threshold,
                header_lines=self.header_lines,
            ),
            scatter="intervals",
        )
        self.step("vc_vardict_merge", Gatk4GatherVcfs_4_1_3(vcfs=self.vc_vardict.out))

        # GRIDSS
        # self.step(
        #     "vc_gridss",
        #     GridssGermlineVariantCaller(
        #         bam=self.merge_and_mark.out,
        #         reference=self.reference,
        #         blacklist=self.gridssBlacklist,
        #     ),
        # )

        # Combine

        self.step(
            "combine_variants",
            CombineVariants_0_0_4(
                vcfs=[
                    self.vc_gatk_merge.out,
                    self.vc_strelka.out,
                    self.vc_vardict_merge.out,
                    # self.vc_gridss.out,
                ],
                type="germline",
                columns=["AC", "AN", "AF", "AD", "DP", "GT"],
            ),
        )
        self.step("sort_combined", BcfToolsSort_1_9(vcf=self.combine_variants.vcf))

        self.output("reports", source=self.fastqc.out, output_folder="reports")
        self.output("bam", source=self.merge_and_mark.out, output_folder="bams")

        self.output(
            "variants_combined", source=self.sort_combined.out, output_folder="variants"
        )

        self.output(
            "variants_gatk", source=self.vc_gatk_merge.out, output_folder="variants"
        )
        self.output(
            "variants_vardict",
            source=self.vc_vardict_merge.out,
            output_folder=["variants"],
        )
        self.output(
            "variants_strelka", source=self.vc_strelka.out, output_folder="variants"
        )

        self.output(
            "variants_gatk_split",
            source=self.vc_gatk.out,
            output_folder=["variants", "gatk"],
        )
        self.output(
            "variants_vardict_split",
            source=self.vc_vardict.out,
            output_folder=["variants", "variants"],
        )

        # self.output("variants_gridss", source=self.vc_gridss.out)

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = [
            "wgs",
            "cancer",
            "germline",
            "variants",
            "gatk",
            "vardict",
            "strelka",
        ]
        meta.contributors = ["Michael Franklin"]
        meta.dateUpdated = date(2019, 10, 16)
        meta.short_documentation = (
            "A variant-calling WGS pipeline using GATK, VarDict and Strelka2."
        )


if __name__ == "__main__":
    import os.path

    w = WGSGermlineMultiCallers()
    args = {
        "to_console": False,
        "to_disk": True,
        "validate": True,
        "export_path": os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "{language}"
        ),
    }
    w.translate("cwl", **args)
    w.translate("wdl", **args)
