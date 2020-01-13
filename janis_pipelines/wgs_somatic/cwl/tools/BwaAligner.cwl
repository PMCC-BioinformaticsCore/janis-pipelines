class: Workflow
cwlVersion: v1.0
doc: Align sorted bam with this subworkflow consisting of BWA Mem + SamTools + Gatk4SortSam
id: BwaAligner
inputs:
  bwamem_markShorterSplits:
    default: true
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
    id: cutadapt_minimumLength
    type: int
  cutadapt_qualityCutoff:
    default: 15
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
  sampleName:
    id: sampleName
    type: string
  sortsam_createIndex:
    default: true
    id: sortsam_createIndex
    type: boolean
  sortsam_maxRecordsInRam:
    default: 5000000
    id: sortsam_maxRecordsInRam
    type: int
  sortsam_sortOrder:
    default: coordinate
    id: sortsam_sortOrder
    type: string
  sortsam_tmpDir:
    default: .
    id: sortsam_tmpDir
    type: string
  sortsam_validationStringency:
    default: SILENT
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
        source: sampleName
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
