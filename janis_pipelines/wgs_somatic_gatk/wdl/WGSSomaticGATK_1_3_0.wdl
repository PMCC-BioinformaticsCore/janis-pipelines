version development

import "tools/somatic_subpipeline.wdl" as S
import "tools/gridss_v2_6_2.wdl" as G
import "tools/GATK4_SomaticVariantCaller_4_1_3_0.wdl" as G2
import "tools/Gatk4GatherVcfs_4_1_3_0.wdl" as G3
import "tools/bgzip_1_2_1.wdl" as B
import "tools/bcftoolssort_v1_9.wdl" as B2
import "tools/UncompressArchive_v1_0_0.wdl" as U
import "tools/AddBamStatsSomatic_v0_1_0.wdl" as A

workflow WGSSomaticGATK {
  input {
    Array[Array[File]] normal_inputs
    Array[Array[File]] tumor_inputs
    String normal_name
    String tumor_name
    File? cutadapt_adapters
    Array[File] gatk_intervals
    File genome_file
    File gridss_blacklist
    File reference
    File reference_fai
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_dict
    File snps_dbsnp
    File snps_dbsnp_tbi
    File snps_1000gp
    File snps_1000gp_tbi
    File known_indels
    File known_indels_tbi
    File mills_indels
    File mills_indels_tbi
    File gnomad
    File gnomad_tbi
    File? panel_of_normals
    File? panel_of_normals_tbi
  }
  call S.somatic_subpipeline as tumor {
    input:
      reads=tumor_inputs,
      sample_name=tumor_name,
      reference=reference,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      cutadapt_adapters=cutadapt_adapters,
      genome_file=genome_file,
      gatk_intervals=gatk_intervals,
      snps_dbsnp=snps_dbsnp,
      snps_dbsnp_tbi=snps_dbsnp_tbi,
      snps_1000gp=snps_1000gp,
      snps_1000gp_tbi=snps_1000gp_tbi,
      known_indels=known_indels,
      known_indels_tbi=known_indels_tbi,
      mills_indels=mills_indels,
      mills_indels_tbi=mills_indels_tbi
  }
  call S.somatic_subpipeline as normal {
    input:
      reads=normal_inputs,
      sample_name=normal_name,
      reference=reference,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      cutadapt_adapters=cutadapt_adapters,
      genome_file=genome_file,
      gatk_intervals=gatk_intervals,
      snps_dbsnp=snps_dbsnp,
      snps_dbsnp_tbi=snps_dbsnp_tbi,
      snps_1000gp=snps_1000gp,
      snps_1000gp_tbi=snps_1000gp_tbi,
      known_indels=known_indels,
      known_indels_tbi=known_indels_tbi,
      mills_indels=mills_indels,
      mills_indels_tbi=mills_indels_tbi
  }
  call G.gridss as vc_gridss {
    input:
      bams=[normal.out, tumor.out],
      bams_bai=[normal.out_bai, tumor.out_bai],
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
  scatter (g in gatk_intervals) {
     call G2.GATK4_SomaticVariantCaller as vc_gatk {
      input:
        normal_bam=normal.bqsr_bam,
        normal_bam_bai=normal.bqsr_bam_bai,
        tumor_bam=tumor.bqsr_bam,
        tumor_bam_bai=tumor.bqsr_bam_bai,
        normal_name=normal_name,
        intervals=g,
        reference=reference,
        reference_fai=reference_fai,
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_dict=reference_dict,
        gnomad=gnomad,
        gnomad_tbi=gnomad_tbi,
        panel_of_normals=panel_of_normals,
        panel_of_normals_tbi=panel_of_normals_tbi
    }
  }
  call G3.Gatk4GatherVcfs as vc_gatk_merge {
    input:
      vcfs=vc_gatk.out
  }
  call B.bgzip as vc_gatk_compressvcf {
    input:
      file=vc_gatk_merge.out
  }
  call B2.bcftoolssort as vc_gatk_sort_combined {
    input:
      vcf=vc_gatk_compressvcf.out
  }
  call U.UncompressArchive as vc_gatk_uncompressvcf {
    input:
      file=vc_gatk_sort_combined.out
  }
  call A.AddBamStatsSomatic as addbamstats {
    input:
      normal_id=normal_name,
      tumor_id=tumor_name,
      normal_bam=normal.out,
      normal_bam_bai=normal.out_bai,
      tumor_bam=tumor.out,
      tumor_bam_bai=tumor.out_bai,
      vcf=vc_gatk_uncompressvcf.out
  }
  output {
    Array[Array[File]] normal_report = normal.reports
    Array[Array[File]] tumor_report = tumor.reports
    File normal_coverage = normal.depth_of_coverage
    File tumor_coverage = tumor.depth_of_coverage
    File normal_summary = normal.summary
    File tumor_summary = tumor.summary
    File gridss_assembly = vc_gridss.assembly
    File variants_gridss = vc_gridss.out
    File normal_bam = normal.out
    File normal_bam_bai = normal.out_bai
    File tumor_bam = tumor.out
    File tumor_bam_bai = tumor.out_bai
    File variants_gatk = vc_gatk_sort_combined.out
    Array[File] variants_split = vc_gatk.out
    File variants_final = addbamstats.out
  }
}