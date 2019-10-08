class: Workflow
cwlVersion: v1.0
id: vardictSomaticVariantCaller
inputs:
  alleleFreqThreshold:
    default: 0.05
    id: alleleFreqThreshold
    type: float
  headerLines:
    id: headerLines
    type: File
  intervals:
    id: intervals
    type: File
  normalBam:
    id: normalBam
    secondaryFiles:
    - ^.bai
    type: File
  normalName:
    id: normalName
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
  tumorBam:
    id: tumorBam
    secondaryFiles:
    - ^.bai
    type: File
  tumorName:
    id: tumorName
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
  vardictVariants:
    id: vardictVariants
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
        source: headerLines
    out:
    - out
    run: bcftoolsAnnotate.cwl
  split:
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
        source: split/out
    out:
    - out
    run: trimIUPAC.cwl
  vardict:
    in:
      alleleFreqThreshold:
        id: alleleFreqThreshold
        source: alleleFreqThreshold
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
        source: normalBam
      normalName:
        id: normalName
        source: normalName
      reference:
        id: reference
        source: reference
      regStartCol:
        id: regStartCol
        source: vardict_regStartCol
      tumorBam:
        id: tumorBam
        source: tumorBam
      tumorName:
        id: tumorName
        source: tumorName
      vcfFormat:
        id: vcfFormat
        source: vardict_vcfFormat
    out:
    - out
    run: vardict_somatic.cwl
