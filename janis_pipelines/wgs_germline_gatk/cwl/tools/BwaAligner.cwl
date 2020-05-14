#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: Align and sort reads
doc: |-
  Align sorted bam with this subworkflow consisting of BWA Mem + SamTools + Gatk4SortSam
requirements:
  InlineJavascriptRequirement: {}
  StepInputExpressionRequirement: {}
inputs:
  bwamem_markShorterSplits:
    id: bwamem_markShorterSplits
    doc: Mark shorter split hits as secondary (for Picard compatibility).
    type: boolean
    default: true
  cutadapt_adapter:
    id: cutadapt_adapter
    type:
    - type: array
      items: string
    - 'null'
  cutadapt_front:
    id: cutadapt_front
    type:
    - string
    - 'null'
  cutadapt_minimumLength:
    id: cutadapt_minimumLength
    doc: '(-m)  Discard reads shorter than LEN. Default: 0'
    type: int
    default: 50
  cutadapt_qualityCutoff:
    id: cutadapt_qualityCutoff
    doc: |-
      (]3'CUTOFF, ]3'CUTOFF, -q)  Trim low-quality bases from 5' and/or 3' ends of each read before adapter removal. Applied to both reads if data is paired. If one value is given, only the 3' end is trimmed. If two comma-separated cutoffs are given, the 5' end is trimmed with the first cutoff, the 3' end with the second.
    type: int
    default: 15
  cutadapt_removeMiddle3Adapter:
    id: cutadapt_removeMiddle3Adapter
    type:
    - type: array
      items: string
    - 'null'
  cutadapt_removeMiddle5Adapter:
    id: cutadapt_removeMiddle5Adapter
    type:
    - string
    - 'null'
  fastq:
    id: fastq
    type:
      type: array
      items: File
  reference:
    id: reference
    type: File
    secondaryFiles:
    - .fai
    - .amb
    - .ann
    - .bwt
    - .pac
    - .sa
    - ^.dict
  sample_name:
    id: sample_name
    type: string
  sortsam_createIndex:
    id: sortsam_createIndex
    doc: Whether to create a BAM index when writing a coordinate-sorted BAM file.
    type: boolean
    default: true
  sortsam_maxRecordsInRam:
    id: sortsam_maxRecordsInRam
    doc: |-
      When writing SAM files that need to be sorted, this will specify the number of records stored in RAM before spilling to disk. Increasing this number reduces the number of file handles needed to sort a SAM file, and increases the amount of RAM needed.
    type: int
    default: 5000000
  sortsam_sortOrder:
    id: sortsam_sortOrder
    doc: |-
      The --SORT_ORDER argument is an enumerated type (SortOrder), which can have one of the following values: [unsorted, queryname, coordinate, duplicate, unknown]
    type: string
    default: coordinate
  sortsam_tmpDir:
    id: sortsam_tmpDir
    doc: Undocumented option
    type: string
    default: .
  sortsam_validationStringency:
    id: sortsam_validationStringency
    doc: |-
      Validation stringency for all SAM files read by this program. Setting stringency to SILENT can improve performance when processing a BAM file in which variable-length data (read, qualities, tags) do not otherwise need to be decoded.The --VALIDATION_STRINGENCY argument is an enumerated type (ValidationStringency), which can have one of the following values: [STRICT, LENIENT, SILENT]
    type: string
    default: SILENT
outputs:
  out:
    id: out
    type: File
    secondaryFiles:
    - .bai
    outputSource: sortsam/out
steps:
  bwamem:
    in:
      markShorterSplits:
        id: markShorterSplits
        source: bwamem_markShorterSplits
      reads:
        id: reads
        source: cutadapt/out
      reference:
        id: reference
        source: reference
      sampleName:
        id: sampleName
        source: sample_name
    run: BwaMemSamtoolsView.cwl
    out:
    - out
  cutadapt:
    in:
      adapter:
        id: adapter
        source: cutadapt_adapter
      fastq:
        id: fastq
        source: fastq
      front:
        id: front
        source: cutadapt_front
      minimumLength:
        id: minimumLength
        source: cutadapt_minimumLength
      qualityCutoff:
        id: qualityCutoff
        source: cutadapt_qualityCutoff
      removeMiddle3Adapter:
        id: removeMiddle3Adapter
        source: cutadapt_removeMiddle3Adapter
      removeMiddle5Adapter:
        id: removeMiddle5Adapter
        source: cutadapt_removeMiddle5Adapter
    run: cutadapt.cwl
    out:
    - out
  sortsam:
    in:
      bam:
        id: bam
        source: bwamem/out
      createIndex:
        id: createIndex
        source: sortsam_createIndex
      maxRecordsInRam:
        id: maxRecordsInRam
        source: sortsam_maxRecordsInRam
      sortOrder:
        id: sortOrder
        source: sortsam_sortOrder
      tmpDir:
        id: tmpDir
        source: sortsam_tmpDir
      validationStringency:
        id: validationStringency
        source: sortsam_validationStringency
    run: Gatk4SortSam.cwl
    out:
    - out
id: BwaAligner
