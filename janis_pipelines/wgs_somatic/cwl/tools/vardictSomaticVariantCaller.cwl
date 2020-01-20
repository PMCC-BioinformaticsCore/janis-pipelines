class: Workflow
cwlVersion: v1.0
id: vardictSomaticVariantCaller
inputs:
  allele_freq_threshold:
    default: 0.05
    id: allele_freq_threshold
    type: float
  header_lines:
    id: header_lines
    type: File
  intervals:
    id: intervals
    type: File
  normal_bam:
    id: normal_bam
    secondaryFiles:
    - .bai
    type: File
  normal_name:
    id: normal_name
    type: string
  reference:
    id: reference
    secondaryFiles:
    - .amb
    - .ann
    - .bwt
    - .pac
    - .sa
    - .fai
    - ^.dict
    type: File
  tumor_bam:
    id: tumor_bam
    secondaryFiles:
    - .bai
    type: File
  tumor_name:
    id: tumor_name
    type: string
  vardict_chromColumn:
    default: 1
    id: vardict_chromColumn
    type: int
  vardict_chromNamesAreNumbers:
    default: true
    id: vardict_chromNamesAreNumbers
    type: boolean
  vardict_geneEndCol:
    default: 3
    id: vardict_geneEndCol
    type: int
  vardict_regStartCol:
    default: 2
    id: vardict_regStartCol
    type: int
  vardict_vcfFormat:
    default: true
    id: vardict_vcfFormat
    type: boolean
label: Vardict Somatic Variant Caller
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
    out:
    - out
    run: vardict_somatic.cwl
