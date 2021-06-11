from datetime import date

from janis_bioinformatics.data_types import (
    FastaWithDict,
    VcfTabix,
    Bed,
    BamBai,
    Vcf,
    CompressedVcf,
)
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9, BcfToolsConcat_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import GATKBaseRecalBQSRWorkflow_4_1_3
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_1_3
from janis_bioinformatics.tools.htslib import BGZipLatest
from janis_bioinformatics.tools.pmac import (
    PerformanceSummaryGenome_0_1_0,
    AddBamStatsGermline_0_1_0,
    GenerateGenomeFileForBedtoolsCoverage,
    GenerateIntervalsByChromosome,
)
from janis_bioinformatics.tools.variantcallers import GatkGermlineVariantCaller_4_1_3
from janis_core import (
    String,
    Array,
    WorkflowMetadata,
    InputQualityType,
)
from janis_core.operators.standard import FirstOperator
from janis_unix.tools import UncompressArchive

from janis_pipelines.reference import WGS_INPUTS

INPUT_DOCS = {
    **WGS_INPUTS,
    "fastqs": {
        "doc": "An array of FastqGz pairs. These are aligned separately and merged "
        "to create higher depth coverages from multiple sets of reads",
        "quality": InputQualityType.user,
        "example": [
            ["sample1_R1.fastq.gz", "sample1_R2.fastq.gz"],
            ["sample1_R1-TOPUP.fastq.gz", "sample1_R2-TOPUP.fastq.gz"],
        ],
    },
    "sample_name": {
        "doc": "Sample name from which to generate the readGroupHeaderLine for BwaMem",
        "quality": InputQualityType.user,
        "example": "NA12878",
    },
    "bam": {
        "doc": "Input indexed bam (+ .bam.bai) to process. You only specify the primary sample.bam, and the index (eg: NA12878.bam.bai) will be picked up automatically.",
        "quality": InputQualityType.user,
        "example": "NA12878.bam",
    },
}


