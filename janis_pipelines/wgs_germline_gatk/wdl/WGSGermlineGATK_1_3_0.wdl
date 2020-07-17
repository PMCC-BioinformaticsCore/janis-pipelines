version development

import "tools/fastqc_v0_11_5.wdl" as F
import "tools/ParseFastqcAdaptors_v0_1_0.wdl" as P
import "tools/BwaAligner_1_0_0.wdl" as B
import "tools/mergeAndMarkBams_4_1_3.wdl" as M
import "tools/Gatk4DepthOfCoverage_4_1_6_0.wdl" as G
import "tools/PerformanceSummaryGenome_v0_1_0.wdl" as P2
import "tools/gridss_v2_6_2.wdl" as G2
import "tools/GATKBaseRecalBQSRWorkflow_4_1_3.wdl" as G3
import "tools/GATK4_GermlineVariantCaller_4_1_3_0.wdl" as G4
import "tools/Gatk4GatherVcfs_4_1_3_0.wdl" as G5
import "tools/bgzip_1_2_1.wdl" as B2
import "tools/bcftoolssort_v1_9.wdl" as B3
import "tools/UncompressArchive_v1_0_0.wdl" as U
import "tools/AddBamStatsGermline_v0_1_0.wdl" as A

workflow WGSGermlineGATK {
  input {
    String sample_name
    Array[Array[File]] fastqs
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
    File gridss_blacklist
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
  scatter (f in fastqs) {
     call F.fastqc as fastqc {
      input:
        reads=f
    }
  }
  scatter (f in fastqc.datafile) {
     call P.ParseFastqcAdaptors as getfastqc_adapters {
      input:
        fastqc_datafiles=f,
        cutadapt_adaptors_lookup=cutadapt_adapters
    }
  }
  scatter (Q in zip(fastqs, zip(getfastqc_adapters.adaptor_sequences, getfastqc_adapters.adaptor_sequences))) {
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
  call G2.gridss as vc_gridss {
    input:
      bams=[merge_and_mark.out],
      bams_bai=[merge_and_mark.out_bai],
      reference=reference,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      blacklist=gridss_blacklist
  }
  call G3.GATKBaseRecalBQSRWorkflow as bqsr {
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
  scatter (g in gatk_intervals) {
     call G4.GATK4_GermlineVariantCaller as vc_gatk {
      input:
        bam=bqsr.out,
        bam_bai=bqsr.out_bai,
        intervals=g,
        reference=reference,
        reference_fai=reference_fai,
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_dict=reference_dict,
        snps_dbsnp=snps_dbsnp,
        snps_dbsnp_tbi=snps_dbsnp_tbi
    }
  }
  call G5.Gatk4GatherVcfs as vc_gatk_merge {
    input:
      vcfs=vc_gatk.out
  }
  call B2.bgzip as vc_gatk_compressvcf {
    input:
      file=vc_gatk_merge.out
  }
  call B3.bcftoolssort as vc_gatk_sort_combined {
    input:
      vcf=vc_gatk_compressvcf.out
  }
  call U.UncompressArchive as vc_gatk_uncompressvcf {
    input:
      file=vc_gatk_sort_combined.out
  }
  call A.AddBamStatsGermline as addbamstats {
    input:
      bam=merge_and_mark.out,
      bam_bai=merge_and_mark.out_bai,
      vcf=vc_gatk_uncompressvcf.out
  }
  output {
    Array[Array[File]] reports = fastqc.out
    File sample_coverage = coverage.out_sampleSummary
    File summary = performance_summary.performanceSummaryOut
    File gridss_assembly = vc_gridss.assembly
    File variants_gridss = vc_gridss.out
    File bam = merge_and_mark.out
    File bam_bai = merge_and_mark.out_bai
    File variants = vc_gatk_sort_combined.out
    Array[File] variants_split = vc_gatk.out
    File variants_final = addbamstats.out
  }
}