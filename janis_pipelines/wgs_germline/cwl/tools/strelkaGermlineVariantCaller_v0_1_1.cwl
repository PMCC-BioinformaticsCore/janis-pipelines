#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: Strelka Germline Variant Caller

requirements:
- class: InlineJavascriptRequirement
- class: StepInputExpressionRequirement

inputs:
- id: bam
  type: File
  secondaryFiles:
  - .bai
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
- id: intervals
  type:
  - File
  - 'null'
  secondaryFiles:
  - .tbi
- id: is_exome
  type:
  - boolean
  - 'null'
- id: filterpass_removeFileteredAll
  doc: Removes all sites with a FILTER flag other than PASS.
  type: boolean
  default: true
- id: filterpass_recode
  doc: ''
  type: boolean
  default: true
- id: filterpass_recodeINFOAll
  doc: |-
    These options can be used with the above recode options to define an INFO key name to keep in the output  file.  This  option can be used multiple times to keep more of the INFO fields. The second option is used to keep all INFO values in the original file.
  type: boolean
  default: true

outputs:
- id: sv
  type: File
  secondaryFiles:
  - .tbi
  outputSource: manta/diploidSV
- id: variants
  type: File
  secondaryFiles:
  - .tbi
  outputSource: strelka/variants
- id: out
  type: File
  outputSource: filterpass/out

steps:
- id: manta
  label: Manta
  in:
  - id: bam
    source: bam
  - id: reference
    source: reference
  - id: exome
    source: is_exome
  - id: callRegions
    source: intervals
  run: manta_1_5_0.cwl
  out:
  - id: python
  - id: pickle
  - id: candidateSV
  - id: candidateSmallIndels
  - id: diploidSV
  - id: alignmentStatsSummary
  - id: svCandidateGenerationStats
  - id: svLocusGraphStats
- id: strelka
  label: Strelka (Germline)
  in:
  - id: bam
    source: bam
  - id: reference
    source: reference
  - id: indelCandidates
    source: manta/candidateSmallIndels
  - id: exome
    source: is_exome
  - id: callRegions
    source: intervals
  run: strelka_germline_2_9_10.cwl
  out:
  - id: configPickle
  - id: script
  - id: stats
  - id: variants
  - id: genome
- id: uncompressvcf
  label: UncompressArchive
  in:
  - id: file
    source: strelka/variants
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
- id: filterpass
  label: VcfTools
  in:
  - id: vcf
    source: splitnormalisevcf/out
  - id: removeFileteredAll
    source: filterpass_removeFileteredAll
  - id: recode
    source: filterpass_recode
  - id: recodeINFOAll
    source: filterpass_recodeINFOAll
  run: VcfTools_0_1_16.cwl
  out:
  - id: out
id: strelkaGermlineVariantCaller
