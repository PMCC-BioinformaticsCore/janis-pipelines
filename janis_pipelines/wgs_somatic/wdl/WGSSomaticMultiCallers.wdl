version development

import "tools/somatic_subpipeline.wdl" as S
import "tools/GATK4_SomaticVariantCaller.wdl" as G
import "tools/Gatk4GatherVcfs.wdl" as G2
import "tools/strelkaSomaticVariantCaller.wdl" as S2
import "tools/gridss.wdl" as G3
import "tools/vardictSomaticVariantCaller.wdl" as V
import "tools/combinevariants.wdl" as C
import "tools/bcftoolssort.wdl" as B

workflow WGSSomaticMultiCallers {
  input {
    Array[Array[File]] normal_inputs
    Array[Array[File]] tumor_inputs
    String normal_name
    String tumor_name
    File? cutadapt_adapters
    Array[File] gatk_intervals
    File gridss_blacklist
    Array[File] vardict_intervals
    File strelka_intervals
    File strelka_intervals_tbi
    File vardict_header_lines
    Float? allele_freq_threshold
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
    String? combine_variants_type
    Array[String]? combine_variants_columns
  }
  call S.somatic_subpipeline as normal {
    input:
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference,
      reads=normal_inputs,
      cutadapt_adapters=cutadapt_adapters,
      sample_name=normal_name
  }
  call S.somatic_subpipeline as tumor {
    input:
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference,
      reads=tumor_inputs,
      cutadapt_adapters=cutadapt_adapters,
      sample_name=tumor_name
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
  call S2.strelkaSomaticVariantCaller as vc_strelka {
    input:
      normal_bam_bai=normal.out_bai,
      normal_bam=normal.out,
      tumor_bam_bai=tumor.out_bai,
      tumor_bam=tumor.out,
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
  call G3.gridss as vc_gridss {
    input:
      bams=[normal.out, tumor.out],
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference,
      blacklist=gridss_blacklist
  }
  scatter (v in vardict_intervals) {
     call V.vardictSomaticVariantCaller as vc_vardict {
      input:
        normal_bam_bai=tumor.out_bai,
        normal_bam=tumor.out,
        tumor_bam_bai=normal.out_bai,
        tumor_bam=normal.out,
        normal_name=normal_name,
        tumor_name=tumor_name,
        intervals=v,
        allele_freq_threshold=select_first([allele_freq_threshold, 0.05]),
        header_lines=vardict_header_lines,
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
      type=select_first([combine_variants_type, "somatic"]),
      columns=select_first([combine_variants_columns, ["AD", "DP", "GT"]]),
      normal=normal_name,
      tumor=tumor_name
  }
  call B.bcftoolssort as sortCombined {
    input:
      vcf=combine_variants.vcf
  }
  output {
    Array[Array[File]] normal_report = normal.reports
    Array[Array[File]] tumor_report = tumor.reports
    File normal_bam = normal.out
    File normal_bam_bai = normal.out_bai
    File tumor_bam = tumor.out
    File tumor_bam_bai = tumor.out_bai
    File gridss_assembly = vc_gridss.out
    File variants_gatk = vc_gatk_merge.out
    File variants_strelka = vc_strelka.out
    File variants_vardict = vc_vardict_merge.out
    File variants_gridss = vc_gridss.out
    File variants = combine_variants.vcf
  }
}