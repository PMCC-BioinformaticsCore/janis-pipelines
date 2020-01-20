class: Workflow
cwlVersion: v1.0
id: strelkaGermlineVariantCaller
inputs:
  bam:
    id: bam
    secondaryFiles:
    - .bai
    type: File
  bcfview_applyFilters:
    default:
    - PASS
    id: bcfview_applyFilters
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
label: Strelka Germline Variant Caller
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
    outputSource: strelka/variants
    secondaryFiles:
    - .tbi
    type: File
requirements:
  InlineJavascriptRequirement: {}
  StepInputExpressionRequirement: {}
steps:
  bcfview:
    in:
      applyFilters:
        id: applyFilters
        source: bcfview_applyFilters
      file:
        id: file
        source: strelka/variants
    out:
    - out
    run: bcftoolsview.cwl
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
        source: bcfview/out
    out:
    - out
    run: SplitMultiAllele.cwl
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
    out:
    - configPickle
    - script
    - stats
    - variants
    - genome
    run: strelka_germline.cwl
