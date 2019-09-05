class: Workflow
cwlVersion: v1.0
doc: "This is a VariantCaller based on the GATK Best Practice pipelines. It uses the\
  \ GATK4 toolkit, specifically 4.0.12.0.\n\nIt has the following steps:\n\n1. Base\
  \ Recalibrator x 2\n3. Mutect2\n4. SplitMultiAllele"
id: GATK4_SomaticVariantCaller
inputs:
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
  normalBam:
    id: normalBam
    secondaryFiles:
    - ^.bai
    type: File
  normalName:
    id: normalName
    type: string
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
  tumorBam:
    id: tumorBam
    secondaryFiles:
    - ^.bai
    type: File
  tumorName:
    id: tumorName
    type: string
label: GATK4 Somatic Variant Caller
outputs:
  out:
    id: out
    outputSource: splitMultiAllele/out
    type: File
requirements:
  InlineJavascriptRequirement: {}
  StepInputExpressionRequirement: {}
steps:
  applyBQSR_normal:
    in:
      bam:
        id: bam
        source: normalBam
      intervals:
        id: intervals
        source: intervals
      recalFile:
        id: recalFile
        source: baseRecalibrator_normal/out
      reference:
        id: reference
        source: reference
    out:
    - out
    run: GATK4ApplyBQSR.cwl
  applyBQSR_tumor:
    in:
      bam:
        id: bam
        source: tumorBam
      intervals:
        id: intervals
        source: intervals
      recalFile:
        id: recalFile
        source: baseRecalibrator_tumor/out
      reference:
        id: reference
        source: reference
    out:
    - out
    run: GATK4ApplyBQSR.cwl
  baseRecalibrator_normal:
    in:
      bam:
        id: bam
        source: normalBam
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
  baseRecalibrator_tumor:
    in:
      bam:
        id: bam
        source: tumorBam
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
  mutect2:
    in:
      intervals:
        id: intervals
        source: intervals
      normal:
        id: normal
        source: applyBQSR_normal/out
      normalName:
        id: normalName
        source: normalName
      reference:
        id: reference
        source: reference
      tumor:
        id: tumor
        source: applyBQSR_tumor/out
      tumorName:
        id: tumorName
        source: tumorName
    out:
    - out
    run: gatkmutect2.cwl
  splitMultiAllele:
    in:
      reference:
        id: reference
        source: reference
      vcf:
        id: vcf
        source: mutect2/out
    out:
    - out
    run: SplitMultiAllele.cwl
