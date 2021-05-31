import operator
from typing import Optional, List

from janis_core import Array, String, WorkflowMetadata

from janis_core.tool.test_classes import (
    TTestCase,
    TTestExpectedOutput,
    TTestPreprocessor,
)

from janis_bioinformatics.data_types import FastqGzPair

from janis_pipelines.wgs_germline.wgsgermline_variantsonly import (
    WGSGermlineMultiCallersVariantsOnly,
    INPUT_DOCS,
)
from janis_pipelines.wgs_germline_gatk.wgsgermlinegatk import WGSGermlineGATK

expected_performance_summary = """\
Total reads,Mapped reads,% Reads mapped,% Mapped reads duplicates,Total reads minus duplicates,Mapped reads minus duplicates,Paired in sequencing,Read1,Read2,Properly paired,With itself and mate mapped,Singletons,With mate mapped to a different chr,With mate mapped to a different chr (mapQ>=5),% Reads OnTarget,% OnTarget duplicates,OnTarget paired in sequencing,OnTarget read1,OnTarget read2,OnTarget properly paired,OnTarget With itself and mate mapped,OnTarget singletons,OnTarget with mate mapped to a different chr,OnTarget with mate mapped to a different chr (mapQ>=5),% Target bases >=1-fold Coverage,% Target bases >=10-fold Coverage,% Target bases >=20-fold Coverage,% Target bases >=100-fold Coverage,Mean coverage for target bases,% Target bases with one fifth of mean coverage,Median Fragment Length
19615,19582,99.83,0.12,19592,19559,19299,9645,9654,18386,19242,24,778,636,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,0.00,0.00,0.00,0.00,0.00,0.00,556
"""

expected_gridss_flagstat = """\
7 + 0 in total (QC-passed reads + QC-failed reads)
0 + 0 secondary
0 + 0 supplementary
0 + 0 duplicates
7 + 0 mapped (100.00% : N/A)
0 + 0 paired in sequencing
0 + 0 read1
0 + 0 read2
0 + 0 properly paired (N/A : N/A)
0 + 0 with itself and mate mapped
0 + 0 singletons (N/A : N/A)
0 + 0 with mate mapped to a different chr
0 + 0 with mate mapped to a different chr (mapQ>=5)
"""


