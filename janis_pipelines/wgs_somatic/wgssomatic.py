from typing import Optional, List

from janis_core import File, String, Array, InputDocumentation, InputQualityType
from janis_core.tool.test_classes import TTestCase

from janis_unix.data_types import TextFile, ZipFile
from janis_bioinformatics.data_types import (
    FastqGzPair,
    Bam,
    BamBai,
    Vcf,
    CompressedVcf,
    VcfTabix,
)

from janis_pipelines.wgs_somatic.wgssomatic_variantsonly import (
    WGSSomaticMultiCallersVariantsOnly,
)
from janis_pipelines.wgs_somatic_gatk.wgssomaticgatk import WGSSomaticGATK


class WGSSomaticMultiCallers(WGSSomaticMultiCallersVariantsOnly, WGSSomaticGATK):
    def id(self):
        return "WGSSomaticMultiCallers"

    def friendly_name(self):
        return "WGS Somatic (Multi callers)"

    def version(self):
        return "1.4.0"

    def constructor(self):
        # don't call super()

        self.add_inputs()
        self.add_preprocessing_steps()
        self.add_gridss(
            normal_bam_source=self.normal.out_bam, tumor_bam_source=self.tumor.out_bam
        )
        self.add_facets(
            normal_bam_source=self.normal.out_bam, tumor_bam_source=self.tumor.out_bam
        )
        self.add_gatk_variantcaller(
            normal_bam_source=self.normal.out_bam, tumor_bam_source=self.tumor.out_bam
        )
        self.add_vardict_variantcaller(
            normal_bam_source=self.normal.out_bam, tumor_bam_source=self.tumor.out_bam
        )
        self.add_strelka_variantcaller(
            normal_bam_source=self.normal.out_bam, tumor_bam_source=self.tumor.out_bam
        )
        self.add_combine_variants(
            normal_bam_source=self.normal.out_bam, tumor_bam_source=self.tumor.out_bam
        )

    def add_inputs(self):
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

        self.add_inputs_for_reference()
        self.add_inputs_for_adapter_trimming()
        self.add_inputs_for_intervals()
        self.add_inputs_for_configuration()

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
                    "tumor_name": "NA12878-NA24385-mixture",
                    "reference": f"{brca1_test_data}/Homo_sapiens_assembly38.chr17.fasta",
                    "gridss_blacklist": f"{brca1_test_data}/consensusBlacklist.hg38.chr17.bed",
                    "gnomad": f"{brca1_test_data}/af-only-gnomad.hg38.BRCA1.vcf.gz",
                    "gatk_intervals": [f"{brca1_test_data}/BRCA1.hg38.bed"],
                    "strelka_intervals": f"{brca1_test_data}/BRCA1.hg38.bed.gz",
                    "vardict_intervals": [
                        f"{brca1_test_data}/BRCA1.hg38.split-intervals.bed"
                    ],
                    "known_indels": f"{brca1_test_data}/Homo_sapiens_assembly38.known_indels.BRCA1.vcf.gz",
                    "mills_indels": f"{brca1_test_data}/Mills_and_1000G_gold_standard.indels.hg38.BRCA1.vcf.gz",
                    "snps_1000gp": f"{brca1_test_data}/1000G_phase1.snps.high_confidence.hg38.BRCA1.vcf.gz",
                    "snps_dbsnp": f"{brca1_test_data}/Homo_sapiens_assembly38.dbsnp138.BRCA1.vcf.gz",
                    "contamination_file": f"{brca1_test_data}/contaminant_list.txt",
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
                + Bam.basic_test("out_gridss_assembly", 60000)
                + Vcf.basic_test("out_variants_gridss", 90000)
                + File.basic_test(
                    "out_facets_summary", 500, "60ba08614ca28b9630e46331d1d22de3"
                )
                + File.basic_test("out_facets_purity_png", 40000)
                + File.basic_test("out_facets_purity_seg", 100)
                + File.basic_test("out_facets_purity_rds", 7000)
                + File.basic_test("out_facets_hisens_png", 40000)
                + File.basic_test("out_facets_hisens_seg", 100)
                + File.basic_test("out_facets_hisens_rds", 7000)
                + CompressedVcf.basic_test("out_variants_gatk", 9000, 149)
                + Array.array_wrapper(
                    [Vcf.basic_test("out_variants_gakt_split", 34000, 147)]
                )
                + CompressedVcf.basic_test("out_variants_vardict", 13000, 189)
                + Array.array_wrapper(
                    [Vcf.basic_test("out_variants_vardict_split", 58000, 187)]
                )
                + CompressedVcf.basic_test("out_variants_strelka", 7000, 159)
                + VcfTabix.basic_test("out_variants_manta_somatic", 1400, 70, 35)
                + Vcf.basic_test("out_variants", 91000, 245),
            )
        ]


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
