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
)
from janis_bioinformatics.tools.papenfuss.gridss.gridss import Gridss_2_6_2
from janis_bioinformatics.tools.variantcallers import (
    GatkGermlineVariantCaller_4_1_3,
    IlluminaGermlineVariantCaller,
    VardictGermlineVariantCaller,
)


class WGSGermlineMultiCallers(BioinformaticsWorkflow):
    def id(self):
        return "WGSGermlineMultiCallers"

    def friendly_name(self):
        return "WGS Germline (Multi callers)"

    def version(self):
        return "1.3.0"

    def constructor(self):

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
        # for fast processing wgs bam
        # to do: create genome file like vardict header
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
        )

        self.step(
            "align_and_sort",
            BwaAligner(
                fastq=self.fastqs,
                reference=self.reference,
                sample_name=self.sample_name,
                sortsam_tmpDir="./tmp",
                cutadapt_adapter=self.getfastqc_adapters,
                cutadapt_removeMiddle3Adapter=self.getfastqc_adapters,
            ),
            scatter=["fastq", "cutadapt_adapter", "cutadapt_removeMiddle3Adapter"],
        )

        self.step(
            "merge_and_mark",
            MergeAndMarkBams_4_1_3(
                bams=self.align_and_sort.out, sampleName=self.sample_name
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

        # Strelka
        self.step(
            "vc_strelka",
            IlluminaGermlineVariantCaller(
                bam=self.merge_and_mark.out,
                reference=self.reference,
                intervals=self.strelka_intervals,
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
                bam=self.merge_and_mark.out,
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
            AddBamStatsGermline_0_1_0(
                bam=self.merge_and_mark, vcf=self.combined_uncompress.out
            ),
        )

        # Outputs
        # FASTQC
        self.output(
            "reports",
            source=self.fastqc.out,
            output_folder="reports",
            doc="A zip file of the FastQC quality report.",
        )
        # COVERGAE
        self.output(
            "sample_coverage",
            source=self.coverage.out_sampleSummary,
            output_folder=["performance_summary", self.sample_name],
            doc="A text file of depth of coverage summary of bam",
        )
        # BAM PERFORMANCE
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
        # BAM
        self.output(
            "bam",
            source=self.merge_and_mark.out,
            output_folder="bams",
            doc="Aligned and indexed bam.",
            output_name=self.sample_name,
        )
        # VCF
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

        meta.short_documentation = (
            "A variant-calling WGS pipeline using GATK, VarDict and Strelka2."
        )
        meta.documentation = """\
This is a genomics pipeline to align sequencing data (Fastq pairs) into BAMs and call variants using:

This workflow is a reference pipeline using the Janis Python framework (pipelines assistant).

- Takes raw sequence data in the FASTQ format;
- align to the reference genome using BWA MEM;
- Marks duplicates using Picard;
- Call the appropriate variant callers (GATK / Strelka / VarDict);
- Outputs the final variants in the VCF format.
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
    }
    w.translate("cwl", **args)
    w.translate("wdl", **args)
