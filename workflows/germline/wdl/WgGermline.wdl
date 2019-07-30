version development

import "tools/alignsortedbam.wdl" as A
import "tools/fastqc.wdl" as F
import "tools/processbamfiles.wdl" as P
import "tools/GATK4_VariantCaller.wdl" as G
import "tools/Gatk4GatherVcfs.wdl" as G2
import "tools/strelkaGermlineVariantCaller.wdl" as S
import "tools/vardictVariantCaller.wdl" as V
import "tools/combinevariants.wdl" as C
import "tools/bcftoolssort.wdl" as B

workflow WgGermline {
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
    String sampleName
    Array[File] gatkIntervals
    File snps_dbsnp
    File snps_dbsnp_tbi
    File snps_1000gp
    File snps_1000gp_tbi
    File known_indels
    File known_indels_tbi
    File mills_1000gp_indels
    File mills_1000gp_indels_tbi
    File strelkaIntervals
    File strelkaIntervals_tbi
    Array[File] vardictIntervals
    Float allelFreqThreshold
    File vardictHeaderLines
    String? variant_type
    Array[String]? columns
  }
  scatter (f in fastqs) {
     call A.alignsortedbam as alignSortedBam {
      input:
        fastq=f,
        sampleName=sampleName,
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
  scatter (f in fastqs) {
     call F.fastqc as fastqc {
      input:
        reads=f
    }
  }
  call P.processbamfiles as processBamFiles {
    input:
      bams_bai=alignSortedBam.out_bai,
      bams=alignSortedBam.out
  }
  scatter (g in gatkIntervals) {
     call G.GATK4_VariantCaller as variantCaller_GATK {
      input:
        bam_bai=processBamFiles.out_bai,
        bam=processBamFiles.out,
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
        knownIndels_tbi=known_indels_tbi,
        knownIndels=known_indels,
        millsIndels_tbi=mills_1000gp_indels_tbi,
        millsIndels=mills_1000gp_indels
    }
  }
  call G2.Gatk4GatherVcfs as variantCaller_merge_GATK {
    input:
      vcfs=variantCaller_GATK.out
  }
  call S.strelkaGermlineVariantCaller as variantCaller_Strelka {
    input:
      bam_bai=processBamFiles.out_bai,
      bam=processBamFiles.out,
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
  scatter (v in vardictIntervals) {
     call V.vardictVariantCaller as variantCaller_Vardict {
      input:
        intervals=v,
        bam_bai=processBamFiles.out_bai,
        bam=processBamFiles.out,
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_fai=reference_fai,
        reference_dict=reference_dict,
        reference=reference,
        sampleName=sampleName,
        allelFreqThreshold=allelFreqThreshold,
        headerLines=vardictHeaderLines
    }
  }
  call G2.Gatk4GatherVcfs as variantCaller_merge_Vardict {
    input:
      vcfs=variantCaller_Vardict.out
  }
  call C.combinevariants as combineVariants {
    input:
      vcfs=[variantCaller_merge_GATK.out, variantCaller_Strelka.out, variantCaller_merge_Vardict.out],
      type=select_first([variant_type, "germline"]),
      columns=select_first([columns, ["AC", "AN", "AF", "AD", "DP", "GT"]])
  }
  call B.bcftoolssort as sortCombined {
    input:
      vcf=combineVariants.vcf
  }
  output {
    Array[File] variants_gatk_split = variantCaller_GATK.out
    Array[File] variants_vardict_split = variantCaller_Vardict.out
    File variants_strelka = variantCaller_Strelka.out
    File variants_gatk = variantCaller_merge_GATK.out
    File variants_vardict = variantCaller_merge_Vardict.out
    File bam = processBamFiles.out
    File bam_bai = processBamFiles.out_bai
    Array[Array[File]] reports = fastqc.out
    File combinedVariants = sortCombined.out
  }
}