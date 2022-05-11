from datetime import date

from janis_core import (
    String,
    WorkflowMetadata,
)

from janis_bioinformatics.data_types import BamBai
from janis_pipelines.wgs_somatic_gatk.wgssomaticgatk import WGSSomaticGATK
from janis_pipelines.wgs_somatic.wgssomatic import INPUT_DOCS
from janis_pipelines.wgs_somatic.wgssomatic_variantsonly import (
    WGSSomaticMultiCallersVariantsOnly,
)


class WGSSomaticGATKVariantsOnly(WGSSomaticGATK, WGSSomaticMultiCallersVariantsOnly):
    def id(self):
        return "WGSSomaticGATKVariantsOnly"

    def friendly_name(self):
        return "WGS Somatic (GATK only) [VARIANTS only]"

    def version(self):
        return "1.4.0"

    def constructor(self):
        self.add_inputs()
        self.add_bam_qc(
            normal_bam_source=self.normal_bam, tumor_bam_source=self.tumor_bam
        )
        self.add_gatk_variantcaller(
            normal_bam_source=self.normal_bam, tumor_bam_source=self.tumor_bam
        )
        self.add_addbamstats(
            normal_bam_source=self.normal_bam, tumor_bam_source=self.tumor_bam
        )

    def add_inputs(self):
        # INPUTS
        self.input("normal_bam", BamBai, doc=INPUT_DOCS["normal_bam"])
        self.input("tumor_bam", BamBai, doc=INPUT_DOCS["tumor_bam"])
        self.input("normal_name", String, doc=INPUT_DOCS["normal_name"])
        self.input("tumor_name", String, doc=INPUT_DOCS["tumor_name"])

        self.add_inputs_for_reference()
        self.add_inputs_for_adapter_trimming()
        self.add_inputs_for_intervals()
        self.add_inputs_for_configuration()

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = ["wgs", "cancer", "somatic", "variants", "gatk"]
        meta.dateUpdated = date(2019, 10, 16)
        meta.dateUpdated = date(2022, 3, 1)

        meta.contributors = ["Michael Franklin", "Richard Lupat", "Jiaan Yu"]
        meta.short_documentation = "A somatic tumor-normal variant-calling WGS pipeline using only GATK Mutect2"
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


if __name__ == "__main__":
    # import os.path

    # w = WGSSomaticGATKVariantsOnly()
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
    WGSSomaticGATKVariantsOnly().translate("wdl")
