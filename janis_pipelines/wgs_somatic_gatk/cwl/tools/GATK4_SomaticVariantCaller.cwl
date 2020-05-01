#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: GATK4 Somatic Variant Caller
doc: |-
  This is a VariantCaller based on the GATK Best Practice pipelines. It uses the GATK4 toolkit, specifically 4.0.12.0.

          It has the following steps:

          1. Base Recalibrator x 2
          3. Mutect2
          4. SplitMultiAllele
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  StepInputExpressionRequirement: {}
inputs:
  intervals:
    id: intervals
    doc: |-
      This optional intervals file supports processing by regions. If this file resolves to null, then GATK will process the whole genome per each tool's spec
    type:
    - File
    - 'null'
  known_indels:
    id: known_indels
    type: File
    secondaryFiles:
    - .tbi
  mills_indels:
    id: mills_indels
    type: File
    secondaryFiles:
    - .tbi
  normal_bam:
    id: normal_bam
    type: File
    secondaryFiles:
    - .bai
  normal_name:
    id: normal_name
    type: string
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
  snps_1000gp:
    id: snps_1000gp
    type: File
    secondaryFiles:
    - .tbi
  snps_dbsnp:
    id: snps_dbsnp
    type: File
    secondaryFiles:
    - .tbi
  tumor_bam:
    id: tumor_bam
    type: File
    secondaryFiles:
    - .bai
  tumor_name:
    id: tumor_name
    type: string
outputs:
  out:
    id: out
    type: File
    outputSource: split_multi_allele/out
steps:
  apply_bqsr_normal:
    in:
      bam:
        id: bam
        source: normal_bam
      intervals:
        id: intervals
        source: intervals
      recalFile:
        id: recalFile
        source: base_recalibrator_normal/out
      reference:
        id: reference
        source: reference
    run: Gatk4ApplyBQSR.cwl
    out:
    - out
  apply_bqsr_tumor:
    in:
      bam:
        id: bam
        source: tumor_bam
      intervals:
        id: intervals
        source: intervals
      recalFile:
        id: recalFile
        source: base_recalibrator_tumor/out
      reference:
        id: reference
        source: reference
    run: Gatk4ApplyBQSR.cwl
    out:
    - out
  base_recalibrator_normal:
    in:
      bam:
        id: bam
        source: normal_bam
      intervals:
        id: intervals
        source: intervals
      knownSites:
        id: knownSites
        source:
        - snps_dbsnp
        - snps_1000gp
        - known_indels
        - mills_indels
      reference:
        id: reference
        source: reference
    run: Gatk4BaseRecalibrator.cwl
    out:
    - out
  base_recalibrator_tumor:
    in:
      bam:
        id: bam
        source: tumor_bam
      intervals:
        id: intervals
        source: intervals
      knownSites:
        id: knownSites
        source:
        - snps_dbsnp
        - snps_1000gp
        - known_indels
        - mills_indels
      reference:
        id: reference
        source: reference
    run: Gatk4BaseRecalibrator.cwl
    out:
    - out
  mutect2:
    in:
      intervals:
        id: intervals
        source: intervals
      normalBams:
        id: normalBams
        source:
        - apply_bqsr_normal/out
        linkMerge: merge_nested
      normalSample:
        id: normalSample
        source: normal_name
      reference:
        id: reference
        source: reference
      tumorBams:
        id: tumorBams
        source:
        - apply_bqsr_tumor/out
        linkMerge: merge_nested
    run: Gatk4Mutect2.cwl
    out:
    - out
    - stats
    - f1f2r_out
  split_multi_allele:
    in:
      reference:
        id: reference
        source: reference
      vcf:
        id: vcf
        source: mutect2/out
    run: SplitMultiAllele.cwl
    out:
    - out
id: GATK4_SomaticVariantCaller
