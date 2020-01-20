class: Workflow
cwlVersion: v1.0
id: WGSGermlineGATK
inputs:
  align_and_sort_sortsam_tmpDir:
    default: .
    id: align_and_sort_sortsam_tmpDir
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
  gatk_intervals:
    id: gatk_intervals
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
  sample_name:
    default: NA12878
    id: sample_name
    type: string
  snps_1000gp:
    id: snps_1000gp
    secondaryFiles:
    - .tbi
    type: File
  snps_dbsnp:
    doc: ''
    id: snps_dbsnp
    secondaryFiles:
    - .tbi
    type: File
label: WGS Germline (GATK only)
outputs:
  bam:
    id: bam
    outputSource: merge_and_mark/out
    secondaryFiles:
    - .bai
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
    outputSource: sort_combined/out
    type: File
  variants_split:
    id: variants_split
    outputSource: vc_gatk/out
    type:
      items: File
      type: array
requirements:
  InlineJavascriptRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
steps:
  align_and_sort:
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
      sample_name:
        id: sample_name
        source: sample_name
      sortsam_tmpDir:
        id: sortsam_tmpDir
        source: align_and_sort_sortsam_tmpDir
    out:
    - out
    run: tools/BwaAligner.cwl
    scatter:
    - fastq
    - cutadapt_adapter
    - cutadapt_removeMiddle3Adapter
    scatterMethod: dotproduct
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
  merge_and_mark:
    in:
      bams:
        id: bams
        source: align_and_sort/out
    out:
    - out
    run: tools/mergeAndMarkBams.cwl
  sort_combined:
    in:
      vcf:
        id: vcf
        source: vc_gatk_merge/out
    out:
    - out
    run: tools/bcftoolssort.cwl
  vc_gatk:
    in:
      bam:
        id: bam
        source: merge_and_mark/out
      intervals:
        id: intervals
        source: gatk_intervals
      known_indels:
        id: known_indels
        source: known_indels
      mills_indels:
        id: mills_indels
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
  vc_gatk_merge:
    in:
      vcfs:
        id: vcfs
        source: vc_gatk/out
    out:
    - out
    run: tools/Gatk4GatherVcfs.cwl
