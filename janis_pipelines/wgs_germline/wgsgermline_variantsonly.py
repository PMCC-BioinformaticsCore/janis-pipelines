from janis_bioinformatics.data_types import Bed, BedTabix, Vcf, CompressedVcf
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9, BcfToolsConcat_1_9
from janis_bioinformatics.tools.common import GATKBaseRecalBQSRWorkflow_4_1_3
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_1_3
from janis_bioinformatics.tools.htslib import BGZipLatest
from janis_bioinformatics.tools.papenfuss import Gridss_2_6_2
from janis_bioinformatics.tools.pmac import (
    CombineVariants_0_0_8,
    GenerateVardictHeaderLines,
    AddBamStatsGermline_0_1_0,
    GenerateIntervalsByChromosome,
    GenerateMantaConfig,
)
from janis_bioinformatics.tools.variantcallers import (
    GatkGermlineVariantCaller_4_1_3,
    IlluminaGermlineVariantCaller,
    VardictGermlineVariantCaller,
)
from janis_core import Array, Float, Int, String, WorkflowMetadata
from janis_core.operators.standard import FirstOperator
from janis_unix.tools import UncompressArchive

from janis_pipelines.wgs_germline_gatk.wgsgermlinegatk_variantsonly import (
    WGSGermlineGATKVariantsOnly,
    INPUT_DOCS,
)


