class: Workflow
cwlVersion: v1.0
id: WGSSomaticGATK
inputs:
  gatkIntervals:
    id: gatkIntervals
    type:
      items: File
      type: array
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
  normalInputs:
    id: normalInputs
    type:
      items: File
      type: array
  normalName:
    default: NA24385_normal
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
  tumorInputs:
    id: tumorInputs
    type:
      items: File
      type: array
  tumorName:
    default: NA24385_tumour
    id: tumorName
    type: string
label: WGS Somatic (GATK only)
outputs:
  normalBam:
    id: normalBam
    outputSource: normal/out
    secondaryFiles:
    - ^.bai
    type: File
  normalReport:
    id: normalReport
    outputSource: normal/reports
    type:
      items:
        items: File
        type: array
      type: array
  tumorBam:
    id: tumorBam
    outputSource: tumor/out
    secondaryFiles:
    - ^.bai
    type: File
  tumorReport:
    id: tumorReport
    outputSource: tumor/reports
    type:
      items:
        items: File
        type: array
      type: array
  variants_gatk:
    id: variants_gatk
    outputSource: sorted/out
    type: File
requirements:
  InlineJavascriptRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
steps:
  normal:
    in:
      reads:
        id: reads
        source: tumorInputs
      reference:
        id: reference
        source: reference
      sampleName:
        id: sampleName
        source: tumorName
    out:
    - out
    - reports
    run: tools/somatic_subpipeline.cwl
  sorted:
    in:
      vcf:
        id: vcf
        source: variantCaller_GATK_merge/out
    out:
    - out
    run: tools/bcftoolssort.cwl
  tumor:
    in:
      reads:
        id: reads
        source: normalInputs
      reference:
        id: reference
        source: reference
      sampleName:
        id: sampleName
        source: normalName
    out:
    - out
    - reports
    run: tools/somatic_subpipeline.cwl
  variantCaller_GATK:
    in:
      intervals:
        id: intervals
        source: gatkIntervals
      knownIndels:
        id: knownIndels
        source: known_indels
      millsIndels:
        id: millsIndels
        source: mills_indels
      normalBam:
        id: normalBam
        source: tumor/out
      normalName:
        id: normalName
        source: normalName
      reference:
        id: reference
        source: reference
      snps_1000gp:
        id: snps_1000gp
        source: snps_1000gp
      snps_dbsnp:
        id: snps_dbsnp
        source: snps_dbsnp
      tumorBam:
        id: tumorBam
        source: normal/out
      tumorName:
        id: tumorName
        source: tumorName
    out:
    - out
    run: tools/GATK4_SomaticVariantCaller.cwl
    scatter:
    - intervals
  variantCaller_GATK_merge:
    in:
      vcfs:
        id: vcfs
        source: variantCaller_GATK/out
    out:
    - out
    run: tools/Gatk4GatherVcfs.cwl
