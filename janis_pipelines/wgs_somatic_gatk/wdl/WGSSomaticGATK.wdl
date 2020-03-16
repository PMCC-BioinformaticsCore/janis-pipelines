version development

import "tools/somatic_subpipeline.wdl" as S
import "tools/GATK4_SomaticVariantCaller.wdl" as G
import "tools/Gatk4GatherVcfs.wdl" as G2
import "tools/bcftoolssort.wdl" as B

workflow WGSSomaticGATK {
  input {
    Array[Array[File]] normal_inputs
    Array[Array[File]] tumor_inputs
    String normal_name
    String tumor_name
    File? cutadapt_adapters
    Array[File] gatk_intervals
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    File snps_dbsnp
    File snps_dbsnp_tbi
    File snps_1000gp
    File snps_1000gp_tbi
    File known_indels
    File known_indels_tbi
    File mills_indels
    File mills_indels_tbi
  }
  call S.somatic_subpipeline as normal {
    input:
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      reads=tumor_inputs,
      cutadapt_adapters=cutadapt_adapters,
      sample_name=tumor_name
  }
  call S.somatic_subpipeline as tumor {
    input:
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      reads=normal_inputs,
      cutadapt_adapters=cutadapt_adapters,
      sample_name=normal_name
  }
  scatter (g in gatk_intervals) {
     call G.GATK4_SomaticVariantCaller as vc_gatk {
      input:
        normal_bam_bai=tumor.out_bai,
        normal_bam=tumor.out,
        tumor_bam_bai=normal.out_bai,
        tumor_bam=normal.out,
        normal_name=normal_name,
        tumor_name=tumor_name,
        intervals=g,
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_fai=reference_fai,
        reference_dict=reference_dict,
        reference=reference,
        snps_dbsnp_tbi=snps_dbsnp_tbi,
        snps_dbsnp=snps_dbsnp,
        snps_1000gp_tbi=snps_1000gp_tbi,
        snps_1000gp=snps_1000gp,
        known_indels_tbi=known_indels_tbi,
        known_indels=known_indels,
        mills_indels_tbi=mills_indels_tbi,
        mills_indels=mills_indels
    }
  }
  call G2.Gatk4GatherVcfs as vc_gatk_merge {
    input:
      vcfs=vc_gatk.out
  }
  call B.bcftoolssort as sorted {
    input:
      vcf=vc_gatk_merge.out
  }
  output {
    File normal_bam = normal.out
    File normal_bam_bai = normal.out_bai
    File tumor_bam = tumor.out
    File tumor_bam_bai = tumor.out_bai
    Array[Array[File]] normal_report = normal.reports
    Array[Array[File]] tumor_report = tumor.reports
    File variants_gatk = sorted.out
  }
}