class: Workflow
cwlVersion: v1.0
doc: "This is a VariantCaller based on the GATK Best Practice pipelines. It uses the\
  \ GATK4 toolkit, specifically 4.0.12.0.\n\n        It has the following steps:\n\
  \n        1. BaseRecalibrator\n        2. ApplyBQSR\n        3. HaplotypeCaller\n\
  \        4. SplitMultiAllele"
id: GATK4_GermlineVariantCaller
inputs:
  bam:
    id: bam
    secondaryFiles:
    - .bai
    type: File
  intervals:
    doc: This optional interval supports processing by regions. If this input resolves
      to null, then GATK will process the whole genome per each tool's spec
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
label: GATK4 Germline Variant Caller
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
    out:
    - out
    run: Gatk4ApplyBQSR.cwl
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
    out:
    - out
    run: Gatk4BaseRecalibrator.cwl
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
    out:
    - out
    run: Gatk4HaplotypeCaller.cwl
  split_bam:
    in:
      bam:
        id: bam
        source: bam
      intervals:
        id: intervals
        source: intervals
    out:
    - out
    run: Gatk4SplitReads.cwl
  split_multi_allele:
    in:
      reference:
        id: reference
        source: reference
      vcf:
        id: vcf
        source: haplotype_caller/out
    out:
    - out
    run: SplitMultiAllele.cwl
