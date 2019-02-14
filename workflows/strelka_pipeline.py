import janis as p
from janis_bioinformatics.data_types import BamBai, FastaWithDict
from janis_bioinformatics.tools.bcftools import BcfToolsViewLatest
from janis_bioinformatics.tools.common import SplitMultiAllele
from janis_bioinformatics.tools.illumina import Strelka_2_9_9


def strelka_pipeline():
    w = p.Workflow("strelka_pipeline")

    ref = p.Input("reference", FastaWithDict())
    bam = p.Input("bam", BamBai())

    s1_strelka = p.Step("strelka", Strelka_2_9_9())
    s2_bcf = p.Step("bcf", BcfToolsViewLatest())
    s3_split = p.Step("splitmultiallele", SplitMultiAllele())

    w.add_edges([
        (bam, s1_strelka),
        (ref, s1_strelka),
        # (s1_strelka.directory, p.Output("directory")),
        (s1_strelka.script, p.Output("script")),
        (s1_strelka.stats, p.Output("stats")),
        (s1_strelka.variants, p.Output("variants"))
    ])

    # Step2
    w.add_edge(s1_strelka.variants, s2_bcf.file)
    w.add_default_value(s2_bcf.applyFilters, ["PASS"])

    # Step3
    w.add_edges([
        (ref, s3_split.reference),
        (s2_bcf, s3_split.input),
        (s3_split, p.Output("split-out"))
    ])

    return w


w = strelka_pipeline()
w.dump_translation("cwl", to_disk=True, with_docker=True)
