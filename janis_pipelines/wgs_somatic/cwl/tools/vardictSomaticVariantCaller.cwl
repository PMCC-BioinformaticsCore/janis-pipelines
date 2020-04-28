#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: Vardict Somatic Variant Caller
requirements:
  InlineJavascriptRequirement: {}
  StepInputExpressionRequirement: {}
inputs:
  allele_freq_threshold:
    id: allele_freq_threshold
    type: float
    default: 0.05
  header_lines:
    id: header_lines
    type: File
  intervals:
    id: intervals
    type: File
  normal_bam:
    id: normal_bam
    type: File
    secondaryFiles:
    - .bai
  normal_name:
    id: normal_name
    type: string
  reference:
    id: reference
    type: File
    secondaryFiles:
    - .fai
    - .amb
    - .ann
    - .bwt
    - .pac
    - .sa
    - ^.dict
  tumor_bam:
    id: tumor_bam
    type: File
    secondaryFiles:
    - .bai
  tumor_name:
    id: tumor_name
    type: string
  vardict_chromColumn:
    id: vardict_chromColumn
    doc: The column for chromosome
    type: int
    default: 1
  vardict_chromNamesAreNumbers:
    id: vardict_chromNamesAreNumbers
    doc: Indicate the chromosome names are just numbers, such as 1, 2, not chr1, chr2
    type: boolean
    default: true
  vardict_geneEndCol:
    id: vardict_geneEndCol
    doc: The column for region end, e.g. gene end
    type: int
    default: 3
  vardict_regStartCol:
    id: vardict_regStartCol
    doc: The column for region start, e.g. gene start
    type: int
    default: 2
  vardict_vcfFormat:
    id: vardict_vcfFormat
    doc: VCF format output
    type: boolean
    default: true
outputs:
  out:
    id: out
    type: File
    outputSource: trim/out
  vardict_variants:
    id: vardict_variants
    type: File
    outputSource: vardict/out
steps:
  annotate:
    in:
      file:
        id: file
        source: vardict/out
      headerLines:
        id: headerLines
        source: header_lines
    run: bcftoolsAnnotate.cwl
    out:
    - out
  split_multi_allele:
    in:
      reference:
        id: reference
        source: reference
      vcf:
        id: vcf
        source: annotate/out
    run: SplitMultiAllele.cwl
    out:
    - out
  trim:
    in:
      vcf:
        id: vcf
        source: split_multi_allele/out
    run: trimIUPAC.cwl
    out:
    - out
  vardict:
    in:
      alleleFreqThreshold:
        id: alleleFreqThreshold
        source: allele_freq_threshold
      chromColumn:
        id: chromColumn
        source: vardict_chromColumn
      chromNamesAreNumbers:
        id: chromNamesAreNumbers
        source: vardict_chromNamesAreNumbers
      geneEndCol:
        id: geneEndCol
        source: vardict_geneEndCol
      intervals:
        id: intervals
        source: intervals
      normalBam:
        id: normalBam
        source: normal_bam
      normalName:
        id: normalName
        source: normal_name
      reference:
        id: reference
        source: reference
      regStartCol:
        id: regStartCol
        source: vardict_regStartCol
      tumorBam:
        id: tumorBam
        source: tumor_bam
      tumorName:
        id: tumorName
        source: tumor_name
      vcfFormat:
        id: vcfFormat
        source: vardict_vcfFormat
    run: vardict_somatic.cwl
    out:
    - out
id: vardictSomaticVariantCaller
