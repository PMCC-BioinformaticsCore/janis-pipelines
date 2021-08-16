from datetime import date

from janis_unix.tools import UncompressArchive
from janis_core import (
    String,
    Array,
    WorkflowMetadata,
    InputQualityType,
)
from janis_core.operators.standard import FirstOperator

from janis_bioinformatics.data_types import (
    FastaWithDict,
    VcfTabix,
    Bed,
    BamBai,
    CompressedVcf,
    Vcf,
)
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9, BcfToolsConcat_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import GATKBaseRecalBQSRWorkflow_4_1_3
from janis_bioinformatics.tools.pmac import (
    AddBamStatsSomatic_0_1_0,
    GenerateIntervalsByChromosome,
)
from janis_bioinformatics.tools.variantcallers import GatkSomaticVariantCaller_4_1_3

from janis_pipelines.reference import WGS_INPUTS

INPUT_DOCS = {
    **WGS_INPUTS,
    "normal_inputs": {
        "doc": "An array of NORMAL FastqGz pairs. These are aligned separately and merged "
        "to create higher depth coverages from multiple sets of reads",
        "quality": InputQualityType.user,
        "example": [
            ["normal_R1.fastq.gz", "normal_R2.fastq.gz"],
            ["normal_R1-TOPUP.fastq.gz", "normal_R2-TOPUP.fastq.gz"],
        ],
    },
    "tumor_inputs": {
        "doc": "An array of TUMOR FastqGz pairs. These are aligned separately and merged "
        "to create higher depth coverages from multiple sets of reads",
        "quality": InputQualityType.user,
        "example": [
            ["tumor_R1.fastq.gz", "tumor_R2.fastq.gz"],
            ["tumor_R1-TOPUP.fastq.gz", "tumor_R2-TOPUP.fastq.gz"],
        ],
    },
    "normal_name": {
        "doc": "Sample name for the NORMAL sample from which to generate the readGroupHeaderLine for BwaMem",
        "quality": InputQualityType.user,
        "example": "NA12878_normal",
    },
    "tumor_name": {
        "doc": "Sample name for the TUMOR sample from which to generate the readGroupHeaderLine for BwaMem",
        "quality": InputQualityType.user,
        "example": "NA12878_tumor",
    },
    "normal_bam": {
        "doc": "Indexed NORMAL bam to call somatic variants against",
        "quality": InputQualityType.user,
        "example": "NA12878-normal.bam",
    },
    "tumor_bam": {
        "doc": "Indexed TUMOR bam to call somatic variants against",
        "quality": InputQualityType.user,
        "example": "NA12878-normal.bam",
    },
}


