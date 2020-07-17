version development

import "vardict_germline_1_6_0.wdl" as V
import "bcftoolsAnnotate_v1_5.wdl" as B
import "bgzip_1_2_1.wdl" as B2
import "tabix_1_2_1.wdl" as T
import "SplitMultiAllele_v0_5772.wdl" as S
import "trimIUPAC_0_0_5.wdl" as T2
import "VcfTools_0_1_16.wdl" as V2

workflow vardictGermlineVariantCaller {
  input {
    File bam
    File bam_bai
    File intervals
    String sample_name
    Float? allele_freq_threshold = 0.5
    File header_lines
    File reference
    File reference_fai
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_dict
    Boolean? vardict_chromNamesAreNumbers = true
    Boolean? vardict_vcfFormat = true
    Int? vardict_chromColumn = 1
    Int? vardict_regStartCol = 2
    Int? vardict_geneEndCol = 3
    Boolean? compressvcf_stdout = true
    Boolean? filterpass_removeFileteredAll = true
    Boolean? filterpass_recode = true
    Boolean? filterpass_recodeINFOAll = true
  }
  call V.vardict_germline as vardict {
    input:
      intervals=intervals,
      bam=bam,
      bam_bai=bam_bai,
      reference=reference,
      reference_fai=reference_fai,
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
      vcf=vardict.out,
      headerLines=header_lines
  }
  call B2.bgzip as compressvcf {
    input:
      file=annotate.out,
      stdout=select_first([compressvcf_stdout, true])
  }
  call T.tabix as tabixvcf {
    input:
      inp=compressvcf.out
  }
  call S.SplitMultiAllele as splitnormalisevcf {
    input:
      vcf=annotate.out,
      reference=reference,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict
  }
  call T2.trimIUPAC as trim {
    input:
      vcf=splitnormalisevcf.out
  }
  call V2.VcfTools as filterpass {
    input:
      vcf=trim.out,
      removeFileteredAll=select_first([filterpass_removeFileteredAll, true]),
      recode=select_first([filterpass_recode, true]),
      recodeINFOAll=select_first([filterpass_recodeINFOAll, true])
  }
  output {
    File variants = tabixvcf.out
    File variants_tbi = tabixvcf.out_tbi
    File out = filterpass.out
  }
}