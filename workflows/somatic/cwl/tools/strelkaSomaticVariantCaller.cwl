class: Workflow
cwlVersion: v1.0
id: strelkaSomaticVariantCaller
inputs:
  filters:
    default:
    - PASS
    id: filters
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
  normalBam:
    id: normalBam
    secondaryFiles:
    - ^.bai
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
  tumorBam:
    id: tumorBam
    secondaryFiles:
    - ^.bai
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
    outputSource: splitMultiAllele/out
    type: File
  variants:
    id: variants
    outputSource: strelka/snvs
    secondaryFiles:
    - .tbi
    type: File
requirements:
  InlineJavascriptRequirement: {}
  StepInputExpressionRequirement: {}
steps:
  bcf_view:
    in:
      applyFilters:
        id: applyFilters
        source: filters
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
        source: normalBam
      callRegions:
        id: callRegions
        source: intervals
      reference:
        id: reference
        source: reference
      tumorBam:
        id: tumorBam
        source: tumorBam
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
  splitMultiAllele:
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
      indelCandidates:
        id: indelCandidates
        source: manta/candidateSmallIndels
      normalBam:
        id: normalBam
        source: normalBam
      reference:
        id: reference
        source: reference
      tumorBam:
        id: tumorBam
        source: tumorBam
    out:
    - configPickle
    - script
    - stats
    - indels
    - snvs
    run: strelka_somatic.cwl
