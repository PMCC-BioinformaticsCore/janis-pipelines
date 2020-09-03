from datetime import date

from janis_bioinformatics.data_types import FastaWithDict, VcfTabix, Bed, File, BamBai
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import GATKBaseRecalBQSRWorkflow_4_1_3
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_1_3
from janis_bioinformatics.tools.htslib import BGZipLatest
from janis_bioinformatics.tools.papenfuss import Gridss_2_6_2
from janis_bioinformatics.tools.pmac import AddBamStatsSomatic_0_1_0
from janis_bioinformatics.tools.variantcallers import GatkSomaticVariantCaller_4_1_3
from janis_core import (
    String,
    Array,
    WorkflowMetadata,
    InputDocumentation,
    InputQualityType,
)
from janis_unix.tools import UncompressArchive


class WGSSomaticGATKVariantsOnly(BioinformaticsWorkflow):
    def id(self):
        return "WGSSomaticGATKVariantsOnly"

    def friendly_name(self):
        return "WGS Somatic (GATK only) [VARIANTS only]"

    def version(self):
        return "1.3.1"

    def constructor(self):

        self.add_inputs()
        self.add_gridss(
            normal_bam_source=self.normal_bam, tumor_bam_source=self.tumor_bam
        )
        self.add_gatk_variantcaller(
            normal_bam_source=self.normal_bam, tumor_bam_source=self.tumor_bam
        )

    def add_inputs(self):

        # INPUTS
        self.input(
            "normal_bam",
            BamBai,
            doc=InputDocumentation(
                "Indexed NORMAL bam to call somatic variants against",
                quality=InputQualityType.user,
                example="normal.bam",
            ),
        )
        self.input(
            "tumor_bam",
            BamBai,
            doc=InputDocumentation(
                "Indexed TUMOR bam to call somatic variants against",
                quality=InputQualityType.user,
                example="tumor.bam",
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

        self.add_inputs_for_configuration()
        self.add_inputs_for_reference()
        self.add_inputs_for_intervals()

    def add_inputs_for_configuration(self):

        self.input(
            "cutadapt_adapters",
            File(optional=True),
            doc=InputDocumentation(
                "Specifies a containment list for cutadapt, which contains a list of sequences to determine valid overrepresented sequences from "
                "the FastQC report to trim with Cuatadapt. The file must contain sets of named adapters in the form: "
                "``name[tab]sequence``. Lines prefixed with a hash will be ignored.",
                quality=InputQualityType.static,
                example="https://github.com/csf-ngs/fastqc/blob/master/Contaminants/contaminant_list.txt",
            ),
        )

        self.input(
            "gnomad",
            VcfTabix(),
            doc=InputDocumentation(
                "The genome Aggregation Database (gnomAD). This VCF must be compressed and tabix indexed. This is specific for your genome (eg: hg38 / br37) and can usually be found with your reference. For example for HG38, the Broad institute provide the following af-only-gnomad compressed and tabix indexed VCF: https://console.cloud.google.com/storage/browser/gatk-best-practices/somatic-hg38;tab=objects?prefix=af-only",
                quality=InputQualityType.static,
                example="https://storage.cloud.google.com/gatk-best-practices/somatic-hg38/af-only-gnomad.hg38.vcf.gz",
            ),
        )
        self.input(
            "panel_of_normals",
            VcfTabix(optional=True),
            doc=InputDocumentation(
                "VCF file of sites observed in normal.",
                quality=InputQualityType.static,
                example="gs://gatk-best-practices/somatic-b37/Mutect2-exome-panel.vcf or gs://gatk-best-practices/somatic-b37/Mutect2-WGS-panel-b37.vcf for hg19/b37",
            ),
        )

    def add_inputs_for_intervals(self):
        self.input(
            "gatk_intervals",
            Array(Bed),
            doc=InputDocumentation(
                "List of intervals over which to split the GATK variant calling",
                quality=InputQualityType.static,
                example="BRCA1.bed",
            ),
        )

        self.input(
            "gridss_blacklist",
            Bed,
            doc=InputDocumentation(
                "BED file containing regions to ignore.",
                quality=InputQualityType.static,
                example="https://github.com/PapenfussLab/gridss#blacklist",
            ),
        )

    def add_inputs_for_reference(self):

        self.input(
            "reference",
            FastaWithDict,
            doc=InputDocumentation(
                """\
The reference genome from which to align the reads. This requires a number indexes (can be generated \
with the 'IndexFasta' pipeline This pipeline has been tested using the HG38 reference set.

This pipeline expects the assembly references to be as they appear in the GCP example:

- (".fai", ".amb", ".ann", ".bwt", ".pac", ".sa", "^.dict").""",
                quality=InputQualityType.static,
                example="HG38: https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/\n\n"
                "File: gs://genomics-public-data/references/hg38/v0/Homo_sapiens_assembly38.fasta",
            ),
        )
        self.input(
            "snps_dbsnp",
            VcfTabix,
            doc=InputDocumentation(
                "From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
                quality=InputQualityType.static,
                example="HG38: https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/\n\n"
                "(WARNING: The file available from the genomics-public-data resource on Google Cloud Storage is NOT compressed and indexed. This will need to be completed prior to starting the pipeline.\n\n"
                "File: gs://genomics-public-data/references/hg38/v0/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            ),
        )
        self.input(
            "snps_1000gp",
            VcfTabix,
            doc=InputDocumentation(
                "From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
                quality=InputQualityType.static,
                example="HG38: https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/\n\n"
                "File: gs://genomics-public-data/references/hg38/v0/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            ),
        )
        self.input(
            "known_indels",
            VcfTabix,
            doc=InputDocumentation(
                "From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
                quality=InputQualityType.static,
                example="HG38: https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/\n\n"
                "File: gs://genomics-public-data/references/hg38/v0/Homo_sapiens_assembly38.known_indels.vcf.gz",
            ),
        )
        self.input(
            "mills_indels",
            VcfTabix,
            doc=InputDocumentation(
                "From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
                quality=InputQualityType.static,
                example="HG38: https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/\n\n"
                "File: gs://genomics-public-data/references/hg38/v0/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
            ),
        )

    def add_gridss(self, normal_bam_source, tumor_bam_source):

        # GRIDSS
        self.step(
            "vc_gridss",
            Gridss_2_6_2(
                bams=[normal_bam_source, tumor_bam_source],
                reference=self.reference,
                blacklist=self.gridss_blacklist,
            ),
        )

        # GRIDSS
        self.output(
            "out_gridss_assembly",
            source=self.vc_gridss.assembly,
            output_folder="gridss",
            doc="Assembly returned by GRIDSS",
        )
        self.output(
            "out_variants_gridss",
            source=self.vc_gridss.out,
            output_folder="gridss",
            doc="Variants from the GRIDSS variant caller",
        )

    def add_gatk_variantcaller(self, normal_bam_source, tumor_bam_source):

        recal_ins = {
            "reference": self.reference,
            "intervals": self.gatk_intervals,
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
                intervals=self.gatk_intervals,
                reference=self.reference,
                gnomad=self.gnomad,
                panel_of_normals=self.panel_of_normals,
            ),
            scatter=["intervals", "normal_bam", "tumor_bam"],
        )

        self.step("vc_gatk_merge", Gatk4GatherVcfs_4_1_3(vcfs=self.vc_gatk.out))
        self.step("vc_gatk_compressvcf", BGZipLatest(file=self.vc_gatk_merge.out))
        self.step(
            "vc_gatk_sort_combined", BcfToolsSort_1_9(vcf=self.vc_gatk_compressvcf.out)
        )
        self.step(
            "vc_gatk_uncompressvcf",
            UncompressArchive(file=self.vc_gatk_sort_combined.out),
        )

        self.step(
            "addbamstats",
            AddBamStatsSomatic_0_1_0(
                normal_id=self.normal_name,
                tumor_id=self.tumor_name,
                normal_bam=normal_bam_source,
                tumor_bam=tumor_bam_source,
                reference=self.reference,
                vcf=self.vc_gatk_uncompressvcf.out,
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
            "out_variants_split",
            source=self.vc_gatk.out,
            output_folder=["variants", "byInterval"],
            doc="Unmerged variants from the GATK caller (by interval)",
        )
        self.output(
            "out_variants",
            source=self.addbamstats.out,
            output_folder="variants",
            doc="Final vcf",
        )

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = ["wgs", "cancer", "somatic", "variants", "gatk"]
        meta.dateUpdated = date(2019, 10, 16)
        meta.dateUpdated = date(2020, 8, 18)

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
        meta.sample_input_overrides = {
            "normal_inputs": [
                ["normal_R1.fastq.gz", "normal_R2.fastq.gz"],
                ["normal_R1-TOPUP.fastq.gz", "normal_R2-TOPUP.fastq.gz"],
            ],
            "tumor_inputs": [
                ["tumor_R1.fastq.gz", "tumor_R2.fastq.gz"],
                ["tumor_R1-TOPUP.fastq.gz", "tumor_R2-TOPUP.fastq.gz"],
            ],
            "reference": "Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_indels": "Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
            "gnomad": "af-only-gnomad.hg38.vcf.gz",
        }


if __name__ == "__main__":
    import os.path

    w = WGSSomaticGATKVariantsOnly()
    args = {
        "to_console": True,
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
