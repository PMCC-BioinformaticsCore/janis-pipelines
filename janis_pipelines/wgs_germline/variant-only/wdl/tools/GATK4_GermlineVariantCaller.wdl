version development

import "Gatk4SplitReads.wdl" as G
import "Gatk4BaseRecalibrator.wdl" as G2
import "Gatk4ApplyBQSR.wdl" as G3
import "Gatk4HaplotypeCaller.wdl" as G4
import "SplitMultiAllele.wdl" as S

workflow GATK4_GermlineVariantCaller {
  input {
    File bam
    File bam_bai
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
  call G.Gatk4SplitReads as split_bam {
    input:
      bam_bai=bam_bai,
      bam=bam,
      intervals=intervals
  }
  call G2.Gatk4BaseRecalibrator as base_recalibrator {
    input:
      bam_bai=split_bam.out_bai,
      bam=split_bam.out,
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
  call G3.Gatk4ApplyBQSR as apply_bqsr {
    input:
      bam_bai=split_bam.out_bai,
      bam=split_bam.out,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference,
      recalFile=base_recalibrator.out,
      intervals=intervals
  }
  call G4.Gatk4HaplotypeCaller as haplotype_caller {
    input:
      inputRead_bai=apply_bqsr.out_bai,
      inputRead=apply_bqsr.out,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference,
      dbsnp_tbi=snps_dbsnp_tbi,
      dbsnp=snps_dbsnp,
      intervals=intervals
  }
  call S.SplitMultiAllele as split_multi_allele {
    input:
      vcf=haplotype_caller.out,
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