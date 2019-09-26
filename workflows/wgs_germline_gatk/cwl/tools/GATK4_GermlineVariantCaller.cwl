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
    - ^.bai
    type: File
  intervals:
    doc: This optional intervals file supports processing by regions. If this file
      resolves to null, then GATK will process the whole genome per each tool's spec
    id: intervals
    type:
    - File
    - 'null'
  knownIndels:
    id: knownIndels
    secondaryFiles:
    - .tbi
    type: File
  millsIndels:
    id: millsIndels
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
    outputSource: splitMultiAllele/out
    type: File
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  StepInputExpressionRequirement: {}
steps:
  applyBQSR:
    in:
      bam:
        id: bam
        source: bam
      intervals:
        id: intervals
        source: intervals
      recalFile:
        id: recalFile
        source: baseRecalibrator/out
      reference:
        id: reference
        source: reference
    out:
    - out
    run: GATK4ApplyBQSR.cwl
  baseRecalibrator:
    in:
      bam:
        id: bam
        source: splitBams/out
      intervals:
        id: intervals
        source: intervals
      knownSites:
        id: knownSites
        source:
        - snps_dbsnp
        - snps_1000gp
        - knownIndels
        - millsIndels
      reference:
        id: reference
        source: reference
    out:
    - out
    run: Gatk4BaseRecalibrator.cwl
  haplotypeCaller:
    in:
      dbsnp:
        id: dbsnp
        source: snps_dbsnp
      inputRead:
        id: inputRead
        source: applyBQSR/out
      intervals:
        id: intervals
        source: intervals
      reference:
        id: reference
        source: reference
    out:
    - out
    run: GatkHaplotypeCaller.cwl
  splitBams:
    in:
      bam:
        id: bam
        source: bam
      intervals:
        id: intervals
        source: intervals
    out:
    - out
    run: gatk4splitreads.cwl
  splitMultiAllele:
    in:
      reference:
        id: reference
        source: reference
      vcf:
        id: vcf
        source: haplotypeCaller/out
    out:
    - out
    run: SplitMultiAllele.cwl
