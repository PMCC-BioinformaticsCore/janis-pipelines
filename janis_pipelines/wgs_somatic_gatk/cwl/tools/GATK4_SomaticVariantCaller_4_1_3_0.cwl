#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0

requirements:
- class: InlineJavascriptRequirement
- class: StepInputExpressionRequirement
- class: MultipleInputFeatureRequirement

inputs:
- id: normal_bam
  type: File
  secondaryFiles:
  - .bai
- id: tumor_bam
  type: File
  secondaryFiles:
  - .bai
- id: normal_name
  type: string
- id: tumor_name
  type: string
- id: intervals
  doc: |-
    This optional intervals file supports processing by regions. If this file resolves to null, then GATK will process the whole genome per each tool's spec
  type:
  - File
  - 'null'
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
- id: snps_dbsnp
  type: File
  secondaryFiles:
  - .tbi
- id: snps_1000gp
  type: File
  secondaryFiles:
  - .tbi
- id: known_indels
  type: File
  secondaryFiles:
  - .tbi
- id: mills_indels
  type: File
  secondaryFiles:
  - .tbi

outputs:
- id: out
  type: File
  outputSource: split_multi_allele/out

steps:
- id: base_recalibrator_normal
  in:
  - id: bam
    source: normal_bam
  - id: knownSites
    source:
    - snps_dbsnp
    - snps_1000gp
    - known_indels
    - mills_indels
  - id: reference
    source: reference
  - id: intervals
    source: intervals
  run: Gatk4BaseRecalibrator_4_1_3_0.cwl
  out:
  - id: out
- id: base_recalibrator_tumor
  in:
  - id: bam
    source: tumor_bam
  - id: knownSites
    source:
    - snps_dbsnp
    - snps_1000gp
    - known_indels
    - mills_indels
  - id: reference
    source: reference
  - id: intervals
    source: intervals
  run: Gatk4BaseRecalibrator_4_1_3_0.cwl
  out:
  - id: out
- id: apply_bqsr_normal
  in:
  - id: bam
    source: normal_bam
  - id: reference
    source: reference
  - id: recalFile
    source: base_recalibrator_normal/out
  - id: intervals
    source: intervals
  run: Gatk4ApplyBQSR_4_1_3_0.cwl
  out:
  - id: out
- id: apply_bqsr_tumor
  in:
  - id: bam
    source: tumor_bam
  - id: reference
    source: reference
  - id: recalFile
    source: base_recalibrator_tumor/out
  - id: intervals
    source: intervals
  run: Gatk4ApplyBQSR_4_1_3_0.cwl
  out:
  - id: out
- id: mutect2
  in:
  - id: tumorBams
    source:
    - apply_bqsr_tumor/out
    linkMerge: merge_nested
  - id: normalBams
    source:
    - apply_bqsr_normal/out
    linkMerge: merge_nested
  - id: normalSample
    source: normal_name
  - id: reference
    source: reference
  - id: intervals
    source: intervals
  run: Gatk4Mutect2_4_1_3_0.cwl
  out:
  - id: out
  - id: stats
  - id: f1f2r_out
- id: split_multi_allele
  in:
  - id: vcf
    source: mutect2/out
  - id: reference
    source: reference
  run: SplitMultiAllele_v0_5772.cwl
  out:
  - id: out
