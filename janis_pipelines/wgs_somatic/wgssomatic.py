from datetime import date

from janis_bioinformatics.data_types import (
    FastaWithDict,
    FastqGzPair,
    VcfTabix,
    Bed,
    BedTabix,
)
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import BwaAligner, MergeAndMarkBams_4_1_3
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_1_3
from janis_bioinformatics.tools.pmac import CombineVariants_0_0_4
from janis_bioinformatics.tools.variantcallers import GatkSomaticVariantCaller_4_1_3
from janis_bioinformatics.tools.variantcallers.illuminasomatic_strelka import (
    IlluminaSomaticVariantCaller,
)
from janis_bioinformatics.tools.variantcallers.vardictsomatic_variants import (
    VardictSomaticVariantCaller,
)
from janis_core import String, WorkflowBuilder, File, Array, Float, WorkflowMetadata


class WGSSomaticMultiCallers(BioinformaticsWorkflow):
    def id(self):
        return "WGSSomaticMultiCallers"

    def friendly_name(self):
        return "WGS Somatic (Multi callers)"

    def constructor(self):
        self.input("normalInputs", Array(FastqGzPair))
        self.input("tumorInputs", Array(FastqGzPair))

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
            self.process_subpipeline(
                reads=self.tumorInputs,
                sampleName=self.tumorName,
                reference=self.reference,
            ),
        )
        self.step(
            "tumor",
            self.process_subpipeline(
                reads=self.normalInputs,
                sampleName=self.normalName,
                reference=self.reference,
            ),
        )

        self.step(
            "variantCaller_GATK",
            GatkSomaticVariantCaller_4_1_3(
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
            ),
            scatter="intervals",
        )

        self.step(
            "variantCaller_merge_GATK",
            Gatk4GatherVcfs_4_1_3(vcfs=self.variantCaller_GATK),
        )

        self.step(
            "variantCaller_Strelka",
            IlluminaSomaticVariantCaller(
                normalBam=self.normal.out,
                tumorBam=self.tumor.out,
                intervals=self.strelkaIntervals,
                reference=self.reference,
            ),
        )
        self.step(
            "variantCaller_VarDict",
            VardictSomaticVariantCaller(
                normalBam=self.tumor.out,
                tumorBam=self.normal.out,
                normalName=self.normalName,
                tumorName=self.tumorName,
                headerLines=self.vardictHeaderLines,
                intervals=self.vardictIntervals,
                reference=self.reference,
                alleleFreqThreshold=self.alleleFreqThreshold,
            ),
            scatter="intervals",
        )

        self.step(
            "variantCaller_merge_VarDict",
            Gatk4GatherVcfs_4_1_3(vcfs=self.variantCaller_VarDict.out),
        )

        self.step(
            "combineVariants",
            CombineVariants_0_0_4(
                normal=self.normalName,
                tumor=self.tumorName,
                vcfs=[
                    self.variantCaller_merge_VarDict,
                    self.variantCaller_Strelka.out,
                    self.variantCaller_merge_GATK,
                ],
                type="somatic",
                columns=["AD", "DP", "GT"],
            ),
        )
        self.step("sortCombined", BcfToolsSort_1_9(vcf=self.combineVariants.vcf))

        # Outputs

        self.output("normalBam", source=self.normal.out, output_tag="variants")
        self.output("tumorBam", source=self.tumor.out, output_tag="variants")
        self.output("normalReport", source=self.normal.reports, output_tag="reports")
        self.output("tumorReport", source=self.tumor.reports, output_tag="reports")

        self.output("variants_gatk", source=self.variantCaller_merge_GATK.out, output_tag="variants")
        self.output("variants_strelka", source=self.variantCaller_Strelka.out, output_tag="variants")
        self.output("variants_vardict", source=self.variantCaller_merge_VarDict.out, output_tag="variants")
        self.output("variants_combined", source=self.combineVariants.vcf, output_tag="variants")

    @staticmethod
    def process_subpipeline(**connections):
        w = WorkflowBuilder("somatic_subpipeline")

        w.input("reference", FastaWithDict)
        w.input("reads", Array(FastqGzPair))

        w.input("sampleName", String)

        w.step(
            "alignAndSort",
            BwaAligner(
                fastq=w.reads,
                reference=w.reference,
                sampleName=w.sampleName,
                sortsam_tmpDir=None,
            ),
            scatter="fastq",
        )
        w.step("mergeAndMark", MergeAndMarkBams_4_1_3(bams=w.alignAndSort.out))
        w.step("fastqc", FastQC_0_11_5(reads=w.reads), scatter="reads")

        w.output("out", source=w.mergeAndMark.out)
        w.output("reports", source=w.fastqc, output_tag=[w.sampleName, "reports"])

        return w(**connections)

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = [
            "wgs",
            "cancer",
            "somatic",
            "variants",
            "gatk",
            "vardict",
            "strelka",
        ]
        meta.contributors = ["Michael Franklin"]
        meta.dateUpdated = date(2019, 10, 16)
        meta.short_documentation = "A somatic tumor-normal variant-calling WGS pipeline using GATK, VarDict and Strelka2."


if __name__ == "__main__":
    w = WGSSomaticMultiCallers()
    args = {
        "to_console": True,
        "to_disk": True,
        "validate": True,
        "export_path": "{language}",
    }
    w.translate("cwl", **args)
    w.translate("wdl", **args)
