class: Workflow
cwlVersion: v1.0
id: vardictGermlineVariantCaller
inputs:
  alleleFreqThreshold:
    default: 0.5
    id: alleleFreqThreshold
    type: float
  bam:
    id: bam
    secondaryFiles:
    - ^.bai
    type: File
  headerLines:
    id: headerLines
    type: File
  intervals:
    id: intervals
    type: File
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
  sampleName:
    id: sampleName
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
label: Vardict Germline Variant Caller
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
        source: sampleName
      var2vcfAlleleFreqThreshold:
        id: var2vcfAlleleFreqThreshold
        source: alleleFreqThreshold
      var2vcfSampleName:
        id: var2vcfSampleName
        source: sampleName
      vcfFormat:
        id: vcfFormat
        source: vardict_vcfFormat
    out:
    - out
    run: vardict_germline.cwl
