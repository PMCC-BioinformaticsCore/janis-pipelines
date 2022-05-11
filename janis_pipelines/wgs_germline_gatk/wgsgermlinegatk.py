from datetime import date
from typing import Optional, List

from janis_core import String, Array, WorkflowMetadata, StringFormatter
from janis_core.tool.test_classes import (
    TTestCase,
    TTestExpectedOutput,
    TTestPreprocessor,
)

from janis_unix.data_types import TextFile, ZipFile
from janis_bioinformatics.data_types import FastqGzPair, BamBai, Bed, Vcf, CompressedVcf
from janis_bioinformatics.tools.pmac import AddBamStatsGermline_0_1_0

from janis_pipelines.wgs_germline.wgsgermline import WGSGermlineMultiCallers, INPUT_DOCS


class WGSGermlineGATK(WGSGermlineMultiCallers):
    def id(self):
        return "WGSGermlineGATK"

    def friendly_name(self):
        return "Janis Germline Variant-Calling Workflow (GATK)"

    ### PIPELINE CONSTRUCTOR
    def constructor(self):
        self.add_inputs()

        self.add_fastqc()
        self.add_trim_and_align_fastq()
        self.add_merge_and_markdups_bam()
        self.add_bam_qc(bam_source=self.merge_and_markdups.out)
        self.add_gatk_variantcaller(bam_source=self.merge_and_markdups.out)
        self.add_addbamstats(bam_source=self.merge_and_markdups.out)

    ### INPUTS
    def add_inputs(self):
        self.input("sample_name", String, doc=INPUT_DOCS["sample_name"])
        self.input("fastqs", Array(FastqGzPair), doc=INPUT_DOCS["fastqs"])

        self.add_inputs_for_reference()
        self.add_inputs_for_adapter_trimming()
        self.add_inputs_for_intervals()
        self.add_inputs_for_configuration()

    def add_inputs_for_intervals(self):
        self.input(
            "gatk_intervals",
            Array(Bed, optional=True),
            doc=INPUT_DOCS["gatk_intervals"],
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
            output_folder=[
                "variants",
            ],
            output_name=StringFormatter(
                "{sample_name}",
                sample_name=self.sample_name,
            ),
            doc="Final vcf from GATK",
        )

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
                    "gatk_intervals": [f"{brca1_test_data}/BRCA1.hg38.bed"],
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
                )
                + CompressedVcf.basic_test("out_variants_gatk", 11000, 223)
                + Array.array_wrapper(
                    [Vcf.basic_test("out_variants_gatk_split", 51000, 221)]
                )
                + Vcf.basic_test("out_variants_bamstats", 6900, 232),
            )
        ]

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = ["wgs", "cancer", "germline", "variants", "gatk"]
        meta.contributors = ["Richard Lupat", "Michael Franklin", "Jiaan Yu"]
        meta.dateCreated = date(2018, 12, 24)
        meta.dateUpdated = date(2022, 2, 25)
        meta.short_documentation = (
            "A variant-calling pipeline using the GATK HaplotypeCaller"
        )
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


if __name__ == "__main__":
    # import os.path
    # w=WGSGermlineGATK()
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
    WGSGermlineGATK().translate("wdl")
