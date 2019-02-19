import janis as p

from janis_bioinformatics.data_types import BamBai, FastaWithDict
from janis_bioinformatics.tools.bcftools import BcfToolsViewLatest
from janis_bioinformatics.tools.common import SplitMultiAllele
from janis_bioinformatics.tools.illumina import Strelka_2_9_9
from janis_bioinformatics.tools.illumina.manta.manta_1_4_0 import Manta_1_4_0


class StrelkaSubworkflow(p.Workflow):

    @staticmethod
    def version():
        return "v1.0.0"
    
    def __init__(self):
        p.Workflow.__init__(self, "strelka_pipeline")
    
        ref = p.Input("reference", FastaWithDict())
        bam = p.Input("bam", BamBai())
    
        s1_manta = p.Step("manta", Manta_1_4_0())
        s2_strelka = p.Step("strelka", Strelka_2_9_9())
        s3_bcf = p.Step("bcf", BcfToolsViewLatest())
        s4_split = p.Step("splitmultiallele", SplitMultiAllele())
    
        # step 1
        self.add_edges([
            (bam, s1_manta),
            (ref, s1_manta)
        ])
    
        # step 2
        self.add_edges([
            (bam, s2_strelka),
            (ref, s2_strelka),
            (s1_manta.candidateSmallIndels, s2_strelka.indelCandidates),
            (s2_strelka.script, p.Output("script")),
            (s2_strelka.stats, p.Output("stats")),
            (s2_strelka.variants, p.Output("variants"))
        ])
    
        # Step2
        self.add_edge(s2_strelka.variants, s3_bcf.file)
        self.add_default_value(s3_bcf.applyFilters, ["PASS"])
    
        # Step3
        self.add_edges([
            (ref, s4_split.reference),
            (s3_bcf, s4_split.input),
            (s4_split, p.Output("split-out"))
        ])


if __name__ == "__main__":
    w = StrelkaSubworkflow()
    w.dump_translation("cwl", to_disk=True, with_docker=True)