class WGSGermlineMultiCallersVariantsOnly(WGSGermlineGATKVariantsOnly):
    def id(self):
        return "WGSGermlineMultiCallersVariantsOnly"

    def friendly_name(self):
        return "WGS Germline (Multi callers) [VARIANTS only]"

    def version(self):
        return "1.4.0"

    def constructor(self):
        self.add_inputs()

        self.add_bam_qc(bam_source=self.bam)

        # Add variant callers

        self.add_gridss(bam_source=self.bam)

        self.add_gatk_variantcaller(bam_source=self.bam)
        self.add_strelka_variantcaller(bam_source=self.bam)
        self.add_vardict_variantcaller(bam_source=self.bam)

        # Combine gatk / strelka / vardict variants
        self.add_combine_variants(bam_source=self.bam)

    def add_inputs_for_intervals(self):
        super().add_inputs_for_intervals()
        self.input("vardict_intervals", Array(Bed), doc=INPUT_DOCS["vardict_intervals"])
        self.input("strelka_intervals", BedTabix, doc=INPUT_DOCS["strelka_intervals"])
        # for fast processing wgs bam
        self.input("gridss_blacklist", Bed, doc=INPUT_DOCS["gridss_blacklist"])

    def add_gridss(self, bam_source):
        # GRIDSS
        self.step(
            "vc_gridss",
            Gridss_2_6_2(
                bams=[bam_source],
                reference=self.reference,
                blacklist=self.gridss_blacklist,
            ),
        )

        self.output(
            "out_gridss_assembly",
            source=self.vc_gridss.assembly,
            output_folder="gridss",
            doc="Assembly returned by GRIDSS",
        )
        self.output(
            "out_variants_gridss",
            source=self.vc_gridss.out,
            output_folder="gridss",
            doc="Variants from the GRIDSS variant caller",
        )

    def add_strelka_variantcaller(self, bam_source):

        # Strelka
        self.step("generate_manta_config", GenerateMantaConfig())

        self.step(
            "vc_strelka",
            IlluminaGermlineVariantCaller(
                bam=bam_source,
                reference=self.reference,
                intervals=self.strelka_intervals,
                manta_config=self.generate_manta_config.out,
            ),
        )

        self.output(
            "out_variants_strelka",
            source=self.vc_strelka.out,
            output_folder="variants",
            output_name="strelka",
            doc="Variants from the Strelka variant caller",
        )

    def add_vardict_variantcaller(self, bam_source):
        self.input(
            "allele_freq_threshold",
            Float,
            0.05,
        ),
        self.input("minMappingQual", Int(optional=True))
        self.input("filter", String(optional=True))
        # Vardict
        self.step(
            "generate_vardict_headerlines",
            GenerateVardictHeaderLines(reference=self.reference),
        )
        self.step(
            "vc_vardict",
            VardictGermlineVariantCaller(
                bam=bam_source,
                reference=self.reference,
                intervals=self.vardict_intervals,
                sample_name=self.sample_name,
                allele_freq_threshold=self.allele_freq_threshold,
                header_lines=self.generate_vardict_headerlines.out,
                minMappingQual=self.minMappingQual,
                filter=self.filter,
            ),
            scatter="intervals",
        )
        self.step(
            "vc_vardict_merge",
            BcfToolsConcat_1_9(vcf=self.vc_vardict.out.as_type(Array(Vcf))),
        )
        self.step(
            "vc_vardict_sort_combined",
            BcfToolsSort_1_9(vcf=self.vc_vardict_merge.out.as_type(CompressedVcf)),
        )

        self.step(
            "vc_vardict_uncompress_for_combine",
            UncompressArchive(file=self.vc_vardict_sort_combined.out),
        )

        self.output(
            "out_variants_vardict",
            source=self.vc_vardict_sort_combined.out,
            output_folder=["variants"],
            output_name="vardict",
            doc="Merged variants from the VarDict caller",
        )
        self.output(
            "out_variants_vardict_split",
            source=self.vc_vardict.out,
            output_folder=["variants", "vardict"],
            doc="Unmerged variants from the VarDict caller (by interval)",
        )

    def add_combine_variants(self, bam_source):

        # Note, this is reliant on the specific step names from previous steps

        # Combine
        self.step(
            "combine_variants",
            CombineVariants_0_0_8(
                vcfs=[
                    self.vc_gatk_uncompress.out.as_type(Vcf),
                    self.vc_strelka.out,
                    self.vc_vardict_uncompress_for_combine.out.as_type(Vcf),
                ],
                type="germline",
                columns=["AC", "AN", "AF", "AD", "DP", "GT"],
            ),
        )
        self.step("combined_compress", BGZipLatest(file=self.combine_variants.out))
        self.step(
            "combined_sort",
            BcfToolsSort_1_9(vcf=self.combined_compress.out.as_type(CompressedVcf)),
        )
        self.step("combined_uncompress", UncompressArchive(file=self.combined_sort.out))

        self.step(
            "combined_addbamstats",
            AddBamStatsGermline_0_1_0(
                bam=bam_source,
                vcf=self.combined_uncompress.out.as_type(Vcf),
                reference=self.reference,
            ),
        )

        self.output(
            "out_variants",
            source=self.combined_addbamstats.out,
            output_folder="variants",
            output_name="combined",
            doc="Combined variants from all 3 callers",
        )

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
        meta.contributors = ["Michael Franklin", "Richard Lupat", "Jiaan Yu"]

        meta.short_documentation = (
            "A variant-calling WGS pipeline using GATK, VarDict and Strelka2."
        )
        meta.documentation = """\
This workflow is a reference pipeline using the Janis Python framework (pipelines assistant).

- Call the appropriate variant callers (GRIDSS / GATK / Strelka / VarDict);
- Merges the variants from GATK / Strelka / VarDict.
- Outputs the final variants in the VCF format.

**Resources**

This pipeline has been tested using the HG38 reference set, available on Google Cloud Storage through:

- https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/

This pipeline expects the assembly references to be as they appear in that storage \
    (".fai", ".amb", ".ann", ".bwt", ".pac", ".sa", "^.dict").
The known sites (snps_dbsnp, snps_1000gp, known_indels, mills_indels) should be gzipped and tabix indexed.
"""


if __name__ == "__main__":
    import os.path

    w = WGSGermlineMultiCallersVariantsOnly()
    args = {
        "to_console": False,
        "to_disk": False,
        "validate": True,
        "export_path": os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "{language}"
        ),
        "with_resource_overrides": True,
    }
    # w.translate("cwl", **args)
    w.translate("wdl", **args)
    # WGSGermlineMultiCallersVariantsOnly().translate("wdl")