class WGSGermlineMultiCallers(WGSGermlineGATK, WGSGermlineMultiCallersVariantsOnly):
    def id(self):
        return "WGSGermlineMultiCallers"

    def friendly_name(self):
        return "WGS Germline (Multi callers)"

    def version(self):
        return "1.4.0"

    def constructor(self):
        self.add_inputs()

        self.add_fastqc()

        self.add_align()

        self.add_bam_process()
        self.add_bam_qc(bam_source=self.merge_and_mark.out)

        # Add variant callers

        self.add_gridss(bam_source=self.merge_and_mark.out)

        self.add_gatk_variantcaller(bam_source=self.merge_and_mark.out)
        self.add_strelka_variantcaller(bam_source=self.merge_and_mark.out)
        self.add_vardict_variantcaller(bam_source=self.merge_and_mark.out)

        # Combine gatk / strelka / vardict variants
        self.add_combine_variants(bam_source=self.merge_and_mark.out)

    def add_inputs(self):
        # INPUTS
        self.input("sample_name", String, doc=INPUT_DOCS["sample_name"])
        self.input("fastqs", Array(FastqGzPair), doc=INPUT_DOCS["fastqs"])

        self.add_inputs_for_reference()
        self.add_inputs_for_intervals()
        self.add_inputs_for_configuration()

    def bind_metadata(self):
        meta: WorkflowMetadata = super().bind_metadata() or self.metadata

        meta.short_documentation = (
            "A variant-calling WGS pipeline using GATK, VarDict and Strelka2."
        )
        meta.documentation = """\
This is a genomics pipeline to align sequencing data (Fastq pairs) into BAMs and call variants using:

This workflow is a reference pipeline using the Janis Python framework (pipelines assistant).

- Takes raw sequence data in the FASTQ format;
- Align to the reference genome using BWA MEM;
- Marks duplicates using Picard;
- Call the appropriate variant callers (GRIDSS / GATK / Strelka / VarDict);
- Merges the variants from GATK / Strelka / VarDict.
- Outputs the final variants in the VCF format.

**Resources**

This pipeline has been tested using the HG38 reference set, available on Google Cloud Storage through:

- https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/

This pipeline expects the assembly references to be as they appear in that storage \
    (".fai", ".amb", ".ann", ".bwt", ".pac", ".sa", "^.dict").
The known sites (snps_dbsnp, snps_1000gp, known_indels, mills_indels) should be gzipped and tabix indexed.
"""

    def tests(self) -> Optional[List[TTestCase]]:
        bioinf_base = "https://swift.rc.nectar.org.au/v1/AUTH_4df6e734a509497692be237549bbe9af/janis-test-data/bioinformatics"
        chr17 = f"{bioinf_base}/petermac_testdata"
        hg38 = f"{bioinf_base}/hg38"

        return [
            TTestCase(
                name="brca1",
                input={
                    "sample_name": "NA12878",
                    "reference": f"{chr17}/Homo_sapiens_assembly38.chr17.fasta",
                    "fastqs": [
                        [
                            f"{chr17}/NA12878-BRCA1_R1.fastq.gz",
                            f"{chr17}/NA12878-BRCA1_R2.fastq.gz",
                        ]
                    ],
                    "gatk_intervals": [f"{chr17}/BRCA1.hg38.bed"],
                    "vardict_intervals": [f"{hg38}/NA12878/BRCA1.intersect.bed"],
                    "strelka_intervals": f"{chr17}/BRCA1.hg38.bed.gz",
                    "known_indels": f"{chr17}/Homo_sapiens_assembly38.known_indels.BRCA1.vcf.gz",
                    "mills_indels": f"{chr17}/Mills_and_1000G_gold_standard.indels.hg38.BRCA1.vcf.gz",
                    "snps_1000gp": f"{chr17}/1000G_phase1.snps.high_confidence.hg38.BRCA1.vcf.gz",
                    "snps_dbsnp": f"{chr17}/Homo_sapiens_assembly38.dbsnp138.BRCA1.vcf.gz",
                    "cutadapt_adapters": f"{chr17}/contaminant_list.txt",
                    "gridss_blacklist": f"{chr17}/consensusBlacklist.hg38.chr17.bed",
                    "MINIMUM_PCT": f""
                },
                output=[
                    TTestExpectedOutput(
                        tag="out_variants",
                        preprocessor=TTestPreprocessor.LinesDiff,
                        file_diff_source=f"{chr17}/NA12878/brca1.germline.combined.vcf",
                        operator=lambda actual, expected: all(
                            a <= b for a, b in zip(actual, expected)
                        ),
                        expected_value=(1, 1),
                    ),
                    TTestExpectedOutput(
                        "out_variants_gridss",
                        preprocessor=TTestPreprocessor.FileContent,
                        operator=operator.eq,
                        expected_file=f"{chr17}/NA12878/brca1.germline.gridss.vcf",
                    ),
                    TTestExpectedOutput(
                        tag="out_bam",
                        preprocessor=TTestPreprocessor.Value,
                        operator=Bam.equal,
                        expected_value=f"{chr17}/NA12878/NA12878.bam",
                    ),
                    TTestExpectedOutput(
                        tag="out_gridss_assembly",
                        preprocessor=Bam.flagstat,
                        operator=operator.eq,
                        expected_value=expected_gridss_flagstat,
                    ),
                    TTestExpectedOutput(
                        tag="out_performance_summary",
                        preprocessor=TTestPreprocessor.FileContent,
                        operator=operator.eq,
                        expected_value=expected_performance_summary,
                    ),
                ],
            )
        ]


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
        "with_resource_overrides": False,
    }
    w.translate("cwl", **args)
    w.translate("wdl", **args)
