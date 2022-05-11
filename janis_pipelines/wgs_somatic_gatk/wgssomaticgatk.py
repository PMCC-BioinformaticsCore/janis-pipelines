from datetime import date
from typing import Optional, List

from janis_core import (
    Array,
    String,
    StringFormatter,
)
from janis_core.tool.test_classes import TTestCase

from janis_unix.data_types import TextFile, ZipFile
from janis_bioinformatics.data_types import (
    FastqGzPair,
    BamBai,
    Bed,
    CompressedVcf,
    Vcf,
)
from janis_bioinformatics.tools.pmac import AddBamStatsSomatic_0_1_0
from janis_pipelines.wgs_somatic.wgssomatic import WGSSomaticMultiCallers, INPUT_DOCS


class WGSSomaticGATK(WGSSomaticMultiCallers):
    def id(self):
        return "WGSSomaticGATK"

    def friendly_name(self):
        return "WGS Somatic (GATK only)"

    def constructor(self):
        self.add_inputs()
        self.add_alignment_normal()
        self.add_alignment_tumor()
        self.add_bam_qc(
            normal_bam_source=self.alignment_normal.out_bam,
            tumor_bam_source=self.alignment_tumor.out_bam,
        )
        self.add_gatk_variantcaller(
            normal_bam_source=self.alignment_normal.out_bam,
            tumor_bam_source=self.alignment_tumor.out_bam,
        )
        self.add_addbamstats(
            normal_bam_source=self.alignment_normal.out_bam,
            tumor_bam_source=self.alignment_tumor.out_bam,
        )

    def add_inputs(self):
        # INPUTS
        self.input("normal_inputs", Array(FastqGzPair), doc=INPUT_DOCS["normal_inputs"])
        self.input("tumor_inputs", Array(FastqGzPair), doc=INPUT_DOCS["tumor_inputs"])
        self.input("normal_name", String(), doc=INPUT_DOCS["normal_name"])
        self.input("tumor_name", String(), doc=INPUT_DOCS["tumor_name"])

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

    def add_addbamstats(self, normal_bam_source, tumor_bam_source):
        self.step(
            "addbamstats",
            AddBamStatsSomatic_0_1_0(
                normal_id=self.normal_name,
                tumor_id=self.tumor_name,
                normal_bam=normal_bam_source,
                tumor_bam=tumor_bam_source,
                reference=self.reference,
                vcf=self.vc_gatk_uncompressvcf.out.as_type(Vcf),
            ),
        )
        self.output(
            "out_variants_bamstats",
            source=self.addbamstats.out,
            output_folder=["variants"],
            output_name=StringFormatter(
                "{tumor_name}--{normal_name}",
                tumor_name=self.tumor_name,
                normal_name=self.normal_name,
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
                    "normal_inputs": [
                        [
                            f"{brca1_test_data}/NA24385-BRCA1_R1.fastq.gz",
                            f"{brca1_test_data}/NA24385-BRCA1_R2.fastq.gz",
                        ]
                    ],
                    "normal_name": "NA24385-BRCA1",
                    "tumor_inputs": [
                        [
                            f"{brca1_test_data}/NA12878-NA24385-mixture-BRCA1_R1.fastq.gz",
                            f"{brca1_test_data}/NA12878-NA24385-mixture-BRCA1_R2.fastq.gz",
                        ]
                    ],
                    "tumor_name": "NA12878-NA24385-mixture-BRCA1",
                    "reference": f"{brca1_test_data}/Homo_sapiens_assembly38.chr17.fasta",
                    "gnomad": f"{brca1_test_data}/af-only-gnomad.hg38.BRCA1.vcf.gz",
                    "gatk_intervals": [f"{brca1_test_data}/BRCA1.hg38.bed"],
                    "known_indels": f"{brca1_test_data}/Homo_sapiens_assembly38.known_indels.BRCA1.vcf.gz",
                    "mills_indels": f"{brca1_test_data}/Mills_and_1000G_gold_standard.indels.hg38.BRCA1.vcf.gz",
                    "snps_1000gp": f"{brca1_test_data}/1000G_phase1.snps.high_confidence.hg38.BRCA1.vcf.gz",
                    "snps_dbsnp": f"{brca1_test_data}/Homo_sapiens_assembly38.dbsnp138.BRCA1.vcf.gz",
                    "contaminant_file": f"{brca1_test_data}/contaminant_list.txt",
                    "adapter_file": f"{brca1_test_data}/adapter_list.txt",
                },
                output=Array.array_wrapper(
                    [ZipFile.basic_test("out_normal_R1_fastqc_reports", 430000)]
                )
                + Array.array_wrapper(
                    [ZipFile.basic_test("out_tumor_R1_fastqc_reports", 430000)]
                )
                + Array.array_wrapper(
                    [ZipFile.basic_test("out_normal_R2_fastqc_reports", 430000)]
                )
                + Array.array_wrapper(
                    [ZipFile.basic_test("out_tumor_R2_fastqc_reports", 430000)]
                )
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
                + BamBai.basic_test("out_normal_bam", 3260000, 49000)
                + BamBai.basic_test("out_tumor_bam", 3340000, 49000)
                + CompressedVcf.basic_test("out_variants_gatk", 9000, 149)
                + Array.array_wrapper(
                    [Vcf.basic_test("out_variants_gatk_split", 34000, 147)]
                )
                + Vcf.basic_test("out_variants_bamstats", 44000, 158),
            )
        ]


if __name__ == "__main__":
    # import os.path

    # w = WGSSomaticGATK()
    # args = {
    #     "to_console": False,
    #     "to_disk": True,
    #     "validate": True,
    #     "export_path": os.path.join(
    #         os.path.dirname(os.path.realpath(__file__)), "{language}"
    #     ),
    # }
    # w.translate("cwl", **args)
    # w.translate("wdl", **args)
    WGSSomaticGATK().translate("wdl")
