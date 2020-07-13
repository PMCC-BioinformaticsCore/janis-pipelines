from datetime import date

from janis_core import (
    File,
    String,
    Array,
    InputSelector,
    WorkflowMetadata,
    ScatterDescription,
    ScatterMethods,
    InputDocumentation,
    InputQualityType,
)
from janis_unix.tools import UncompressArchive
from janis_unix.data_types import TextFile

from janis_bioinformatics.data_types import (
    FastaWithDict,
    VcfTabix,
    FastqGzPair,
    Bed,
    Bam,
    BamBai,
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
from janis_bioinformatics.tools.variantcallers import GatkGermlineVariantCaller_4_1_3
from janis_bioinformatics.tools.papenfuss.gridss.gridss import Gridss_2_6_2
from janis_bioinformatics.tools.pmac import (
    ParseFastqcAdaptors,
    PerformanceSummaryGenome_0_1_0,
    AddBamStatsGermline_0_1_0,
)


class WGSGermlineGATK(BioinformaticsWorkflow):
    def id(self):
        return "WGSGermlineGATK"

    def friendly_name(self):
        return "WGS Germline (GATK only)"

    @staticmethod
    def version():
        return "1.3.0"

    def constructor(self):

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
            "fastqs",
            Array(FastqGzPair),
            doc=InputDocumentation(
                "An array of FastqGz pairs. These are aligned separately and merged "
                "to create higher depth coverages from multiple sets of reads",
                quality=InputQualityType.user,
                example="[[BRCA1_R1.fastq.gz, BRCA1_R2.fastq.gz]]",
            ),
        )
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
            "cutadapt_adapters",
            File(optional=True),
            doc=InputDocumentation(
                "Specifies a containment list for cutadapt, which contains a list of sequences to determine valid overrepresented sequences from "
                "the FastQC report to trim with Cuatadapt. The file must contain sets of named adapters in the form: "
                "``name[tab]sequence``. Lines prefixed with a hash will be ignored.",
                quality=InputQualityType.static,
                example="https://github.com/csf-ngs/fastqc/blob/master/Contaminants/contaminant_list.txt",
            ),
        )
        self.input(
            "gatk_intervals",
            Array(Bed),
            doc=InputDocumentation(
                "List of intervals over which to split the GATK variant calling",
                quality=InputQualityType.static,
                example="BRCA1.bed",
            ),
        )
        self.input(
            "genome_file",
            TextFile(),
            doc=InputDocumentation(
                "Genome file for bedtools query", quality=InputQualityType.static,
            ),
        )
        self.input(
            "gridss_blacklist",
            Bed,
            doc=InputDocumentation(
                "BED file containing regions to ignore.",
                quality=InputQualityType.static,
                example="https://github.com/PapenfussLab/gridss#blacklist",
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

        # STEPS

        self.step("fastqc", FastQC_0_11_5(reads=self.fastqs), scatter="reads")

        self.step(
            "getfastqc_adapters",
            ParseFastqcAdaptors(
                fastqc_datafiles=self.fastqc.datafile,
                cutadapt_adaptors_lookup=self.cutadapt_adapters,
            ),
            scatter="fastqc_datafiles",
            # when=NotNullOperator(self.cutadapt_adapters)
        )

        self.step(
            "align_and_sort",
            BwaAligner(
                fastq=self.fastqs,
                reference=self.reference,
                sample_name=self.sample_name,
                sortsam_tmpDir=".",
                cutadapt_adapter=self.getfastqc_adapters,
                cutadapt_removeMiddle3Adapter=self.getfastqc_adapters,
            ),
            scatter=["fastq", "cutadapt_adapter", "cutadapt_removeMiddle3Adapter"],
        )

        self.step(
            "merge_and_mark",
            MergeAndMarkBams_4_1_3(
                bams=self.align_and_sort, sampleName=self.sample_name
            ),
        )

        # STATISTICS of BAM
        self.step(
            "coverage",
            Gatk4DepthOfCoverage_4_1_6(
                bam=self.merge_and_mark,
                reference=self.reference,
                outputPrefix=self.sample_name,
                intervals=self.gatk_intervals,
                # current version gatk 4.1.6.0 only support --count-type as COUNT_READS
                # countType="COUNT_FRAGMENTS_REQUIRE_SAME_BASE",
                omitDepthOutputAtEachBase=True,
                summaryCoverageThreshold=[1, 50, 100, 300, 500],
            ),
        )

        self.step(
            "performance_summary",
            PerformanceSummaryGenome_0_1_0(
                bam=self.merge_and_mark,
                genome_file=self.genome_file,
                sample_name=self.sample_name,
            ),
        )

        # GRIDSS
        self.step(
            "vc_gridss",
            Gridss_2_6_2(
                bams=[self.merge_and_mark.out],
                reference=self.reference,
                blacklist=self.gridss_blacklist,
            ),
        )

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
        self.step("vc_gatk_compressvcf", BGZipLatest(file=self.vc_gatk_merge.out))
        self.step(
            "vc_gatk_sort_combined", BcfToolsSort_1_9(vcf=self.vc_gatk_compressvcf.out)
        )
        self.step(
            "vc_gatk_uncompressvcf",
            UncompressArchive(file=self.vc_gatk_sort_combined.out),
        )

        self.step(
            "addbamstats",
            AddBamStatsGermline_0_1_0(
                bam=self.merge_and_mark, vcf=self.vc_gatk_uncompressvcf.out
            ),
        )

        # RESULTS
        self.output(
            "reports",
            source=self.fastqc.out,
            output_folder=["reports", self.sample_name],
            doc="A zip file of the FastQC quality report.",
        )
        self.output(
            "sample_coverage",
            source=self.coverage.out_sampleSummary,
            output_folder=["performance_summary", self.sample_name],
            doc="A text file of depth of coverage summary of bam",
        )
        self.output(
            "summary",
            source=self.performance_summary.performanceSummaryOut,
            output_folder=["performance_summary", self.sample_name],
            doc="A text file of performance summary of bam",
        )
        # GRIDSS
        self.output(
            "gridss_assembly",
            source=self.vc_gridss.assembly,
            output_folder="gridss",
            doc="Assembly returned by GRIDSS",
        )
        self.output(
            "variants_gridss",
            source=self.vc_gridss.out,
            output_folder="gridss",
            doc="Variants from the GRIDSS variant caller",
        )
        self.output(
            "bam",
            source=self.merge_and_mark.out,
            output_folder=["bams", self.sample_name],
            output_name=self.sample_name,
            doc="Aligned and indexed bam.",
        )
        self.output(
            "variants",
            source=self.vc_gatk_sort_combined.out,
            output_folder="variants",
            output_name=self.sample_name,
            doc="Merged variants from the GATK caller",
        )
        self.output(
            "variants_split",
            source=self.vc_gatk.out,
            output_folder=["variants", "byInterval"],
            doc="Unmerged variants from the GATK caller (by interval)",
        )
        self.output(
            "variants_final",
            source=self.addbamstats.out,
            output_folder="variants",
            doc="Final vcf",
        )

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = ["wgs", "cancer", "germline", "variants", "gatk"]
        meta.contributors = ["Michael Franklin", "Richard Lupat", "Jiaan Yu"]
        meta.dateCreated = date(2018, 12, 24)
        meta.dateUpdated = date(2020, 6, 22)
        meta.short_documentation = "A variant-calling WGS pipeline using only the GATK Haplotype variant caller."
        meta.documentation = """\
This is a genomics pipeline to align sequencing data (Fastq pairs) into BAMs and call variants using GATK. The final variants are outputted in the VCF format.

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

    w = WGSGermlineGATK()
    args = {
        "to_console": False,
        "to_disk": True,
        "validate": True,
        "export_path": os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "{language}"
        ),
    }
    w.translate("cwl", **args)
    w.translate("wdl", **args)
