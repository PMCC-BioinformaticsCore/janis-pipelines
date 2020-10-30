version development

import "tools/somatic_subpipeline.wdl" as S
import "tools/gridss_v2_6_2.wdl" as G
import "tools/GATKBaseRecalBQSRWorkflow_4_1_3.wdl" as G2
import "tools/GATK4_SomaticVariantCaller_4_1_3_0.wdl" as G3
import "tools/Gatk4GatherVcfs_4_1_3_0.wdl" as G4
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
    Array[File] gatk_intervals
    File gridss_blacklist
    File gnomad
    File gnomad_tbi
    File? panel_of_normals
    File? panel_of_normals_tbi
    File cutadapt_adapters
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
      bams=[normal.out_bam, tumor.out_bam],
      bams_bai=[normal.out_bam_bai, tumor.out_bam_bai],
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
     call G2.GATKBaseRecalBQSRWorkflow as bqsr_normal {
      input:
        bam=normal.out_bam,
        bam_bai=normal.out_bam_bai,
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
        snps_dbsnp_tbi=snps_dbsnp_tbi,
        snps_1000gp=snps_1000gp,
        snps_1000gp_tbi=snps_1000gp_tbi,
        known_indels=known_indels,
        known_indels_tbi=known_indels_tbi,
        mills_indels=mills_indels,
        mills_indels_tbi=mills_indels_tbi
    }
  }
  scatter (g in gatk_intervals) {
     call G2.GATKBaseRecalBQSRWorkflow as bqsr_tumor {
      input:
        bam=tumor.out_bam,
        bam_bai=tumor.out_bam_bai,
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
        snps_dbsnp_tbi=snps_dbsnp_tbi,
        snps_1000gp=snps_1000gp,
        snps_1000gp_tbi=snps_1000gp_tbi,
        known_indels=known_indels,
        known_indels_tbi=known_indels_tbi,
        mills_indels=mills_indels,
        mills_indels_tbi=mills_indels_tbi
    }
  }
  scatter (Q in zip(gatk_intervals, zip(transpose([bqsr_normal.out, bqsr_normal.out_bai]), transpose([bqsr_tumor.out, bqsr_tumor.out_bai])))) {
     call G3.GATK4_SomaticVariantCaller as vc_gatk {
      input:
        normal_bam=Q.right.left[0],
        normal_bam_bai=Q.right.left[1],
        tumor_bam=Q.right.right[0],
        tumor_bam_bai=Q.right.right[1],
        normal_name=normal_name,
        intervals=Q.left,
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
  call G4.Gatk4GatherVcfs as vc_gatk_merge {
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
      normal_bam=normal.out_bam,
      normal_bam_bai=normal.out_bam_bai,
      tumor_bam=tumor.out_bam,
      tumor_bam_bai=tumor.out_bam_bai,
      reference=reference,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      vcf=vc_gatk_uncompressvcf.out
  }
  output {
    Array[Array[File]] out_normal_fastqc_reports = normal.out_fastqc_reports
    Array[Array[File]] out_tumor_fastqc_reports = tumor.out_fastqc_reports
    File out_normal_performance_summary = normal.out_performance_summary
    File out_tumor_performance_summary = tumor.out_performance_summary
    File out_normal_bam = normal.out_bam
    File out_normal_bam_bai = normal.out_bam_bai
    File out_tumor_bam = tumor.out_bam
    File out_tumor_bam_bai = tumor.out_bam_bai
    File out_gridss_assembly = vc_gridss.assembly
    File out_variants_gridss = vc_gridss.out
    File out_variants_gatk = vc_gatk_sort_combined.out
    Array[File] out_variants_split = vc_gatk.out
    File out_variants = addbamstats.out
  }
}