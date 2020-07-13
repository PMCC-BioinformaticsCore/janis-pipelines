from datetime import date

from janis_core import String, Array, Float, WorkflowMetadata
from janis_unix.tools import UncompressArchive

from janis_bioinformatics.data_types import (
    FastaWithDict,
    VcfTabix,
    Bed,
    BedTabix,
    BamBai,
)
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import GATKBaseRecalBQSRWorkflow_4_1_3
from janis_bioinformatics.tools.htslib import BGZipLatest
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_1_3
from janis_bioinformatics.tools.pmac import (
    CombineVariants_0_0_8,
    GenerateVardictHeaderLines,
    AddBamStatsSomatic_0_1_0,
)
from janis_bioinformatics.tools.variantcallers import (
    GatkSomaticVariantCaller_4_1_3,
    IlluminaSomaticVariantCaller,
    VardictSomaticVariantCaller,
)


class WGSSomaticMultiCallers(BioinformaticsWorkflow):
    def id(self):
        return "WGSSomaticMultiCallers"

    def friendly_name(self):
        return "WGS Somatic (Multi callers)"

    def version(self):
        return "1.3.0"

    def constructor(self):
        self.input("normal", BamBai)
        self.input("tumor", BamBai)
        self.input("normal_name", String())
        self.input("tumor_name", String())

        self.input("gatk_intervals", Array(Bed))
        self.input("vardict_intervals", Array(Bed))
        self.input("strelka_intervals", BedTabix(optional=True))

        self.input("allele_freq_threshold", Float, default=0.05)

        self.input("reference", FastaWithDict)
        self.input("snps_dbsnp", VcfTabix)
        self.input("snps_1000gp", VcfTabix)
        self.input("known_indels", VcfTabix)
        self.input("mills_indels", VcfTabix)
        self.input("gnomad", VcfTabix)
        self.input("panel_of_normals", VcfTabix(optional=True))

        # STEPS
        self.step(
            "normal_bqsr",
            GATKBaseRecalBQSRWorkflow_4_1_3(
                bam=self.normal,
                reference=self.reference,
                snps_dbsnp=self.snps_dbsnp,
                snps_1000gp=self.snps_1000gp,
                known_indels=self.known_indels,
                mills_indels=self.mills_indels,
            ),
        )
        self.step(
            "tumor_bqsr",
            GATKBaseRecalBQSRWorkflow_4_1_3(
                bam=self.tumor,
                reference=self.reference,
                snps_dbsnp=self.snps_dbsnp,
                snps_1000gp=self.snps_1000gp,
                known_indels=self.known_indels,
                mills_indels=self.mills_indels,
            ),
        )
        self.step(
            "vc_gatk",
            GatkSomaticVariantCaller_4_1_3(
                normal_bam=self.normal_bqsr.out,
                tumor_bam=self.tumor_bqsr.out,
                normal_name=self.normal_name,
                intervals=self.gatk_intervals,
                reference=self.reference,
                gnomad=self.gnomad,
                panel_of_normals=self.panel_of_normals,
            ),
            scatter="intervals",
        )
        self.step("vc_gatk_merge", Gatk4GatherVcfs_4_1_3(vcfs=self.vc_gatk.out))
        self.step("vc_gatk_compressvcf", BGZipLatest(file=self.vc_gatk_merge.out))
        self.step(
            "vc_gatk_sort_combined", BcfToolsSort_1_9(vcf=self.vc_gatk_compressvcf.out)
        )
        self.step(
            "vc_gatk_uncompressvcf",
            UncompressArchive(file=self.vc_gatk_sort_combined.out),
        )

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
            "generate_vardict_headerlines",
            GenerateVardictHeaderLines(reference=self.reference),
        )
        self.step(
            "vc_vardict",
            VardictSomaticVariantCaller(
                normal_bam=self.normal,
                tumor_bam=self.tumor,
                normal_name=self.normal_name,
                tumor_name=self.tumor_name,
                header_lines=self.generate_vardict_headerlines.out,
                intervals=self.vardict_intervals,
                reference=self.reference,
                allele_freq_threshold=self.allele_freq_threshold,
            ),
            scatter="intervals",
        )
        self.step("vc_vardict_merge", Gatk4GatherVcfs_4_1_3(vcfs=self.vc_vardict.out))
        self.step("vc_vardict_compressvcf", BGZipLatest(file=self.vc_vardict_merge.out))
        self.step(
            "vc_vardict_sort_combined",
            BcfToolsSort_1_9(vcf=self.vc_vardict_compressvcf.out),
        )
        self.step(
            "vc_vardict_uncompressvcf",
            UncompressArchive(file=self.vc_vardict_sort_combined.out),
        )

        self.step(
            "combine_variants",
            CombineVariants_0_0_8(
                normal=self.normal_name,
                tumor=self.tumor_name,
                vcfs=[
                    self.vc_gatk_uncompressvcf.out,
                    self.vc_strelka.out,
                    self.vc_vardict_uncompressvcf.out,
                ],
                type="somatic",
                columns=["AD", "DP", "GT"],
            ),
        )
        self.step("combined_compress", BGZipLatest(file=self.combine_variants.out))
        self.step("combined_sort", BcfToolsSort_1_9(vcf=self.combined_compress.out))
        self.step("combined_uncompress", UncompressArchive(file=self.combined_sort.out))

        self.step(
            "addbamstats",
            AddBamStatsSomatic_0_1_0(
                normal_id=self.normal_name,
                tumor_id=self.tumor_name,
                normal_bam=self.normal,
                tumor_bam=self.tumor,
                vcf=self.combined_uncompress.out,
            ),
        )

        # Outputs
        self.output(
            "variants_gatk",
            source=self.vc_gatk_sort_combined.out,
            output_folder="variants",
        )
        self.output(
            "variants_strelka", source=self.vc_strelka.out, output_folder="variants"
        )
        self.output(
            "variants_vardict",
            source=self.vc_vardict_sort_combined.out,
            output_folder="variants",
        )
        self.output(
            "variants_combined", source=self.addbamstats.out, output_folder="variants",
        )
        self.output(
            "variants_gatk_split",
            source=self.vc_gatk.out,
            output_folder=["variants", "gatk"],
            doc="Unmerged variants from the GATK caller (by interval)",
        )
        self.output(
            "variants_vardict_split",
            source=self.vc_vardict.out,
            output_folder=["variants", "vardict"],
            doc="Unmerged variants from the VarDict caller (by interval)",
        )
