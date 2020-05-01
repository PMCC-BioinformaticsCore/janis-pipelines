#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: GATK4 Germline Variant Caller
doc: |-
  This is a VariantCaller based on the GATK Best Practice pipelines. It uses the GATK4 toolkit, specifically 4.0.12.0.

          It has the following steps:

          1. BaseRecalibrator
          2. ApplyBQSR
          3. HaplotypeCaller
          4. SplitMultiAllele
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  StepInputExpressionRequirement: {}
inputs:
  bam:
    id: bam
    type: File
    secondaryFiles:
    - .bai
  intervals:
    id: intervals
    doc: |-
      This optional interval supports processing by regions. If this input resolves to null, then GATK will process the whole genome per each tool's spec
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
outputs:
  out:
    id: out
    type: File
    outputSource: split_multi_allele/out
steps:
  apply_bqsr:
    in:
      bam:
        id: bam
        source: split_bam/out
      intervals:
        id: intervals
        source: intervals
      recalFile:
        id: recalFile
        source: base_recalibrator/out
      reference:
        id: reference
        source: reference
    run: Gatk4ApplyBQSR.cwl
    out:
    - out
  base_recalibrator:
    in:
      bam:
        id: bam
        source: split_bam/out
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
  haplotype_caller:
    in:
      dbsnp:
        id: dbsnp
        source: snps_dbsnp
      inputRead:
        id: inputRead
        source: apply_bqsr/out
      intervals:
        id: intervals
        source: intervals
      reference:
        id: reference
        source: reference
    run: Gatk4HaplotypeCaller.cwl
    out:
    - out
  split_bam:
    in:
      bam:
        id: bam
        source: bam
      intervals:
        id: intervals
        source: intervals
    run: Gatk4SplitReads.cwl
    out:
    - out
  split_multi_allele:
    in:
      reference:
        id: reference
        source: reference
      vcf:
        id: vcf
        source: haplotype_caller/out
    run: SplitMultiAllele.cwl
    out:
    - out
id: GATK4_GermlineVariantCaller
