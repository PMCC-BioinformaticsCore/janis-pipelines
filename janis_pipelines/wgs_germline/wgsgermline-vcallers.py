from datetime import date
from janis_core import Array, File, String, Float, WorkflowMetadata
from janis_unix.tools import UncompressArchive

from janis_bioinformatics.data_types import (
    FastaWithDict,
    VcfTabix,
    BamBai,
    Bed,
    BedTabix,
)

from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import GATKBaseRecalBQSRWorkflow_4_1_3
from janis_bioinformatics.tools.htslib import BGZipLatest
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_1_3
from janis_bioinformatics.tools.pmac import (
    CombineVariants_0_0_8,
    AddBamStatsGermline_0_1_0,
    GenerateVardictHeaderLines,
)
from janis_bioinformatics.tools.variantcallers import (
    GatkGermlineVariantCaller_4_1_3,
    IlluminaGermlineVariantCaller,
    VardictGermlineVariantCaller,
)


class WGSGermlineMultiCallersVariantsOnly(BioinformaticsWorkflow):
    def id(self):
        return "WGSGermlineMultiCallersVariantsOnly"

    def friendly_name(self):
        return "WGS Germline (Multi callers) [VARIANTS ONLY]"

    @staticmethod
    def version():
        return "1.3.0"

    def constructor(self):

        self.input(
            "sample_name",
            String,
            doc="Sample name from which to generate the readGroupHeaderLine for BwaMem",
        )
        self.input(
            "bam",
            BamBai,
            doc="An array of FastqGz pairs. These are aligned separately and merged to create higher depth coverages from multiple sets of reads",
        )
        self.input(
            "reference",
            FastaWithDict,
            doc="The reference genome from which to align the reads. This requires a number indexes (can be generated with the 'IndexFasta' pipeline. This pipeline has been tested with the hg38 reference genome.",
        )
        self.input(
            "gatk_intervals",
            Array(Bed),
            doc="List of intervals over which to split the GATK variant calling",
        )
        self.input(
            "vardict_intervals",
            Array(Bed),
            doc="List of intervals over which to split the VarDict variant calling",
        )
        self.input(
            "strelka_intervals",
            BedTabix,
            doc="An interval for which to restrict the analysis to. Recommended HG38 interval: ",
        )
        self.input(
            "allele_freq_threshold",
            Float,
            default=0.05,
            doc="The threshold for VarDict's allele frequency, default: 0.05 or 5%",
        )
        self.input(
            "snps_dbsnp",
            VcfTabix,
            doc="From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
        )
        self.input(
            "snps_1000gp",
            VcfTabix,
            doc="From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
        )
        self.input(
            "known_indels",
            VcfTabix,
            doc="From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
        )
        self.input(
            "mills_indels",
            VcfTabix,
            doc="From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
        )

        # VARIANT CALLERS
        # GATK
        self.step(
            "bqsr",
            GATKBaseRecalBQSRWorkflow_4_1_3(
                bam=self.bam,
                reference=self.reference,
                snps_dbsnp=self.snps_dbsnp,
                snps_1000gp=self.snps_1000gp,
                known_indels=self.known_indels,
                mills_indels=self.mills_indels,
            ),
        )
        self.step(
            "vc_gatk",
            GatkGermlineVariantCaller_4_1_3(
                bam=self.bqsr.out,
                intervals=self.gatk_intervals,
                reference=self.reference,
                snps_dbsnp=self.snps_dbsnp,
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

        # Strelka
        self.step(
            "vc_strelka",
            IlluminaGermlineVariantCaller(
                bam=self.bam, reference=self.reference, intervals=self.strelka_intervals
            ),
        )

        # Vardict
        self.step(
            "generate_vardict_headerlines",
            GenerateVardictHeaderLines(reference=self.reference),
        )
        self.step(
            "vc_vardict",
            VardictGermlineVariantCaller(
                bam=self.bam,
                reference=self.reference,
                intervals=self.vardict_intervals,
                sample_name=self.sample_name,
                allele_freq_threshold=self.allele_freq_threshold,
                header_lines=self.generate_vardict_headerlines.out,
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

        # Combine
        self.step(
            "combine_variants",
            CombineVariants_0_0_8(
                vcfs=[
                    self.vc_gatk_uncompressvcf.out,
                    self.vc_strelka.out,
                    self.vc_vardict_uncompressvcf.out,
                ],
                type="germline",
                columns=["AC", "AN", "AF", "AD", "DP", "GT"],
            ),
        )
        self.step("combined_compress", BGZipLatest(file=self.combine_variants.out))
        self.step("combined_sort", BcfToolsSort_1_9(vcf=self.combined_compress.out))
        self.step("combined_uncompress", UncompressArchive(file=self.combined_sort.out))
        self.step(
            "addbamstats",
            AddBamStatsGermline_0_1_0(bam=self.bam, vcf=self.combined_uncompress.out),
        )

        self.output(
            "variants_combined",
            source=self.addbamstats.out,
            output_folder="variants",
            doc="Combined variants from all 3 callers",
        )

        self.output(
            "variants_gatk",
            source=self.vc_gatk_sort_combined.out,
            output_folder="variants",
            output_name="gatk",
            doc="Merged variants from the GATK caller",
        )
        self.output(
            "variants_vardict",
            source=self.vc_vardict_sort_combined.out,
            output_folder=["variants"],
            output_name="vardict",
            doc="Merged variants from the VarDict caller",
        )
        self.output(
            "variants_strelka",
            source=self.vc_strelka.out,
            output_folder="variants",
            output_name="strelka",
            doc="Variants from the Strelka variant caller",
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
        meta.dateCreated = date(2018, 12, 24)
        meta.dateUpdated = date(2020, 6, 22)

        meta.short_documentation = "A (VARIANT ONLY) variant-calling WGS pipeline using GATK, VarDict and Strelka2."
        meta.documentation = """\
This is a genomics pipeline which:

- Call the appropriate variant callers (GATK / Strelka / VarDict);
- Outputs the final variants in the VCF format.

**Resources**

This pipeline has been tested using the HG38 reference set, available on Google Cloud Storage through:

- https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/

This pipeline expects the assembly references to be as they appear in that storage \
    (".fai", ".amb", ".ann", ".bwt", ".pac", ".sa", "^.dict").
The known sites (snps_dbsnp, snps_1000gp, known_indels, mills_indels) should be gzipped and tabix indexed.
"""
        meta.sample_input_overrides = {
            "reference": "Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_indels": "Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        }


if __name__ == "__main__":
    import os.path

    w = WGSGermlineMultiCallersVariantsOnly()
    args = {
        "to_console": False,
        "to_disk": True,
        "validate": True,
        "export_path": os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "variant-only/{language}"
        ),
    }
    w.translate("cwl", **args)
    w.translate("wdl", **args)
