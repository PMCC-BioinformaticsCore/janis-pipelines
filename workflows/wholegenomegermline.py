import unittest

from janis import Input, String, Step, Directory, Workflow, Array, Output
import janis.bioinformatics as jb

from janis_bioinformatics.data_types import FastaWithDict, Fastq, VcfIdx, VcfTabix, Fastq, VcfIdx
from janis_bioinformatics.tools.common import AlignSortedBam
from janis_bioinformatics.tools.common.processbam import ProcessBamFiles_4_0
from janis_bioinformatics.tools.validation import PerformanceValidator_1_2_1
import janis_bioinformatics.tools.gatk4 as GATK4

BcfToolsNorm = jb.tools.bcftools.BcfToolsNormLatest


class WholeGenomeGermlineWorkflow(Workflow):

    @staticmethod
    def version():
        return "1.0.0"

    def __init__(self):
        Workflow.__init__(self, "whole_genome_germline")

        reference = Input("reference", FastaWithDict())
        fastqInputs = Input("inputs", Array(Fastq()))

        s1_inp_header = Input("readGroupHeaderLine", String())
        snps_dbsnp = Input("snps_dbsnp", VcfIdx())
        snps_1000gp = Input("snps_1000gp", VcfTabix())
        omni = Input("omni", VcfTabix())
        hapmap = Input("hapmap", VcfTabix())
        validator_truth = Input("truthVCF", VcfIdx())
        validator_intervals = Input("intervals", Array(VcfIdx()))

        inp_tmpdir = Input("tmpdir", Directory())

        s1_sw = Step("s1_alignSortedBam", AlignSortedBam())
        s2_process = Step("s2_processBamFiles", ProcessBamFiles_4_0())

        s6_haploy = Step("s6_haploy", GATK4.Gatk4HaplotypeCaller_4_0())
        s7_bcfNorm = Step("s7_bcfNorm", BcfToolsNorm())
        s8_validator = Step("s8_validator", PerformanceValidator_1_2_1())

        # step1
        self.add_edge(fastqInputs, s1_sw.fastq)
        self.add_edges([
            (reference, s1_sw.reference),
            (s1_inp_header, s1_sw.read_group_header_line),
            (inp_tmpdir, s1_sw.tmpdir)
        ])

        # step2 - process bam files
        self.add_edges([
            (s1_sw.o3_sortsam, s2_process.input),
            (reference, s2_process),
            (inp_tmpdir, s2_process.tmpDir),
            (snps_dbsnp, s2_process.snps_dbsnp),
            (snps_1000gp, s2_process.snps_1000gp),
            (omni, s2_process.omni),
            (hapmap, s2_process.hapmap)
        ])

        # step6 - haplotype caller
        self.add_edges([
            (s2_process, s6_haploy),
            (reference, s6_haploy),
            (snps_dbsnp, s6_haploy)
        ])

        # step7 - BcfToolsNorm
        self.add_edges([
            (reference, s7_bcfNorm.reference),
            (s6_haploy, s7_bcfNorm.input)
            # (s7_cheat_inp, s7_bcfNorm.input)
        ])

        # step8 - validator

        self.add_edges([
            (s7_bcfNorm, s8_validator),
            (validator_truth, s8_validator.truth),
            (validator_intervals, s8_validator.intervals)
        ])

        # Outputs

        self.add_edges([
            (s1_sw.o1_bwa, Output("sw_bwa")),
            (s1_sw.o2_samtools, Output("sw_samtools")),
            (s1_sw.o3_sortsam, Output("sw_sortsam")),
            (s6_haploy.output, Output("o8_halpo")),
            (s7_bcfNorm, Output("o9_bcfnorm")),
            (s8_validator.summaryMetrics, Output("o12_concord_summary")),
            (s8_validator.detailMetrics, Output("o12_concord_detail")),
            (s8_validator.contingencyMetrics, Output("o12_concord_contig"))
        ])


if __name__ == "__main__":
    WholeGenomeGermlineWorkflow().dump_translation("cwl", to_disk=True)


