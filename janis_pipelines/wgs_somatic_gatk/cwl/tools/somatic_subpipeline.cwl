class: Workflow
cwlVersion: v1.0
id: somatic_subpipeline
inputs:
  align_and_sort_sortsam_tmpDir:
    id: align_and_sort_sortsam_tmpDir
    type:
    - string
    - 'null'
  cutadapt_adapters:
    id: cutadapt_adapters
    type: File
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
  sample_name:
    id: sample_name
    type: string
outputs:
  out:
    id: out
    outputSource: merge_and_mark/out
    secondaryFiles:
    - .bai
    type: File
  reports:
    id: reports
    outputSource: fastqc/out
    type:
      items:
        items: File
        type: array
      type: array
requirements:
  InlineJavascriptRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
steps:
  align_and_sort:
    in:
      cutadapt_adapter:
        id: cutadapt_adapter
        source: getfastqc_adapters/adaptor_sequences
      cutadapt_removeMiddle3Adapter:
        id: cutadapt_removeMiddle3Adapter
        source: getfastqc_adapters/adaptor_sequences
      fastq:
        id: fastq
        source: reads
      reference:
        id: reference
        source: reference
      sample_name:
        id: sample_name
        source: sample_name
      sortsam_tmpDir:
        id: sortsam_tmpDir
        source: align_and_sort_sortsam_tmpDir
    out:
    - out
    run: BwaAligner.cwl
    scatter:
    - fastq
    - cutadapt_adapter
    - cutadapt_removeMiddle3Adapter
    scatterMethod: dotproduct
  fastqc:
    in:
      reads:
        id: reads
        source: reads
    out:
    - out
    - datafile
    run: fastqc.cwl
    scatter:
    - reads
  getfastqc_adapters:
    in:
      cutadapt_adaptors_lookup:
        id: cutadapt_adaptors_lookup
        source: cutadapt_adapters
      fastqc_datafiles:
        id: fastqc_datafiles
        source: fastqc/datafile
    out:
    - adaptor_sequences
    run: ParseFastqcAdaptors.cwl
    scatter:
    - fastqc_datafiles
  merge_and_mark:
    in:
      bams:
        id: bams
        source: align_and_sort/out
    out:
    - out
    run: mergeAndMarkBams.cwl
