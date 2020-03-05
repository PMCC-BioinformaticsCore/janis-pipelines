from datetime import date

from janis_bioinformatics.data_types import (
    FastaWithDict,
    VcfTabix,
    BamBai,
    Bed,
    BedTabix,
)

from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import MergeAndMarkBams_4_1_3
from janis_bioinformatics.tools.common.bwaaligner import BwaAligner
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_1_3
from janis_bioinformatics.tools.pmac import CombineVariants_0_0_4
from janis_bioinformatics.tools.variantcallers import (
    GatkGermlineVariantCaller_4_1_3,
    IlluminaGermlineVariantCaller,
    VardictGermlineVariantCaller,
)
from janis_bioinformatics.tools.variantcallers.gridssgermline import (
    GridssGermlineVariantCaller,
)
from janis_bioinformatics.tools.pmac import ParseFastqcAdaptors

from janis_core import Array, File, String, Float, WorkflowMetadata


class WGSGermlineMultiCallersVariantsOnly(BioinformaticsWorkflow):
    def id(self):
        return "WGSGermlineMultiCallersVariantsOnly"

    def friendly_name(self):
        return "WGS Germline (Multi callers) [VARIANTS ONLY]"

    @staticmethod
    def version():
        return "1.2.0"

    def constructor(self):

        self.input(
            "sample_name",
            String,
            doc="Sample name from which to generate the readGroupHeaderLine for BwaMem",
        )

        self.input(
            "bam",
            BamBai,
            doc="An array of FastqGz pairs. These are aligned separately and merged to create higher depth coverages from multiple sets of reads",
        )
        self.input(
            "reference",
            FastaWithDict,
            doc="The reference genome from which to align the reads. This requires a number indexes (can be generated with the 'IndexFasta' pipeline. This pipeline has been tested with the hg38 reference genome.",
        )
        self.input(
            "cutadapt_adapters",
            File(optional=True),
            doc="Specifies a file which contains a list of sequences to determine valid overrepresented sequences from the FastQC report to trim with Cuatadapt. The file must contain sets of named adapters in the form: ``name[tab]sequence``. Lines prefixed with a hash will be ignored.",
        )
        self.input(
            "gatk_intervals",
            Array(Bed),
            doc="List of intervals over which to split the GATK variant calling",
        )
        self.input(
            "vardict_intervals",
            Array(Bed),
            doc="List of intervals over which to split the VarDict variant calling",
        )
        self.input(
            "strelka_intervals",
            BedTabix,
            doc="An interval for which to restrict the analysis to. Recommended HG38 interval: ",
        )

        self.input(
            "header_lines",
            File(optional=True),
            doc="Header lines passed to BCFTools annotate as ``--header-lines``.",
        )

        self.input(
            "allele_freq_threshold",
            Float,
            default=0.05,
            doc="The threshold for VarDict's allele frequency, default: 0.05 or 5%",
        )

        # self.input("gridssBlacklist", Bed)

        self.input(
            "snps_dbsnp",
            VcfTabix,
            doc="From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
        )
        self.input(
            "snps_1000gp",
            VcfTabix,
            doc="From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
        )
        self.input(
            "known_indels",
            VcfTabix,
            doc="From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
        )
        self.input(
            "mills_indels",
            VcfTabix,
            doc="From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
        )

        # VARIANT CALLERS

        # GATK
        self.step(
            "vc_gatk",
            GatkGermlineVariantCaller_4_1_3(
                bam=self.bam,
                intervals=self.gatk_intervals,
                reference=self.reference,
                snps_dbsnp=self.snps_dbsnp,
                snps_1000gp=self.snps_1000gp,
                known_indels=self.known_indels,
                mills_indels=self.mills_indels,
            ),
            scatter="intervals",
        )

        self.step("vc_gatk_merge", Gatk4GatherVcfs_4_1_3(vcfs=self.vc_gatk.out))

        # Strelka
        self.step(
            "vc_strelka",
            IlluminaGermlineVariantCaller(
                bam=self.bam, reference=self.reference, intervals=self.strelka_intervals
            ),
        )

        # Vardict
        self.step(
            "vc_vardict",
            VardictGermlineVariantCaller(
                bam=self.bam,
                reference=self.reference,
                intervals=self.vardict_intervals,
                sample_name=self.sample_name,
                allele_freq_threshold=self.allele_freq_threshold,
                header_lines=self.header_lines,
            ),
            scatter="intervals",
        )
        self.step("vc_vardict_merge", Gatk4GatherVcfs_4_1_3(vcfs=self.vc_vardict.out))

        # GRIDSS
        # self.step(
        #     "vc_gridss",
        #     GridssGermlineVariantCaller(
        #         bam=self.merge_and_mark.out,
        #         reference=self.reference,
        #         blacklist=self.gridssBlacklist,
        #     ),
        # )

        # Combine

        self.step(
            "combine_variants",
            CombineVariants_0_0_4(
                vcfs=[
                    self.vc_gatk_merge.out,
                    self.vc_strelka.out,
                    self.vc_vardict_merge.out,
                    # self.vc_gridss.out,
                ],
                type="germline",
                columns=["AC", "AN", "AF", "AD", "DP", "GT"],
            ),
        )
        self.step("sort_combined", BcfToolsSort_1_9(vcf=self.combine_variants.vcf))

        self.output(
            "variants_combined",
            source=self.sort_combined.out,
            output_folder="variants",
            doc="Combined variants from all 3 callers",
        )

        self.output(
            "variants_gatk",
            source=self.vc_gatk_merge.out,
            output_folder="variants",
            output_name="gatk",
            doc="Merged variants from the GATK caller",
        )
        self.output(
            "variants_vardict",
            source=self.vc_vardict_merge.out,
            output_folder=["variants"],
            output_name="vardict",
            doc="Merged variants from the VarDict caller",
        )
        self.output(
            "variants_strelka",
            source=self.vc_strelka.out,
            output_folder="variants",
            output_name="strelka",
            doc="Variants from the Strelka variant caller",
        )

        self.output(
            "variants_gatk_split",
            source=self.vc_gatk.out,
            output_folder=["variants", "gatk"],
            doc="Unmerged variants from the GATK caller (by interval)",
        )
        self.output(
            "variants_vardict_split",
            source=self.vc_vardict.out,
            output_folder=["variants", "variants"],
            doc="Unmerged variants from the VarDict caller (by interval)",
        )

        # self.output("variants_gridss", source=self.vc_gridss.out)

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = [
            "wgs",
            "cancer",
            "germline",
            "variants",
            "gatk",
            "vardict",
            "strelka",
        ]
        meta.contributors = ["Michael Franklin", "Richard Lupat", "Jiaan Yu"]
        meta.dateCreated = date(2018, 12, 24)
        meta.dateUpdated = date(2020, 3, 5)

        meta.short_documentation = "A (VARIANT ONLY) variant-calling WGS pipeline using GATK, VarDict and Strelka2."
        meta.documentation = """\
This is a genomics pipeline which:

- Call the appropriate variant callers (GATK / Strelka / VarDict);
- Outputs the final variants in the VCF format.

**Resources**

This pipeline has been tested using the HG38 reference set, available on Google Cloud Storage through:

- https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/

This pipeline expects the assembly references to be as they appear in that storage \
    (".fai", ".amb", ".ann", ".bwt", ".pac", ".sa", "^.dict").
The known sites (snps_dbsnp, snps_1000gp, known_indels, mills_indels) should be gzipped and tabix indexed.
"""
        meta.sample_input_overrides = {
            "reference": "Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_indels": "Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        }


if __name__ == "__main__":
    import os.path

    w = WGSGermlineMultiCallersVariantsOnly()
    args = {
        "to_console": False,
        "to_disk": True,
        "validate": True,
        "export_path": os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "variant-only/{language}"
        ),
    }
    w.translate("cwl", **args)
    w.translate("wdl", **args)
