version development

import "Gatk4BaseRecalibrator.wdl" as G
import "GATK4ApplyBQSR.wdl" as G2
import "gatkmutect2.wdl" as G3
import "SplitMultiAllele.wdl" as S

workflow GATK4_SomaticVariantCaller {
  input {
    File normalBam
    File normalBam_bai
    File tumorBam
    File tumorBam_bai
    String normalName
    String tumorName
    File? intervals
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
    File knownIndels
    File knownIndels_tbi
    File millsIndels
    File millsIndels_tbi
  }
  call G.Gatk4BaseRecalibrator as baseRecalibrator_normal {
    input:
      bam_bai=normalBam_bai,
      bam=normalBam,
      knownSites=[snps_dbsnp, snps_1000gp, knownIndels, millsIndels],
      knownSites_tbi=[snps_dbsnp_tbi, snps_1000gp_tbi, knownIndels_tbi, millsIndels_tbi],
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      intervals=intervals
  }
  call G.Gatk4BaseRecalibrator as baseRecalibrator_tumor {
    input:
      bam_bai=tumorBam_bai,
      bam=tumorBam,
      knownSites=[snps_dbsnp, snps_1000gp, knownIndels, millsIndels],
      knownSites_tbi=[snps_dbsnp_tbi, snps_1000gp_tbi, knownIndels_tbi, millsIndels_tbi],
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      intervals=intervals
  }
  call G2.GATK4ApplyBQSR as applyBQSR_normal {
    input:
      bam_bai=normalBam_bai,
      bam=normalBam,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      recalFile=baseRecalibrator_normal.out,
      intervals=intervals
  }
  call G2.GATK4ApplyBQSR as applyBQSR_tumor {
    input:
      bam_bai=tumorBam_bai,
      bam=tumorBam,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      recalFile=baseRecalibrator_tumor.out,
      intervals=intervals
  }
  call G3.gatkmutect2 as mutect2 {
    input:
      tumor_bai=applyBQSR_tumor.out_bai,
      tumor=applyBQSR_tumor.out,
      tumorName=tumorName,
      normal_bai=applyBQSR_normal.out_bai,
      normal=applyBQSR_normal.out,
      normalName=normalName,
      intervals=intervals,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference
  }
  call S.SplitMultiAllele as splitMultiAllele {
    input:
      vcf=mutect2.out,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference
  }
  output {
    File out = splitMultiAllele.out
  }
}