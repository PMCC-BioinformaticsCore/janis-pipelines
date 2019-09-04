from janis_bioinformatics.data_types import (
    FastaWithDict,
    Fastq,
    VcfTabix,
    Bed,
    BedTabix,
)
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import BwaAligner, MergeAndMarkBams_4_0
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_0
from janis_bioinformatics.tools.pmac import CombineVariants_0_0_4
from janis_bioinformatics.tools.variantcallers.gatksomatic_variants import (
    GatkSomaticVariantCaller,
)
from janis_bioinformatics.tools.variantcallers.illuminasomatic_strelka import (
    IlluminaSomaticVariantCaller,
)
from janis_bioinformatics.tools.variantcallers.vardictsomatic_variants import (
    VardictSomaticVariantCaller,
)
from janis_core import String, Workflow, File, Array, Float


class WGSSomaticMultiCallers(BioinformaticsWorkflow):
    def __init__(self):
        BioinformaticsWorkflow.__init__(
            self, "WGSSomaticMultiCallers", "WGS Somatic (Multi callers)"
        )

        self.input("normalInputs", Array(Fastq))
        self.input("tumorInputs", Array(Fastq))

        self.input("normalName", String(), default="NA24385_normal")
        self.input("tumorName", String(), default="NA24385_tumour")

        self.input("gatkIntervals", Array(Bed))

        self.input("vardictIntervals", Array(Bed))
        self.input("strelkaIntervals", BedTabix(optional=True))

        self.input("vardictHeaderLines", File)
        self.input("alleleFreqThreshold", Float, default=0.05)

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

        self.step(
            "variantCaller_Strelka",
            IlluminaSomaticVariantCaller,
            normalBam=self.normal.out,
            tumorBam=self.tumor.out,
            intervals=self.strelkaIntervals,
            reference=self.reference,
        )
        self.step(
            "variantCaller_VarDict",
            VardictSomaticVariantCaller,
            normalBam=self.tumor.out,
            tumorBam=self.normal.out,
            normalName=self.normalName,
            tumorName=self.tumorName,
            headerLines=self.vardictHeaderLines,
            intervals=self.vardictIntervals,
            reference=self.reference,
            alleleFreqThreshold=self.alleleFreqThreshold,
        )

        self.step(
            "variantCaller_VarDict_merge",
            Gatk4GatherVcfs_4_0,
            vcfs=self.variantCaller_VarDict.out,
        )

        self.step(
            "combineVariants",
            CombineVariants_0_0_4,
            normal=self.normalName,
            tumor=self.tumorName,
            vcfs=[
                self.variantCaller_GATK_merge,
                self.variantCaller_Strelka.out,
                self.variantCaller_VarDict_merge,
            ],
            type="somatic",
            columns=["AD", "DP", "GT"],
        )
        self.step("sortCombined", BcfToolsSort_1_9, vcf=self.combineVariants.vcf)

        # Outputs

        self.output("normalBam", source=self.normal.out)
        self.output("tumorBam", source=self.tumor.out)
        self.output("normalReport", source=self.normal.reports)
        self.output("tumorReport", source=self.tumor.reports)

        self.output("variants_gatk", source=self.variantCaller_GATK_merge.out)
        self.output("variants_strelka", source=self.variantCaller_Strelka.out)
        self.output("variants_vardict", source=self.variantCaller_VarDict_merge.out)
        self.output("variants_combined", source=self.combineVariants.vcf)

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
    w = WGSSomaticMultiCallers()
    w.translate("cwl", to_console=True, to_disk=False, export_path="{language}")
    w.translate("wdl", to_console=True, to_disk=False, export_path="{language}")
