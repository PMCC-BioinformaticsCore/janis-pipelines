from datetime import date

from janis_core import String, Array, InputSelector, WorkflowMetadata

from janis_bioinformatics.data_types import (
    FastaWithDict,
    VcfTabix,
    FastqGzPair,
    Bed,
    Bam,
    BamBai,
)
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import BwaAligner, MergeAndMarkBams_4_1_3
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_0, Gatk4SortSam_4_1_3
from janis_bioinformatics.tools.variantcallers import GatkGermlineVariantCaller_4_1_3


class WGSGermlineGATK(BioinformaticsWorkflow):
    def id(self):
        return "WGSGermlineGATK"

    def friendly_name(self):
        return "WGS Germline (GATK only)"

    @staticmethod
    def version():
        return "1.0.0"

    def constructor(self):

        self.input("fastqs", Array(FastqGzPair))
        self.input("reference", FastaWithDict)
        self.input("gatkIntervals", Array(Bed))

        self.input("sampleName", String(), default="NA12878")

        self.input("snps_dbsnp", VcfTabix, doc="")
        self.input("snps_1000gp", VcfTabix)
        self.input("known_indels", VcfTabix)
        self.input("mills_indels", VcfTabix)

        # STEPS

        self.step("fastqc", FastQC_0_11_5(reads=self.fastqs), scatter="reads")
        self.step(
            "alignSortedBam",
            BwaAligner(
                fastq=self.fastqs,
                reference=self.reference,
                sampleName=self.sampleName,
                sortsam_tmpDir=".",
            ),
            scatter="fastq",
        )
        self.step("processBamFiles", MergeAndMarkBams_4_1_3(bams=self.alignSortedBam))

        # VARIANT CALLERS

        # GATK
        self.step(
            "variantCaller_GATK",
            GatkGermlineVariantCaller_4_1_3(
                bam=self.processBamFiles,
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
            Gatk4GatherVcfs_4_0(vcfs=self.variantCaller_GATK.out),
        )
        # sort

        self.step(
            "sortCombined", BcfToolsSort_1_9(vcf=self.variantCaller_merge_GATK.out)
        )

        self.output(
            "bam", source=self.processBamFiles.out, output_tag=["bams", self.sampleName]
        )
        self.output(
            "reports", source=self.fastqc, output_tag=["reports", self.sampleName]
        )
        self.output("variants", source=self.sortCombined.out, output_tag="variants")
        self.output(
            "variants_split",
            source=self.variantCaller_GATK.out,
            output_tag=["variants", "byInterval"],
        )

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = ["wgs", "cancer", "germline", "variants", "gatk"]
        meta.contributors = ["Michael Franklin"]
        meta.dateUpdated = date(2019, 10, 16)
        meta.short_documentation = "A variant-calling WGS pipeline using only the GATK Haplotype variant caller."


if __name__ == "__main__":
    w = WGSGermlineGATK()
    args = {
        "to_console": False,
        "to_disk": True,
        "validate": True,
        "export_path": "{language}",
    }
    w.translate("cwl", **args)
    w.translate("wdl", **args)
