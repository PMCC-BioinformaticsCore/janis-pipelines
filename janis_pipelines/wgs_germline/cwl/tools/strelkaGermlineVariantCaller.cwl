#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: Strelka Germline Variant Caller
requirements:
  InlineJavascriptRequirement: {}
  StepInputExpressionRequirement: {}
inputs:
  bam:
    id: bam
    type: File
    secondaryFiles:
    - .bai
  bcfview_applyFilters:
    id: bcfview_applyFilters
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
    outputSource: strelka/variants
steps:
  bcfview:
    in:
      applyFilters:
        id: applyFilters
        source: bcfview_applyFilters
      file:
        id: file
        source: strelka/variants
    run: bcftoolsview.cwl
    out:
    - out
  manta:
    in:
      bam:
        id: bam
        source: bam
      callRegions:
        id: callRegions
        source: intervals
      exome:
        id: exome
        source: is_exome
      reference:
        id: reference
        source: reference
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
        source: bcfview/out
    run: SplitMultiAllele.cwl
    out:
    - out
  strelka:
    in:
      bam:
        id: bam
        source: bam
      callRegions:
        id: callRegions
        source: intervals
      exome:
        id: exome
        source: is_exome
      indelCandidates:
        id: indelCandidates
        source: manta/candidateSmallIndels
      reference:
        id: reference
        source: reference
    run: strelka_germline.cwl
    out:
    - configPickle
    - script
    - stats
    - variants
    - genome
id: strelkaGermlineVariantCaller
