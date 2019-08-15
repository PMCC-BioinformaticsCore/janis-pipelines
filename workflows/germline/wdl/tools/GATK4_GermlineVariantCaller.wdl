version development

import "Gatk4BaseRecalibrator.wdl" as G
import "GATK4ApplyBQSR.wdl" as G2
import "GatkHaplotypeCaller.wdl" as G3
import "SplitMultiAllele.wdl" as S

workflow GATK4_GermlineVariantCaller {
  input {
    File bam
    File bam_bai
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
  call G.Gatk4BaseRecalibrator as baseRecalibrator {
    input:
      bam_bai=bam_bai,
      bam=bam,
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
  call G2.GATK4ApplyBQSR as applyBQSR {
    input:
      bam_bai=bam_bai,
      bam=bam,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      recalFile=baseRecalibrator.out,
      intervals=intervals
  }
  call G3.GatkHaplotypeCaller as haplotypeCaller {
    input:
      inputRead_bai=applyBQSR.out_bai,
      inputRead=applyBQSR.out,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      dbsnp_tbi=snps_dbsnp_tbi,
      dbsnp=snps_dbsnp,
      intervals=intervals
  }
  call S.SplitMultiAllele as splitMultiAllele {
    input:
      vcf=haplotypeCaller.out,
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