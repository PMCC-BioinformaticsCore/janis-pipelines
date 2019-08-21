class: Workflow
cwlVersion: v1.0
doc: Align sorted bam with this subworkflow consisting of BWA Mem + SamTools + Gatk4SortSam
id: BwaAligner
inputs:
  adapter:
    id: adapter
    type:
    - string
    - 'null'
  adapter_g:
    id: adapter_g
    type:
    - string
    - 'null'
  createIndex:
    default: true
    id: createIndex
    type: boolean
  fastq:
    id: fastq
    type:
      items: File
      type: array
  maxRecordsInRam:
    default: 5000000
    id: maxRecordsInRam
    type: int
  minReadLength:
    default: 50
    id: minReadLength
    type: int
  qualityCutoff:
    default: 15
    id: qualityCutoff
    type: int
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
  removeMiddle3Adapter:
    id: removeMiddle3Adapter
    type:
    - string
    - 'null'
  removeMiddle5Adapter:
    id: removeMiddle5Adapter
    type:
    - string
    - 'null'
  sampleName:
    id: sampleName
    type: string
  sortOrder:
    default: coordinate
    id: sortOrder
    type: string
  sortSamTmpDir:
    id: sortSamTmpDir
    type:
    - string
    - 'null'
  validationStringency:
    default: SILENT
    id: validationStringency
    type: string
label: Align and sort reads
outputs:
  out:
    id: out
    outputSource: sortsam/out
    secondaryFiles:
    - ^.bai
    type: File
  out_bwa:
    id: out_bwa
    outputSource: bwa_sam/out
    type: File
requirements:
  InlineJavascriptRequirement: {}
  StepInputExpressionRequirement: {}
steps:
  bwa_sam:
    in:
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
        source: adapter
      adapter_g:
        id: adapter_g
        source: adapter_g
      fastq:
        id: fastq
        source: fastq
      minReadLength:
        id: minReadLength
        source: minReadLength
      qualityCutoff:
        id: qualityCutoff
        source: qualityCutoff
      removeMiddle3Adapter:
        id: removeMiddle3Adapter
        source: removeMiddle3Adapter
      removeMiddle5Adapter:
        id: removeMiddle5Adapter
        source: removeMiddle5Adapter
    out:
    - out
    run: cutadapt.cwl
  sortsam:
    in:
      bam:
        id: bam
        source: bwa_sam/out
      createIndex:
        id: createIndex
        source: createIndex
      maxRecordsInRam:
        id: maxRecordsInRam
        source: maxRecordsInRam
      sortOrder:
        id: sortOrder
        source: sortOrder
      tmpDir:
        id: tmpDir
        source: sortSamTmpDir
      validationStringency:
        id: validationStringency
        source: validationStringency
    out:
    - out
    run: gatk4sortsam.cwl
