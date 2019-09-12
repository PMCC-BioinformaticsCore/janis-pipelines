class: Workflow
cwlVersion: v1.0
id: WGSGermlineGATK
inputs:
  alignSortedBam_sortsam_tmpDir:
    id: alignSortedBam_sortsam_tmpDir
    type:
    - string
    - 'null'
  fastqs:
    id: fastqs
    type:
      items:
        items: File
        type: array
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
  sampleName:
    default: NA12878
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
label: WGS Germline (GATK only)
outputs:
  bam:
    id: bam
    outputSource: processBamFiles/out
    secondaryFiles:
    - ^.bai
    type: File
  reports:
    id: reports
    outputSource: fastqc/out
    type:
      items:
        items: File
        type: array
      type: array
  variants:
    id: variants
    outputSource: sortCombined/out
    type: File
  variants_split:
    id: variants_split
    outputSource: variantCaller_GATK/out
    type:
      items: File
      type: array
requirements:
  InlineJavascriptRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
steps:
  alignSortedBam:
    in:
      fastq:
        id: fastq
        source: fastqs
      name:
        id: name
        source: sampleName
      reference:
        id: reference
        source: reference
      sortsam_tmpDir:
        id: sortsam_tmpDir
        source: alignSortedBam_sortsam_tmpDir
    out:
    - out
    run: tools/BwaAligner.cwl
    scatter:
    - fastq
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
    run: tools/mergeAndMarkBams.cwl
  sortCombined:
    in:
      vcf:
        id: vcf
        source: variantCaller_merge_GATK/out
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
        source: mills_indels
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
    run: tools/GATK4_GermlineVariantCaller.cwl
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
