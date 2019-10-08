from datetime import date

from janis_bioinformatics.data_types import FastqGzPair, FastaWithDict
from janis_bioinformatics.tools import BioinformaticsWorkflow
from janis_bioinformatics.tools.common.bwamem_samtoolsview import BwaMem_SamToolsView
from janis_bioinformatics.tools.cutadapt.cutadapt_1_18 import CutAdapt_1_18
from janis_bioinformatics.tools.gatk4 import Gatk4SortSam_4_1_2


class BwaAlignment(BioinformaticsWorkflow):
    def id(self):
        return "alignment"

    def friendly_name(self):
        return "Alignment (BWA MEM)"

    @staticmethod
    def tool_provider():
        return "Common"

    @staticmethod
    def version():
        return "1.0.0"

    def constructor(self):

        # Inputs
        self.input("sampleName", str)
        self.input("reference", FastaWithDict)
        self.input("fastq", FastqGzPair)

        # Steps
        self.step(
            "cutadapt",
            CutAdapt_1_18(
                fastq=self.fastq,
                adapter=None,
                adapter_g=None,
                removeMiddle5Adapter=None,
                removeMiddle3Adapter=None,
                qualityCutoff=15,
                minReadLength=50,
            ),
        )

        self.step(
            "bwamem",
            BwaMem_SamToolsView(
                reads=self.cutadapt.out,
                sampleName=self.sampleName,
                reference=self.reference,
            ),
        )

        self.step(
            "sortsam",
            Gatk4SortSam_4_1_2(
                bam=self.bwamem.out,
                sortOrder="coordinate",
                createIndex=True,
                validationStringency="SILENT",
                maxRecordsInRam=5000000,
                tmpDir=".",
            ),
        )

        # outputs
        self.output("out", source=self.sortsam)

    def bind_metadata(self):
        self.metadata.documentation = (
            "Alignment and sort of reads using BWA Mem + SamTools + Gatk4SortSam"
        )
        self.metadata.creator = "Michael Franklin"
        self.metadata.dateCreated = date(2018, 12, 24)
        self.metadata.dateUpdated = date(2019, 8, 20)
        self.metadata.version = "1.0.0"


if __name__ == "__main__":
    w = BwaAlignment()
    args = {
        "to_console": False,
        "to_disk": True,
        "validate": True,
        "export_path": "{language}",
    }
    w.translate("cwl", **args)
    w.translate("wdl", **args)
