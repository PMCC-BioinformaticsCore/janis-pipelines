#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
doc: "This is a genomics pipeline which:\n\n- Call the appropriate variant callers\
  \ (GATK / Strelka / VarDict);\n- Outputs the final variants in the VCF format.\n\
  \n**Resources**\n\nThis pipeline has been tested using the HG38 reference set, available\
  \ on Google Cloud Storage through:\n\n- https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/\n\
  \nThis pipeline expects the assembly references to be as they appear in that storage\
  \     (\".fai\", \".amb\", \".ann\", \".bwt\", \".pac\", \".sa\", \"^.dict\").\n\
  The known sites (snps_dbsnp, snps_1000gp, known_indels, mills_indels) should be\
  \ gzipped and tabix indexed.\n"
id: WGSGermlineMultiCallersVariantsOnly
inputs:
  allele_freq_threshold:
    default: 0.05
    doc: "The threshold for VarDict's allele frequency, default: 0.05 or 5%"
    id: allele_freq_threshold
    type: float
  bam:
    doc: An array of FastqGz pairs. These are aligned separately and merged to create
      higher depth coverages from multiple sets of reads
    id: bam
    secondaryFiles:
    - .bai
    type: File
  combine_variants_columns:
    default:
    - AC
    - AN
    - AF
    - AD
    - DP
    - GT
    doc: Columns to keep, seperated by space output vcf (unsorted)
    id: combine_variants_columns
    type:
      items: string
      type: array
  combine_variants_type:
    default: germline
    doc: germline | somatic
    id: combine_variants_type
    type: string
  cutadapt_adapters:
    doc: 'Specifies a file which contains a list of sequences to determine valid overrepresented
      sequences from the FastQC report to trim with Cuatadapt. The file must contain
      sets of named adapters in the form: ``name[tab]sequence``. Lines prefixed with
      a hash will be ignored.'
    id: cutadapt_adapters
    type:
    - File
    - 'null'
  gatk_intervals:
    doc: List of intervals over which to split the GATK variant calling
    id: gatk_intervals
    type:
      items: File
      type: array
  header_lines:
    doc: Header lines passed to BCFTools annotate as ``--header-lines``.
    id: header_lines
    type:
    - File
    - 'null'
  known_indels:
    doc: From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``
    id: known_indels
    secondaryFiles:
    - .tbi
    type: File
  mills_indels:
    doc: From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``
    id: mills_indels
    secondaryFiles:
    - .tbi
    type: File
  reference:
    doc: The reference genome from which to align the reads. This requires a number
      indexes (can be generated with the 'IndexFasta' pipeline. This pipeline has
      been tested with the hg38 reference genome.
    id: reference
    secondaryFiles:
    - .fai
    - .amb
    - .ann
    - .bwt
    - .pac
    - .sa
    - ^.dict
    type: File
  sample_name:
    doc: Sample name from which to generate the readGroupHeaderLine for BwaMem
    id: sample_name
    type: string
  snps_1000gp:
    doc: From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``
    id: snps_1000gp
    secondaryFiles:
    - .tbi
    type: File
  snps_dbsnp:
    doc: From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``
    id: snps_dbsnp
    secondaryFiles:
    - .tbi
    type: File
  strelka_intervals:
    doc: 'An interval for which to restrict the analysis to. Recommended HG38 interval: '
    id: strelka_intervals
    secondaryFiles:
    - .tbi
    type: File
  vardict_intervals:
    doc: List of intervals over which to split the VarDict variant calling
    id: vardict_intervals
    type:
      items: File
      type: array
label: WGS Germline (Multi callers) [VARIANTS ONLY]
outputs:
  variants_combined:
    doc: Combined variants from all 3 callers
    id: variants_combined
    outputSource: sort_combined/out
    type: File
  variants_gatk:
    doc: Merged variants from the GATK caller
    id: variants_gatk
    outputSource: vc_gatk_merge/out
    type: File
  variants_gatk_split:
    doc: Unmerged variants from the GATK caller (by interval)
    id: variants_gatk_split
    outputSource: vc_gatk/out
    type:
      items: File
      type: array
  variants_strelka:
    doc: Variants from the Strelka variant caller
    id: variants_strelka
    outputSource: vc_strelka/out
    type: File
  variants_vardict:
    doc: Merged variants from the VarDict caller
    id: variants_vardict
    outputSource: vc_vardict_merge/out
    type: File
  variants_vardict_split:
    doc: Unmerged variants from the VarDict caller (by interval)
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
        source: bam
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
        source: bam
      intervals:
        id: intervals
        source: strelka_intervals
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
        source: bam
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
