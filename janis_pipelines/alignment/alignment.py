from datetime import date

from janis_core import Array, String
from janis_bioinformatics.tools import BioinformaticsWorkflow
from janis_bioinformatics.data_types import FastqGzPair, FastaWithDict
from janis_bioinformatics.tools.common import BwaAligner, MergeAndMarkBams_4_1_3


class BwaAlignment(BioinformaticsWorkflow):
    def id(self):
        return "alignment"

    def friendly_name(self):
        return "Alignment (BWA MEM) and MarkDuplicates"

    @staticmethod
    def tool_provider():
        return "Common"

    @staticmethod
    def version():
        return "1.0.0"

    def constructor(self):

        # Inputs
        self.input("sample_name", String)
        self.input("reference", FastaWithDict)
        self.input("fastqs", Array(FastqGzPair))

        # Optionals
        self.input("cutadapt_adapter", Array(str, optional=True))
        self.input("cutadapt_removeMiddle3Adapter", Array(str, optional=True))

        # Steps
        self.step(
            "align_and_sort",
            BwaAligner(
                fastq=self.fastqs,
                reference=self.reference,
                sample_name=self.sample_name,
                sortsam_tmpDir="./tmp",
                cutadapt_adapter=self.cutadapt_adapter,
                cutadapt_removeMiddle3Adapter=self.cutadapt_removeMiddle3Adapter,
            ),
            scatter=["fastq"],
        )

        self.step(
            "merge_and_mark",
            MergeAndMarkBams_4_1_3(
                bams=self.align_and_sort.out, sampleName=self.sample_name
            ),
        )

        self.output(
            "out",
            source=self.merge_and_mark.out,
            output_folder="output",
            output_name=self.sample_name,
        )

    def bind_metadata(self):
        self.metadata.documentation = "Alignment and sort of reads using \
BWA Mem + SamTools + Gatk4SortSam, mark duplicate reads using Gatk4MarkDuplicates"
        self.metadata.creator = ["Michael Franklin", "Jiaan Yu"]
        self.metadata.dateCreated = date(2018, 12, 24)
        self.metadata.dateUpdated = date(2021, 5, 28)
        self.metadata.version = "1.0.0"


if __name__ == "__main__":
    import os.path

    w = BwaAlignment()
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
