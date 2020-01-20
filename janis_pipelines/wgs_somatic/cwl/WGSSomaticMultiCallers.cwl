class: Workflow
cwlVersion: v1.0
id: WGSSomaticMultiCallers
inputs:
  allele_freq_threshold:
    default: 0.05
    id: allele_freq_threshold
    type: float
  combine_variants_columns:
    default:
    - AD
    - DP
    - GT
    id: combine_variants_columns
    type:
      items: string
      type: array
  combine_variants_type:
    default: somatic
    id: combine_variants_type
    type: string
  cutadapt_adapters:
    id: cutadapt_adapters
    type: File
  gatk_intervals:
    id: gatk_intervals
    type:
      items: File
      type: array
  gridss_blacklist:
    id: gridss_blacklist
    type: File
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
  strelka_intervals:
    id: strelka_intervals
    secondaryFiles:
    - .tbi
    type:
    - File
    - 'null'
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
  vardict_header_lines:
    id: vardict_header_lines
    type: File
  vardict_intervals:
    id: vardict_intervals
    type:
      items: File
      type: array
label: WGS Somatic (Multi callers)
outputs:
  gridss_assembly:
    id: gridss_assembly
    outputSource: vc_gridss/out
    type: File
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
  variants_combined:
    id: variants_combined
    outputSource: combine_variants/vcf
    type: File
  variants_gatk:
    id: variants_gatk
    outputSource: vc_gatk_merge/out
    type: File
  variants_gridss:
    id: variants_gridss
    outputSource: vc_gridss/out
    type: File
  variants_strelka:
    id: variants_strelka
    outputSource: vc_strelka/out
    type: File
  variants_vardict:
    id: variants_vardict
    outputSource: vc_vardict_merge/out
    type: File
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
steps:
  combine_variants:
    in:
      columns:
        id: columns
        source: combine_variants_columns
      normal:
        id: normal
        source: normal_name
      tumor:
        id: tumor
        source: tumor_name
      type:
        id: type
        source: combine_variants_type
      vcfs:
        id: vcfs
        source:
        - vc_gatk_merge/out
        - vc_strelka/out
        - vc_vardict_merge/out
    out:
    - vcf
    - tsv
    run: tools/combinevariants.cwl
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
  sortCombined:
    in:
      vcf:
        id: vcf
        source: combine_variants/vcf
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
  vc_gridss:
    in:
      bams:
        id: bams
        source:
        - normal/out
        - tumor/out
      blacklist:
        id: blacklist
        source: gridss_blacklist
      reference:
        id: reference
        source: reference
    out:
    - out
    - assembly
    run: tools/gridss.cwl
  vc_strelka:
    in:
      intervals:
        id: intervals
        source: strelka_intervals
      normal_bam:
        id: normal_bam
        source: normal/out
      reference:
        id: reference
        source: reference
      tumor_bam:
        id: tumor_bam
        source: tumor/out
    out:
    - diploid
    - variants
    - out
    run: tools/strelkaSomaticVariantCaller.cwl
  vc_vardict:
    in:
      allele_freq_threshold:
        id: allele_freq_threshold
        source: allele_freq_threshold
      header_lines:
        id: header_lines
        source: vardict_header_lines
      intervals:
        id: intervals
        source: vardict_intervals
      normal_bam:
        id: normal_bam
        source: tumor/out
      normal_name:
        id: normal_name
        source: normal_name
      reference:
        id: reference
        source: reference
      tumor_bam:
        id: tumor_bam
        source: normal/out
      tumor_name:
        id: tumor_name
        source: tumor_name
    out:
    - vardict_variants
    - out
    run: tools/vardictSomaticVariantCaller.cwl
    scatter:
    - intervals
  vc_vardict_merge:
    in:
      vcfs:
        id: vcfs
        source: vc_vardict/out
    out:
    - out
    run: tools/Gatk4GatherVcfs.cwl
