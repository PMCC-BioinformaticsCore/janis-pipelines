class: Workflow
cwlVersion: v1.0
id: somatic_subpipeline
inputs:
  alignAndSort_sortsam_tmpDir:
    id: alignAndSort_sortsam_tmpDir
    type:
    - string
    - 'null'
  reads:
    id: reads
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
outputs:
  out:
    id: out
    outputSource: mergeAndMark/out
    secondaryFiles:
    - ^.bai
    type: File
  reports:
    id: reports
    outputSource: fastqc/out
    type:
      items: File
      type: array
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
steps:
  alignAndSort:
    in:
      fastq:
        id: fastq
        source: reads
      name:
        id: name
        source: sampleName
      reference:
        id: reference
        source: reference
      sortsam_tmpDir:
        id: sortsam_tmpDir
        source: alignAndSort_sortsam_tmpDir
    out:
    - out
    run: BwaAligner.cwl
    scatter:
    - fastq
  fastqc:
    in:
      reads:
        id: reads
        source: reads
    out:
    - out
    run: fastqc.cwl
    scatter:
    - reads
  mergeAndMark:
    in:
      bams:
        id: bams
        linkMerge: merge_nested
        source:
        - alignAndSort/out
    out:
    - out
    run: mergeAndMarkBams.cwl
