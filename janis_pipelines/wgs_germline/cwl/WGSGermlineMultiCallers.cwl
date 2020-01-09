class: Workflow
cwlVersion: v1.0
id: WGSGermlineMultiCallers
inputs:
  alignSortedBam_sortsam_tmpDir:
    default: ./tmp
    id: alignSortedBam_sortsam_tmpDir
    type: string
  alleleFreqThreshold:
    default: 0.05
    id: alleleFreqThreshold
    type: float
  combineVariants_columns:
    default:
    - AC
    - AN
    - AF
    - AD
    - DP
    - GT
    id: combineVariants_columns
    type:
      items: string
      type: array
  combineVariants_type:
    default: germline
    id: combineVariants_type
    type: string
  cutadapt_adapters:
    id: cutadapt_adapters
    type: File
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
  strelkaIntervals:
    id: strelkaIntervals
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
label: WGS Germline (Multi callers)
outputs:
  bam:
    id: bam
    outputSource: processBamFiles/out
    secondaryFiles:
    - .bai
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
      cutadapt_adapter:
        id: cutadapt_adapter
        source: getfastqc_adapters/adaptor_sequences
      cutadapt_removeMiddle3Adapter:
        id: cutadapt_removeMiddle3Adapter
        source: getfastqc_adapters/adaptor_sequences
      fastq:
        id: fastq
        source: fastqs
      reference:
        id: reference
        source: reference
      sampleName:
        id: sampleName
        source: sampleName
      sortsam_tmpDir:
        id: sortsam_tmpDir
        source: alignSortedBam_sortsam_tmpDir
    out:
    - out
    run: tools/BwaAligner.cwl
    scatter:
    - fastq
    - cutadapt_adapter
    - cutadapt_removeMiddle3Adapter
    scatterMethod: dotproduct
  combineVariants:
    in:
      columns:
        id: columns
        source: combineVariants_columns
      type:
        id: type
        source: combineVariants_type
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
    - datafile
    run: tools/fastqc.cwl
    scatter:
    - reads
  getfastqc_adapters:
    in:
      cutadapt_adaptors_lookup:
        id: cutadapt_adaptors_lookup
        source: cutadapt_adapters
      fastqc_datafiles:
        id: fastqc_datafiles
        source: fastqc/datafile
    out:
    - adaptor_sequences
    run: tools/ParseFastqcAdaptors.cwl
    scatter:
    - fastqc_datafiles
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
  variantCaller_Strelka:
    in:
      bam:
        id: bam
        source: processBamFiles/out
      intervals:
        id: intervals
        source: strelkaIntervals
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
      alleleFreqThreshold:
        id: alleleFreqThreshold
        source: alleleFreqThreshold
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
    run: tools/vardictGermlineVariantCaller.cwl
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
