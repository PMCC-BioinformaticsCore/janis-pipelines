from datetime import date

from janis_core import Step, String, Input, Output, Int, Boolean
from janis_core import WorkflowMetadata

from janis_bioinformatics.data_types import Fastq, FastaWithDict
from janis_bioinformatics.tools import BioinformaticsWorkflow
from janis_bioinformatics.tools.common.bwamem_samtoolsview import BwaMem_SamToolsView
from janis_bioinformatics.tools.cutadapt.cutadapt_1_18 import CutAdapt_1_18
from janis_bioinformatics.tools.gatk4 import Gatk4SortSam_4_0


class BwaAlignment(BioinformaticsWorkflow):
    @staticmethod
    def tool_provider():
        return "Common"

    @staticmethod
    def version():
        return "1.0.0"

    def __init__(self):
        super(BwaAlignment, self).__init__(
            "alignment", friendly_name="Alignment (BWA MEM)"
        )

        if not self._metadata:
            self._metadata = WorkflowMetadata()

        self._metadata.documentation = "Alignment and sort of reads using BWA Mem + SamTools + Gatk4SortSam"
        self._metadata.creator = "Michael Franklin"
        self._metadata.dateCreated = date(2018, 12, 24)
        self._metadata.dateUpdated = date(2019, 8, 20)
        self._metadata.version = "1.0.0"

        cutadapt = Step("cutadapt", CutAdapt_1_18())
        bwasam = Step("bwa_sam", BwaMem_SamToolsView())
        sortsam = Step("sortsam", Gatk4SortSam_4_0())

        sample_name = Input("sampleName", String())
        reference = Input("reference", FastaWithDict())
        fastqs = Input("fastq", Fastq())

        out_bam = Output("out_bwa")
        out = Output("out")

        # S1: Cutadapt
        self.add_edge(fastqs, cutadapt.fastq)
        # Step 1 with defaults
        self.add_edges(
            [
                (
                    Input(
                        "adapter",
                        String(optional=True),
                        include_in_inputs_file_if_none=False,
                    ),
                    cutadapt.adapter,
                ),
                (
                    Input(
                        "adapter_g",
                        String(optional=True),
                        include_in_inputs_file_if_none=False,
                    ),
                    cutadapt.adapter_g,
                ),
                (
                    Input(
                        "removeMiddle5Adapter",
                        String(optional=True),
                        include_in_inputs_file_if_none=False,
                    ),
                    cutadapt.removeMiddle5Adapter,
                ),
                (
                    Input(
                        "removeMiddle3Adapter",
                        String(optional=True),
                        include_in_inputs_file_if_none=False,
                    ),
                    cutadapt.removeMiddle3Adapter,
                ),
                (
                    Input("qualityCutoff", Int(optional=True), default=15),
                    cutadapt.qualityCutoff,
                ),
                (
                    Input("minReadLength", Int(optional=True), default=50),
                    cutadapt.minReadLength,
                ),
            ]
        )

        # S2: BWA mem + Samtools View
        self.add_edges(
            [
                (cutadapt.out, bwasam.reads),
                (sample_name, bwasam.sampleName),
                (reference, bwasam.reference),
            ]
        )

        # S3: SortSam
        self.add_edge(bwasam.out, sortsam.bam)
        self.add_edges(
            [
                (
                    Input("sortOrder", String(optional=True), default="coordinate"),
                    sortsam.sortOrder,
                ),
                (
                    Input("createIndex", Boolean(optional=True), default=True),
                    sortsam.createIndex,
                ),
                (
                    Input(
                        "validationStringency", String(optional=True), default="SILENT"
                    ),
                    sortsam.validationStringency,
                ),
                (
                    Input("maxRecordsInRam", Int(optional=True), default=5000000),
                    sortsam.maxRecordsInRam,
                ),
                (
                    Input(
                        "sortSamTmpDir",
                        String(optional=True),
                        include_in_inputs_file_if_none=False,
                    ),
                    sortsam.tmpDir,
                ),
            ]
        )

        # connect to output
        self.add_edge(bwasam.out, out_bam)
        self.add_edge(sortsam.out, out)


if __name__ == "__main__":
    w = BwaAlignment()

    w.translate("cwl", to_disk=True, export_path="{language}")

    # print(build_resources_input(w, "wdl", {CaptureType.KEY: CaptureType.CHROMOSOME}))

    # print(AlignSortedBam().help())

    # import shepherd
    #
    # task = shepherd.from_workflow(w, engine=shepherd.Cromwell(), env="pmac")
    # print(task.outputs)
