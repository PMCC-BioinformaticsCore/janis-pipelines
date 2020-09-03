from datetime import date

from janis_bioinformatics.data_types import Bed, BedTabix
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.common import GATKBaseRecalBQSRWorkflow_4_1_3
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_1_3
from janis_bioinformatics.tools.htslib import BGZipLatest
from janis_bioinformatics.tools.pmac import (
    CombineVariants_0_0_8,
    GenerateVardictHeaderLines,
    AddBamStatsSomatic_0_1_0,
)
from janis_bioinformatics.tools.variantcallers import GatkSomaticVariantCaller_4_1_3
from janis_bioinformatics.tools.variantcallers.illuminasomatic_strelka import (
    IlluminaSomaticVariantCaller,
)
from janis_bioinformatics.tools.variantcallers.vardictsomatic_variants import (
    VardictSomaticVariantCaller,
)
from janis_core import (
    Array,
    Float,
    WorkflowMetadata,
    InputDocumentation,
    InputQualityType,
)
from janis_unix.tools import UncompressArchive

from janis_pipelines.wgs_somatic_gatk.wgssomaticgatk_variantsonly import (
    WGSSomaticGATKVariantsOnly,
)


class WGSSomaticMultiCallersVariantsOnly(WGSSomaticGATKVariantsOnly):
    def id(self):
        return "WGSSomaticMultiCallersVariantsOnly"

    def friendly_name(self):
        return "WGS Somatic (Multi callers) [VARIANTS only]"

    def version(self):
        return "1.3.0"

    def constructor(self):
        # don't call super()

        self.add_inputs()
        self.add_gridss(
            normal_bam_source=self.normal_bam, tumor_bam_source=self.tumor_bam
        )
        self.add_gatk_variantcaller(
            normal_bam_source=self.normal_bam, tumor_bam_source=self.tumor_bam
        )
        self.add_vardict_variantcaller(
            normal_bam_source=self.normal_bam, tumor_bam_source=self.tumor_bam
        )
        self.add_strelka_variantcaller(
            normal_bam_source=self.normal_bam, tumor_bam_source=self.tumor_bam
        )
        self.add_combine_variants(
            normal_bam_source=self.normal_bam, tumor_bam_source=self.tumor_bam
        )

    def add_inputs_for_intervals(self):
        super().add_inputs_for_intervals()

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

    def add_inputs_for_configuration(self):
        super().add_inputs_for_configuration()
        self.input(
            "allele_freq_threshold",
            Float,
            default=0.05,
            doc=InputDocumentation(
                "The threshold for VarDict's allele frequency, default: 0.05 or 5%",
                quality=InputQualityType.configuration,
                example=None,
            ),
        )

    def add_gatk_variantcaller(self, normal_bam_source, tumor_bam_source):

        recal_ins = {
            "reference": self.reference,
            "intervals": self.gatk_intervals,
            "snps_dbsnp": self.snps_dbsnp,
            "snps_1000gp": self.snps_1000gp,
            "known_indels": self.known_indels,
            "mills_indels": self.mills_indels,
        }
        self.step(
            "bqsr_normal",
            GATKBaseRecalBQSRWorkflow_4_1_3(bam=normal_bam_source, **recal_ins),
            scatter="intervals",
        )

        self.step(
            "bqsr_tumor",
            GATKBaseRecalBQSRWorkflow_4_1_3(bam=tumor_bam_source, **recal_ins),
            scatter="intervals",
        )

        self.step(
            "vc_gatk",
            GatkSomaticVariantCaller_4_1_3(
                normal_bam=self.bqsr_normal.out,
                tumor_bam=self.bqsr_tumor.out,
                normal_name=self.normal_name,
                intervals=self.gatk_intervals,
                reference=self.reference,
                gnomad=self.gnomad,
                panel_of_normals=self.panel_of_normals,
            ),
            scatter=["intervals", "normal_bam", "tumor_bam"],
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

        self.step(
            "addbamstats",
            AddBamStatsSomatic_0_1_0(
                normal_id=self.normal_name,
                tumor_id=self.tumor_name,
                normal_bam=normal_bam_source,
                tumor_bam=tumor_bam_source,
                reference=self.reference,
                vcf=self.vc_gatk_uncompress_for_combine.out,
            ),
        )

        # VCF
        self.output(
            "out_variants_gatk",
            source=self.vc_gatk_sort_combined.out,
            output_folder="variants",
            doc="Merged variants from the GATK caller",
        )
        self.output(
            "out_variants_split",
            source=self.vc_gatk.out,
            output_folder=["variants", "byInterval"],
            doc="Unmerged variants from the GATK caller (by interval)",
        )

    def add_strelka_variantcaller(self, normal_bam_source, tumor_bam_source):
        self.step(
            "vc_strelka",
            IlluminaSomaticVariantCaller(
                normal_bam=normal_bam_source,
                tumor_bam=tumor_bam_source,
                intervals=self.strelka_intervals,
                reference=self.reference,
            ),
        )

        self.output(
            "out_variants_strelka",
            source=self.vc_strelka.out,
            output_folder="variants",
            output_name="strelka",
            doc="Variants from the Strelka variant caller",
        )

    def add_vardict_variantcaller(self, normal_bam_source, tumor_bam_source):
        self.step(
            "generate_vardict_headerlines",
            GenerateVardictHeaderLines(reference=self.reference),
        )
        self.step(
            "vc_vardict",
            VardictSomaticVariantCaller(
                normal_bam=normal_bam_source,
                tumor_bam=tumor_bam_source,
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
            "out_variants_vardict_split",
            source=self.vc_vardict.out,
            output_folder=["variants", "vardict"],
            doc="Unmerged variants from the VarDict caller (by interval)",
        )

        self.output(
            "out_variants_vardict",
            source=self.vc_vardict_sort_combined.out,
            output_folder="variants",
            output_name="vardict",
            doc="Merged variants from the VarDict caller",
        )

    def add_combine_variants(self, normal_bam_source, tumor_bam_source):
        self.step(
            "combine_variants",
            CombineVariants_0_0_8(
                normal=self.normal_name,
                tumor=self.tumor_name,
                vcfs=[
                    self.vc_gatk_uncompress_for_combine.out,
                    self.vc_strelka.out,
                    self.vc_vardict_uncompress_for_combine.out,
                ],
                type="somatic",
                columns=["AD", "DP", "GT"],
            ),
        )

        self.step("combined_compress", BGZipLatest(file=self.combine_variants.out))
        self.step("combined_sort", BcfToolsSort_1_9(vcf=self.combined_compress.out))
        self.step("combined_uncompress", UncompressArchive(file=self.combined_sort.out))

        self.step(
            "combined_addbamstats",
            AddBamStatsSomatic_0_1_0(
                normal_id=self.normal_name,
                tumor_id=self.tumor_name,
                normal_bam=normal_bam_source,
                tumor_bam=tumor_bam_source,
                vcf=self.combined_uncompress.out,
                reference=self.reference,
            ),
        )

        self.output(
            "out_variants",
            source=self.addbamstats.out,
            output_folder="variants",
            doc="Combined variants from GATK, VarDict and Strelka callers",
        )

    def bind_metadata(self):
        meta: WorkflowMetadata = super().bind_metadata() or self.metadata

        meta.keywords = [
            "wgs",
            "cancer",
            "somatic",
            "variants",
            "gatk",
            "vardict",
            "strelka",
            "gridss",
        ]
        meta.contributors = ["Michael Franklin", "Richard Lupat", "Jiaan Yu"]
        meta.dateCreated = date(2018, 12, 24)
        meta.dateUpdated = date(2020, 8, 19)
        meta.short_documentation = "A somatic tumor-normal variant-calling WGS pipeline using GATK, VarDict and Strelka2."
        meta.documentation = """\
This is a genomics pipeline to align sequencing data (Fastq pairs) into BAMs:

- Takes raw sequence data in the FASTQ format;
- align to the reference genome using BWA MEM;
- Marks duplicates using Picard;
- Call the appropriate somatic variant callers (GATK / Strelka / VarDict);
- Outputs the final variants in the VCF format.

**Resources**

This pipeline has been tested using the HG38 reference set, available on Google Cloud Storage through:

- https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/

This pipeline expects the assembly references to be as they appear in that storage \
    (".fai", ".amb", ".ann", ".bwt", ".pac", ".sa", "^.dict").
The known sites (snps_dbsnp, snps_1000gp, known_indels, mills_indels) should be gzipped and tabix indexed.
"""

        # mfranklin: mostly handled by super call, but can override specific ones here:
        # meta.sample_input_overrides.update({
        #
        # })


if __name__ == "__main__":
    import os.path

    w = WGSSomaticMultiCallersVariantsOnly()
    args = {
        "to_console": True,
        "to_disk": False,
        "validate": True,
        "export_path": os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "{language}"
        ),
    }
    # w.translate("cwl", **args)
    w.translate("wdl", **args)
