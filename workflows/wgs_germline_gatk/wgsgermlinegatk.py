from janis_core import String, Array

from janis_bioinformatics.data_types import FastaWithDict, VcfTabix, Fastq, Bed
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import BwaAligner, MergeAndMarkBams_4_0
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_0
from janis_bioinformatics.tools.variantcallers import GatkGermlineVariantCaller


class WGSGermlineGATK(BioinformaticsWorkflow):
    @staticmethod
    def version():
        return "1.0.0"

    def __init__(self):

        super().__init__("WGSGermlineGATK", name="WGS Germline (GATK only)")

        self.input("fastqs", Array(Fastq))
        self.input("reference", FastaWithDict)
        self.input("gatkIntervals", Array(Bed))

        self.input("sampleName", String(), default="NA12878")

        self.input("snps_dbsnp", VcfTabix)
        self.input("snps_1000gp", VcfTabix)
        self.input("known_indels", VcfTabix)
        self.input("mills_indels", VcfTabix)

        # STEPS

        self.step(
            "alignSortedBam",
            BwaAligner,
            scatter="fastq",
            fastq=self.fastqs,
            reference=self.reference,
            name=self.sampleName,
            sortsam_tmpDir=None,
        )
        self.step("fastqc", FastQC_0_11_5, scatter="reads", reads=self.fastqs)
        self.step("processBamFiles", MergeAndMarkBams_4_0, bams=self.alignSortedBam.out)

        # VARIANT CALLERS

        # GATK
        self.step(
            "variantCaller_GATK",
            GatkGermlineVariantCaller,
            scatter="intervals",
            bam=self.processBamFiles.out,
            intervals=self.gatkIntervals,
            reference=self.reference,
            snps_dbsnp=self.snps_dbsnp,
            snps_1000gp=self.snps_1000gp,
            knownIndels=self.known_indels,
            millsIndels=self.mills_indels,
        )

        self.step(
            "variantCaller_merge_GATK",
            Gatk4GatherVcfs_4_0,
            vcfs=self.variantCaller_GATK.out,
        )
        # sort

        self.step(
            "sortCombined", BcfToolsSort_1_9, vcf=self.variantCaller_merge_GATK.out
        )

        self.output("bam", source=self.processBamFiles.out)
        self.output("reports", source=self.fastqc)
        self.output("variants", source=self.sortCombined.out)
        self.output("variants_split", source=self.variantCaller_GATK.out)


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
