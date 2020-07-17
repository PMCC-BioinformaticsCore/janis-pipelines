version development

import "fastqc_v0_11_5.wdl" as F
import "ParseFastqcAdaptors_v0_1_0.wdl" as P
import "BwaAligner_1_0_0.wdl" as B
import "mergeAndMarkBams_4_1_3.wdl" as M
import "Gatk4DepthOfCoverage_4_1_6_0.wdl" as G
import "PerformanceSummaryGenome_v0_1_0.wdl" as P2
import "GATKBaseRecalBQSRWorkflow_4_1_3.wdl" as G2

workflow somatic_subpipeline {
  input {
    Array[Array[File]] reads
    String sample_name
    File reference
    File reference_fai
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_dict
    File? cutadapt_adapters
    Array[File] gatk_intervals
    File genome_file
    File snps_dbsnp
    File snps_dbsnp_tbi
    File snps_1000gp
    File snps_1000gp_tbi
    File known_indels
    File known_indels_tbi
    File mills_indels
    File mills_indels_tbi
    String? align_and_sort_sortsam_tmpDir = "."
    Boolean? coverage_omitDepthOutputAtEachBase = true
    Array[Int]? coverage_summaryCoverageThreshold = [1, 50, 100, 300, 500]
  }
  scatter (r in reads) {
     call F.fastqc as fastqc {
      input:
        reads=r
    }
  }
  scatter (f in fastqc.datafile) {
     call P.ParseFastqcAdaptors as getfastqc_adapters {
      input:
        fastqc_datafiles=f,
        cutadapt_adaptors_lookup=cutadapt_adapters
    }
  }
  scatter (Q in zip(reads, zip(getfastqc_adapters.adaptor_sequences, getfastqc_adapters.adaptor_sequences))) {
     call B.BwaAligner as align_and_sort {
      input:
        sample_name=sample_name,
        reference=reference,
        reference_fai=reference_fai,
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_dict=reference_dict,
        fastq=Q.left,
        cutadapt_adapter=Q.right.right,
        cutadapt_removeMiddle3Adapter=Q.right.right,
        sortsam_tmpDir=select_first([align_and_sort_sortsam_tmpDir, "."])
    }
  }
  call M.mergeAndMarkBams as merge_and_mark {
    input:
      bams=align_and_sort.out,
      bams_bai=align_and_sort.out_bai,
      sampleName=sample_name
  }
  call G.Gatk4DepthOfCoverage as coverage {
    input:
      bam=merge_and_mark.out,
      bam_bai=merge_and_mark.out_bai,
      reference=reference,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      outputPrefix=sample_name,
      intervals=gatk_intervals,
      summaryCoverageThreshold=select_first([coverage_summaryCoverageThreshold, [1, 50, 100, 300, 500]]),
      omitDepthOutputAtEachBase=select_first([coverage_omitDepthOutputAtEachBase, true])
  }
  call P2.PerformanceSummaryGenome as performance_summary {
    input:
      bam=merge_and_mark.out,
      bam_bai=merge_and_mark.out_bai,
      sample_name=sample_name,
      genome_file=genome_file
  }
  call G2.GATKBaseRecalBQSRWorkflow as bqsr {
    input:
      bam=merge_and_mark.out,
      bam_bai=merge_and_mark.out_bai,
      reference=reference,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      snps_dbsnp=snps_dbsnp,
      snps_dbsnp_tbi=snps_dbsnp_tbi,
      snps_1000gp=snps_1000gp,
      snps_1000gp_tbi=snps_1000gp_tbi,
      known_indels=known_indels,
      known_indels_tbi=known_indels_tbi,
      mills_indels=mills_indels,
      mills_indels_tbi=mills_indels_tbi
  }
  output {
    File out = merge_and_mark.out
    File out_bai = merge_and_mark.out_bai
    File bqsr_bam = bqsr.out
    File bqsr_bam_bai = bqsr.out_bai
    Array[Array[File]] reports = fastqc.out
    File depth_of_coverage = coverage.out_sampleSummary
    File summary = performance_summary.performanceSummaryOut
  }
}