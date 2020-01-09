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
    Array[File] gatkIntervals
    Array[File] vardictIntervals
    File strelkaIntervals
    File strelkaIntervals_tbi
    File vardictHeaderLines
    String? sampleName
    Float? alleleFreqThreshold
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
     call B.BwaAligner as alignSortedBam {
      input:
        sampleName=select_first([sampleName, "NA12878"]),
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
        sortsam_tmpDir=select_first([alignSortedBam_sortsam_tmpDir, "./tmp"])
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
  call C.combinevariants as combineVariants {
    input:
      vcfs=[variantCaller_merge_GATK.out, variantCaller_Strelka.out, variantCaller_merge_Vardict.out],
      type=select_first([combineVariants_type, "germline"]),
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
    File variants_gatk = variantCaller_merge_GATK.out
    File variants_vardict = variantCaller_merge_Vardict.out
    File variants_strelka = variantCaller_Strelka.out
    Array[File] variants_gatk_split = variantCaller_GATK.out
    Array[File] variants_vardict_split = variantCaller_Vardict.out
  }
}