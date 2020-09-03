from janis_bioinformatics.data_types import FastqGzPair
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.common import BwaAligner, MergeAndMarkBams_4_1_3
from janis_bioinformatics.tools.pmac import ParseFastqcAdaptors
from janis_core import String, Array, InputDocumentation, InputQualityType

from janis_pipelines.wgs_germline_gatk.wgsgermlinegatk_variantsonly import (
    WGSGermlineGATKVariantsOnly,
)


class WGSGermlineGATK(WGSGermlineGATKVariantsOnly):
    def id(self):
        return "WGSGermlineGATK"

    def friendly_name(self):
        return "WGS Germline (GATK)"

    def constructor(self):
        self.add_inputs()

        self.add_fastqc()
        self.add_align()

        self.add_bam_process()

        # mfranklin (2020-08-20): This is pretty cool, it allows us to reuse
        # these step definitions in different pipelines (without creating a whole subworkflow)

        self.add_bam_qc(bam_source=self.merge_and_mark.out)

        # Add variant callers
        self.add_gridss(bam_source=self.merge_and_mark.out)
        self.add_gatk_variantcaller(bam_source=self.merge_and_mark.out)

    def add_inputs(self):
        # INPUTS
        self.input(
            "sample_name",
            String,
            doc=InputDocumentation(
                "Sample name from which to generate the readGroupHeaderLine for BwaMem",
                quality=InputQualityType.user,
                example="NA12878",
            ),
        )
        self.input(
            "fastqs",
            Array(FastqGzPair),
            doc=InputDocumentation(
                "An array of FastqGz pairs. These are aligned separately and merged "
                "to create higher depth coverages from multiple sets of reads",
                quality=InputQualityType.user,
                example="[[BRCA1_R1.fastq.gz, BRCA1_R2.fastq.gz]]",
            ),
        )

        self.inputs_for_reference()
        self.inputs_for_intervals()
        self.inputs_for_configuration()

    def add_fastqc(self):
        self.step("fastqc", FastQC_0_11_5(reads=self.fastqs), scatter="reads")

        self.output(
            "out_fastqc_reports",
            source=self.fastqc.out,
            output_folder="reports",
            doc="A zip file of the FastQC quality report.",
        )

    def add_align(self):
        self.step(
            "getfastqc_adapters",
            ParseFastqcAdaptors(
                fastqc_datafiles=self.fastqc.datafile,
                cutadapt_adaptors_lookup=self.cutadapt_adapters,
            ),
            scatter="fastqc_datafiles",
        )

        self.step(
            "align_and_sort",
            BwaAligner(
                fastq=self.fastqs,
                reference=self.reference,
                sample_name=self.sample_name,
                sortsam_tmpDir="./tmp",
                cutadapt_adapter=self.getfastqc_adapters,
                cutadapt_removeMiddle3Adapter=self.getfastqc_adapters,
            ),
            scatter=["fastq", "cutadapt_adapter", "cutadapt_removeMiddle3Adapter"],
        )

    def add_bam_process(self):
        self.step(
            "merge_and_mark",
            MergeAndMarkBams_4_1_3(
                bams=self.align_and_sort.out, sampleName=self.sample_name
            ),
        )

        self.output(
            "out_bam",
            source=self.merge_and_mark.out,
            output_folder="bams",
            doc="Aligned and indexed bam.",
            output_name=self.sample_name,
        )
