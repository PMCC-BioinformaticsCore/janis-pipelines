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
from janis_core import Array, File, String, Float, WorkflowMetadata


class WGSGermlineMultiCallers(BioinformaticsWorkflow):
    def id(self):
        return "WGSGermlineMultiCallers"

    def friendly_name(self):
        return "WGS Germline (Multi callers)"

    @staticmethod
    def version():
        return "1.0.0"

    def constructor(self):

        self.input("fastqs", Array(FastqGzPair))
        self.input("reference", FastaWithDict)

        self.input("gatkIntervals", Array(Bed))
        self.input("vardictIntervals", Array(Bed))
        self.input("strelkaIntervals", BedTabix)

        self.input("vardictHeaderLines", File)

        self.input("sampleName", String, default="NA12878")
        self.input("alleleFreqThreshold", Float, default=0.05)

        # self.input("gridssBlacklist", Bed)

        self.input("snps_dbsnp", VcfTabix)
        self.input("snps_1000gp", VcfTabix)
        self.input("known_indels", VcfTabix)
        self.input("mills_indels", VcfTabix)

        # STEPS

        self.step(
            "alignSortedBam",
            BwaAligner(
                fastq=self.fastqs,
                reference=self.reference,
                sampleName=self.sampleName,
                sortsam_tmpDir="./tmp",
            ),
            scatter="fastq",
        )
        self.step("fastqc", FastQC_0_11_5(reads=self.fastqs), scatter="reads"),
        self.step(
            "processBamFiles", MergeAndMarkBams_4_1_3(bams=self.alignSortedBam.out)
        )

        # VARIANT CALLERS

        # GATK
        self.step(
            "variantCaller_GATK",
            GatkGermlineVariantCaller_4_1_3(
                bam=self.processBamFiles.out,
                intervals=self.gatkIntervals,
                reference=self.reference,
                snps_dbsnp=self.snps_dbsnp,
                snps_1000gp=self.snps_1000gp,
                knownIndels=self.known_indels,
                millsIndels=self.mills_indels,
            ),
            scatter="intervals",
        )

        self.step(
            "variantCaller_merge_GATK",
            Gatk4GatherVcfs_4_1_3(vcfs=self.variantCaller_GATK.out),
        )

        # Strelka
        self.step(
            "variantCaller_Strelka",
            IlluminaGermlineVariantCaller(
                bam=self.processBamFiles.out,
                reference=self.reference,
                intervals=self.strelkaIntervals,
            ),
        )

        # Vardict
        self.step(
            "variantCaller_Vardict",
            VardictGermlineVariantCaller(
                bam=self.processBamFiles.out,
                reference=self.reference,
                intervals=self.vardictIntervals,
                sampleName=self.sampleName,
                alleleFreqThreshold=self.alleleFreqThreshold,
                headerLines=self.vardictHeaderLines,
            ),
            scatter="intervals",
        )
        self.step(
            "variantCaller_merge_Vardict",
            Gatk4GatherVcfs_4_1_3(vcfs=self.variantCaller_Vardict.out),
        )

        # GRIDSS
        # self.step(
        #     "variantCaller_GRIDSS",
        #     GridssGermlineVariantCaller(
        #         bam=self.processBamFiles.out,
        #         reference=self.reference,
        #         blacklist=self.gridssBlacklist,
        #     ),
        # )

        # Combine

        self.step(
            "combineVariants",
            CombineVariants_0_0_4(
                vcfs=[
                    self.variantCaller_merge_GATK.out,
                    self.variantCaller_Strelka.out,
                    self.variantCaller_merge_Vardict.out,
                    # self.variantCaller_GRIDSS.out,
                ],
                type="germline",
                columns=["AC", "AN", "AF", "AD", "DP", "GT"],
            ),
        )
        self.step("sortCombined", BcfToolsSort_1_9(vcf=self.combineVariants.vcf))

        self.output("bam", source=self.processBamFiles.out, output_tag="bams")
        self.output("reports", source=self.fastqc, output_tag="reports")
        self.output("combinedVariants", source=self.sortCombined.out, output_tag="variants")
        self.output("variants_gatk_split", source=self.variantCaller_GATK.out, output_tag=["variants", "gatk"])
        self.output(
            "variants_vardict_split", source=self.variantCaller_merge_Vardict.out, output_tag=["variants", "vardict"]
        )
        self.output(
            "variants_strelka",
            source=self.variantCaller_Strelka.out,
            output_tag="variants"
            # prefix_source=self.tumorName,
            # output_tag="vcf",
        )
        self.output(
            "variants_gatk",
            source=self.variantCaller_merge_GATK.out,
            output_tag="variants"
            # prefix_source=self.normalName,
        )
        self.output("variants_vardict", source=self.variantCaller_Vardict.out, output_tag="variants")
        # self.output("variants_gridss", source=self.variantCaller_GRIDSS.out)

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
    w = WGSGermlineMultiCallers()
    args = {
        "to_console": False,
        "to_disk": True,
        "validate": True,
        "export_path": "{language}",
    }
    w.translate("cwl", **args)
    w.translate("wdl", **args)
