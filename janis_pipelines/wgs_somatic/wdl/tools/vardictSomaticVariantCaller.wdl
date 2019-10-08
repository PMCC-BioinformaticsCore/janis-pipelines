version development

import "vardict_somatic.wdl" as V
import "bcftoolsAnnotate.wdl" as B
import "SplitMultiAllele.wdl" as S
import "trimIUPAC.wdl" as T

workflow vardictSomaticVariantCaller {
  input {
    File normalBam
    File normalBam_bai
    File tumorBam
    File tumorBam_bai
    String normalName
    String tumorName
    File intervals
    Float? alleleFreqThreshold
    File headerLines
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    Boolean? vardict_chromNamesAreNumbers
    Boolean? vardict_vcfFormat
    Int? vardict_chromColumn
    Int? vardict_regStartCol
    Int? vardict_geneEndCol
  }
  call V.vardict_somatic as vardict {
    input:
      tumorBam_bai=tumorBam_bai,
      tumorBam=tumorBam,
      normalBam_bai=normalBam_bai,
      normalBam=normalBam,
      intervals=intervals,
      reference_fai=reference_fai,
      reference=reference,
      tumorName=tumorName,
      normalName=normalName,
      alleleFreqThreshold=select_first([alleleFreqThreshold, 0.05]),
      chromNamesAreNumbers=select_first([vardict_chromNamesAreNumbers, true]),
      chromColumn=select_first([vardict_chromColumn, 1]),
      geneEndCol=select_first([vardict_geneEndCol, 3]),
      regStartCol=select_first([vardict_regStartCol, 2]),
      vcfFormat=select_first([vardict_vcfFormat, true])
  }
  call B.bcftoolsAnnotate as annotate {
    input:
      file=vardict.out,
      headerLines=headerLines
  }
  call S.SplitMultiAllele as split {
    input:
      vcf=annotate.out,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference
  }
  call T.trimIUPAC as trim {
    input:
      vcf=split.out
  }
  output {
    File vardictVariants = vardict.out
    File out = trim.out
  }
}