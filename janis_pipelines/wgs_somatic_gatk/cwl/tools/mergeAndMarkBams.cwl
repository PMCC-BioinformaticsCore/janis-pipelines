#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: Merge and Mark Duplicates
requirements:
  InlineJavascriptRequirement: {}
  StepInputExpressionRequirement: {}
inputs:
  bams:
    id: bams
    type:
      type: array
      items: File
  createIndex:
    id: createIndex
    type: boolean
    default: true
  maxRecordsInRam:
    id: maxRecordsInRam
    type: int
    default: 5000000
  mergeSamFiles_useThreading:
    id: mergeSamFiles_useThreading
    doc: |-
      Option to create a background thread to encode, compress and write to disk the output file. The threaded version uses about 20% more CPU and decreases runtime by ~20% when writing out a compressed BAM file.
    type: boolean
    default: true
  mergeSamFiles_validationStringency:
    id: mergeSamFiles_validationStringency
    doc: |-
      Validation stringency for all SAM files read by this program. Setting stringency to SILENT can improve performance when processing a BAM file in which variable-length data (read, qualities, tags) do not otherwise need to be decoded.The --VALIDATION_STRINGENCY argument is an enumerated type (ValidationStringency), which can have one of the following values: [STRICT, LENIENT, SILENT]
    type: string
    default: SILENT
  sampleName:
    id: sampleName
    type:
    - string
    - 'null'
outputs:
  out:
    id: out
    type: File
    secondaryFiles:
    - .bai
    outputSource: markDuplicates/out
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
    run: Gatk4MarkDuplicates.cwl
    out:
    - out
    - metrics
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
      sampleName:
        id: sampleName
        source: sampleName
      useThreading:
        id: useThreading
        source: mergeSamFiles_useThreading
      validationStringency:
        id: validationStringency
        source: mergeSamFiles_validationStringency
    run: Gatk4MergeSamFiles.cwl
    out:
    - out
id: mergeAndMarkBams
