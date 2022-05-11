from datetime import date

from janis_core import String, WorkflowMetadata
from janis_bioinformatics.data_types import BamBai
from janis_pipelines.wgs_germline.wgsgermline import WGSGermlineMultiCallers, INPUT_DOCS


class WGSGermlineMultiCallersVariantsOnly(WGSGermlineMultiCallers):
    def id(self):
        return "WGSGermlineMultiCallersVariantsOnly"

    def friendly_name(self):
        return "WGS Germline (Multi callers) [VARIANTS only]"

    def version(self):
        return "1.4.0"

    ### PIPELINE CONSTRUCTOR
    def constructor(self):
        self.add_inputs()

        self.add_bam_qc(bam_source=self.bam)
        self.add_gridss(bam_source=self.bam)
        self.add_gatk_variantcaller(bam_source=self.bam)
        self.add_strelka_variantcaller(bam_source=self.bam)
        self.add_vardict_variantcaller(bam_source=self.bam)
        self.add_combine_variants(bam_source=self.bam)

    ### INPUTS
    def add_inputs(self):
        self.input("sample_name", String, doc=INPUT_DOCS["sample_name"])
        self.input("bam", BamBai, doc=INPUT_DOCS["bam"])

        self.add_inputs_for_reference()
        self.add_inputs_for_adapter_trimming()
        self.add_inputs_for_intervals()
        self.add_inputs_for_configuration()

    ### PIPELINE STEPS
    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = [
            "wgs",
            "cancer",
            "germline",
            "variants",
            "gatk",
            "strelka",
            "vardict",
            "gridss",
        ]
        meta.contributors = ["Richard Lupat", "Michael Franklin", "Jiaan Yu"]
        meta.dateCreated = date(2018, 12, 24)
        meta.dateUpdated = date(2022, 2, 25)

        meta.short_documentation = (
            "A variant-calling WGS pipeline using GATK, VarDict and Strelka2."
        )
        meta.documentation = """\
This workflow is a reference pipeline using the Janis Python framework (pipelines assistant).

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


if __name__ == "__main__":
    # import os.path
    # w=WGSGermlineMultiCallersVariantsOnly()
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
    WGSGermlineMultiCallersVariantsOnly().translate("wdl")
