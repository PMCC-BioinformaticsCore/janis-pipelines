#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0

requirements:
- class: InlineJavascriptRequirement
- class: StepInputExpressionRequirement
- class: ScatterFeatureRequirement
- class: SubworkflowFeatureRequirement

inputs:
- id: reference
  type: File
  secondaryFiles:
  - .fai
  - .amb
  - .ann
  - .bwt
  - .pac
  - .sa
  - ^.dict
- id: reads
  type:
    type: array
    items:
      type: array
      items: File
- id: cutadapt_adapters
  type:
  - File
  - 'null'
- id: sample_name
  type: string
- id: align_and_sort_sortsam_tmpDir
  type:
  - string
  - 'null'

outputs:
- id: out
  type: File
  secondaryFiles:
  - .bai
  outputSource: merge_and_mark/out
- id: reports
  type:
    type: array
    items:
      type: array
      items: File
  outputSource: fastqc/out

steps:
- id: fastqc
  in:
  - id: reads
    source: reads
  scatter:
  - reads
  run: fastqc_v0_11_5.cwl
  out:
  - id: out
  - id: datafile
- id: getfastqc_adapters
  in:
  - id: fastqc_datafiles
    source: fastqc/datafile
  - id: cutadapt_adaptors_lookup
    source: cutadapt_adapters
  scatter:
  - fastqc_datafiles
  run: ParseFastqcAdaptors_v0_1_0.cwl
  out:
  - id: adaptor_sequences
- id: align_and_sort
  in:
  - id: sample_name
    source: sample_name
  - id: reference
    source: reference
  - id: fastq
    source: reads
  - id: cutadapt_adapter
    source: getfastqc_adapters/adaptor_sequences
  - id: cutadapt_removeMiddle3Adapter
    source: getfastqc_adapters/adaptor_sequences
  - id: sortsam_tmpDir
    source: align_and_sort_sortsam_tmpDir
  scatter:
  - fastq
  - cutadapt_adapter
  - cutadapt_removeMiddle3Adapter
  scatterMethod: dotproduct
  run: BwaAligner_1_0_0.cwl
  out:
  - id: out
- id: merge_and_mark
  in:
  - id: bams
    source: align_and_sort/out
  - id: sampleName
    source: sample_name
  run: mergeAndMarkBams_4_1_3.cwl
  out:
  - id: out