class WGSGermlineGATKVariantsOnly(BioinformaticsWorkflow):
    def id(self):
        return "WGSGermlineGATKVariantsOnly"

    def friendly_name(self):
        return "WGS Germline (GATK) [VARIANTS only]"

    def version(self):
        return "1.4.0"

    def constructor(self):
        self.add_inputs()
        self.add_bam_qc(bam_source=self.bam)

        # Add variant callers

        self.add_gatk_variantcaller(bam_source=self.bam)
        self.add_addbamstats(bam_source=self.bam)

    def add_inputs(self):
        # INPUTS
        self.input("sample_name", String, doc=INPUT_DOCS["sample_name"])

        self.input("bam", BamBai, doc=INPUT_DOCS["bam"])

        self.add_inputs_for_reference()
        self.add_inputs_for_intervals()
        self.add_inputs_for_configuration()

    def add_inputs_for_intervals(self):
        self.input(
            "gatk_intervals",
            Array(Bed, optional=True),
            doc=INPUT_DOCS["gatk_intervals"],
        )

    def add_inputs_for_configuration(self):
        pass

    def add_inputs_for_reference(self):
        self.input("reference", FastaWithDict, doc=INPUT_DOCS["reference"])

        self.input("snps_dbsnp", VcfTabix, doc=INPUT_DOCS["snps_dbsnp"])
        self.input("snps_1000gp", VcfTabix, doc=INPUT_DOCS["snps_1000gp"])
        self.input("known_indels", VcfTabix, doc=INPUT_DOCS["known_indels"])
        self.input("mills_indels", VcfTabix, doc=INPUT_DOCS["mills_indels"])

    def add_bam_qc(self, bam_source):
        # Temporarily remove GATK4 DepthOfCoverage for performance reasons, see:
        #   https://gatk.broadinstitute.org/hc/en-us/community/posts/360071895391-Speeding-up-GATK4-DepthOfCoverage

        # self.step(
        #     "coverage",
        #     Gatk4DepthOfCoverage_4_1_6(
        #         bam=bam_source,
        #         reference=self.reference,
        #         outputPrefix=self.sample_name,
        #         intervals=intervals,
        #         # current version gatk 4.1.6.0 only support --count-type as COUNT_READS
        #         # countType="COUNT_FRAGMENTS_REQUIRE_SAME_BASE",
        #         omitDepthOutputAtEachBase=True,
        #         summaryCoverageThreshold=[1, 50, 100, 300, 500],
        #     ),
        # )

        self.step(
            "calculate_performancesummary_genomefile",
            GenerateGenomeFileForBedtoolsCoverage(reference=self.reference),
        )

        self.step(
            "performance_summary",
            PerformanceSummaryGenome_0_1_0(
                bam=bam_source,
                genome_file=self.calculate_performancesummary_genomefile.out,
                sample_name=self.sample_name,
            ),
        )

        # COVERGAE
        # self.output(
        #     "sample_coverage",
        #     source=self.coverage.out_sampleSummary,
        #     output_folder=["performance_summary", self.sample_name],
        #     doc="A text file of depth of coverage summary of bam",
        # )
        # BAM PERFORMANCE
        self.output(
            "out_performance_summary",
            source=self.performance_summary.performanceSummaryOut,
            output_folder=["performance_summary", self.sample_name],
            doc="A text file of performance summary of bam",
        )

    def add_gatk_variantcaller(self, bam_source):
        # VARIANT CALLERS

        intervals = FirstOperator(
            [
                self.gatk_intervals,
                self.step(
                    "generate_gatk_intervals",
                    GenerateIntervalsByChromosome(reference=self.reference),
                    when=self.gatk_intervals.is_null(),
                ).out_regions,
            ]
        )

        # GATK
        self.step(
            "bqsr",
            GATKBaseRecalBQSRWorkflow_4_1_3(
                bam=bam_source,
                reference=self.reference,
                snps_dbsnp=self.snps_dbsnp,
                snps_1000gp=self.snps_1000gp,
                known_indels=self.known_indels,
                mills_indels=self.mills_indels,
                intervals=intervals,
            ),
            scatter="intervals",
            doc="Perform base quality score recalibration",
        )
        self.step(
            "vc_gatk",
            GatkGermlineVariantCaller_4_1_3(
                bam=self.bqsr.out,
                intervals=intervals,
                reference=self.reference,
                snps_dbsnp=self.snps_dbsnp,
            ),
            scatter=["intervals", "bam"],
        )
        self.step(
            "vc_gatk_merge",
            BcfToolsConcat_1_9(vcf=self.vc_gatk.out.as_type(Array(Vcf))),
        )
        self.step(
            "vc_gatk_sort_combined",
            BcfToolsSort_1_9(vcf=self.vc_gatk_merge.out.as_type(CompressedVcf)),
        )
        self.step(
            "vc_gatk_uncompress",
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

    def add_addbamstats(self, bam_source):
        self.step(
            "vc_gatk_addbamstats",
            AddBamStatsGermline_0_1_0(
                bam=bam_source,
                vcf=self.vc_gatk_uncompress.out.as_type(Vcf),
                reference=self.reference,
            ),
        )
        self.output(
            "out_variants_bamstats",
            source=self.vc_gatk_addbamstats.out,
            output_folder="variants",
            output_name="gatk_bamstats",
        )

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = ["wgs", "cancer", "germline", "variants", "gatk"]
        meta.contributors = ["Michael Franklin", "Richard Lupat", "Jiaan Yu"]
        meta.dateCreated = date(2018, 12, 24)
        meta.dateUpdated = date(2021, 5, 28)
        meta.short_documentation = "A variant-calling WGS pipeline using only the GATK Haplotype variant caller."
        meta.documentation = """\
This is a genomics pipeline to ONLY call variants using GATK from an indexed bam. The final variants are outputted in the VCF format.

This workflow is a reference pipeline using the Janis Python framework (pipelines assistant).

- Call variants using GATK4;
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

    w = WGSGermlineGATKVariantsOnly()
    args = {
        "to_console": False,
        "to_disk": False,
        "validate": False,
        "export_path": os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "{language}"
        ),
        "with_resource_overrides": True,
    }
    # w.translate("cwl", **args)
    # w.translate("wdl", **args)
    w.translate("wdl")
