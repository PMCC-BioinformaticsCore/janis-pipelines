class: Workflow
cwlVersion: v1.0
id: WGSSomaticGATK
inputs:
  cutadapt_adapters:
    id: cutadapt_adapters
    type: File
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
  normal_inputs:
    id: normal_inputs
    type:
      items:
        items: File
        type: array
      type: array
  normal_name:
    default: NA24385_normal
    id: normal_name
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
  tumor_inputs:
    id: tumor_inputs
    type:
      items:
        items: File
        type: array
      type: array
  tumor_name:
    default: NA24385_tumour
    id: tumor_name
    type: string
label: WGS Somatic (GATK only)
outputs:
  normal_bam:
    id: normal_bam
    outputSource: normal/out
    secondaryFiles:
    - .bai
    type: File
  normal_report:
    id: normal_report
    outputSource: normal/reports
    type:
      items:
        items: File
        type: array
      type: array
  tumor_bam:
    id: tumor_bam
    outputSource: tumor/out
    secondaryFiles:
    - .bai
    type: File
  tumor_report:
    id: tumor_report
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
      cutadapt_adapters:
        id: cutadapt_adapters
        source: cutadapt_adapters
      reads:
        id: reads
        source: tumor_inputs
      reference:
        id: reference
        source: reference
      sample_name:
        id: sample_name
        source: tumor_name
    out:
    - out
    - reports
    run: tools/somatic_subpipeline.cwl
  sorted:
    in:
      vcf:
        id: vcf
        source: vc_gatk_merge/out
    out:
    - out
    run: tools/bcftoolssort.cwl
  tumor:
    in:
      cutadapt_adapters:
        id: cutadapt_adapters
        source: cutadapt_adapters
      reads:
        id: reads
        source: normal_inputs
      reference:
        id: reference
        source: reference
      sample_name:
        id: sample_name
        source: normal_name
    out:
    - out
    - reports
    run: tools/somatic_subpipeline.cwl
  vc_gatk:
    in:
      intervals:
        id: intervals
        source: gatk_intervals
      known_indels:
        id: known_indels
        source: known_indels
      mills_indels:
        id: mills_indels
        source: mills_indels
      normal_bam:
        id: normal_bam
        source: tumor/out
      normal_name:
        id: normal_name
        source: normal_name
      reference:
        id: reference
        source: reference
      snps_1000gp:
        id: snps_1000gp
        source: snps_1000gp
      snps_dbsnp:
        id: snps_dbsnp
        source: snps_dbsnp
      tumor_bam:
        id: tumor_bam
        source: normal/out
      tumor_name:
        id: tumor_name
        source: tumor_name
    out:
    - out
    run: tools/GATK4_SomaticVariantCaller.cwl
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
