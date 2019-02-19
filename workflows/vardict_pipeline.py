import janis as j

from janis_bioinformatics.data_types import BamBai, Bed, FastaWithDict, VcfIdx
from janis_bioinformatics.tools.bcftools import BcfToolsAnnotateLatest
from janis_bioinformatics.tools.common import SplitMultiAllele
from janis_bioinformatics.tools.common import VarDict
import janis_bioinformatics.tools.gatk4 as GATK4
from janis_bioinformatics.tools.htslib import BGZipLatest, TabixLatest


class VardictSubworkflow(j.Workflow):
    def __init__(self):
        j.Workflow.__init__(self, "vardict_pipeline")
    
        input_bed = j.Input("input_bed", Bed())
        indexed_bam = j.Input("indexed_bam", BamBai())
        reference = j.Input("reference", FastaWithDict())
        header_lines = j.Input("headerLines", j.File())
        truth_vcf = j.Input("truthVcf", VcfIdx())
        intervals = j.Input("intervals", j.Array(j.File()))
        sample_name = j.Input("sampleName", j.String())
        allele_freq_threshold = j.Input("allelFreqThreshold", j.Float())
    
        step1 = j.Step("vardict", VarDict())
        step2 = j.Step("annotate", BcfToolsAnnotateLatest())
        step3 = j.Step("split", SplitMultiAllele())
        step4 = j.Step("zip", BGZipLatest())
        step5 = j.Step("tabix", TabixLatest())
        step6 = j.Step("concord", GATK4.Gatk4GenotypeConcordanceLatest())
    
        # Step1
        self.add_edges([
            (input_bed, step1.input),
            (indexed_bam, step1.indexedBam),
            (reference, step1),
            (sample_name, step1.sampleName),
            (sample_name, step1.var2vcfSampleName),
            (allele_freq_threshold, step1.alleleFreqThreshold),
            (allele_freq_threshold, step1.var2vcfAlleleFreqThreshold)
    
        ])
        self.add_default_value(step1.chromNamesAreNumbers, True)
        self.add_default_value(step1.vcfFormat, True)
        self.add_default_value(step1.chromColumn, 1)
        self.add_default_value(step1.regStartCol, 2)
        self.add_default_value(step1.geneEndCol, 3)


        # Step2
        self.add_edges([
            (header_lines, step2.headerLines),
            (step1, step2)
        ])
    
        # Step3 - splitmulti
        self.add_edges([
            (reference, step3.reference),
            (step2, step3)
        ])
    
        # Step4 - BGZip
        self.add_edge(step3, step4)
    
        # Step5 - Tabix
        self.add_edge(step4, step5)
    
        # Step6 - genotypeConcordance
        self.add_edges([
            (truth_vcf, step6.truthVCF),
            (step5, step6.callVCF),
            (intervals, step6.intervals)
        ])
    
        self.add_default_value(step6.treatMissingSitesAsHomeRef, True)
    
    
        self.add_edges([
            (step1.output, j.Output("vardicted")),
            (step5.output, j.Output("tabixed")),
            (step6.summaryMetrics, j.Output("summaryMetrics")),
            (step6.detailMetrics, j.Output("detailMetrics")),
            (step6.contingencyMetrics, j.Output("contingencyMetrics"))
        ])
    
        self.dump_translation("cwl")
        # self.dump_cwl(to_disk=True, with_docker=False)
        # self.dump_wdl(to_disk=True, with_docker=False)


if __name__ == "__main__":
    w = VardictSubworkflow()
    w.dump_translation("cwl")
