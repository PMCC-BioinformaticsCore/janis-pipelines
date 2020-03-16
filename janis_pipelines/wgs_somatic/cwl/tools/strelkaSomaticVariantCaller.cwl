#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
id: strelkaSomaticVariantCaller
inputs:
  bcf_view_applyFilters:
    default:
    - PASS
    doc: (-f) require at least one of the listed FILTER strings (e.g. 'PASS,.'')
    id: bcf_view_applyFilters
    type:
      items: string
      type: array
  intervals:
    id: intervals
    secondaryFiles:
    - .tbi
    type:
    - File
    - 'null'
  is_exome:
    id: is_exome
    type:
    - boolean
    - 'null'
  normal_bam:
    id: normal_bam
    secondaryFiles:
    - .bai
    type: File
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
  tumor_bam:
    id: tumor_bam
    secondaryFiles:
    - .bai
    type: File
label: Strelka Somatic Variant Caller
outputs:
  diploid:
    id: diploid
    outputSource: manta/diploidSV
    secondaryFiles:
    - .tbi
    type: File
  out:
    id: out
    outputSource: split_multi_allele/out
    type: File
  variants:
    id: variants
    outputSource: strelka/snvs
    secondaryFiles:
    - .tbi
    type: File
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  StepInputExpressionRequirement: {}
steps:
  bcf_view:
    in:
      applyFilters:
        id: applyFilters
        source: bcf_view_applyFilters
      file:
        id: file
        source: strelka/snvs
    out:
    - out
    run: bcftoolsview.cwl
  manta:
    in:
      bam:
        id: bam
        source: normal_bam
      callRegions:
        id: callRegions
        source: intervals
      exome:
        id: exome
        source: is_exome
      reference:
        id: reference
        source: reference
      tumorBam:
        id: tumorBam
        source: tumor_bam
    out:
    - python
    - pickle
    - candidateSV
    - candidateSmallIndels
    - diploidSV
    - alignmentStatsSummary
    - svCandidateGenerationStats
    - svLocusGraphStats
    run: manta.cwl
  split_multi_allele:
    in:
      reference:
        id: reference
        source: reference
      vcf:
        id: vcf
        source: bcf_view/out
    out:
    - out
    run: SplitMultiAllele.cwl
  strelka:
    in:
      callRegions:
        id: callRegions
        source: intervals
      exome:
        id: exome
        source: is_exome
      indelCandidates:
        id: indelCandidates
        linkMerge: merge_nested
        source:
        - manta/candidateSmallIndels
      normalBam:
        id: normalBam
        source: normal_bam
      reference:
        id: reference
        source: reference
      tumorBam:
        id: tumorBam
        source: tumor_bam
    out:
    - configPickle
    - script
    - stats
    - indels
    - snvs
    run: strelka_somatic.cwl
