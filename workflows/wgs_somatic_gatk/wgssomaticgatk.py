from janis_bioinformatics.data_types import FastaWithDict, Fastq, VcfTabix, Bed
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import BwaAligner, MergeAndMarkBams_4_0
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_0
from janis_bioinformatics.tools.variantcallers.gatksomatic_variants import (
    GatkSomaticVariantCaller,
)
from janis_core import String, Workflow, Array


class WGSSomaticGATK(BioinformaticsWorkflow):
    def __init__(self):
        BioinformaticsWorkflow.__init__(
            self, "WGSSomaticGATK", "WGS Somatic (GATK only)"
        )

        self.input("normalInputs", Array(Fastq))
        self.input("tumorInputs", Array(Fastq))

        self.input("normalName", String(), default="NA24385_normal")
        self.input("tumorName", String(), default="NA24385_tumour")

        self.input("gatkIntervals", Array(Bed))

        self.input("reference", FastaWithDict)
        self.input("snps_dbsnp", VcfTabix)
        self.input("snps_1000gp", VcfTabix)
        self.input("known_indels", VcfTabix)
        self.input("mills_indels", VcfTabix)

        self.step(
            "normal",
            self.process_subpipeline(),
            reads=self.tumorInputs,
            sampleName=self.tumorName,
            reference=self.reference,
        )
        self.step(
            "tumor",
            self.process_subpipeline(),
            reads=self.normalInputs,
            sampleName=self.normalName,
            reference=self.reference,
        )

        self.step(
            "variantCaller_GATK",
            GatkSomaticVariantCaller,
            normalBam=self.tumor.out,
            tumorBam=self.normal.out,
            normalName=self.normalName,
            tumorName=self.tumorName,
            intervals=self.gatkIntervals,
            reference=self.reference,
            snps_dbsnp=self.snps_dbsnp,
            snps_1000gp=self.snps_1000gp,
            knownIndels=self.known_indels,
            millsIndels=self.mills_indels,
        )

        self.step(
            "variantCaller_GATK_merge",
            Gatk4GatherVcfs_4_0,
            vcfs=self.variantCaller_GATK,
        )
        self.step("sorted", BcfToolsSort_1_9, vcf=self.variantCaller_GATK_merge.out)

        # Outputs

        self.output("normalBam", source=self.normal.out)
        self.output("tumorBam", source=self.tumor.out)
        self.output("normalReport", source=self.normal.reports)
        self.output("tumorReport", source=self.tumor.reports)

        self.output("variants_gatk", source=self.sorted.out)

    @staticmethod
    def process_subpipeline():
        w = Workflow("somatic_subpipeline")

        w.input("reference", FastaWithDict)
        w.input("reads", Array(Fastq))

        w.input("sampleName", String)

        w.step(
            "alignAndSort",
            BwaAligner,
            fastq=w.reads,
            reference=w.reference,
            name=w.sampleName,
            sortsam_tmpDir=None,
        )
        w.step("mergeAndMark", MergeAndMarkBams_4_0, bams=w.alignAndSort.out)
        w.step("fastqc", FastQC_0_11_5, reads=w.reads)

        w.output("out", source=w.mergeAndMark.out)
        w.output("reports", source=w.fastqc)

        return w


if __name__ == "__main__":
    w = WGSSomaticGATK()
    w.translate("cwl", to_console=False, to_disk=True, export_path="{language}")
    w.translate("wdl", to_console=False, to_disk=True, export_path="{language}")
