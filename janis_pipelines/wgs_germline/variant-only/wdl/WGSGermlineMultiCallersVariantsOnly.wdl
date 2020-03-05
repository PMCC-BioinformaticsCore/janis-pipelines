version development

import "tools/GATK4_GermlineVariantCaller.wdl" as G
import "tools/Gatk4GatherVcfs.wdl" as G2
import "tools/strelkaGermlineVariantCaller.wdl" as S
import "tools/vardictGermlineVariantCaller.wdl" as V
import "tools/combinevariants.wdl" as C
import "tools/bcftoolssort.wdl" as B

workflow WGSGermlineMultiCallersVariantsOnly {
  input {
    String sample_name
    File bam
    File bam_bai
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
    Array[File] vardict_intervals
    File strelka_intervals
    File strelka_intervals_tbi
    File? header_lines
    Float? allele_freq_threshold
    File snps_dbsnp
    File snps_dbsnp_tbi
    File snps_1000gp
    File snps_1000gp_tbi
    File known_indels
    File known_indels_tbi
    File mills_indels
    File mills_indels_tbi
    String? combine_variants_type
    Array[String]? combine_variants_columns
  }
  scatter (g in gatk_intervals) {
     call G.GATK4_GermlineVariantCaller as vc_gatk {
      input:
        bam_bai=bam_bai,
        bam=bam,
        intervals=g,
        reference_fai=reference_fai,
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
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
  call S.strelkaGermlineVariantCaller as vc_strelka {
    input:
      bam_bai=bam_bai,
      bam=bam,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference,
      intervals_tbi=strelka_intervals_tbi,
      intervals=strelka_intervals
  }
  scatter (v in vardict_intervals) {
     call V.vardictGermlineVariantCaller as vc_vardict {
      input:
        bam_bai=bam_bai,
        bam=bam,
        intervals=v,
        sample_name=sample_name,
        allele_freq_threshold=select_first([allele_freq_threshold, 0.05]),
        header_lines=header_lines,
        reference_fai=reference_fai,
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_dict=reference_dict,
        reference=reference
    }
  }
  call G2.Gatk4GatherVcfs as vc_vardict_merge {
    input:
      vcfs=vc_vardict.out
  }
  call C.combinevariants as combine_variants {
    input:
      vcfs=[vc_gatk_merge.out, vc_strelka.out, vc_vardict_merge.out],
      type=select_first([combine_variants_type, "germline"]),
      columns=select_first([combine_variants_columns, ["AC", "AN", "AF", "AD", "DP", "GT"]])
  }
  call B.bcftoolssort as sort_combined {
    input:
      vcf=combine_variants.vcf
  }
  output {
    File variants_combined = sort_combined.out
    File variants_gatk = vc_gatk_merge.out
    File variants_vardict = vc_vardict_merge.out
    File variants_strelka = vc_strelka.out
    Array[File] variants_gatk_split = vc_gatk.out
    Array[File] variants_vardict_split = vc_vardict.out
  }
}