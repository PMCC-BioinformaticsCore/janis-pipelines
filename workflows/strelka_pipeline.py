from janis import Workflow, Input, Step, Output

from janis_bioinformatics.data_types import BamBai, FastaWithDict
from janis_bioinformatics.tools.variantcallers import StrelkaVariantCaller


class StrelkaWrapped(Workflow):

    @staticmethod
    def version():
        return "v1.0.0"
    
    def __init__(self):
        Workflow.__init__(self, "strelka_pipeline")
    
        bam = Input("bam", BamBai(), "/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/intermediate/processed.bam")
        ref = Input("reference", FastaWithDict(), "/Users/franklinmichael/reference/hg38/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta")

        strelka_vc = Step("strelka", StrelkaVariantCaller())

        self.add_edges([
            (bam, strelka_vc),
            (ref, strelka_vc)
        ])

        self.add_edges([
            (strelka_vc.variants, Output("variants")),
            (strelka_vc.out, Output("out"))
        ])


if __name__ == "__main__":
    w = StrelkaWrapped()
    w.dump_translation("wdl", to_disk=True, write_inputs_file=True)
