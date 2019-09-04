from janis_bioinformatics.tools.variantcallers.gridssgermline import (
    GridssGermlineVariantCaller,
)

from janis_core import Array, File, String, Float

from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.data_types import (
    FastaWithDict,
    VcfTabix,
    Fastq,
    Bed,
    BedTabix,
)
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.common import BwaAligner, MergeAndMarkBams_4_0
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_0
from janis_bioinformatics.tools.pmac import CombineVariants_0_0_4
from janis_bioinformatics.tools.variantcallers import (
    GatkGermlineVariantCaller,
    IlluminaGermlineVariantCaller,
    VardictGermlineVariantCaller,
)


class WGSGermlineMultiCallers(BioinformaticsWorkflow):
    @staticmethod
    def version():
        return "1.0.0"

    def __init__(self):

        super().__init__("WGSGermlineMultiCallers", "WGS Germline (Multi callers)")

        self.input("fastqs", Array(Fastq()))
        self.input("reference", FastaWithDict)

        self.input("gatkIntervals", Array(Bed()))
        self.input("vardictIntervals", Array(Bed()))
        self.input("strelkaIntervals", BedTabix)

        self.input("vardictHeaderLines", File)

        self.input("sampleName", String(), "NA12878")
        self.input("allelFreqThreshold", Float(), 0.05)

        self.input("gridssBlacklist", Bed)

        self.input("snps_dbsnp", VcfTabix)
        self.input("snps_1000gp", VcfTabix)
        self.input("known_indels", VcfTabix)
        self.input("mills_indels", VcfTabix)

        # STEPS

        self.step(
            "alignSortedBam",
            BwaAligner,
            fastq=self.fastqs,
            reference=self.reference,
            name=self.sampleName,
            sortsam_tmpDir="./tmp",
        )
        self.step("fastqc", FastQC_0_11_5, reads=self.fastqs)
        self.step("processBamFiles", MergeAndMarkBams_4_0, bams=self.alignSortedBam.out)

        # VARIANT CALLERS

        # GATK
        self.step(
            "variantCaller_GATK",
            GatkGermlineVariantCaller,
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

        # Strelka
        self.step(
            "variantCaller_Strelka",
            IlluminaGermlineVariantCaller,
            bam=self.processBamFiles.out,
            reference=self.reference,
            intervals=self.strelkaIntervals,
        )

        # Vardict
        self.step(
            "variantCaller_Vardict",
            VardictGermlineVariantCaller,
            bam=self.processBamFiles.out,
            reference=self.reference,
            intervals=self.vardictIntervals,
            sampleName=self.sampleName,
            allelFreqThreshold=self.allelFreqThreshold,
            headerLines=self.vardictHeaderLines,
        )
        self.step(
            "variantCaller_merge_Vardict",
            Gatk4GatherVcfs_4_0,
            vcfs=self.variantCaller_Vardict.out,
        )

        # GRIDSS
        self.step(
            "variantCaller_GRIDSS",
            GridssGermlineVariantCaller,
            bam=self.processBamFiles.out,
            reference=self.reference,
            blacklist=self.gridssBlacklist,
        )

        # Combine

        self.step(
            "combineVariants",
            CombineVariants_0_0_4,
            vcfs=[
                self.variantCaller_merge_GATK.out,
                self.variantCaller_Strelka.out,
                self.variantCaller_merge_Vardict.out,
                self.variantCaller_GRIDSS.out,
            ],
            type="Germline",
            columns=["AC", "AN", "AF", "AD", "DP", "GT"],
        )
        self.step("sortCombined", BcfToolsSort_1_9, vcf=self.combineVariants.vcf)

        self.output("bam", source=self.processBamFiles.out)
        self.output("reports", source=self.fastqc)
        self.output("combinedVariants", source=self.sortCombined.out)
        self.output("variants_gatk_split", source=self.variantCaller_GATK.out)
        self.output(
            "variants_vardict_split", source=self.variantCaller_merge_Vardict.out
        )
        self.output("variants_strelka", source=self.variantCaller_Strelka.out)
        self.output("variants_gatk", source=self.variantCaller_merge_GATK.out)
        self.output("variants_vardict", source=self.variantCaller_Vardict.out)
        self.output("variants_gridss", source=self.variantCaller_GRIDSS.out)


if __name__ == "__main__":
    w = WGSGermlineMultiCallers()
    # w.translate("cwl", to_console=False, to_disk=True, export_path="{language}")
    w.translate("wdl", to_console=True)  # , to_disk=True, export_path="{language}")
