class: Workflow
cwlVersion: v1.0
id: gridssGermlineVariantCaller
inputs:
  bam:
    id: bam
    secondaryFiles:
    - ^.bai
    type: File
  blacklist:
    id: blacklist
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
  samtools_doNotOutputAlignmentsWithBitsSet:
    default: '0x100'
    id: samtools_doNotOutputAlignmentsWithBitsSet
    type: string
label: Gridss Germline Variant Caller
outputs:
  assembly:
    id: assembly
    outputSource: gridss/assembly
    type: File
  out:
    id: out
    outputSource: gridss/out
    type: File
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  StepInputExpressionRequirement: {}
steps:
  gridss:
    in:
      bams:
        id: bams
        linkMerge: merge_nested
        source:
        - samtools/out
      blacklist:
        id: blacklist
        source: blacklist
      reference:
        id: reference
        source: reference
    out:
    - out
    - assembly
    run: gridss.cwl
  samtools:
    in:
      doNotOutputAlignmentsWithBitsSet:
        id: doNotOutputAlignmentsWithBitsSet
        source: samtools_doNotOutputAlignmentsWithBitsSet
      sam:
        id: sam
        source: bam
    out:
    - out
    run: SamToolsView.cwl
