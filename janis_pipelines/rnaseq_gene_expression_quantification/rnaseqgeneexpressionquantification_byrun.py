from datetime import datetime
from janis_core import (
    Array,
    String,
    Int,
    StringFormatter,
    File,
    Directory,
    WorkflowMetadata,
    ScatterDescription,
    ScatterMethod,
)

from janis_bioinformatics.data_types import FastqGzPair
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow

# Tools
from janis_unix.tools.localisefolder import LocaliseFolder
from janis_pipelines.rnaseq_gene_expression_quantification.rnaseqgeneexpressionquantification import (
    RNASeqGeneExpressionQuantification,
)


class RNASeqGeneExpressionQuantificationByRun(BioinformaticsWorkflow):
    def id(self):
        return "RNASeqGeneExpressionQuantificationByRun"

    def friendly_name(self):
        return "RNASeq Gene Expression and Quantification (Per Run)"

    def version(self):
        return "1.0.0"

    def constructor(self):

        # Inputs
        self.input("fastqs_list", Array(FastqGzPair))
        self.input("sample_name_list", Array(String))

        # References
        self.input("gtf", File)
        self.input("star_ref_genome", Directory)

        # Configuration
        self.input("star_threads", Int, default=8)

        # Steps
        self.step(
            "localise_star_genome",
            LocaliseFolder(dir=self.star_ref_genome),
        )

        self.step(
            "singleSampleWorkflow",
            RNASeqGeneExpressionQuantification(
                fastqs=self.fastqs_list,
                sample_name=self.sample_name_list,
                gtf=self.gtf,
                star_ref_genome=self.localise_star_genome.out,
            ),
            scatter=["fastqs", "sample_name"],
        )

        # Gets all the outputs + output_folders + output_names
        self.capture_outputs_from_step(self.singleSampleWorkflow)


if __name__ == "__main__":
    RNASeqGeneExpressionQuantificationByRun().translate(
        "wdl", allow_empty_container=True
    )
