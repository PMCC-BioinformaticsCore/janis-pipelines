from datetime import date
from typing import Optional, List

from janis_bioinformatics.data_types import (
    FastaWithDict,
    VcfTabix,
    Bed,
    FastqGzPair,
    File,
    BamBai,
    CompressedVcf,
    Vcf,
)
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_8
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import (
    BwaAligner,
    MergeAndMarkBams_4_1_3,
    GATKBaseRecalBQSRWorkflow_4_1_3,
)
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_1_3
from janis_bioinformatics.tools.htslib import BGZipLatest
from janis_bioinformatics.tools.papenfuss import Gridss_2_6_2
from janis_bioinformatics.tools.pmac import (
    ParseFastqcAdaptors,
    PerformanceSummaryGenome_0_1_0,
    AddBamStatsSomatic_0_1_0,
    GenerateGenomeFileForBedtoolsCoverage,
    GenerateIntervalsByChromosome,
)
from janis_bioinformatics.tools.variantcallers import GatkSomaticVariantCaller_4_1_3
from janis_core import (
    String,
    WorkflowBuilder,
    Array,
    WorkflowMetadata,
    InputDocumentation,
    InputQualityType,
)
from janis_core.operators.standard import FirstOperator
from janis_core.tool.test_classes import TTestCase
from janis_unix.tools import UncompressArchive
from janis_unix.data_types import TextFile

from janis_pipelines.wgs_somatic_gatk.wgssomaticgatk_variantsonly import (
    WGSSomaticGATKVariantsOnly,
    INPUT_DOCS,
)


