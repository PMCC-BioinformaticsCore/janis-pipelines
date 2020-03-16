#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
doc: "This is a VariantCaller based on the GATK Best Practice pipelines. It uses the\
  \ GATK4 toolkit, specifically 4.0.12.0.\n\n        It has the following steps:\n\
  \n        1. Base Recalibrator x 2\n        3. Mutect2\n        4. SplitMultiAllele"
id: GATK4_SomaticVariantCaller
inputs:
  intervals:
    doc: This optional intervals file supports processing by regions. If this file
      resolves to null, then GATK will process the whole genome per each tool's spec
    id: intervals
    type:
    - File
    - 'null'
  known_indels:
    id: known_indels
    secondaryFiles:
    - .tbi
    type: File
  mills_indels:
    id: mills_indels
    secondaryFiles:
    - .tbi
    type: File
  normal_bam:
    id: normal_bam
    secondaryFiles:
    - .bai
    type: File
  normal_name:
    id: normal_name
    type: string
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
  snps_1000gp:
    id: snps_1000gp
    secondaryFiles:
    - .tbi
    type: File
  snps_dbsnp:
    id: snps_dbsnp
    secondaryFiles:
    - .tbi
    type: File
  tumor_bam:
    id: tumor_bam
    secondaryFiles:
    - .bai
    type: File
  tumor_name:
    id: tumor_name
    type: string
label: GATK4 Somatic Variant Caller
outputs:
  out:
    id: out
    outputSource: split_multi_allele/out
    type: File
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  StepInputExpressionRequirement: {}
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
    out:
    - out
    run: Gatk4ApplyBQSR.cwl
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
    out:
    - out
    run: Gatk4ApplyBQSR.cwl
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
    out:
    - out
    run: Gatk4BaseRecalibrator.cwl
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
    out:
    - out
    run: Gatk4BaseRecalibrator.cwl
  mutect2:
    in:
      intervals:
        id: intervals
        source: intervals
      normalBams:
        id: normalBams
        linkMerge: merge_nested
        source:
        - apply_bqsr_normal/out
      normalSample:
        id: normalSample
        source: normal_name
      reference:
        id: reference
        source: reference
      tumorBams:
        id: tumorBams
        linkMerge: merge_nested
        source:
        - apply_bqsr_tumor/out
    out:
    - out
    - stats
    - f1f2r_out
    run: Gatk4Mutect2.cwl
  split_multi_allele:
    in:
      reference:
        id: reference
        source: reference
      vcf:
        id: vcf
        source: mutect2/out
    out:
    - out
    run: SplitMultiAllele.cwl
