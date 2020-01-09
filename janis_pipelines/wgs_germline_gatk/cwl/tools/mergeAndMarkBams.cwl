class: Workflow
cwlVersion: v1.0
id: mergeAndMarkBams
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
  mergeSamFiles_useThreading:
    default: true
    id: mergeSamFiles_useThreading
    type: boolean
  mergeSamFiles_validationStringency:
    default: SILENT
    id: mergeSamFiles_validationStringency
    type: string
label: Merge and Mark Duplicates
outputs:
  out:
    id: out
    outputSource: markDuplicates/out
    secondaryFiles:
    - .bai
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
        source: mergeSamFiles_useThreading
      validationStringency:
        id: validationStringency
        source: mergeSamFiles_validationStringency
    out:
    - out
    run: Gatk4MergeSamFiles.cwl
