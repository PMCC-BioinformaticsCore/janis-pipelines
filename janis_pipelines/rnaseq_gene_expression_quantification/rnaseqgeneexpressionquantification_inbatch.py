from datetime import datetime
from janis_core import (
    Array,
    String,
    Int,
    File,
    Directory,
    ScatterDescription,
    ScatterMethod,
)

from janis_bioinformatics.data_types import FastqGzPair

# Tools
from janis_pipelines.rnaseq_gene_expression_quantification.rnaseqgeneexpressionquantification import (
    RNASeqGeneExpressionQuantification,
)


class RNASeqGeneExpressionQuantificationInBatch(RNASeqGeneExpressionQuantification):
    def id(self):
        return "RNASeqGeneExpressionQuantificationInBatch"

    def friendly_name(self):
        return "RNASeq Gene Expression and Quantification (in Batch)"

    def version(self):
        return "1.0.0"

    def constructor(self):

        # Inputs
        self.input("fastqs_list", Array(FastqGzPair))
        self.input("sample_name", Array(String))

        # References
        self.input("gtf", File)
        self.input("star_ref_genome", Directory)

        # Configuration
        self.input("star_threads", Int, default=8)

        # Steps
        self.step(
            "single_sample_workflow",
            RNASeqGeneExpressionQuantification(
                fastqs=self.fastqs_list,
                sample_name=self.sample_name,
                gtf=self.gtf,
                star_ref_genome=self.star_ref_genome,
                star_threads=self.star_threads,
            ),
            scatter=ScatterDescription(
                ["fastqs", "sample_name"],
                method=ScatterMethod.dot,
                labels=self.sample_name,
            ),
        )
        self.capture_outputs_from_step(self.single_sample_workflow)


if __name__ == "__main__":
    RNASeqGeneExpressionQuantificationInBatch().translate(
        "wdl", allow_empty_container=True
    )
