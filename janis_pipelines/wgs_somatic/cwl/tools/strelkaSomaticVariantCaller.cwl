#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: Strelka Somatic Variant Caller
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  StepInputExpressionRequirement: {}
inputs:
  bcf_view_applyFilters:
    id: bcf_view_applyFilters
    doc: (-f) require at least one of the listed FILTER strings (e.g. 'PASS,.'')
    type:
      type: array
      items: string
    default:
    - PASS
  intervals:
    id: intervals
    type:
    - File
    - 'null'
    secondaryFiles:
    - .tbi
  is_exome:
    id: is_exome
    type:
    - boolean
    - 'null'
  normal_bam:
    id: normal_bam
    type: File
    secondaryFiles:
    - .bai
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
  tumor_bam:
    id: tumor_bam
    type: File
    secondaryFiles:
    - .bai
outputs:
  out:
    id: out
    type: File
    outputSource: split_multi_allele/out
  diploid:
    id: diploid
    type: File
    secondaryFiles:
    - .tbi
    outputSource: manta/diploidSV
  variants:
    id: variants
    type: File
    secondaryFiles:
    - .tbi
    outputSource: strelka/snvs
steps:
  bcf_view:
    in:
      applyFilters:
        id: applyFilters
        source: bcf_view_applyFilters
      file:
        id: file
        source: strelka/snvs
    run: bcftoolsview.cwl
    out:
    - out
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
    run: manta.cwl
    out:
    - python
    - pickle
    - candidateSV
    - candidateSmallIndels
    - diploidSV
    - alignmentStatsSummary
    - svCandidateGenerationStats
    - svLocusGraphStats
  split_multi_allele:
    in:
      reference:
        id: reference
        source: reference
      vcf:
        id: vcf
        source: bcf_view/out
    run: SplitMultiAllele.cwl
    out:
    - out
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
        source:
        - manta/candidateSmallIndels
        linkMerge: merge_nested
      normalBam:
        id: normalBam
        source: normal_bam
      reference:
        id: reference
        source: reference
      tumorBam:
        id: tumorBam
        source: tumor_bam
    run: strelka_somatic.cwl
    out:
    - configPickle
    - script
    - stats
    - indels
    - snvs
id: strelkaSomaticVariantCaller
