#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
requirements:
  InlineJavascriptRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
inputs:
  align_and_sort_sortsam_tmpDir:
    id: align_and_sort_sortsam_tmpDir
    doc: Undocumented option
    type: string
    default: .
  cutadapt_adapters:
    id: cutadapt_adapters
    type:
    - File
    - 'null'
  reads:
    id: reads
    type:
      type: array
      items:
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
outputs:
  out:
    id: out
    type: File
    secondaryFiles:
    - .bai
    outputSource: merge_and_mark/out
  reports:
    id: reports
    type:
      type: array
      items:
        type: array
        items: File
    outputSource: fastqc/out
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
    scatter:
    - fastq
    - cutadapt_adapter
    - cutadapt_removeMiddle3Adapter
    scatterMethod: dotproduct
    run: BwaAligner.cwl
    out:
    - out
  fastqc:
    in:
      reads:
        id: reads
        source: reads
    scatter:
    - reads
    run: fastqc.cwl
    out:
    - out
    - datafile
  getfastqc_adapters:
    in:
      cutadapt_adaptors_lookup:
        id: cutadapt_adaptors_lookup
        source: cutadapt_adapters
      fastqc_datafiles:
        id: fastqc_datafiles
        source: fastqc/datafile
    scatter:
    - fastqc_datafiles
    run: ParseFastqcAdaptors.cwl
    out:
    - adaptor_sequences
  merge_and_mark:
    in:
      bams:
        id: bams
        source: align_and_sort/out
    run: mergeAndMarkBams.cwl
    out:
    - out
id: somatic_subpipeline
