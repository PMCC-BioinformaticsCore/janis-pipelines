from datetime import date

from janis_core import String, WorkflowMetadata

from janis_bioinformatics.data_types import BamBai

from janis_pipelines.wgs_germline.wgsgermline import INPUT_DOCS
from janis_pipelines.wgs_germline.wgsgermline_variantsonly import (
    WGSGermlineMultiCallersVariantsOnly,
)
from janis_pipelines.wgs_germline_gatk.wgsgermlinegatk import WGSGermlineGATK


class WGSGermlineGATKVariantsOnly(WGSGermlineGATK, WGSGermlineMultiCallersVariantsOnly):
    def id(self):
        return "WGSGermlineGATKVariantsOnly"

    def friendly_name(self):
        return "WGS Germline (GATK) [VARIANTS only]"

    def version(self):
        return "1.4.0"

    ### PIPELINE CONSTRUCTOR
    def constructor(self):
        self.add_inputs()

        self.add_bam_qc(bam_source=self.bam)
        self.add_gatk_variantcaller(bam_source=self.bam)
        self.add_addbamstats(bam_source=self.bam)

    ### INPUTS
    def add_inputs(self):
        self.input("sample_name", String, doc=INPUT_DOCS["sample_name"])
        self.input("bam", BamBai, doc=INPUT_DOCS["bam"])

        self.add_inputs_for_reference()
        self.add_inputs_for_adapter_trimming()
        self.add_inputs_for_intervals()
        self.add_inputs_for_configuration()

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = ["wgs", "cancer", "germline", "variants", "gatk"]
        meta.contributors = ["Michael Franklin", "Richard Lupat", "Jiaan Yu"]
        meta.dateCreated = date(2018, 12, 24)
        meta.dateUpdated = date(2022, 2, 25)
        meta.short_documentation = "A variant-calling WGS pipeline using only the GATK Haplotype variant caller."
        meta.documentation = """\
This is a genomics pipeline to ONLY call variants using GATK from an indexed bam. The final variants are outputted in the VCF format.

This workflow is a reference pipeline using the Janis Python framework (pipelines assistant).

- Call variants using GATK4;
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
    # w=WGSGermlineGATKVariantsOnly()
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
    WGSGermlineGATKVariantsOnly().translate("wdl")
