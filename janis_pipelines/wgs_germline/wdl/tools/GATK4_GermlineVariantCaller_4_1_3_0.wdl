version development

import "Gatk4SplitReads_4_1_3_0.wdl" as G
import "Gatk4HaplotypeCaller_4_1_3_0.wdl" as G2
import "UncompressArchive_v1_0_0.wdl" as U
import "SplitMultiAllele_v0_5772.wdl" as S

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
    String? haplotype_caller_pairHmmImplementation = "LOGLESS_CACHING"
  }
  call G.Gatk4SplitReads as split_bam {
    input:
      bam=bam,
      bam_bai=bam_bai,
      intervals=intervals
  }
  call G2.Gatk4HaplotypeCaller as haplotype_caller {
    input:
      pairHmmImplementation=select_first([haplotype_caller_pairHmmImplementation, "LOGLESS_CACHING"]),
      inputRead=split_bam.out,
      inputRead_bai=split_bam.out_bai,
      reference=reference,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      dbsnp=snps_dbsnp,
      dbsnp_tbi=snps_dbsnp_tbi,
      intervals=intervals
  }
  call U.UncompressArchive as uncompressvcf {
    input:
      file=haplotype_caller.out
  }
  call S.SplitMultiAllele as splitnormalisevcf {
    input:
      vcf=uncompressvcf.out,
      reference=reference,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict
  }
  output {
    File variants = haplotype_caller.out
    File variants_tbi = haplotype_caller.out_tbi
    File out_bam = haplotype_caller.bam
    File out_bam_bai = haplotype_caller.bam_bai
    File out = splitnormalisevcf.out
  }
}