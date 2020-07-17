#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: GATK4 Germline Variant Caller
doc: |-
  This is a VariantCaller based on the GATK Best Practice pipelines. It uses the GATK4 toolkit, specifically 4.1.3.

          It has the following steps:

          1. Split Bam based on intervals (bed)
          2. HaplotypeCaller
          3. SplitMultiAllele

requirements:
- class: InlineJavascriptRequirement
- class: StepInputExpressionRequirement

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
- id: haplotype_caller_pairHmmImplementation
  doc: |-
    The PairHMM implementation to use for genotype likelihood calculations. The various implementations balance a tradeoff of accuracy and runtime. The --pair-hmm-implementation argument is an enumerated type (Implementation), which can have one of the following values: EXACT;ORIGINAL;LOGLESS_CACHING;AVX_LOGLESS_CACHING;AVX_LOGLESS_CACHING_OMP;EXPERIMENTAL_FPGA_LOGLESS_CACHING;FASTEST_AVAILABLE. Implementation:  FASTEST_AVAILABLE
  type: string
  default: LOGLESS_CACHING

outputs:
- id: variants
  type: File
  secondaryFiles:
  - .tbi
  outputSource: haplotype_caller/out
- id: out_bam
  type: File
  secondaryFiles:
  - .bai
  outputSource: haplotype_caller/bam
- id: out
  type: File
  outputSource: splitnormalisevcf/out

steps:
- id: split_bam
  label: 'GATK4: SplitReads'
  in:
  - id: bam
    source: bam
  - id: intervals
    source: intervals
  run: Gatk4SplitReads_4_1_3_0.cwl
  out:
  - id: out
- id: haplotype_caller
  label: 'GATK4: Haplotype Caller'
  in:
  - id: pairHmmImplementation
    source: haplotype_caller_pairHmmImplementation
  - id: inputRead
    source: split_bam/out
  - id: reference
    source: reference
  - id: dbsnp
    source: snps_dbsnp
  - id: intervals
    source: intervals
  run: Gatk4HaplotypeCaller_4_1_3_0.cwl
  out:
  - id: out
  - id: bam
- id: uncompressvcf
  label: UncompressArchive
  in:
  - id: file
    source: haplotype_caller/out
  run: UncompressArchive_v1_0_0.cwl
  out:
  - id: out
- id: splitnormalisevcf
  label: Split Multiple Alleles
  in:
  - id: vcf
    source: uncompressvcf/out
  - id: reference
    source: reference
  run: SplitMultiAllele_v0_5772.cwl
  out:
  - id: out
id: GATK4_GermlineVariantCaller
