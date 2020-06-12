version development

import "vardict_somatic_1_6_0.wdl" as V
import "bcftoolsAnnotate_v1_5.wdl" as B
import "SplitMultiAllele_v0_5772.wdl" as S
import "trimIUPAC_0_0_5.wdl" as T

workflow vardictSomaticVariantCaller {
  input {
    File normal_bam
    File normal_bam_bai
    File tumor_bam
    File tumor_bam_bai
    String normal_name
    String tumor_name
    File intervals
    Float? allele_freq_threshold
    File header_lines
    File reference
    File reference_fai
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_dict
    Boolean? vardict_chromNamesAreNumbers
    Boolean? vardict_vcfFormat
    Int? vardict_chromColumn
    Int? vardict_regStartCol
    Int? vardict_geneEndCol
  }
  call V.vardict_somatic as vardict {
    input:
      tumorBam_bai=tumor_bam_bai,
      tumorBam=tumor_bam,
      normalBam_bai=normal_bam_bai,
      normalBam=normal_bam,
      intervals=intervals,
      reference_fai=reference_fai,
      reference=reference,
      tumorName=tumor_name,
      normalName=normal_name,
      alleleFreqThreshold=select_first([allele_freq_threshold, 0.05]),
      chromNamesAreNumbers=select_first([vardict_chromNamesAreNumbers, true]),
      chromColumn=select_first([vardict_chromColumn, 1]),
      geneEndCol=select_first([vardict_geneEndCol, 3]),
      regStartCol=select_first([vardict_regStartCol, 2]),
      vcfFormat=select_first([vardict_vcfFormat, true])
  }
  call B.bcftoolsAnnotate as annotate {
    input:
      file=vardict.out,
      headerLines=header_lines
  }
  call S.SplitMultiAllele as split_multi_allele {
    input:
      vcf=annotate.out,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference
  }
  call T.trimIUPAC as trim {
    input:
      vcf=split_multi_allele.out
  }
  output {
    File vardict_variants = vardict.out
    File out = trim.out
  }
}