original_bash = """
#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --partition=debug
#SBATCH --mem=64G
#SBATCH --time=10-00:00:00
#SBATCH --mail-user=jiaan.yu@petermac.org
#SBATCH --mail-type=ALL
#SBATCH --output=pipeline-%j.out
#SBATCH --job-name="WGSpipeline"


echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running on $SLURM_NPROCS processors."
echo "Current working directory is `pwd`"

STARTTIME=$(date +%s)


module load bwa/0.7.17
module load samtools/1.9
module load gatk/4.0.10.0
module load bcftools/1.9
module load igvtools

## Input parameters: R1 of fastq files

READ_GROUP_HEADER_LINE='@RG\tID:NA12878\tSM:NA12878\tLB:NA12878\tPL:ILLUMINA'
REFERENCE="/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.fasta"
SNPS_dbSNP='/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/Homo_sapiens_assembly38.dbsnp138.vcf'
SNPS_1000GP='/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/1000G_phase1.snps.high_confidence.hg38.vcf.gz'
OMNI='/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/1000G_omni2.5.hg38.vcf.gz'
HAPMAP='/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hapmap_3.3.hg38.vcf.gz'
TRUTH_VCF=${1/_R1.fastq/.vcf}
INTERVAL_LIST=${1/_R1.fastq/.interval_list}

## Fill in the output file here
SAM='test3/test.sam'


bwa mem -R $READ_GROUP_HEADER_LINE \
 -M \
 -t 36 \
 $REFERENCE \
 $1 ${1/R1/R2} >  $SAM


samtools view -S -h -b $SAM > ${SAM/sam/bam}


gatk SortSam \
 -I=$SAM \
 -O=${SAM/sam/sorted.bam} \
 --SORT_ORDER=coordinate \
 --VALIDATION_STRINGENCY=SILENT \
 --CREATE_INDEX=true \
 --MAX_RECORDS_IN_RAM=5000000 \
 --TMP_DIR='/researchers/jiaan.yu/WGS_pipeline/germline/tmp'


gatk MergeSamFiles \
 -I=${SAM/sam/sorted.bam} \
 -O=${SAM/sam/sorted.merged.bam} \
 --USE_THREADING=true \
 --CREATE_INDEX=true \
 --MAX_RECORDS_IN_RAM=5000000 \
 --VALIDATION_STRINGENCY=SILENT \
 --TMP_DIR='/researchers/jiaan.yu/WGS_pipeline/germline/tmp'


gatk MarkDuplicates \
 -I=${SAM/sam/sorted.merged.bam} \
 -O=${SAM/sam/sorted.merged.markdups.bam} \
 --CREATE_INDEX=true \
 --METRICS_FILE=${SAM/sam/metrics.txt} \
 --MAX_RECORDS_IN_RAM=5000000 \
 --TMP_DIR='/researchers/jiaan.yu/WGS_pipeline/germline/tmp' 


gatk BaseRecalibrator \
 -I=${SAM/sam/sorted.merged.markdups.bam} \
 -O=${SAM/sam/recal.table} \
 -R=$REFERENCE \
 --known-sites=$SNPS_dbSNP \
 --known-sites=$SNPS_1000GP \
 --known-sites=$OMNI \
 --known-sites=$HAPMAP \
 --tmp-dir='/researchers/jiaan.yu/WGS_pipeline/germline/tmp'


gatk ApplyBQSR \
 -R=$REFERENCE \
 -I=${SAM/sam/sorted.merged.markdups.bam} \
 --bqsr-recal-file=${SAM/sam/recal.table} \
 -O=${SAM/sam/sorted.merged.markdups.recal.bam} \
 --tmp-dir='/researchers/jiaan.yu/WGS_pipeline/germline/tmp'


gatk HaplotypeCaller \
 -I=${SAM/sam/sorted.merged.markdups.recal.bam} \
 -R=$REFERENCE \
 -O=${SAM/sam/hap.vcf}
 -D=$SNPS_dbSNP


# The normalised vcf for future steps
bcftools norm -m -both -f $REFERENCE ${SAM/sam/hap.vcf} -o ${SAM/sam/hap.norm.vcf}

# The compressed and indexed vcf for the sake for the validation
bgzip -c ${SAM/sam/hap.norm.vcf} > ${SAM/sam/hap.norm.vcf.gz}
tabix -j vcf ${SAM/sam/hap.norm.vcf.gz}
gatk GenotypeConcordance \
 --TRUTH_VCF $TRUTH_VCF \
 --CALL_VCF ${SAM/sam/hap.norm.vcf.gz} \
 --OUTPUT ${SAM/sam/hap} \
 --MISSING_SITES_HOM_REF true \
 --INTERVALS $INTERVAL_LIST


ENDTIME=$(date +%s)

echo "Time to complete: $(($ENDTIME - $STARTTIME))"
"""
