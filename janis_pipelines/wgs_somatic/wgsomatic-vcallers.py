from datetime import date

from janis_bioinformatics.data_types import (
    FastaWithDict,
    FastqGzPair,
    VcfTabix,
    Bed,
    BedTabix,
    BamBai,
)
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import BwaAligner, MergeAndMarkBams_4_1_3
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_1_3
from janis_bioinformatics.tools.pmac import CombineVariants_0_0_4
from janis_bioinformatics.tools.variantcallers import GatkSomaticVariantCaller_4_1_3
from janis_bioinformatics.tools.papenfuss.gridss.gridss import Gridss_2_6_3
from janis_bioinformatics.tools.variantcallers.illuminasomatic_strelka import (
    IlluminaSomaticVariantCaller,
)
from janis_bioinformatics.tools.variantcallers.vardictsomatic_variants import (
    VardictSomaticVariantCaller,
)
from janis_bioinformatics.tools.pmac import ParseFastqcAdaptors

from janis_core import String, WorkflowBuilder, File, Array, Float, WorkflowMetadata


class WGSSomaticMultiCallers(BioinformaticsWorkflow):
    def id(self):
        return "WGSSomaticMultiCallers"

    def friendly_name(self):
        return "WGS Somatic (Multi callers)"

    def version(self):
        return "1.2.0"

    def constructor(self):
        self.input("normal", BamBai)
        self.input("tumor", BamBai)

        self.input("normal_name", String(), value="NA24385_normal")
        self.input("tumor_name", String(), value="NA24385_tumour")

        self.input("gridss_blacklist", Bed)

        self.input("gatk_intervals", Array(Bed))
        self.input("vardict_intervals", Array(Bed))
        self.input("strelka_intervals", BedTabix(optional=True))

        self.input("vardict_header_lines", File)
        self.input("allele_freq_threshold", Float, default=0.05)

        self.input("reference", FastaWithDict)
        self.input("snps_dbsnp", VcfTabix)
        self.input("snps_1000gp", VcfTabix)
        self.input("known_indels", VcfTabix)
        self.input("mills_indels", VcfTabix)

        self.step(
            "vc_gatk",
            GatkSomaticVariantCaller_4_1_3(
                normal_bam=self.tumor,
                tumor_bam=self.normal,
                normal_name=self.normal_name,
                tumor_name=self.tumor_name,
                intervals=self.gatk_intervals,
                reference=self.reference,
                snps_dbsnp=self.snps_dbsnp,
                snps_1000gp=self.snps_1000gp,
                known_indels=self.known_indels,
                mills_indels=self.mills_indels,
            ),
            scatter="intervals",
        )

        self.step("vc_gatk_merge", Gatk4GatherVcfs_4_1_3(vcfs=self.vc_gatk))

        self.step(
            "vc_strelka",
            IlluminaSomaticVariantCaller(
                normal_bam=self.normal,
                tumor_bam=self.tumor,
                intervals=self.strelka_intervals,
                reference=self.reference,
            ),
        )

        self.step(
            "vc_gridss",
            Gridss_2_6_3(
                bams=[self.normal, self.tumor],
                reference=self.reference,
                blacklist=self.gridss_blacklist,
            ),
        )

        self.step(
            "vc_vardict",
            VardictSomaticVariantCaller(
                normal_bam=self.tumor,
                tumor_bam=self.normal,
                normal_name=self.normal_name,
                tumor_name=self.tumor_name,
                header_lines=self.vardict_header_lines,
                intervals=self.vardict_intervals,
                reference=self.reference,
                allele_freq_threshold=self.allele_freq_threshold,
            ),
            scatter="intervals",
        )

        self.step("vc_vardict_merge", Gatk4GatherVcfs_4_1_3(vcfs=self.vc_vardict.out))

        self.step(
            "combine_variants",
            CombineVariants_0_0_4(
                normal=self.normal_name,
                tumor=self.tumor_name,
                vcfs=[
                    self.vc_gatk_merge.out,
                    self.vc_strelka.out,
                    self.vc_vardict_merge.out,
                ],
                type="somatic",
                columns=["AD", "DP", "GT"],
            ),
        )
        self.step("sortCombined", BcfToolsSort_1_9(vcf=self.combine_variants.vcf))

        # Outputs

        self.output("gridss_assembly", source=self.vc_gridss.out, output_folder="bams")

        self.output(
            "variants_gatk", source=self.vc_gatk_merge.out, output_folder="variants"
        )
        self.output(
            "variants_strelka", source=self.vc_strelka.out, output_folder="variants"
        )
        self.output(
            "variants_vardict",
            source=self.vc_vardict_merge.out,
            output_folder="variants",
        )
        self.output(
            "variants_gridss", source=self.vc_gridss.out, output_folder="variants"
        )
        self.output(
            "variants_combined",
            source=self.combine_variants.vcf,
            output_folder="variants",
        )
