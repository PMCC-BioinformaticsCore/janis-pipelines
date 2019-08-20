version development

import "tools/alignsortedbam.wdl" as A
import "tools/fastqc.wdl" as F
import "tools/mergeAndMarkBams.wdl" as M
import "tools/GATK4_GermlineVariantCaller.wdl" as G
import "tools/Gatk4GatherVcfs.wdl" as G2
import "tools/bcftoolssort.wdl" as B

workflow WGSGermlineGATK {
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
  call M.mergeAndMarkBams as processBamFiles {
    input:
      bams_bai=alignSortedBam.out_bai,
      bams=[alignSortedBam.out]
  }
  scatter (g in gatkIntervals) {
     call G.GATK4_GermlineVariantCaller as variantCaller_GATK {
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
      vcfs=[variantCaller_GATK.out]
  }
  call B.bcftoolssort as sortCombined {
    input:
      vcf=variantCaller_merge_GATK.out
  }
  output {
    File bam = processBamFiles.out
    File bam_bai = processBamFiles.out_bai
    Array[Array[File]] reports = fastqc.out
    File variants = sortCombined.out
    Array[File] scattered_variants = variantCaller_GATK.out
  }
}