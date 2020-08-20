from janis_bioinformatics.data_types import Bed, BedTabix
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.common import GATKBaseRecalBQSRWorkflow_4_1_3
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_1_3
from janis_bioinformatics.tools.htslib import BGZipLatest
from janis_bioinformatics.tools.pmac import (
    CombineVariants_0_0_8,
    GenerateVardictHeaderLines,
    AddBamStatsGermline_0_1_0,
)
from janis_bioinformatics.tools.variantcallers import (
    GatkGermlineVariantCaller_4_1_3,
    IlluminaGermlineVariantCaller,
    VardictGermlineVariantCaller,
)
from janis_core import Array, WorkflowMetadata, InputDocumentation, InputQualityType
from janis_unix.tools import UncompressArchive

from janis_pipelines.wgs_germline_gatk.wgsgermlinegatk_variantsonly import (
    WGSGermlineGATKVariantsOnly,
)


class WGSGermlineMultiCallersVariantsOnly(WGSGermlineGATKVariantsOnly):
    def id(self):
        return "WGSGermlineMultiCallersVariantsOnly"

    def friendly_name(self):
        return "WGS Germline (Multi callers) [VARIANTS only]"

    def version(self):
        return "1.3.1"

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

    def inputs_for_intervals(self):
        super().inputs_for_intervals()
        self.input(
            "vardict_intervals",
            Array(Bed),
            doc=InputDocumentation(
                "List of intervals over which to split the VarDict variant calling",
                quality=InputQualityType.static,
                example="BRCA1.bed",
            ),
        )
        self.input(
            "strelka_intervals",
            BedTabix,
            doc=InputDocumentation(
                "An interval for which to restrict the analysis to.",
                quality=InputQualityType.static,
                example="BRCA1.bed.gz",
            ),
        )

    def add_gatk_variantcaller(self, bam_source):

        # VARIANT CALLERS
        # GATK
        self.step(
            "bqsr",
            GATKBaseRecalBQSRWorkflow_4_1_3(
                bam=bam_source,
                reference=self.reference,
                intervals=self.gatk_intervals,
                snps_dbsnp=self.snps_dbsnp,
                snps_1000gp=self.snps_1000gp,
                known_indels=self.known_indels,
                mills_indels=self.mills_indels,
            ),
            scatter="intervals",
        )
        self.step(
            "vc_gatk",
            GatkGermlineVariantCaller_4_1_3(
                bam=self.bqsr.out,
                intervals=self.gatk_intervals,
                reference=self.reference,
                snps_dbsnp=self.snps_dbsnp,
            ),
            scatter=["intervals", "bam"],
        )
        self.step("vc_gatk_merge", Gatk4GatherVcfs_4_1_3(vcfs=self.vc_gatk.out))
        self.step("vc_gatk_compress_for_sort", BGZipLatest(file=self.vc_gatk_merge.out))
        self.step(
            "vc_gatk_sort_combined",
            BcfToolsSort_1_9(vcf=self.vc_gatk_compress_for_sort.out),
        )

        self.step(
            "vc_gatk_uncompress_for_combine",
            UncompressArchive(file=self.vc_gatk_sort_combined.out),
        )

        self.output(
            "out_variants_gatk",
            source=self.vc_gatk_sort_combined.out,
            output_folder="variants",
            output_name="gatk",
            doc="Merged variants from the GATK caller",
        )
        self.output(
            "out_variants_gatk_split",
            source=self.vc_gatk.out,
            output_folder=["variants", "gatk"],
            doc="Unmerged variants from the GATK caller (by interval)",
        )

    def add_strelka_variantcaller(self, bam_source):

        # Strelka
        self.step(
            "vc_strelka",
            IlluminaGermlineVariantCaller(
                bam=bam_source,
                reference=self.reference,
                intervals=self.strelka_intervals,
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
                allele_freq_threshold=0.05,
                header_lines=self.generate_vardict_headerlines.out,
            ),
            scatter="intervals",
        )
        self.step("vc_vardict_merge", Gatk4GatherVcfs_4_1_3(vcfs=self.vc_vardict.out))
        self.step(
            "vc_vardict_compress_for_sort", BGZipLatest(file=self.vc_vardict_merge.out)
        )
        self.step(
            "vc_vardict_sort_combined",
            BcfToolsSort_1_9(vcf=self.vc_vardict_compress_for_sort.out),
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
                    self.vc_gatk_uncompress_for_combine.out,
                    self.vc_strelka.out,
                    self.vc_vardict_uncompress_for_combine.out,
                ],
                type="germline",
                columns=["AC", "AN", "AF", "AD", "DP", "GT"],
            ),
        )
        self.step("combined_compress", BGZipLatest(file=self.combine_variants.out))
        self.step("combined_sort", BcfToolsSort_1_9(vcf=self.combined_compress.out))
        self.step("combined_uncompress", UncompressArchive(file=self.combined_sort.out))

        self.step(
            "combined_addbamstats",
            AddBamStatsGermline_0_1_0(
                bam=bam_source,
                vcf=self.combined_uncompress.out,
                reference=self.reference,
            ),
        )

        self.output(
            "out_variants",
            source=self.combined_addbamstats.out,
            output_folder="variants",
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
        "to_console": True,
        "to_disk": False,
        "validate": True,
        "export_path": os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "{language}"
        ),
        "with_resource_overrides": True,
    }
    # w.translate("cwl", **args)
    w.translate("wdl", **args)
