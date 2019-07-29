class: Workflow
cwlVersion: v1.0
id: vardictVariantCaller
inputs:
  allelFreqThreshold:
    id: allelFreqThreshold
    type: float
  bam:
    id: bam
    secondaryFiles:
    - ^.bai
    type: File
  chromColumn:
    default: 1
    id: chromColumn
    type: int
  chromNamesAreNumbers:
    default: true
    id: chromNamesAreNumbers
    type: boolean
  geneEndCol:
    default: 3
    id: geneEndCol
    type: int
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
  regStartCol:
    default: 2
    id: regStartCol
    type: int
  sampleName:
    id: sampleName
    type: string
  vcfFormat:
    default: true
    id: vcfFormat
    type: boolean
label: Vardict Variant Caller
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
        source: allelFreqThreshold
      bam:
        id: bam
        source: bam
      chromColumn:
        id: chromColumn
        source: chromColumn
      chromNamesAreNumbers:
        id: chromNamesAreNumbers
        source: chromNamesAreNumbers
      geneEndCol:
        id: geneEndCol
        source: geneEndCol
      intervals:
        id: intervals
        source: intervals
      reference:
        id: reference
        source: reference
      regStartCol:
        id: regStartCol
        source: regStartCol
      sampleName:
        id: sampleName
        source: sampleName
      var2vcfAlleleFreqThreshold:
        id: var2vcfAlleleFreqThreshold
        source: allelFreqThreshold
      var2vcfSampleName:
        id: var2vcfSampleName
        source: sampleName
      vcfFormat:
        id: vcfFormat
        source: vcfFormat
    out:
    - out
    run: vardict_germline.cwl
