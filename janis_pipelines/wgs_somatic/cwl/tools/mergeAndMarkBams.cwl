#!/usr/bin/env cwl-runner
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
    doc: Option to create a background thread to encode, compress and write to disk
      the output file. The threaded version uses about 20% more CPU and decreases
      runtime by ~20% when writing out a compressed BAM file.
    id: mergeSamFiles_useThreading
    type: boolean
  mergeSamFiles_validationStringency:
    default: SILENT
    doc: 'Validation stringency for all SAM files read by this program. Setting stringency
      to SILENT can improve performance when processing a BAM file in which variable-length
      data (read, qualities, tags) do not otherwise need to be decoded.The --VALIDATION_STRINGENCY
      argument is an enumerated type (ValidationStringency), which can have one of
      the following values: [STRICT, LENIENT, SILENT]'
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
