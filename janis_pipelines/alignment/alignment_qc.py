from datetime import date
from typing import Optional, List

from janis_core import Array, String
from janis_bioinformatics.data_types import FastqGzPair, BamBai
from janis_pipelines.wgs_germline.wgsgermline import WGSGermlineMultiCallers, INPUT_DOCS
from janis_core.tool.test_classes import (
    TTestCase,
    TTestExpectedOutput,
    TTestPreprocessor,
)

from janis_unix.data_types import TextFile, ZipFile


class BwaAlignmentAndQC(WGSGermlineMultiCallers):
    def id(self):
        return "BwaAlignmentAndQC"

    def friendly_name(self):
        return "Alignment (BWA MEM) and MarkDuplicates, and BAM QC"

    @staticmethod
    def tool_provider():
        return "Common"

    @staticmethod
    def version():
        return "1.0.0"

    ### PIPELINE CONSTRUCTOR
    def constructor(self):
        self.add_inputs()

        self.add_fastqc()
        self.add_trim_and_align_fastq()
        self.add_merge_and_markdups_bam()
        self.add_bam_qc(bam_source=self.merge_and_markdups.out)

    ### INPUTS
    def add_inputs(self):
        self.input("sample_name", String, doc=INPUT_DOCS["sample_name"])
        self.input("fastqs", Array(FastqGzPair), doc=INPUT_DOCS["fastqs"])

        self.add_inputs_for_reference()
        self.add_inputs_for_adapter_trimming()
        self.add_inputs_for_configuration()

    def tests(self) -> Optional[List[TTestCase]]:
        parent_dir = "https://swift.rc.nectar.org.au/v1/AUTH_4df6e734a509497692be237549bbe9af/janis-test-data/bioinformatics"
        brca1_test_data = f"{parent_dir}/brca1_test/test_data"

        return [
            TTestCase(
                name="brca1",
                input={
                    "sample_name": "NA12878-BRCA1",
                    "fastqs": [
                        [
                            f"{brca1_test_data}/NA12878-BRCA1_R1.fastq.gz",
                            f"{brca1_test_data}/NA12878-BRCA1_R2.fastq.gz",
                        ]
                    ],
                    "reference": f"{brca1_test_data}/Homo_sapiens_assembly38.chr17.fasta",
                    "known_indels": f"{brca1_test_data}/Homo_sapiens_assembly38.known_indels.BRCA1.vcf.gz",
                    "mills_indels": f"{brca1_test_data}/Mills_and_1000G_gold_standard.indels.hg38.BRCA1.vcf.gz",
                    "snps_1000gp": f"{brca1_test_data}/1000G_phase1.snps.high_confidence.hg38.BRCA1.vcf.gz",
                    "snps_dbsnp": f"{brca1_test_data}/Homo_sapiens_assembly38.dbsnp138.BRCA1.vcf.gz",
                    "contaminant_file": f"{brca1_test_data}/contaminant_list.txt",
                    "adapter_file": f"{brca1_test_data}/adapter_list.txt",
                },
                output=Array.array_wrapper(
                    [ZipFile.basic_test("out_fastqc_R1_reports", 408000)]
                )
                + Array.array_wrapper(
                    [ZipFile.basic_test("out_fastqc_R2_reports", 408000)]
                )
                + BamBai.basic_test("out_bam", 2822000, 49600)
                + TextFile.basic_test(
                    "out_performance_summary",
                    948,
                    md5="575354942cfb8d0367725f9020181443",
                ),
            )
        ]


if __name__ == "__main__":
    # import os.path
    # w=BwaAlignmentAndQC()
    # args = {
    #     "to_console": False,
    #     "to_disk": False,
    #     "validate": True,
    #     "export_path": os.path.join(
    #         os.path.dirname(os.path.realpath(__file__)), "{language}"
    #     ),
    #     "with_resource_overrides": True,
    # }
    # w.translate("cwl", **args)
    # w.translate("wdl", **args)
    BwaAlignmentAndQC().translate("wdl")
