from datetime import date

from janis_bioinformatics.data_types import FastaWithDict, VcfTabix, Bed, BamBai
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import GATKBaseRecalBQSRWorkflow_4_1_3
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_1_3
from janis_bioinformatics.tools.htslib import BGZipLatest
from janis_bioinformatics.tools.papenfuss.gridss.gridss import Gridss_2_6_2
from janis_bioinformatics.tools.pmac import (
    PerformanceSummaryGenome_0_1_0,
    AddBamStatsGermline_0_1_0,
    GenerateGenomeFileForBedtoolsCoverage,
)
from janis_bioinformatics.tools.variantcallers import GatkGermlineVariantCaller_4_1_3
from janis_core import (
    File,
    String,
    Array,
    WorkflowMetadata,
    InputDocumentation,
    InputQualityType,
)
from janis_unix.tools import UncompressArchive


class WGSGermlineGATKVariantsOnly(BioinformaticsWorkflow):
    def id(self):
        return "WGSGermlineGATKVariantsOnly"

    def friendly_name(self):
        return "WGS Germline (GATK) [VARIANTS only]"

    def version(self):
        return "1.3.1"

    def constructor(self):
        self.add_inputs()
        self.add_bam_qc(bam_source=self.bam)

        # Add variant callers

        self.add_gridss(bam_source=self.bam)

        self.add_gatk_variantcaller(bam_source=self.bam)

    def add_inputs(self):
        # INPUTS
        self.input(
            "sample_name",
            String,
            doc=InputDocumentation(
                "Sample name from which to generate the readGroupHeaderLine for BwaMem",
                quality=InputQualityType.user,
                example="NA12878",
            ),
        )

        self.input(
            "bam",
            BamBai,
            doc=InputDocumentation(
                "Input indexed bam (+ .bam.bai) to process",
                quality=InputQualityType.user,
                example="NA12878.bam (the NA12878.bam.bai will be picked up automatically)",
            ),
        )

        self.inputs_for_reference()
        self.inputs_for_intervals()
        self.inputs_for_configuration()

    def inputs_for_intervals(self):
        self.input(
            "gatk_intervals",
            Array(Bed),
            doc=InputDocumentation(
                "List of intervals over which to split the GATK variant calling",
                quality=InputQualityType.static,
                example="BRCA1.bed",
            ),
        )

    def inputs_for_configuration(self):
        pass

    def inputs_for_reference(self):
        self.input(
            "reference",
            FastaWithDict,
            doc=InputDocumentation(
                """\
    The reference genome from which to align the reads. This requires a number indexes (can be generated \
    with the 'IndexFasta' pipeline This pipeline has been tested using the HG38 reference set.

    This pipeline expects the assembly references to be as they appear in the GCP example:

    - (".fai", ".amb", ".ann", ".bwt", ".pac", ".sa", "^.dict").""",
                quality=InputQualityType.static,
                example="HG38: https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/\n\n"
                "File: gs://genomics-public-data/references/hg38/v0/Homo_sapiens_assembly38.fasta",
            ),
        )

        self.input(
            "snps_dbsnp",
            VcfTabix,
            doc=InputDocumentation(
                "From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
                quality=InputQualityType.static,
                example="HG38: https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/\n\n"
                "(WARNING: The file available from the genomics-public-data resource on Google Cloud Storage is NOT compressed and indexed. This will need to be completed prior to starting the pipeline.\n\n"
                "File: gs://genomics-public-data/references/hg38/v0/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            ),
        )
        self.input(
            "snps_1000gp",
            VcfTabix,
            doc=InputDocumentation(
                "From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
                quality=InputQualityType.static,
                example="HG38: https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/\n\n"
                "File: gs://genomics-public-data/references/hg38/v0/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            ),
        )
        self.input(
            "known_indels",
            VcfTabix,
            doc=InputDocumentation(
                "From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
                quality=InputQualityType.static,
                example="HG38: https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/\n\n"
                "File: gs://genomics-public-data/references/hg38/v0/Homo_sapiens_assembly38.known_indels.vcf.gz",
            ),
        )
        self.input(
            "mills_indels",
            VcfTabix,
            doc=InputDocumentation(
                "From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
                quality=InputQualityType.static,
                example="HG38: https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/\n\n"
                "File: gs://genomics-public-data/references/hg38/v0/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
            ),
        )

        self.input(
            "cutadapt_adapters",
            File(optional=True),
            doc=InputDocumentation(
                "Specifies a containment list for cutadapt, which contains a list of sequences to determine valid "
                "overrepresented sequences from the FastQC report to trim with Cuatadapt. The file must contain sets "
                "of named adapters in the form: ``name[tab]sequence``. Lines prefixed with a hash will be ignored.",
                quality=InputQualityType.static,
                example="https://github.com/csf-ngs/fastqc/blob/master/Contaminants/contaminant_list.txt",
            ),
        )

        # for fast processing wgs bam
        self.input(
            "gridss_blacklist",
            Bed,
            doc=InputDocumentation(
                "BED file containing regions to ignore.",
                quality=InputQualityType.static,
                example="https://github.com/PapenfussLab/gridss#blacklist",
            ),
        )

    def add_bam_qc(self, bam_source):
        # Temporarily remove GATK4 DepthOfCoverage for performance reasons, see:
        #   https://gatk.broadinstitute.org/hc/en-us/community/posts/360071895391-Speeding-up-GATK4-DepthOfCoverage

        # self.step(
        #     "coverage",
        #     Gatk4DepthOfCoverage_4_1_6(
        #         bam=bam_source,
        #         reference=self.reference,
        #         outputPrefix=self.sample_name,
        #         intervals=self.gatk_intervals,
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

    def add_gatk_variantcaller(self, bam_source):
        # VARIANT CALLERS
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
                intervals=self.gatk_intervals,
            ),
            scatter=["intervals"],
            doc="Perform base quality score recalibration",
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
        self.step("vc_gatk_compressvcf", BGZipLatest(file=self.vc_gatk_merge.out))
        self.step(
            "vc_gatk_sort_combined", BcfToolsSort_1_9(vcf=self.vc_gatk_compressvcf.out)
        )

        self.step(
            "vc_gatk_uncompress_for_bamstats",
            UncompressArchive(file=self.vc_gatk_sort_combined.out),
        )

        self.step(
            "vc_gatk_addbamstats",
            AddBamStatsGermline_0_1_0(
                bam=bam_source,
                vcf=self.vc_gatk_uncompress_for_bamstats.out,
                reference=self.reference,
            ),
        )

        self.output(
            "out_variants",
            source=self.vc_gatk_sort_combined.out,
            output_folder="variants",
            output_name="gatk",
            doc="Merged variants from the GATK caller",
        )
        self.output(
            "out_variants_split",
            source=self.vc_gatk.out,
            output_folder=["variants", "gatk"],
            doc="Unmerged variants from the GATK caller (by interval)",
        )

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = ["wgs", "cancer", "germline", "variants", "gatk"]
        meta.contributors = ["Michael Franklin", "Richard Lupat", "Jiaan Yu"]
        meta.dateCreated = date(2018, 12, 24)
        meta.dateUpdated = date(2020, 6, 22)
        meta.short_documentation = "A variant-calling WGS pipeline using only the GATK Haplotype variant caller."
        meta.documentation = """\
This is a genomics pipeline to ONLY call variants using GATK and GRIDSS from an indexed bam. The final variants are outputted in the VCF format.

This workflow is a reference pipeline using the Janis Python framework (pipelines assistant).

- Call variants using GRIDSS and GATK4;
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
        "to_console": True,
        "to_disk": False,
        "validate": True,
        "export_path": os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "{language}"
        ),
        "with_resource_overrides": True,
    }
    w.translate("cwl", **args)
    w.translate("wdl", **args)
