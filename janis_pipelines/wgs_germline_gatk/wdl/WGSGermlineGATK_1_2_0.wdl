version development

import "tools/fastqc_v0_11_5.wdl" as F
import "tools/ParseFastqcAdaptors_v0_1_0.wdl" as P
import "tools/BwaAligner_1_0_0.wdl" as B
import "tools/mergeAndMarkBams_4_1_3.wdl" as M
import "tools/GATK4_GermlineVariantCaller_4_1_3_0.wdl" as G
import "tools/Gatk4GatherVcfs_4_0_12_0.wdl" as G2
import "tools/bcftoolssort_v1_9.wdl" as B2

workflow WGSGermlineGATK {
  input {
    String sample_name
    Array[Array[File]] fastqs
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
    File snps_dbsnp
    File snps_dbsnp_tbi
    File snps_1000gp
    File snps_1000gp_tbi
    File known_indels
    File known_indels_tbi
    File mills_indels
    File mills_indels_tbi
    String? align_and_sort_sortsam_tmpDir
  }
  scatter (f in fastqs) {
     call F.fastqc as fastqc {
      input:
        reads=f
    }
  }
  scatter (d in fastqc.datafile) {
     call P.ParseFastqcAdaptors as getfastqc_adapters {
      input:
        fastqc_datafiles=d,
        cutadapt_adaptors_lookup=cutadapt_adapters
    }
  }
  scatter (Q in zip(fastqs, zip(getfastqc_adapters.adaptor_sequences, getfastqc_adapters.adaptor_sequences))) {
     call B.BwaAligner as align_and_sort {
      input:
        sample_name=sample_name,
        reference_fai=reference_fai,
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_dict=reference_dict,
        reference=reference,
        fastq=Q.left,
        cutadapt_adapter=Q.right.right,
        cutadapt_removeMiddle3Adapter=Q.right.right,
        sortsam_tmpDir=select_first([align_and_sort_sortsam_tmpDir, "."])
    }
  }
  call M.mergeAndMarkBams as merge_and_mark {
    input:
      bams_bai=align_and_sort.out_bai,
      bams=align_and_sort.out,
      sampleName=sample_name
  }
  scatter (g in gatk_intervals) {
     call G.GATK4_GermlineVariantCaller as vc_gatk {
      input:
        bam_bai=merge_and_mark.out_bai,
        bam=merge_and_mark.out,
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
  call B2.bcftoolssort as sort_combined {
    input:
      vcf=vc_gatk_merge.out
  }
  output {
    File bam = merge_and_mark.out
    File bam_bai = merge_and_mark.out_bai
    Array[Array[File]] reports = fastqc.out
    File variants = sort_combined.out
    Array[File] variants_split = vc_gatk.out
  }
}