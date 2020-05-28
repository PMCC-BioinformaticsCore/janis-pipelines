#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0

requirements:
- class: InlineJavascriptRequirement
- class: StepInputExpressionRequirement
- class: MultipleInputFeatureRequirement

inputs:
- id: bam
  type: File
  secondaryFiles:
  - .bai
- id: intervals
  doc: |-
    This optional interval supports processing by regions. If this input resolves to null, then GATK will process the whole genome per each tool's spec
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
- id: split_bam
  in:
  - id: bam
    source: bam
  - id: intervals
    source: intervals
  run: Gatk4SplitReads_4_1_3_0.cwl
  out:
  - id: out
- id: base_recalibrator
  in:
  - id: bam
    source: split_bam/out
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
- id: apply_bqsr
  in:
  - id: bam
    source: split_bam/out
  - id: reference
    source: reference
  - id: recalFile
    source: base_recalibrator/out
  - id: intervals
    source: intervals
  run: Gatk4ApplyBQSR_4_1_3_0.cwl
  out:
  - id: out
- id: haplotype_caller
  in:
  - id: inputRead
    source: apply_bqsr/out
  - id: reference
    source: reference
  - id: dbsnp
    source: snps_dbsnp
  - id: intervals
    source: intervals
  run: Gatk4HaplotypeCaller_4_1_3_0.cwl
  out:
  - id: out
- id: split_multi_allele
  in:
  - id: vcf
    source: haplotype_caller/out
  - id: reference
    source: reference
  run: SplitMultiAllele_v0_5772.cwl
  out:
  - id: out
