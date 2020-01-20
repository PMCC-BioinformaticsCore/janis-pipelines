from datetime import date

from janis_bioinformatics.data_types import (
    FastaWithDict,
    Fastq,
    VcfTabix,
    Bed,
    FastqGzPair,
    File
)
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.common import BwaAligner, MergeAndMarkBams_4_1_3
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_1_3
from janis_bioinformatics.tools.variantcallers import GatkSomaticVariantCaller_4_1_3
from janis_bioinformatics.tools.pmac import ParseFastqcAdaptors
from janis_core import String, WorkflowBuilder, Array, WorkflowMetadata


class WGSSomaticGATK(BioinformaticsWorkflow):
    def id(self):
        return "WGSSomaticGATK"

    def friendly_name(self):
        return "WGS Somatic (GATK only)"

    @staticmethod
    def version():
        return "1.2.0"
        
    def constructor(self):

        self.input("normal_inputs", Array(FastqGzPair))
        self.input("tumor_inputs", Array(FastqGzPair))

        self.input("normal_name", String, default="NA24385_normal")
        self.input("tumor_name", String, default="NA24385_tumour")

        self.input("gatk_intervals", Array(Bed))
        self.input("cutadapt_adapters", File)

        self.input("reference", FastaWithDict)
        self.input("snps_dbsnp", VcfTabix)
        self.input("snps_1000gp", VcfTabix)
        self.input("known_indels", VcfTabix)
        self.input("mills_indels", VcfTabix)

        self.step(
            "normal",
            self.process_subpipeline(
                reads=self.tumor_inputs,
                sample_name=self.tumor_name,
                reference=self.reference,
                cutadapt_adapters=self.cutadapt_adapters,
            ),
        )
        self.step(
            "tumor",
            self.process_subpipeline(
                reads=self.normal_inputs,
                sample_name=self.normal_name,
                reference=self.reference,
                cutadapt_adapters=self.cutadapt_adapters,
            ),
        )

        self.step(
            "vc_gatk",
            GatkSomaticVariantCaller_4_1_3(
                normal_bam=self.tumor.out,
                tumor_bam=self.normal.out,
                normal_name=self.normal_name,
                tumor_name=self.tumor_name,
                intervals=self.gatk_intervals,
                reference=self.reference,
                snps_dbsnp=self.snps_dbsnp,
                snps_1000gp=self.snps_1000gp,
                known_indels=self.known_indels,
                mills_indels=self.mills_indels,
            ),
            scatter="intervals",
        )

        self.step(
            "vc_gatk_merge",
            Gatk4GatherVcfs_4_1_3(vcfs=self.vc_gatk),
        )
        self.step("sorted", BcfToolsSort_1_9(vcf=self.vc_gatk_merge.out))

        # Outputs

        self.output("normal_bam", source=self.normal.out, output_folder="bams")
        self.output("tumor_bam", source=self.tumor.out, output_folder="bams")
        self.output("normal_report", source=self.normal.reports, output_folder="reports")
        self.output("tumor_report", source=self.tumor.reports, output_folder="reports")

        self.output("variants_gatk", source=self.sorted.out, output_folder="variants")

    @staticmethod
    def process_subpipeline(**connections):
        w = WorkflowBuilder("somatic_subpipeline")

        w.input("reference", FastaWithDict)
        w.input("reads", Array(FastqGzPair))
        w.input("cutadapt_adapters", File)

        w.input("sample_name", String)

        w.step("fastqc", FastQC_0_11_5(reads=w.reads), scatter="reads")

        w.step(
            "getfastqc_adapters", 
            ParseFastqcAdaptors(
                fastqc_datafiles=w.fastqc.datafile,
                cutadapt_adaptors_lookup=w.cutadapt_adapters
            ),
            scatter="fastqc_datafiles"
        )

        w.step(
            "align_and_sort",
            BwaAligner(
                fastq=w.reads,
                reference=w.reference,
                sample_name=w.sample_name,
                sortsam_tmpDir=None,
                cutadapt_adapter=w.getfastqc_adapters,
                cutadapt_removeMiddle3Adapter=w.getfastqc_adapters,
            ),
            scatter=["fastq", "cutadapt_adapter", "cutadapt_removeMiddle3Adapter"]
        )

        w.step("merge_and_mark", MergeAndMarkBams_4_1_3(bams=w.align_and_sort.out))

        w.output("out", source=w.merge_and_mark.out)
        w.output("reports", source=w.fastqc.out)

        return w(**connections)

    def bind_metadata(self):
        meta: WorkflowMetadata = self.metadata

        meta.keywords = ["wgs", "cancer", "somatic", "variants", "gatk"]
        meta.contributors = ["Michael Franklin"]
        meta.dateUpdated = date(2019, 10, 16)
        meta.short_documentation = "A somatic tumor-normal variant-calling WGS pipeline using only GATK Mutect2"


if __name__ == "__main__":
    import os.path
    w = WGSSomaticGATK()
    args = {
        "to_console": False,
        "to_disk": True,
        "validate": True,
        "export_path": os.path.join(os.path.dirname(os.path.realpath(__file__)), "{language}"),
    }
    w.translate("cwl", **args)
    w.translate("wdl", **args)
