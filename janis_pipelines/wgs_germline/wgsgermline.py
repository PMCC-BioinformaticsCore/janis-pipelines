from datetime import date
from janis_unix.tools import UncompressArchive
from janis_unix.data_types import TextFile

from janis_core import (
    Array,
    File,
    String,
    Float,
    WorkflowMetadata,
    InputDocumentation,
    InputQualityType,
)

from janis_bioinformatics.data_types import (
    FastaWithDict,
    VcfTabix,
    FastqGzPair,
    Bed,
    BedTabix,
)
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import (
    BwaAligner,
    MergeAndMarkBams_4_1_3,
    GATKBaseRecalBQSRWorkflow_4_1_3,
)
from janis_bioinformatics.tools.htslib import BGZipLatest
from janis_bioinformatics.tools.gatk4 import (
    Gatk4GatherVcfs_4_1_3,
    Gatk4DepthOfCoverage_4_1_6,
)
from janis_bioinformatics.tools.pmac import (
    CombineVariants_0_0_8,
    GenerateVardictHeaderLines,
    ParseFastqcAdaptors,
    PerformanceSummaryGenome_0_1_0,
    AddBamStatsGermline_0_1_0,
    GenerateGenomeFileForBedtoolsCoverage,
)
from janis_bioinformatics.tools.papenfuss.gridss.gridss import Gridss_2_6_2
from janis_bioinformatics.tools.variantcallers import (
    GatkGermlineVariantCaller_4_1_3,
    IlluminaGermlineVariantCaller,
    VardictGermlineVariantCaller,
)

from janis_pipelines.wgs_germline_gatk.wgsgermlinegatk import WGSGermlineGATK


class WGSGermlineMultiCallers(WGSGermlineGATK):
    def id(self):
        return "WGSGermlineMultiCallers"

    def friendly_name(self):
        return "WGS Germline (Multi callers)"

    def version(self):
        return "1.3.1"

    def constructor(self):
        self.add_inputs()

        self.add_fastqc()

        self.add_align()

        self.add_bam_process()
        self.add_bam_qc()

        # Add variant callers

        self.add_gridss()

        self.add_gatk_variantcaller()
        self.add_strelka_variantcaller()
        self.add_vardict_variantcaller()

        # Combine gatk / strelka / vardict variants
        self.add_combine_variants()

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

    def add_gatk_variantcaller(self):

        # VARIANT CALLERS
        # GATK
        self.step(
            "bqsr",
            GATKBaseRecalBQSRWorkflow_4_1_3(
                bam=self.merge_and_mark,
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

    def add_strelka_variantcaller(self):

        # Strelka
        self.step(
            "vc_strelka",
            IlluminaGermlineVariantCaller(
                bam=self.merge_and_mark.out,
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

    def add_vardict_variantcaller(self):

        # Vardict
        self.step(
            "generate_vardict_headerlines",
            GenerateVardictHeaderLines(reference=self.reference),
        )
        self.step(
            "vc_vardict",
            VardictGermlineVariantCaller(
                bam=self.merge_and_mark.out,
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

    def add_combine_variants(self):

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
                bam=self.merge_and_mark, vcf=self.combined_uncompress.out
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
        meta.dateCreated = date(2018, 12, 24)
        meta.dateUpdated = date(2020, 7, 29)

        meta.short_documentation = (
            "A variant-calling WGS pipeline using GATK, VarDict and Strelka2."
        )
        meta.documentation = """\
This is a genomics pipeline to align sequencing data (Fastq pairs) into BAMs and call variants using:

This workflow is a reference pipeline using the Janis Python framework (pipelines assistant).

- Takes raw sequence data in the FASTQ format;
- Align to the reference genome using BWA MEM;
- Marks duplicates using Picard;
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
        meta.sample_input_overrides = {
            "fastqs": [
                ["sample1_R1.fastq.gz", "sample1_R2.fastq.gz"],
                ["sample1_R1-TOPUP.fastq.gz", "sample1_R2-TOPUP.fastq.gz"],
            ],
            "reference": "Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_indels": "Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        }


if __name__ == "__main__":
    import os.path

    w = WGSGermlineMultiCallers()
    args = {
        "to_console": False,
        "to_disk": True,
        "validate": True,
        "export_path": os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "{language}"
        ),
        "with_resource_overrides": True,
    }
    w.translate("cwl", **args)
    w.translate("wdl", **args)
