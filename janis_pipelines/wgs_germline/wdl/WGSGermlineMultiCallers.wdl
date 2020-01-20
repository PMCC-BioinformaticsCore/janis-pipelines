version development

import "tools/fastqc.wdl" as F
import "tools/ParseFastqcAdaptors.wdl" as P
import "tools/BwaAligner.wdl" as B
import "tools/mergeAndMarkBams.wdl" as M
import "tools/GATK4_GermlineVariantCaller.wdl" as G
import "tools/Gatk4GatherVcfs.wdl" as G2
import "tools/strelkaGermlineVariantCaller.wdl" as S
import "tools/vardictGermlineVariantCaller.wdl" as V
import "tools/combinevariants.wdl" as C
import "tools/bcftoolssort.wdl" as B2

workflow WGSGermlineMultiCallers {
  input {
    Array[Array[File]] fastqs
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    File cutadapt_adapters
    Array[File] gatk_intervals
    Array[File] vardict_intervals
    File strelkaIntervals
    File strelkaIntervals_tbi
    File header_lines
    String? sample_name
    Float? allele_freq_threshold
    File snps_dbsnp
    File snps_dbsnp_tbi
    File snps_1000gp
    File snps_1000gp_tbi
    File known_indels
    File known_indels_tbi
    File mills_indels
    File mills_indels_tbi
    String? align_and_sort_sortsam_tmpDir
    String? combine_variants_type
    Array[String]? combine_variants_columns
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
        sample_name=select_first([sample_name, "NA12878"]),
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_fai=reference_fai,
        reference_dict=reference_dict,
        reference=reference,
        fastq=Q.left,
        cutadapt_adapter=Q.right.right,
        cutadapt_removeMiddle3Adapter=Q.right.right,
        sortsam_tmpDir=select_first([align_and_sort_sortsam_tmpDir, "./tmp"])
    }
  }
  call M.mergeAndMarkBams as merge_and_mark {
    input:
      bams_bai=align_and_sort.out_bai,
      bams=align_and_sort.out
  }
  scatter (g in gatk_intervals) {
     call G.GATK4_GermlineVariantCaller as vc_gatk {
      input:
        bam_bai=merge_and_mark.out_bai,
        bam=merge_and_mark.out,
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
  call S.strelkaGermlineVariantCaller as vc_strelka {
    input:
      bam_bai=merge_and_mark.out_bai,
      bam=merge_and_mark.out,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      intervals_tbi=strelkaIntervals_tbi,
      intervals=strelkaIntervals
  }
  scatter (v in vardict_intervals) {
     call V.vardictGermlineVariantCaller as vc_vardict {
      input:
        bam_bai=merge_and_mark.out_bai,
        bam=merge_and_mark.out,
        intervals=v,
        sample_name=select_first([sample_name, "NA12878"]),
        allele_freq_threshold=select_first([allele_freq_threshold, 0.05]),
        header_lines=header_lines,
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_fai=reference_fai,
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
  call B2.bcftoolssort as sort_combined {
    input:
      vcf=combine_variants.vcf
  }
  output {
    Array[Array[File]] reports = fastqc.out
    File bam = merge_and_mark.out
    File bam_bai = merge_and_mark.out_bai
    File variants_combined = sort_combined.out
    File variants_gatk = vc_gatk_merge.out
    File variants_vardict = vc_vardict_merge.out
    File variants_strelka = vc_strelka.out
    Array[File] variants_gatk_split = vc_gatk.out
    Array[File] variants_vardict_split = vc_vardict.out
  }
}