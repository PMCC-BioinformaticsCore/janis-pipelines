import operator
import os
from datetime import date
from typing import Optional, List

from janis_bioinformatics.data_types import FastqGzPair, Bam, Vcf, CompressedVcf, BamBai
from janis_bioinformatics.tools import BioinformaticsTool
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_8
from janis_bioinformatics.tools.common import BwaAligner, MergeAndMarkBams_4_1_3
from janis_bioinformatics.tools.pmac import ParseFastqcAdaptors
from janis_core import String, Array, File, WorkflowMetadata
from janis_core.tool.test_classes import (
    TTestCase,
    TTestExpectedOutput,
    TTestPreprocessor,
)
from janis_unix.data_types import TextFile, ZipFile

from janis_pipelines.wgs_germline_gatk.wgsgermlinegatk_variantsonly import (
    WGSGermlineGATKVariantsOnly,
    INPUT_DOCS,
)


class WGSGermlineGATK(WGSGermlineGATKVariantsOnly):
    def id(self):
        return "WGSGermlineGATK"

    def friendly_name(self):
        return "Janis Germline Variant-Calling Workflow (GATK)"

    def constructor(self):
        self.add_inputs()

        self.add_fastqc()
        self.add_align()

        self.add_bam_process()

        # mfranklin (2020-08-20): This is pretty cool, it allows us to reuse
        # these step definitions in different pipelines (without creating a whole subworkflow)

        self.add_bam_qc(bam_source=self.merge_and_mark.out)

        # Add variant callers
        self.add_gatk_variantcaller(bam_source=self.merge_and_mark.out)
        self.add_addbamstats(bam_source=self.merge_and_mark.out)

    def add_inputs(self):
        # INPUTS
        self.input("sample_name", String, doc=INPUT_DOCS["sample_name"])
        self.input("fastqs", Array(FastqGzPair), doc=INPUT_DOCS["fastqs"])

        self.add_inputs_for_reference()
        self.add_inputs_for_intervals()
        self.add_inputs_for_configuration()

    def add_inputs_for_configuration(self):
        super().add_inputs_for_configuration()

        self.input("cutadapt_adapters", File, doc=INPUT_DOCS["cutadapt_adapters"])

    def add_fastqc(self):
        self.step("fastqc", FastQC_0_11_8(reads=self.fastqs), scatter="reads")

        self.output(
            "out_fastqc_reports",
            source=self.fastqc.out,
            output_folder="reports",
            doc="A zip file of the FastQC quality report.",
        )

    def add_align(self):
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

    def add_bam_process(self):
        self.step(
            "merge_and_mark",
            MergeAndMarkBams_4_1_3(
                bams=self.align_and_sort.out, sampleName=self.sample_name
            ),
        )

        self.output(
            "out_bam",
            source=self.merge_and_mark.out,
            output_folder="bams",
            doc="Aligned and indexed bam.",
            output_name=self.sample_name,
        )

    def tests(self) -> Optional[List[TTestCase]]:
        parent_dir = "https://swift.rc.nectar.org.au/v1/AUTH_4df6e734a509497692be237549bbe9af/janis-test-data/bioinformatics"
        germline_data = f"{parent_dir}/wgsgermline_data"

        return [
            TTestCase(
                name="brca1",
                input={
                    "sample_name": "NA12878",
                    "reference": f"{germline_data}/Homo_sapiens_assembly38.chr17.fasta",
                    "fastqs": [
                        [
                            f"{germline_data}/NA12878-BRCA1_R1.fastq.gz",
                            f"{germline_data}/NA12878-BRCA1_R2.fastq.gz",
                        ]
                    ],
                    "gatk_intervals": [f"{germline_data}/BRCA1.hg38.bed"],
                    "known_indels": f"{germline_data}/Homo_sapiens_assembly38.known_indels.BRCA1.vcf.gz",
                    "mills_indels": f"{germline_data}/Mills_and_1000G_gold_standard.indels.hg38.BRCA1.vcf.gz",
                    "snps_1000gp": f"{germline_data}/1000G_phase1.snps.high_confidence.hg38.BRCA1.vcf.gz",
                    "snps_dbsnp": f"{germline_data}/Homo_sapiens_assembly38.dbsnp138.BRCA1.vcf.gz",
                    "cutadapt_adapters": f"{germline_data}/contaminant_list.txt",
                },
                output=Vcf.basic_test("out_variants_bamstats", 51300, 230)
                + Vcf.basic_test("out_variants_gatk_split", 50700, 221)
                + BamBai.basic_test("out_bam", 2822000, 49600)
                + TextFile.basic_test(
                    "out_performance_summary",
                    948,
                    md5="575354942cfb8d0367725f9020181443",
                )
                + Array.array_wrapper(
                    [
                        ZipFile.basic_test("out_fastqc_reports", 408000),
                        ZipFile.basic_test("out_fastqc_reports", 408000),
                    ]
                ),
            )
        ]

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = ["wgs", "cancer", "germline", "variants", "gatk"]
        meta.contributors = ["Richard Lupat", "Michael Franklin", "Jiaan Yu"]
        meta.dateCreated = date(2018, 12, 24)
        meta.dateUpdated = date(2021, 11, 10)
        meta.short_documentation = "A variant-calling pipeline using the GATK HaplotypeCaller"
        meta.documentation = """\
This is a genomics pipeline to do a single germline sample variant-calling, adapted from GATK Best Practice Workflow.

This workflow is a reference pipeline for using the Janis Python framework (pipelines assistant).
- Alignment: bwa-mem
- Variant-Calling: GATK HaplotypeCaller
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
    # from toolbuilder.runtest.runner import run_test_case, EngineType

    tool = WGSGermlineGATK()
    tool.translate("wdl", to_console=False)
    # results = run_test_case(
    #     tool,
    #     test_case=tool.tests()[0].name,
    #     engine=EngineType.cromwell,
    #     # circumvent running tests by declaring outputs = {<outputs}>
    #     # output=outputs,
    # )
    # print(results)
