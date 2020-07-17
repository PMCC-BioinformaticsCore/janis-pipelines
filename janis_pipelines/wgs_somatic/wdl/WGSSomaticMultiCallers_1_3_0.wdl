version development

import "tools/somatic_subpipeline.wdl" as S
import "tools/gridss_v2_6_2.wdl" as G
import "tools/GATK4_SomaticVariantCaller_4_1_3_0.wdl" as G2
import "tools/Gatk4GatherVcfs_4_1_3_0.wdl" as G3
import "tools/bgzip_1_2_1.wdl" as B
import "tools/bcftoolssort_v1_9.wdl" as B2
import "tools/UncompressArchive_v1_0_0.wdl" as U
import "tools/strelkaSomaticVariantCaller_v0_1_1.wdl" as S2
import "tools/GenerateVardictHeaderLines_v0_1_0.wdl" as G4
import "tools/vardictSomaticVariantCaller_v0_1_0.wdl" as V
import "tools/combinevariants_0_0_8.wdl" as C
import "tools/AddBamStatsSomatic_v0_1_0.wdl" as A

workflow WGSSomaticMultiCallers {
  input {
    Array[Array[File]] normal_inputs
    Array[Array[File]] tumor_inputs
    String normal_name
    String tumor_name
    File? cutadapt_adapters
    Array[File] gatk_intervals
    File genome_file
    File gridss_blacklist
    Array[File] vardict_intervals
    File strelka_intervals
    File strelka_intervals_tbi
    Float? allele_freq_threshold = 0.05
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
    String? combine_variants_type = "somatic"
    Array[String]? combine_variants_columns = ["AD", "DP", "GT"]
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
      genome_file=genome_file,
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
      genome_file=genome_file,
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
  call S2.strelkaSomaticVariantCaller as vc_strelka {
    input:
      normal_bam=normal.out,
      normal_bam_bai=normal.out_bai,
      tumor_bam=tumor.out,
      tumor_bam_bai=tumor.out_bai,
      reference=reference,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      intervals=strelka_intervals,
      intervals_tbi=strelka_intervals_tbi
  }
  call G4.GenerateVardictHeaderLines as generate_vardict_headerlines {
    input:
      reference=reference,
      reference_dict=reference_dict
  }
  scatter (v in vardict_intervals) {
     call V.vardictSomaticVariantCaller as vc_vardict {
      input:
        normal_bam=normal.out,
        normal_bam_bai=normal.out_bai,
        tumor_bam=tumor.out,
        tumor_bam_bai=tumor.out_bai,
        normal_name=normal_name,
        tumor_name=tumor_name,
        intervals=v,
        allele_freq_threshold=select_first([allele_freq_threshold, 0.05]),
        header_lines=generate_vardict_headerlines.out,
        reference=reference,
        reference_fai=reference_fai,
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_dict=reference_dict
    }
  }
  call G3.Gatk4GatherVcfs as vc_vardict_merge {
    input:
      vcfs=vc_vardict.out
  }
  call B.bgzip as vc_vardict_compressvcf {
    input:
      file=vc_vardict_merge.out
  }
  call B2.bcftoolssort as vc_vardict_sort_combined {
    input:
      vcf=vc_vardict_compressvcf.out
  }
  call U.UncompressArchive as vc_vardict_uncompressvcf {
    input:
      file=vc_vardict_sort_combined.out
  }
  call C.combinevariants as combine_variants {
    input:
      vcfs=[vc_gatk_uncompressvcf.out, vc_strelka.out, vc_vardict_uncompressvcf.out],
      type=select_first([combine_variants_type, "somatic"]),
      columns=select_first([combine_variants_columns, ["AD", "DP", "GT"]]),
      normal=normal_name,
      tumor=tumor_name
  }
  call B.bgzip as combined_compress {
    input:
      file=combine_variants.out
  }
  call B2.bcftoolssort as combined_sort {
    input:
      vcf=combined_compress.out
  }
  call U.UncompressArchive as combined_uncompress {
    input:
      file=combined_sort.out
  }
  call A.AddBamStatsSomatic as addbamstats {
    input:
      normal_id=normal_name,
      tumor_id=tumor_name,
      normal_bam=normal.out,
      normal_bam_bai=normal.out_bai,
      tumor_bam=tumor.out,
      tumor_bam_bai=tumor.out_bai,
      vcf=combined_uncompress.out
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
    File variants_vardict = vc_vardict_sort_combined.out
    File variants_strelka = vc_strelka.out
    Array[File] variants_gatk_split = vc_gatk.out
    Array[File] variants_vardict_split = vc_vardict.out
  }
}