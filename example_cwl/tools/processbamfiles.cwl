class: Workflow
cwlVersion: v1.0
id: processbamfiles
inputs:
  bams:
    id: bams
    type:
      items: File
      type: array
  createIndex:
    default: true
    id: createIndex
    type: boolean
  maxRecordsInRam:
    default: 5000000
    id: maxRecordsInRam
    type: int
  useThreading:
    default: true
    id: useThreading
    type: boolean
  validationStringency:
    default: SILENT
    id: validationStringency
    type: string
label: Process BAM Files
outputs:
  out:
    id: out
    outputSource: markDuplicates/out
    secondaryFiles:
    - ^.bai
    type: File
requirements:
  InlineJavascriptRequirement: {}
  StepInputExpressionRequirement: {}
steps:
  markDuplicates:
    in:
      bam:
        id: bam
        source: mergeSamFiles/out
      createIndex:
        id: createIndex
        source: createIndex
      maxRecordsInRam:
        id: maxRecordsInRam
        source: maxRecordsInRam
    out:
    - out
    - metrics
    run: Gatk4MarkDuplicates.cwl
  mergeSamFiles:
    in:
      bams:
        id: bams
        source: bams
      createIndex:
        id: createIndex
        source: createIndex
      maxRecordsInRam:
        id: maxRecordsInRam
        source: maxRecordsInRam
      useThreading:
        id: useThreading
        source: useThreading
      validationStringency:
        id: validationStringency
        source: validationStringency
    out:
    - out
    run: Gatk4MergeSamFiles.cwl
