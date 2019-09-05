version development

import "tools/BwaAligner.wdl" as B
import "tools/fastqc.wdl" as F
import "tools/mergeAndMarkBams.wdl" as M
import "tools/GATK4_GermlineVariantCaller.wdl" as G
import "tools/Gatk4GatherVcfs.wdl" as G2
import "tools/strelkaGermlineVariantCaller.wdl" as S
import "tools/vardictGermlineVariantCaller.wdl" as V
import "tools/gridssGermlineVariantCaller.wdl" as G3
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
    Array[File] gatkIntervals
    Array[File] vardictIntervals
    File strelkaIntervals
    File strelkaIntervals_tbi
    File vardictHeaderLines
    String? sampleName
    Float? alleleFreqThreshold
    File gridssBlacklist
    File snps_dbsnp
    File snps_dbsnp_tbi
    File snps_1000gp
    File snps_1000gp_tbi
    File known_indels
    File known_indels_tbi
    File mills_indels
    File mills_indels_tbi
    String? alignSortedBam_sortsam_tmpDir
    String? combineVariants_type
    Array[String]? combineVariants_columns
  }
  scatter (f in fastqs) {
     call B.BwaAligner as alignSortedBam {
      input:
        name=select_first([sampleName, "NA12878"]),
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_fai=reference_fai,
        reference_dict=reference_dict,
        reference=reference,
        fastq=f,
        sortsam_tmpDir=select_first([alignSortedBam_sortsam_tmpDir, "./tmp"])
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
      bams=alignSortedBam.out
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
        millsIndels_tbi=mills_indels_tbi,
        millsIndels=mills_indels
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
     call V.vardictGermlineVariantCaller as variantCaller_Vardict {
      input:
        bam_bai=processBamFiles.out_bai,
        bam=processBamFiles.out,
        intervals=v,
        sampleName=select_first([sampleName, "NA12878"]),
        alleleFreqThreshold=select_first([alleleFreqThreshold, 0.05]),
        headerLines=vardictHeaderLines,
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
  call G2.Gatk4GatherVcfs as variantCaller_merge_Vardict {
    input:
      vcfs=variantCaller_Vardict.out
  }
  call G3.gridssGermlineVariantCaller as variantCaller_GRIDSS {
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
      blacklist=gridssBlacklist
  }
  call C.combinevariants as combineVariants {
    input:
      vcfs=[variantCaller_merge_GATK.out, variantCaller_Strelka.out, variantCaller_merge_Vardict.out, variantCaller_GRIDSS.out],
      type=select_first([combineVariants_type, "Germline"]),
      columns=select_first([combineVariants_columns, ["AC", "AN", "AF", "AD", "DP", "GT"]])
  }
  call B2.bcftoolssort as sortCombined {
    input:
      vcf=combineVariants.vcf
  }
  output {
    File bam = processBamFiles.out
    File bam_bai = processBamFiles.out_bai
    Array[Array[File]] reports = fastqc.out
    File combinedVariants = sortCombined.out
    Array[File] variants_gatk_split = variantCaller_GATK.out
    File variants_vardict_split = variantCaller_merge_Vardict.out
    File variants_strelka = variantCaller_Strelka.out
    File variants_gatk = variantCaller_merge_GATK.out
    Array[File] variants_vardict = variantCaller_Vardict.out
    File variants_gridss = variantCaller_GRIDSS.out
  }
}