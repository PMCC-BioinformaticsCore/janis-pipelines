from janis_bioinformatics.data_types import FastqGzPair
from janis_core import (
    Array,
    String,
    WorkflowMetadata,
    InputDocumentation,
    InputQualityType,
)

from janis_pipelines.wgs_germline.wgsgermline_variantsonly import (
    WGSGermlineMultiCallersVariantsOnly,
)
from janis_pipelines.wgs_germline_gatk.wgsgermlinegatk import WGSGermlineGATK


class WGSGermlineMultiCallers(WGSGermlineGATK, WGSGermlineMultiCallersVariantsOnly):
    def id(self):
        return "WGSGermlineMultiCallers"

    def friendly_name(self):
        return "WGS Germline (Multi callers)"

    def version(self):
        return "1.3.1"

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
        self.input(
            "sample_name",
            String,
            doc=InputDocumentation(
                "Sample name from which to generate the readGroupHeaderLine for BwaMem",
                quality=InputQualityType.user,
                example="NA12878",
            ),
        )
        self.input(
            "fastqs",
            Array(FastqGzPair),
            doc=InputDocumentation(
                "An array of FastqGz pairs. These are aligned separately and merged "
                "to create higher depth coverages from multiple sets of reads",
                quality=InputQualityType.user,
                example="[[BRCA1_R1.fastq.gz, BRCA1_R2.fastq.gz]]",
            ),
        )

        self.inputs_for_reference()
        self.inputs_for_intervals()
        self.inputs_for_configuration()

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


if __name__ == "__main__":
    import os.path

    w = WGSGermlineMultiCallers()
    args = {
        "to_console": True,
        "to_disk": False,
        "validate": True,
        "export_path": os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "{language}"
        ),
        "with_resource_overrides": False,
    }
    w.translate("cwl", **args)
    w.translate("wdl", **args)
