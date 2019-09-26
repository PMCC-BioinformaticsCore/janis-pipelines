class: Workflow
cwlVersion: v1.0
id: WGSSomaticMultiCallers
inputs:
  alleleFreqThreshold:
    default: 0.05
    id: alleleFreqThreshold
    type: float
  combineVariants_columns:
    default:
    - AD
    - DP
    - GT
    id: combineVariants_columns
    type:
      items: string
      type: array
  combineVariants_type:
    default: somatic
    id: combineVariants_type
    type: string
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
      items:
        items: File
        type: array
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
  strelkaIntervals:
    id: strelkaIntervals
    secondaryFiles:
    - .tbi
    type:
    - File
    - 'null'
  tumorInputs:
    id: tumorInputs
    type:
      items:
        items: File
        type: array
      type: array
  tumorName:
    default: NA24385_tumour
    id: tumorName
    type: string
  vardictHeaderLines:
    id: vardictHeaderLines
    type: File
  vardictIntervals:
    id: vardictIntervals
    type:
      items: File
      type: array
label: WGS Somatic (Multi callers)
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
  variants_combined:
    id: variants_combined
    outputSource: combineVariants/vcf
    type: File
  variants_gatk:
    id: variants_gatk
    outputSource: variantCaller_merge_GATK/out
    type: File
  variants_strelka:
    id: variants_strelka
    outputSource: variantCaller_Strelka/out
    type: File
  variants_vardict:
    id: variants_vardict
    outputSource: variantCaller_merge_VarDict/out
    type: File
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
steps:
  combineVariants:
    in:
      columns:
        id: columns
        source: combineVariants_columns
      normal:
        id: normal
        source: normalName
      tumor:
        id: tumor
        source: tumorName
      type:
        id: type
        source: combineVariants_type
      vcfs:
        id: vcfs
        source:
        - variantCaller_merge_VarDict/out
        - variantCaller_Strelka/out
        - variantCaller_merge_GATK/out
    out:
    - vcf
    - tsv
    run: tools/combinevariants.cwl
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
  sortCombined:
    in:
      vcf:
        id: vcf
        source: combineVariants/vcf
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
  variantCaller_Strelka:
    in:
      intervals:
        id: intervals
        source: strelkaIntervals
      normalBam:
        id: normalBam
        source: normal/out
      reference:
        id: reference
        source: reference
      tumorBam:
        id: tumorBam
        source: tumor/out
    out:
    - diploid
    - variants
    - out
    run: tools/strelkaSomaticVariantCaller.cwl
  variantCaller_VarDict:
    in:
      alleleFreqThreshold:
        id: alleleFreqThreshold
        source: alleleFreqThreshold
      headerLines:
        id: headerLines
        source: vardictHeaderLines
      intervals:
        id: intervals
        source: vardictIntervals
      normalBam:
        id: normalBam
        source: tumor/out
      normalName:
        id: normalName
        source: normalName
      reference:
        id: reference
        source: reference
      tumorBam:
        id: tumorBam
        source: normal/out
      tumorName:
        id: tumorName
        source: tumorName
    out:
    - vardictVariants
    - out
    run: tools/vardictSomaticVariantCaller.cwl
    scatter:
    - intervals
  variantCaller_merge_GATK:
    in:
      vcfs:
        id: vcfs
        source: variantCaller_GATK/out
    out:
    - out
    run: tools/Gatk4GatherVcfs.cwl
  variantCaller_merge_VarDict:
    in:
      vcfs:
        id: vcfs
        source: variantCaller_VarDict/out
    out:
    - out
    run: tools/Gatk4GatherVcfs.cwl
