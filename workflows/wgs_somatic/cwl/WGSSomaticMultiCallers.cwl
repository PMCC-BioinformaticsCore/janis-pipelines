class: Workflow
cwlVersion: v1.0
id: WGSSomaticMultiCallers
inputs:
  allelFreqThreshold:
    id: allelFreqThreshold
    type: float
  columns:
    default:
    - AD
    - DP
    - GT
    id: columns
    type:
      items: string
      type: array
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
  mills_1000gp_indels:
    id: mills_1000gp_indels
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
  sortSamTmpDir:
    id: sortSamTmpDir
    type:
    - string
    - 'null'
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
  variant_type:
    default: somatic
    id: variant_type
    type: string
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
    outputSource: normal/fastq
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
    outputSource: tumor/fastq
    type:
      items:
        items: File
        type: array
      type: array
  variants_combined:
    id: variants_combined
    outputSource: sortCombined/out
    type: File
  variants_gatk:
    id: variants_gatk
    outputSource: variantCaller_merge_GATK/out
    type: File
  variants_strelka:
    id: variants_strelka
    outputSource: Strelka_VariantCaller/out
    type: File
  variants_vardict:
    id: variants_vardict
    outputSource: variantCaller_merge_Vardict/out
    type: File
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
steps:
  GATK_VariantCaller:
    in:
      intervals:
        id: intervals
        source: gatkIntervals
      knownIndels:
        id: knownIndels
        source: known_indels
      millsIndels:
        id: millsIndels
        source: mills_1000gp_indels
      normalBam:
        id: normalBam
        source: normal/out
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
        source: tumor/out
      tumorName:
        id: tumorName
        source: tumorName
    out:
    - out
    run: tools/GATK4_SomaticVariantCaller.cwl
    scatter:
    - intervals
  Strelka_VariantCaller:
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
  VarDict_VariantCaller:
    in:
      alleleFreqThreshold:
        id: alleleFreqThreshold
        source: allelFreqThreshold
      headerLines:
        id: headerLines
        source: vardictHeaderLines
      intervals:
        id: intervals
        source: vardictIntervals
      normalBam:
        id: normalBam
        source: normal/out
      normalName:
        id: normalName
        source: normalName
      reference:
        id: reference
        source: reference
      tumorBam:
        id: tumorBam
        source: tumor/out
      tumorName:
        id: tumorName
        source: tumorName
    out:
    - vardictVariants
    - out
    run: tools/vardictSomaticVariantCaller.cwl
    scatter:
    - intervals
  combineVariants:
    in:
      columns:
        id: columns
        source: columns
      normal:
        id: normal
        source: normalName
      tumor:
        id: tumor
        source: tumorName
      type:
        id: type
        source: variant_type
      vcfs:
        id: vcfs
        source:
        - variantCaller_merge_GATK/out
        - Strelka_VariantCaller/out
        - variantCaller_merge_Vardict/out
    out:
    - vcf
    - tsv
    run: tools/combinevariants.cwl
  normal:
    in:
      inputs:
        id: inputs
        source: normalInputs
      reference:
        id: reference
        source: reference
      sampleName:
        id: sampleName
        source: normalName
      sortSamTmpDir:
        id: sortSamTmpDir
        source: sortSamTmpDir
    out:
    - out
    - fastq
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
      inputs:
        id: inputs
        source: tumorInputs
      reference:
        id: reference
        source: reference
      sampleName:
        id: sampleName
        source: tumorName
      sortSamTmpDir:
        id: sortSamTmpDir
        source: sortSamTmpDir
    out:
    - out
    - fastq
    run: tools/somatic_subpipeline.cwl
  variantCaller_merge_GATK:
    in:
      vcfs:
        id: vcfs
        linkMerge: merge_nested
        source:
        - GATK_VariantCaller/out
    out:
    - out
    run: tools/Gatk4GatherVcfs.cwl
  variantCaller_merge_Vardict:
    in:
      vcfs:
        id: vcfs
        linkMerge: merge_nested
        source:
        - VarDict_VariantCaller/out
    out:
    - out
    run: tools/Gatk4GatherVcfs.cwl
