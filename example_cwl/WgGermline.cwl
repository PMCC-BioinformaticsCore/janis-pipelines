class: Workflow
cwlVersion: v1.0
id: WgGermline
inputs:
  allelFreqThreshold:
    id: allelFreqThreshold
    type: float
  columns:
    default:
    - AC
    - AN
    - AF
    - AD
    - DP
    - GT
    id: columns
    type:
      items: string
      type: array
  fastqs:
    id: fastqs
    type:
      items:
        items: File
        type: array
      type: array
  gatkIntervals:
    default:
    - null
    id: gatkIntervals
    type:
      items:
      - File
      - 'null'
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
  sampleName:
    id: sampleName
    type: string
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
  vardictHeaderLines:
    id: vardictHeaderLines
    type: File
  vardictIntervals:
    id: vardictIntervals
    type:
      items: File
      type: array
  variant_type:
    default: germline
    id: variant_type
    type: string
outputs:
  bam:
    id: bam
    outputSource: processBamFiles/out
    secondaryFiles:
    - ^.bai
    type: File
  combinedVariants:
    id: combinedVariants
    outputSource: sortCombined/out
    type: File
  reports:
    id: reports
    outputSource: fastqc/out
    type:
      items:
        items: File
        type: array
      type: array
  variants_gatk:
    id: variants_gatk
    outputSource: variantCaller_merge_GATK/out
    type: File
  variants_gatk_split:
    id: variants_gatk_split
    outputSource: variantCaller_GATK/out
    type:
      items: File
      type: array
  variants_strelka:
    id: variants_strelka
    outputSource: variantCaller_Strelka/out
    type: File
  variants_vardict:
    id: variants_vardict
    outputSource: variantCaller_merge_Vardict/out
    type: File
  variants_vardict_split:
    id: variants_vardict_split
    outputSource: variantCaller_Vardict/out
    type:
      items: File
      type: array
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
steps:
  alignSortedBam:
    in:
      fastq:
        id: fastq
        source: fastqs
      reference:
        id: reference
        source: reference
      sampleName:
        id: sampleName
        source: sampleName
    out:
    - out_bwa
    - out
    run: tools/alignsortedbam.cwl
    scatter:
    - fastq
  combineVariants:
    in:
      columns:
        id: columns
        source: columns
      type:
        id: type
        source: variant_type
      vcfs:
        id: vcfs
        source:
        - variantCaller_merge_GATK/out
        - variantCaller_Strelka/out
        - variantCaller_merge_Vardict/out
    out:
    - vcf
    - tsv
    run: tools/combinevariants.cwl
  fastqc:
    in:
      reads:
        id: reads
        source: fastqs
    out:
    - out
    run: tools/fastqc.cwl
    scatter:
    - reads
  processBamFiles:
    in:
      bams:
        id: bams
        source: alignSortedBam/out
    out:
    - out
    run: tools/processbamfiles.cwl
  sortCombined:
    in:
      vcf:
        id: vcf
        source: combineVariants/vcf
    out:
    - out
    run: tools/bcftoolssort.cwl
  variantCaller_GATK:
    in:
      bam:
        id: bam
        source: processBamFiles/out
      intervals:
        id: intervals
        source: gatkIntervals
      knownIndels:
        id: knownIndels
        source: known_indels
      millsIndels:
        id: millsIndels
        source: mills_1000gp_indels
      reference:
        id: reference
        source: reference
      snps_1000gp:
        id: snps_1000gp
        source: snps_1000gp
      snps_dbsnp:
        id: snps_dbsnp
        source: snps_dbsnp
    out:
    - out
    run: tools/GATK4_VariantCaller.cwl
    scatter:
    - intervals
  variantCaller_Strelka:
    in:
      bam:
        id: bam
        source: processBamFiles/out
      reference:
        id: reference
        source: reference
    out:
    - diploid
    - variants
    - out
    run: tools/strelkaGermlineVariantCaller.cwl
  variantCaller_Vardict:
    in:
      allelFreqThreshold:
        id: allelFreqThreshold
        source: allelFreqThreshold
      bam:
        id: bam
        source: processBamFiles/out
      headerLines:
        id: headerLines
        source: vardictHeaderLines
      intervals:
        id: intervals
        source: vardictIntervals
      reference:
        id: reference
        source: reference
      sampleName:
        id: sampleName
        source: sampleName
    out:
    - vardictVariants
    - out
    run: tools/vardictVariantCaller.cwl
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
  variantCaller_merge_Vardict:
    in:
      vcfs:
        id: vcfs
        source: variantCaller_Vardict/out
    out:
    - out
    run: tools/Gatk4GatherVcfs.cwl
