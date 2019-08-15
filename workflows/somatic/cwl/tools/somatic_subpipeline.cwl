class: Workflow
cwlVersion: v1.0
id: somatic_subpipeline
inputs:
  inputs:
    id: inputs
    type:
      items:
        items: File
        type: array
      type: array
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
  sortSamTmpDir:
    id: sortSamTmpDir
    type:
    - string
    - 'null'
outputs:
  fastq:
    id: fastq
    outputSource: fastqc/out
    type:
      items:
        items: File
        type: array
      type: array
  out:
    id: out
    outputSource: mergeAndMark/out
    secondaryFiles:
    - ^.bai
    type: File
requirements:
  InlineJavascriptRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
steps:
  alignAndSort:
    in:
      fastq:
        id: fastq
        source: inputs
      reference:
        id: reference
        source: reference
      sampleName:
        id: sampleName
        source: sampleName
      sortSamTmpDir:
        id: sortSamTmpDir
        source: sortSamTmpDir
    out:
    - out_bwa
    - out
    run: alignsortedbam.cwl
    scatter:
    - fastq
  fastqc:
    in:
      reads:
        id: reads
        source: inputs
    out:
    - out
    run: fastqc.cwl
    scatter:
    - reads
  mergeAndMark:
    in:
      bams:
        id: bams
        source: alignAndSort/out
    out:
    - out
    run: processbamfiles.cwl