class WGSSomaticGATK(WGSSomaticGATKVariantsOnly):
    def id(self):
        return "WGSSomaticGATK"

    def friendly_name(self):
        return "WGS Somatic (GATK only)"

    def constructor(self):
        self.add_inputs()
        self.add_preprocessing_steps()

        self.add_gatk_variantcaller(
            normal_bam_source=self.normal.out_bam, tumor_bam_source=self.tumor.out_bam
        )

    def add_inputs(self):
        # INPUTS
        self.input("normal_inputs", Array(FastqGzPair), doc=INPUT_DOCS["normal_inputs"])
        self.input("tumor_inputs", Array(FastqGzPair), doc=INPUT_DOCS["tumor_inputs"])
        self.input("normal_name", String(), doc=INPUT_DOCS["normal_name"])
        self.input("tumor_name", String(), doc=INPUT_DOCS["tumor_name"])

        self.add_inputs_for_reference()
        self.add_inputs_for_intervals()
        self.add_inputs_for_configuration()

    def add_inputs_for_configuration(self):
        super().add_inputs_for_configuration()
        self.input("cutadapt_adapters", File, doc=INPUT_DOCS["cutadapt_adapters"])

    def add_preprocessing_steps(self):
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

        sub_inputs = {
            "reference": self.reference,
            "cutadapt_adapters": self.cutadapt_adapters,
            "gatk_intervals": intervals,
            "snps_dbsnp": self.snps_dbsnp,
            "snps_1000gp": self.snps_1000gp,
            "known_indels": self.known_indels,
            "mills_indels": self.mills_indels,
        }

        # STEPS
        self.step(
            "tumor",
            self.process_subpipeline(
                reads=self.tumor_inputs, sample_name=self.tumor_name, **sub_inputs
            ),
        )
        self.step(
            "normal",
            self.process_subpipeline(
                reads=self.normal_inputs, sample_name=self.normal_name, **sub_inputs
            ),
        )

        # FASTQC
        self.output(
            "out_normal_fastqc_reports",
            source=self.normal.out_fastqc_reports,
            output_folder="reports",
        )
        self.output(
            "out_tumor_fastqc_reports",
            source=self.tumor.out_fastqc_reports,
            output_folder="reports",
        )

        # COVERAGE
        # self.output(
        #     "out_normal_coverage",
        #     source=self.normal.depth_of_coverage,
        #     output_folder=["summary", self.normal_name],
        #     doc="A text file of depth of coverage summary of NORMAL bam",
        # )
        # self.output(
        #     "out_tumor_coverage",
        #     source=self.tumor.depth_of_coverage,
        #     output_folder=["summary", self.tumor_name],
        #     doc="A text file of depth of coverage summary of TUMOR bam",
        # )
        # BAM PERFORMANCE
        self.output(
            "out_normal_performance_summary",
            source=self.normal.out_performance_summary,
            output_folder=["summary", self.normal_name],
            doc="A text file of performance summary of NORMAL bam",
        )
        self.output(
            "out_tumor_performance_summary",
            source=self.tumor.out_performance_summary,
            output_folder=["summary", self.tumor_name],
            doc="A text file of performance summary of TUMOR bam",
        )

        self.output(
            "out_normal_bam",
            source=self.normal.out_bam,
            output_folder="bams",
            output_name=self.normal_name,
        )

        self.output(
            "out_tumor_bam",
            source=self.tumor.out_bam,
            output_folder="bams",
            output_name=self.tumor_name,
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
        w.input("snps_dbsnp", VcfTabix)
        w.input("snps_1000gp", VcfTabix)
        w.input("known_indels", VcfTabix)
        w.input("mills_indels", VcfTabix)

        # STEPS
        w.step("fastqc", FastQC_0_11_8(reads=w.reads), scatter="reads")

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
                sortsam_tmpDir=None,
                cutadapt_adapter=w.getfastqc_adapters,
                cutadapt_removeMiddle3Adapter=w.getfastqc_adapters,
            ),
            scatter=["fastq", "cutadapt_adapter", "cutadapt_removeMiddle3Adapter"],
        )

        w.step(
            "merge_and_mark",
            MergeAndMarkBams_4_1_3(bams=w.align_and_sort.out, sampleName=w.sample_name),
        )

        # Temporarily remove GATK4 DepthOfCoverage for performance reasons, see:
        #   https://gatk.broadinstitute.org/hc/en-us/community/posts/360071895391-Speeding-up-GATK4-DepthOfCoverage

        # w.step(
        #     "coverage",
        #     Gatk4DepthOfCoverage_4_1_6(
        #         bam=w.merge_and_mark.out,
        #         reference=w.reference,
        #         intervals=w.gatk_intervals,
        #         omitDepthOutputAtEachBase=True,
        #         # countType="COUNT_FRAGMENTS_REQUIRE_SAME_BASE",
        #         summaryCoverageThreshold=[1, 50, 100, 300, 500],
        #         outputPrefix=w.sample_name,
        #     ),
        # )

        w.step(
            "calculate_performancesummary_genomefile",
            GenerateGenomeFileForBedtoolsCoverage(reference=w.reference),
        )

        w.step(
            "performance_summary",
            PerformanceSummaryGenome_0_1_0(
                bam=w.merge_and_mark.out,
                sample_name=w.sample_name,
                genome_file=w.calculate_performancesummary_genomefile.out,
            ),
        )

        # OUTPUTS
        w.output("out_bam", source=w.merge_and_mark.out)
        w.output("out_fastqc_reports", source=w.fastqc.out)
        # w.output("depth_of_coverage", source=w.coverage.out_sampleSummary)
        w.output(
            "out_performance_summary",
            source=w.performance_summary.performanceSummaryOut,
        )

        return w(**connections)

    def tests(self) -> Optional[List[TTestCase]]:
        parent_dir = "https://swift.rc.nectar.org.au/v1/AUTH_4df6e734a509497692be237549bbe9af/janis-test-data/bioinformatics"
        germline_data = f"{parent_dir}/wgsgermline_data"
        somatic_data = f"{parent_dir}/wgssomatic_data"

        return [
            TTestCase(
                name="basic",
                input={
                    "normal_inputs": [
                        [
                            f"{somatic_data}/NA24385-BRCA1_R1.fastq.gz",
                            f"{somatic_data}/NA24385-BRCA1_R21.fastq.gz",
                        ]
                    ],
                    "normal_name": "NA24385-BRCA1",
                    "tumor_inputs": [
                        [
                            f"{somatic_data}/NA12878-NA24385-mixture-BRCA1_R1.fastq.gz",
                            f"{somatic_data}/NA12878-NA24385-mixture-BRCA1_R2.fastq.gz",
                        ]
                    ],
                    "tumor_name": "NA12878-NA24385-mixture",
                    "reference": f"{germline_data}/Homo_sapiens_assembly38.chr17.fasta",
                    "gridss_blacklist": f"{somatic_data}/consensusBlacklist.hg38.chr17.bed",
                    "gnomad": f"{somatic_data}/af-only-gnomad.hg38.BRCA1.vcf.gz",
                    "gatk_intervals": [f"{germline_data}/BRCA1.hg38.bed"],
                    "known_indels": f"{germline_data}/Homo_sapiens_assembly38.known_indels.BRCA1.vcf.gz",
                    "mills_indels": f"{germline_data}/Mills_and_1000G_gold_standard.indels.hg38.BRCA1.vcf.gz",
                    "snps_1000gp": f"{germline_data}/1000G_phase1.snps.high_confidence.hg38.BRCA1.vcf.gz",
                    "snps_dbsnp": f"{germline_data}/Homo_sapiens_assembly38.dbsnp138.BRCA1.vcf.gz",
                    "cutadapt_adapters": f"{germline_data}/contaminant_list.txt",
                },
                output=BamBai.basic_test("out_normal_bam", 3265300, 49500)
                + BamBai.basic_test("out_tumor_bam", 3341700, 49000)
                + TextFile.basic_test(
                    "out_normal_performance_summary",
                    950,
                    md5="e3205735e5fe8c900f05050f8ed73f19",
                )
                + TextFile.basic_test(
                    "out_tumor_performance_summary",
                    950,
                    md5="122bfa2ece90c0f030015feba4ba7d84",
                )
                + FastqGzPair.basic_test("out_normal_fastqc_reports", 881300)
                + FastqGzPair.basic_test("out_tumor_fastqc_reports", 874900),
            )
        ]


if __name__ == "__main__":
    import os.path

    w = WGSSomaticGATK()
    args = {
        "to_console": False,
        "to_disk": True,
        "validate": True,
        "export_path": os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "{language}"
        ),
    }
    # w.translate("cwl", **args)
    w.translate("wdl", **args)

    # from cwltool import main
    # import logging

    # op = os.path.dirname(os.path.realpath(__file__)) + "/cwl/WGSGermlineGATK.py"

    # main.run(*["--validate", op], logger_handler=logging.Handler())
