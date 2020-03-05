#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
id: vardictGermlineVariantCaller
inputs:
  allele_freq_threshold:
    default: 0.05
    id: allele_freq_threshold
    type: float
  bam:
    id: bam
    secondaryFiles:
    - .bai
    type: File
  header_lines:
    id: header_lines
    type:
    - File
    - 'null'
  intervals:
    id: intervals
    type: File
  reference:
    id: reference
    secondaryFiles:
    - .fai
    - .amb
    - .ann
    - .bwt
    - .pac
    - .sa
    - ^.dict
    type: File
  sample_name:
    id: sample_name
    type: string
  vardict_chromColumn:
    default: 1
    doc: The column for chromosome
    id: vardict_chromColumn
    type: int
  vardict_chromNamesAreNumbers:
    default: true
    doc: Indicate the chromosome names are just numbers, such as 1, 2, not chr1, chr2
    id: vardict_chromNamesAreNumbers
    type: boolean
  vardict_geneEndCol:
    default: 3
    doc: The column for region end, e.g. gene end
    id: vardict_geneEndCol
    type: int
  vardict_regStartCol:
    default: 2
    doc: The column for region start, e.g. gene start
    id: vardict_regStartCol
    type: int
  vardict_vcfFormat:
    default: true
    doc: VCF format output
    id: vardict_vcfFormat
    type: boolean
label: Vardict Germline Variant Caller
outputs:
  out:
    id: out
    outputSource: trim/out
    type: File
  vardict_variants:
    id: vardict_variants
    outputSource: vardict/out
    type: File
requirements:
  InlineJavascriptRequirement: {}
  StepInputExpressionRequirement: {}
steps:
  annotate:
    in:
      file:
        id: file
        source: vardict/out
      headerLines:
        id: headerLines
        source: header_lines
    out:
    - out
    run: bcftoolsAnnotate.cwl
  split_multi_allele:
    in:
      reference:
        id: reference
        source: reference
      vcf:
        id: vcf
        source: annotate/out
    out:
    - out
    run: SplitMultiAllele.cwl
  trim:
    in:
      vcf:
        id: vcf
        source: split_multi_allele/out
    out:
    - out
    run: trimIUPAC.cwl
  vardict:
    in:
      alleleFreqThreshold:
        id: alleleFreqThreshold
        source: allele_freq_threshold
      bam:
        id: bam
        source: bam
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
      reference:
        id: reference
        source: reference
      regStartCol:
        id: regStartCol
        source: vardict_regStartCol
      sampleName:
        id: sampleName
        source: sample_name
      var2vcfAlleleFreqThreshold:
        id: var2vcfAlleleFreqThreshold
        source: allele_freq_threshold
      var2vcfSampleName:
        id: var2vcfSampleName
        source: sample_name
      vcfFormat:
        id: vcfFormat
        source: vardict_vcfFormat
    out:
    - out
    run: vardict_germline.cwl
