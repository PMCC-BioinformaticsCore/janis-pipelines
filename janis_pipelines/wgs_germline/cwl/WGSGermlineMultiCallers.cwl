class: Workflow
cwlVersion: v1.0
id: WGSGermlineMultiCallers
inputs:
  align_and_sort_sortsam_tmpDir:
    default: ./tmp
    id: align_and_sort_sortsam_tmpDir
    type: string
  allele_freq_threshold:
    default: 0.05
    id: allele_freq_threshold
    type: float
  combine_variants_columns:
    default:
    - AC
    - AN
    - AF
    - AD
    - DP
    - GT
    id: combine_variants_columns
    type:
      items: string
      type: array
  combine_variants_type:
    default: germline
    id: combine_variants_type
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
  header_lines:
    id: header_lines
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
    id: snps_dbsnp
    secondaryFiles:
    - .tbi
    type: File
  strelkaIntervals:
    id: strelkaIntervals
    secondaryFiles:
    - .tbi
    type: File
  vardict_intervals:
    id: vardict_intervals
    type:
      items: File
      type: array
label: WGS Germline (Multi callers)
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
  variants_combined:
    id: variants_combined
    outputSource: sort_combined/out
    type: File
  variants_gatk:
    id: variants_gatk
    outputSource: vc_gatk_merge/out
    type: File
  variants_gatk_split:
    id: variants_gatk_split
    outputSource: vc_gatk/out
    type:
      items: File
      type: array
  variants_strelka:
    id: variants_strelka
    outputSource: vc_strelka/out
    type: File
  variants_vardict:
    id: variants_vardict
    outputSource: vc_vardict_merge/out
    type: File
  variants_vardict_split:
    id: variants_vardict_split
    outputSource: vc_vardict/out
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
  combine_variants:
    in:
      columns:
        id: columns
        source: combine_variants_columns
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
        source: combine_variants/vcf
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
  vc_strelka:
    in:
      bam:
        id: bam
        source: merge_and_mark/out
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
  vc_vardict:
    in:
      allele_freq_threshold:
        id: allele_freq_threshold
        source: allele_freq_threshold
      bam:
        id: bam
        source: merge_and_mark/out
      header_lines:
        id: header_lines
        source: header_lines
      intervals:
        id: intervals
        source: vardict_intervals
      reference:
        id: reference
        source: reference
      sample_name:
        id: sample_name
        source: sample_name
    out:
    - vardict_variants
    - out
    run: tools/vardictGermlineVariantCaller.cwl
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