class WGSSomaticGATKVariantsOnly(BioinformaticsWorkflow):
    def id(self):
        return "WGSSomaticGATKVariantsOnly"

    def friendly_name(self):
        return "WGS Somatic (GATK only) [VARIANTS only]"

    def version(self):
        return "1.4.0"

    def constructor(self):

        self.add_inputs()
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
        self.input("normal_name", String(), doc=INPUT_DOCS["normal_name"])
        self.input("tumor_name", String(), doc=INPUT_DOCS["tumor_name"])

        self.add_inputs_for_configuration()
        self.add_inputs_for_reference()
        self.add_inputs_for_intervals()

    def add_inputs_for_configuration(self):

        self.input("gnomad", VcfTabix(), doc=INPUT_DOCS["gnomad"])
        self.input(
            "panel_of_normals",
            VcfTabix(optional=True),
            doc=INPUT_DOCS["panel_of_normals"],
        )

    def add_inputs_for_intervals(self):
        self.input("gatk_intervals", Array(Bed), doc=INPUT_DOCS["gatk_intervals"])
        self.input("gridss_blacklist", Bed, doc=INPUT_DOCS["gridss_blacklist"])

    def add_inputs_for_reference(self):

        self.input("reference", FastaWithDict, doc=INPUT_DOCS["reference"])
        self.input("snps_dbsnp", VcfTabix, doc=INPUT_DOCS["snps_dbsnp"])
        self.input("snps_1000gp", VcfTabix, doc=INPUT_DOCS["snps_1000gp"])
        self.input("known_indels", VcfTabix, doc=INPUT_DOCS["known_indels"])
        self.input("mills_indels", VcfTabix, doc=INPUT_DOCS["mills_indels"])

    def add_gatk_variantcaller(self, normal_bam_source, tumor_bam_source):
        if "generate_gatk_intervals" in self.step_nodes:
            generated_intervals = self.generate_gatk_intervals.out_regions
        else:
            generated_intervals = self.step(
                "generate_gatk_intervals",
                GenerateIntervalsByChromosome(reference=self.reference),
                when=self.gatk_intervals.is_null(),
            ).out_regions

        intervals = FirstOperator([self.gatk_intervals, generated_intervals])

        recal_ins = {
            "reference": self.reference,
            "intervals": intervals,
            "snps_dbsnp": self.snps_dbsnp,
            "snps_1000gp": self.snps_1000gp,
            "known_indels": self.known_indels,
            "mills_indels": self.mills_indels,
        }
        self.step(
            "bqsr_normal",
            GATKBaseRecalBQSRWorkflow_4_1_3(bam=normal_bam_source, **recal_ins),
            scatter="intervals",
        )

        self.step(
            "bqsr_tumor",
            GATKBaseRecalBQSRWorkflow_4_1_3(bam=tumor_bam_source, **recal_ins),
            scatter="intervals",
        )

        self.step(
            "vc_gatk",
            GatkSomaticVariantCaller_4_1_3(
                normal_bam=self.bqsr_normal.out,
                tumor_bam=self.bqsr_tumor.out,
                normal_name=self.normal_name,
                intervals=intervals,
                reference=self.reference,
                gnomad=self.gnomad,
                panel_of_normals=self.panel_of_normals,
            ),
            scatter=["intervals", "normal_bam", "tumor_bam"],
        )

        self.step(
            "vc_gatk_merge",
            BcfToolsConcat_1_9(vcf=self.vc_gatk.out.as_type(Array(Vcf))),
        )
        self.step(
            "vc_gatk_sort_combined",
            BcfToolsSort_1_9(vcf=self.vc_gatk_merge.out.as_type(CompressedVcf)),
        )
        self.step(
            "vc_gatk_uncompressvcf",
            UncompressArchive(file=self.vc_gatk_sort_combined.out),
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

        # VCF
        self.output(
            "out_variants_gatk",
            source=self.vc_gatk_sort_combined.out,
            output_folder="variants",
            doc="Merged variants from the GATK caller",
        )
        self.output(
            "out_variants_gakt_split",
            source=self.vc_gatk.out,
            output_folder=["variants", "byInterval"],
            doc="Unmerged variants from the GATK caller (by interval)",
        )
        self.output(
            "out_variants_bamstats",
            source=self.addbamstats.out,
            output_folder="variants",
            doc="Final vcf",
        )

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = ["wgs", "cancer", "somatic", "variants", "gatk"]
        meta.dateUpdated = date(2019, 10, 16)
        meta.dateUpdated = date(2021, 5, 28)

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
    import os.path

    w = WGSSomaticGATKVariantsOnly()
    args = {
        "to_console": False,
        "to_disk": True,
        "validate": True,
        "export_path": os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "{language}"
        ),
    }
    w.get_dot_plot(show=True, expand_subworkflows=True)
    # w.translate("cwl", **args)
    # w.translate("wdl", **args)
    #
    # # from cwltool import main
    # # import logging
    #
    # # op = os.path.dirname(os.path.realpath(__file__)) + "/cwl/WGSGermlineGATK.py"
    #
    # # main.run(*["--validate", op], logger_handler=logging.Handler())
