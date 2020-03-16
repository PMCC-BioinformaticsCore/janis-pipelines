#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
doc: Align sorted bam with this subworkflow consisting of BWA Mem + SamTools + Gatk4SortSam
id: BwaAligner
inputs:
  bwamem_markShorterSplits:
    default: true
    doc: Mark shorter split hits as secondary (for Picard compatibility).
    id: bwamem_markShorterSplits
    type: boolean
  cutadapt_adapter:
    id: cutadapt_adapter
    type:
    - items: string
      type: array
    - 'null'
  cutadapt_front:
    id: cutadapt_front
    type:
    - string
    - 'null'
  cutadapt_minimumLength:
    default: 50
    doc: '(-m)  Discard reads shorter than LEN. Default: 0'
    id: cutadapt_minimumLength
    type: int
  cutadapt_qualityCutoff:
    default: 15
    doc: (]3'CUTOFF, ]3'CUTOFF, -q)  Trim low-quality bases from 5' and/or 3' ends
      of each read before adapter removal. Applied to both reads if data is paired.
      If one value is given, only the 3' end is trimmed. If two comma-separated cutoffs
      are given, the 5' end is trimmed with the first cutoff, the 3' end with the
      second.
    id: cutadapt_qualityCutoff
    type: int
  cutadapt_removeMiddle3Adapter:
    id: cutadapt_removeMiddle3Adapter
    type:
    - items: string
      type: array
    - 'null'
  cutadapt_removeMiddle5Adapter:
    id: cutadapt_removeMiddle5Adapter
    type:
    - string
    - 'null'
  fastq:
    id: fastq
    type:
      items: File
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
  sample_name:
    id: sample_name
    type: string
  sortsam_createIndex:
    default: true
    doc: Whether to create a BAM index when writing a coordinate-sorted BAM file.
    id: sortsam_createIndex
    type: boolean
  sortsam_maxRecordsInRam:
    default: 5000000
    doc: When writing SAM files that need to be sorted, this will specify the number
      of records stored in RAM before spilling to disk. Increasing this number reduces
      the number of file handles needed to sort a SAM file, and increases the amount
      of RAM needed.
    id: sortsam_maxRecordsInRam
    type: int
  sortsam_sortOrder:
    default: coordinate
    doc: 'The --SORT_ORDER argument is an enumerated type (SortOrder), which can have
      one of the following values: [unsorted, queryname, coordinate, duplicate, unknown]'
    id: sortsam_sortOrder
    type: string
  sortsam_tmpDir:
    default: .
    doc: Undocumented option
    id: sortsam_tmpDir
    type: string
  sortsam_validationStringency:
    default: SILENT
    doc: 'Validation stringency for all SAM files read by this program. Setting stringency
      to SILENT can improve performance when processing a BAM file in which variable-length
      data (read, qualities, tags) do not otherwise need to be decoded.The --VALIDATION_STRINGENCY
      argument is an enumerated type (ValidationStringency), which can have one of
      the following values: [STRICT, LENIENT, SILENT]'
    id: sortsam_validationStringency
    type: string
label: Align and sort reads
outputs:
  out:
    id: out
    outputSource: sortsam/out
    secondaryFiles:
    - .bai
    type: File
requirements:
  InlineJavascriptRequirement: {}
  StepInputExpressionRequirement: {}
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
    out:
    - out
    run: BwaMemSamtoolsView.cwl
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
    out:
    - out
    run: cutadapt.cwl
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
    out:
    - out
    run: Gatk4SortSam.cwl
