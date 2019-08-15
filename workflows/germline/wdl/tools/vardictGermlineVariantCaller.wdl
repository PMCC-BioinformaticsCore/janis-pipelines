version development

import "vardict_germline.wdl" as V
import "bcftoolsAnnotate.wdl" as B
import "SplitMultiAllele.wdl" as S
import "trimIUPAC.wdl" as T

workflow vardictGermlineVariantCaller {
  input {
    File intervals
    File bam
    File bam_bai
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    String sampleName
    Float allelFreqThreshold
    Boolean? chromNamesAreNumbers
    Boolean? vcfFormat
    Int? chromColumn
    Int? regStartCol
    Int? geneEndCol
    File headerLines
  }
  call V.vardict_germline as vardict {
    input:
      intervals=intervals,
      bam_bai=bam_bai,
      bam=bam,
      reference_fai=reference_fai,
      reference=reference,
      chromNamesAreNumbers=select_first([chromNamesAreNumbers, true]),
      chromColumn=select_first([chromColumn, 1]),
      geneEndCol=select_first([geneEndCol, 3]),
      alleleFreqThreshold=allelFreqThreshold,
      sampleName=sampleName,
      regStartCol=select_first([regStartCol, 2]),
      vcfFormat=select_first([vcfFormat, true]),
      var2vcfSampleName=sampleName,
      var2vcfAlleleFreqThreshold=allelFreqThreshold
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