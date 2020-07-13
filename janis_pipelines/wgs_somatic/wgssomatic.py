from datetime import date
from janis_core import (
    String,
    WorkflowBuilder,
    File,
    Array,
    Float,
    WorkflowMetadata,
    InputDocumentation,
    InputQualityType,
)
from janis_unix.tools import UncompressArchive
from janis_unix.data_types import TextFile

from janis_bioinformatics.data_types import (
    FastaWithDict,
    FastqGzPair,
    VcfTabix,
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
    AddBamStatsSomatic_0_1_0,
    ParseFastqcAdaptors,
    PerformanceSummaryGenome_0_1_0,
)
from janis_bioinformatics.tools.papenfuss.gridss.gridss import Gridss_2_6_2
from janis_bioinformatics.tools.variantcallers import GatkSomaticVariantCaller_4_1_3
from janis_bioinformatics.tools.variantcallers.illuminasomatic_strelka import (
    IlluminaSomaticVariantCaller,
)
from janis_bioinformatics.tools.variantcallers.vardictsomatic_variants import (
    VardictSomaticVariantCaller,
)


class WGSSomaticMultiCallers(BioinformaticsWorkflow):
    def id(self):
        return "WGSSomaticMultiCallers"

    def friendly_name(self):
        return "WGS Somatic (Multi callers)"

    @staticmethod
    def version():
        return "1.3.0"

    def constructor(self):

        # INPUTS
        self.input(
            "normal_inputs",
            Array(FastqGzPair),
            doc=InputDocumentation(
                "An array of NORMAL FastqGz pairs. These are aligned separately and merged to create higher depth coverages from multiple sets of reads",
                quality=InputQualityType.user,
                example='["normal_R1.fastq.gz", "normal_R2.fastq.gz"]',
            ),
        )
        self.input(
            "tumor_inputs",
            Array(FastqGzPair),
            doc=InputDocumentation(
                "An array of TUMOR FastqGz pairs. These are aligned separately and merged to create higher depth coverages from multiple sets of reads",
                quality=InputQualityType.user,
                example='["tumor_R1.fastq.gz", "tumor_R2.fastq.gz"]',
            ),
        )
        self.input(
            "normal_name",
            String(),
            doc=InputDocumentation(
                "Sample name for the NORMAL sample from which to generate the readGroupHeaderLine for BwaMem",
                quality=InputQualityType.user,
                example="NA24385_normal",
            ),
        )
        self.input(
            "tumor_name",
            String(),
            doc=InputDocumentation(
                "Sample name for the TUMOR sample from which to generate the readGroupHeaderLine for BwaMem",
                quality=InputQualityType.user,
                example="NA24385_tumor",
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
            "gnomad",
            VcfTabix(),
            doc=InputDocumentation(
                "The genome Aggregation Database (gnomAD)",
                quality=InputQualityType.static,
            ),
        )
        self.input(
            "panel_of_normals",
            VcfTabix(optional=True),
            doc=InputDocumentation(
                "VCF file of sites observed in normal.",
                quality=InputQualityType.static,
                example="gs://gatk-best-practices/somatic-b37/Mutect2-exome-panel.vcf or gs://gatk-best-practices/somatic-b37/Mutect2-WGS-panel-b37.vcf for hg19/b37",
            ),
        )

        # STEPS
        self.step(
            "tumor",
            self.process_subpipeline(
                reads=self.tumor_inputs,
                sample_name=self.tumor_name,
                reference=self.reference,
                cutadapt_adapters=self.cutadapt_adapters,
                genome_file=self.genome_file,
                gatk_intervals=self.gatk_intervals,
                snps_dbsnp=self.snps_dbsnp,
                snps_1000gp=self.snps_1000gp,
                known_indels=self.known_indels,
                mills_indels=self.mills_indels,
            ),
        )
        self.step(
            "normal",
            self.process_subpipeline(
                reads=self.normal_inputs,
                sample_name=self.normal_name,
                reference=self.reference,
                cutadapt_adapters=self.cutadapt_adapters,
                genome_file=self.genome_file,
                gatk_intervals=self.gatk_intervals,
                snps_dbsnp=self.snps_dbsnp,
                snps_1000gp=self.snps_1000gp,
                known_indels=self.known_indels,
                mills_indels=self.mills_indels,
            ),
        )

        # GRIDSS
        self.step(
            "vc_gridss",
            Gridss_2_6_2(
                bams=[self.normal.out, self.tumor.out],
                reference=self.reference,
                blacklist=self.gridss_blacklist,
            ),
        )

        # VARIANT CALLING
        self.step(
            "vc_gatk",
            GatkSomaticVariantCaller_4_1_3(
                normal_bam=self.normal.bqsr_bam,
                tumor_bam=self.tumor.bqsr_bam,
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
                normal_bam=self.normal.out,
                tumor_bam=self.tumor.out,
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
                normal_bam=self.normal.out,
                tumor_bam=self.tumor.out,
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
                normal_bam=self.normal.out,
                tumor_bam=self.tumor.out,
                vcf=self.combined_uncompress.out,
            ),
        )

        # Outputs
        # FASTQC
        self.output(
            "normal_report", source=self.normal.reports, output_folder="reports"
        )
        self.output("tumor_report", source=self.tumor.reports, output_folder="reports")
        # COVERAGE
        self.output(
            "normal_coverage",
            source=self.normal.depth_of_coverage,
            output_folder=["summary", self.normal_name],
            doc="A text file of depth of coverage summary of NORMAL bam",
        )
        self.output(
            "tumor_coverage",
            source=self.tumor.depth_of_coverage,
            output_folder=["summary", self.tumor_name],
            doc="A text file of depth of coverage summary of TUMOR bam",
        )
        # BAM PERFORMANCE
        self.output(
            "normal_summary",
            source=self.normal.summary,
            output_folder=["summary", self.normal_name],
            doc="A text file of performance summary of NORMAL bam",
        )
        self.output(
            "tumor_summary",
            source=self.tumor.summary,
            output_folder=["summary", self.tumor_name],
            doc="A text file of performance summary of TUMOR bam",
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
            "normal_bam",
            source=self.normal.out,
            output_folder="bams",
            output_name=self.normal_name,
        )
        self.output(
            "tumor_bam",
            source=self.tumor.out,
            output_folder="bams",
            output_name=self.tumor_name,
        )
        # VCF
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
            output_folder="variants",
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

    @staticmethod
    def process_subpipeline(**connections):
        w = WorkflowBuilder("somatic_subpipeline")

        # INPUTS
        w.input("reads", Array(FastqGzPair))
        w.input("sample_name", String)
        w.input("reference", FastaWithDict)
        w.input("cutadapt_adapters", File(optional=True))
        w.input("gatk_intervals", Array(Bed))
        w.input("genome_file", TextFile)
        w.input("snps_dbsnp", VcfTabix)
        w.input("snps_1000gp", VcfTabix)
        w.input("known_indels", VcfTabix)
        w.input("mills_indels", VcfTabix)

        # STEPS
        w.step("fastqc", FastQC_0_11_5(reads=w.reads), scatter="reads")

        w.step(
            "getfastqc_adapters",
            ParseFastqcAdaptors(
                fastqc_datafiles=w.fastqc.datafile,
                cutadapt_adaptors_lookup=w.cutadapt_adapters,
            ),
            scatter="fastqc_datafiles",
        )

        w.step(
            "align_and_sort",
            BwaAligner(
                fastq=w.reads,
                reference=w.reference,
                sample_name=w.sample_name,
                sortsam_tmpDir=".",
                cutadapt_adapter=w.getfastqc_adapters,
                cutadapt_removeMiddle3Adapter=w.getfastqc_adapters,
            ),
            scatter=["fastq", "cutadapt_adapter", "cutadapt_removeMiddle3Adapter"],
        )

        w.step(
            "merge_and_mark",
            MergeAndMarkBams_4_1_3(bams=w.align_and_sort.out, sampleName=w.sample_name),
        )

        w.step(
            "coverage",
            Gatk4DepthOfCoverage_4_1_6(
                bam=w.merge_and_mark.out,
                reference=w.reference,
                intervals=w.gatk_intervals,
                omitDepthOutputAtEachBase=True,
                # countType="COUNT_FRAGMENTS_REQUIRE_SAME_BASE",
                summaryCoverageThreshold=[1, 50, 100, 300, 500],
                outputPrefix=w.sample_name,
            ),
        )

        w.step(
            "performance_summary",
            PerformanceSummaryGenome_0_1_0(
                bam=w.merge_and_mark.out,
                sample_name=w.sample_name,
                genome_file=w.genome_file,
            ),
        )

        w.step(
            "bqsr",
            GATKBaseRecalBQSRWorkflow_4_1_3(
                bam=w.merge_and_mark,
                reference=w.reference,
                snps_dbsnp=w.snps_dbsnp,
                snps_1000gp=w.snps_1000gp,
                known_indels=w.known_indels,
                mills_indels=w.mills_indels,
            ),
        )

        # OUTPUTS
        w.output("out", source=w.merge_and_mark.out)
        w.output("bqsr_bam", source=w.bqsr.out)
        w.output(
            "reports", source=w.fastqc.out, output_folder=[w.sample_name, "reports"]
        )
        w.output("depth_of_coverage", source=w.coverage.out_sampleSummary)
        w.output(
            "summary", source=w.performance_summary.performanceSummaryOut,
        )

        return w(**connections)

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

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
        meta.dateUpdated = date(2020, 6, 22)
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
        meta.sample_input_overrides = {
            "normal_inputs": [
                ["normal_R1.fastq.gz", "normal_R2.fastq.gz"],
                ["normal_R1-TOPUP.fastq.gz", "normal_R2-TOPUP.fastq.gz"],
            ],
            "tumor_inputs": [
                ["tumor_R1.fastq.gz", "tumor_R2.fastq.gz"],
                ["tumor_R1-TOPUP.fastq.gz", "tumor_R2-TOPUP.fastq.gz"],
            ],
            "reference": "Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_indels": "Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        }


if __name__ == "__main__":
    import os.path

    w = WGSSomaticMultiCallers()
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
