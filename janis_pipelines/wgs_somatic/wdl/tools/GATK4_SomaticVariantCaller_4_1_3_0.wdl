version development

import "Gatk4BaseRecalibrator_4_1_3_0.wdl" as G
import "Gatk4ApplyBQSR_4_1_3_0.wdl" as G2
import "Gatk4Mutect2_4_1_3_0.wdl" as G3
import "SplitMultiAllele_v0_5772.wdl" as S

workflow GATK4_SomaticVariantCaller {
  input {
    File normal_bam
    File normal_bam_bai
    File tumor_bam
    File tumor_bam_bai
    String normal_name
    String tumor_name
    File? intervals
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
  }
  call G.Gatk4BaseRecalibrator as base_recalibrator_normal {
    input:
      bam_bai=normal_bam_bai,
      bam=normal_bam,
      knownSites=[snps_dbsnp, snps_1000gp, known_indels, mills_indels],
      knownSites_tbi=[snps_dbsnp_tbi, snps_1000gp_tbi, known_indels_tbi, mills_indels_tbi],
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference,
      intervals=intervals
  }
  call G.Gatk4BaseRecalibrator as base_recalibrator_tumor {
    input:
      bam_bai=tumor_bam_bai,
      bam=tumor_bam,
      knownSites=[snps_dbsnp, snps_1000gp, known_indels, mills_indels],
      knownSites_tbi=[snps_dbsnp_tbi, snps_1000gp_tbi, known_indels_tbi, mills_indels_tbi],
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference,
      intervals=intervals
  }
  call G2.Gatk4ApplyBQSR as apply_bqsr_normal {
    input:
      bam_bai=normal_bam_bai,
      bam=normal_bam,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference,
      recalFile=base_recalibrator_normal.out,
      intervals=intervals
  }
  call G2.Gatk4ApplyBQSR as apply_bqsr_tumor {
    input:
      bam_bai=tumor_bam_bai,
      bam=tumor_bam,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference,
      recalFile=base_recalibrator_tumor.out,
      intervals=intervals
  }
  call G3.Gatk4Mutect2 as mutect2 {
    input:
      tumorBams_bai=[apply_bqsr_tumor.out_bai],
      tumorBams=[apply_bqsr_tumor.out],
      normalBams_bai=[apply_bqsr_normal.out_bai],
      normalBams=[apply_bqsr_normal.out],
      normalSample=normal_name,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference,
      intervals=intervals
  }
  call S.SplitMultiAllele as split_multi_allele {
    input:
      vcf=mutect2.out,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference
  }
  output {
    File out = split_multi_allele.out
  }
}