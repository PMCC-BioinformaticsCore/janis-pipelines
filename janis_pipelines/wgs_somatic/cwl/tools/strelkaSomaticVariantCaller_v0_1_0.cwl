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
- id: bcf_view_applyFilters
  doc: (-f) require at least one of the listed FILTER strings (e.g. 'PASS,.'')
  type:
    type: array
    items: string
  default:
  - PASS

outputs:
- id: diploid
  type: File
  secondaryFiles:
  - .tbi
  outputSource: manta/diploidSV
- id: variants
  type: File
  secondaryFiles:
  - .tbi
  outputSource: strelka/snvs
- id: out
  type: File
  outputSource: split_multi_allele/out

steps:
- id: manta
  in:
  - id: bam
    source: normal_bam
  - id: reference
    source: reference
  - id: tumorBam
    source: tumor_bam
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
  in:
  - id: normalBam
    source: normal_bam
  - id: tumorBam
    source: tumor_bam
  - id: reference
    source: reference
  - id: indelCandidates
    source:
    - manta/candidateSmallIndels
    linkMerge: merge_nested
  - id: exome
    source: is_exome
  - id: callRegions
    source: intervals
  run: strelka_somatic_2_9_10.cwl
  out:
  - id: configPickle
  - id: script
  - id: stats
  - id: indels
  - id: snvs
- id: bcf_view
  in:
  - id: file
    source: strelka/snvs
  - id: applyFilters
    source: bcf_view_applyFilters
  run: bcftoolsview_v1_5.cwl
  out:
  - id: out
- id: split_multi_allele
  in:
  - id: vcf
    source: bcf_view/out
  - id: reference
    source: reference
  run: SplitMultiAllele_v0_5772.cwl
  out:
  - id: out
