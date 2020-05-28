version development

import "vardict_germline_1_6_0.wdl" as V
import "bcftoolsAnnotate_v1_5.wdl" as B
import "SplitMultiAllele_v0_5772.wdl" as S
import "trimIUPAC_0_0_5.wdl" as T

workflow vardictGermlineVariantCaller {
  input {
    File bam
    File bam_bai
    File intervals
    String sample_name
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
  call V.vardict_germline as vardict {
    input:
      intervals=intervals,
      bam_bai=bam_bai,
      bam=bam,
      reference_fai=reference_fai,
      reference=reference,
      chromNamesAreNumbers=select_first([vardict_chromNamesAreNumbers, true]),
      chromColumn=select_first([vardict_chromColumn, 1]),
      geneEndCol=select_first([vardict_geneEndCol, 3]),
      alleleFreqThreshold=select_first([allele_freq_threshold, 0.5]),
      sampleName=sample_name,
      regStartCol=select_first([vardict_regStartCol, 2]),
      vcfFormat=select_first([vardict_vcfFormat, true]),
      var2vcfSampleName=sample_name,
      var2vcfAlleleFreqThreshold=select_first([allele_freq_threshold, 0.5])
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