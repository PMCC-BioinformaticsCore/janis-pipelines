#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: WGS Somatic (Multi callers)
doc: |
  This is a genomics pipeline to align sequencing data (Fastq pairs) into BAMs:

  - Takes raw sequence data in the FASTQ format;
  - align to the reference genome using BWA MEM;
  - Marks duplicates using Picard;
  - Call the appropriate somatic variant callers (GATK / Strelka / VarDict);
  - Outputs the final variants in the VCF format.

  **Resources**

  This pipeline has been tested using the HG38 reference set, available on Google Cloud Storage through:

  - https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/

  This pipeline expects the assembly references to be as they appear in that storage     (".fai", ".amb", ".ann", ".bwt", ".pac", ".sa", "^.dict").
  The known sites (snps_dbsnp, snps_1000gp, known_indels, mills_indels) should be gzipped and tabix indexed.

requirements:
- class: InlineJavascriptRequirement
- class: StepInputExpressionRequirement
- class: ScatterFeatureRequirement
- class: SubworkflowFeatureRequirement
- class: MultipleInputFeatureRequirement

inputs:
- id: normal_inputs
  doc: |-
    An array of NORMAL FastqGz pairs. These are aligned separately and merged to create higher depth coverages from multiple sets of reads
  type:
    type: array
    items:
      type: array
      items: File
- id: tumor_inputs
  doc: |-
    An array of TUMOR FastqGz pairs. These are aligned separately and merged to create higher depth coverages from multiple sets of reads
  type:
    type: array
    items:
      type: array
      items: File
- id: normal_name
  doc: |-
    Sample name for the NORMAL sample from which to generate the readGroupHeaderLine for BwaMem
  type: string
- id: tumor_name
  doc: |-
    Sample name for the TUMOR sample from which to generate the readGroupHeaderLine for BwaMem
  type: string
- id: cutadapt_adapters
  doc: |-
    Specifies a containment list for cutadapt, which contains a list of sequences to determine valid overrepresented sequences from the FastQC report to trim with Cuatadapt. The file must contain sets of named adapters in the form: ``name[tab]sequence``. Lines prefixed with a hash will be ignored.
  type:
  - File
  - 'null'
- id: gatk_intervals
  doc: List of intervals over which to split the GATK variant calling
  type:
    type: array
    items: File
- id: genome_file
  doc: Genome file for bedtools query
  type: File
- id: gridss_blacklist
  doc: BED file containing regions to ignore.
  type: File
- id: vardict_intervals
  doc: List of intervals over which to split the VarDict variant calling
  type:
    type: array
    items: File
- id: strelka_intervals
  doc: An interval for which to restrict the analysis to.
  type: File
  secondaryFiles:
  - .tbi
- id: allele_freq_threshold
  doc: "The threshold for VarDict's allele frequency, default: 0.05 or 5%"
  type: float
  default: 0.05
- id: reference
  doc: |-
    The reference genome from which to align the reads. This requires a number indexes (can be generated with the 'IndexFasta' pipeline This pipeline has been tested using the HG38 reference set.

    This pipeline expects the assembly references to be as they appear in the GCP example:

    - (".fai", ".amb", ".ann", ".bwt", ".pac", ".sa", "^.dict").
  type: File
  secondaryFiles:
  - .fai
  - .amb
  - .ann
  - .bwt
  - .pac
  - .sa
  - ^.dict
- id: snps_dbsnp
  doc: From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``
  type: File
  secondaryFiles:
  - .tbi
- id: snps_1000gp
  doc: From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``
  type: File
  secondaryFiles:
  - .tbi
- id: known_indels
  doc: From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``
  type: File
  secondaryFiles:
  - .tbi
- id: mills_indels
  doc: From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``
  type: File
  secondaryFiles:
  - .tbi
- id: gnomad
  doc: The genome Aggregation Database (gnomAD)
  type: File
  secondaryFiles:
  - .tbi
- id: panel_of_normals
  doc: VCF file of sites observed in normal.
  type:
  - File
  - 'null'
  secondaryFiles:
  - .tbi
- id: combine_variants_type
  doc: germline | somatic
  type: string
  default: somatic
- id: combine_variants_columns
  doc: Columns to keep, seperated by space output vcf (unsorted)
  type:
    type: array
    items: string
  default:
  - AD
  - DP
  - GT

outputs:
- id: normal_report
  type:
    type: array
    items:
      type: array
      items: File
  outputSource: normal/reports
- id: tumor_report
  type:
    type: array
    items:
      type: array
      items: File
  outputSource: tumor/reports
- id: normal_coverage
  doc: A text file of depth of coverage summary of NORMAL bam
  type: File
  outputSource: normal/depth_of_coverage
- id: tumor_coverage
  doc: A text file of depth of coverage summary of TUMOR bam
  type: File
  outputSource: tumor/depth_of_coverage
- id: normal_summary
  doc: A text file of performance summary of NORMAL bam
  type: File
  outputSource: normal/summary
- id: tumor_summary
  doc: A text file of performance summary of TUMOR bam
  type: File
  outputSource: tumor/summary
- id: gridss_assembly
  doc: Assembly returned by GRIDSS
  type: File
  outputSource: vc_gridss/assembly
- id: variants_gridss
  doc: Variants from the GRIDSS variant caller
  type: File
  outputSource: vc_gridss/out
- id: normal_bam
  type: File
  secondaryFiles:
  - .bai
  outputSource: normal/out
- id: tumor_bam
  type: File
  secondaryFiles:
  - .bai
  outputSource: tumor/out
- id: variants_gatk
  doc: Merged variants from the GATK caller
  type: File
  outputSource: vc_gatk_sort_combined/out
- id: variants_vardict
  doc: Merged variants from the VarDict caller
  type: File
  outputSource: vc_vardict_sort_combined/out
- id: variants_strelka
  doc: Variants from the Strelka variant caller
  type: File
  outputSource: vc_strelka/out
- id: variants_gatk_split
  doc: Unmerged variants from the GATK caller (by interval)
  type:
    type: array
    items: File
  outputSource: vc_gatk/out
- id: variants_vardict_split
  doc: Unmerged variants from the VarDict caller (by interval)
  type:
    type: array
    items: File
  outputSource: vc_vardict/out

steps:
- id: tumor
  in:
  - id: reads
    source: tumor_inputs
  - id: sample_name
    source: tumor_name
  - id: reference
    source: reference
  - id: cutadapt_adapters
    source: cutadapt_adapters
  - id: gatk_intervals
    source: gatk_intervals
  - id: genome_file
    source: genome_file
  - id: snps_dbsnp
    source: snps_dbsnp
  - id: snps_1000gp
    source: snps_1000gp
  - id: known_indels
    source: known_indels
  - id: mills_indels
    source: mills_indels
  run: tools/somatic_subpipeline.cwl
  out:
  - id: out
  - id: bqsr_bam
  - id: reports
  - id: depth_of_coverage
  - id: summary
- id: normal
  in:
  - id: reads
    source: normal_inputs
  - id: sample_name
    source: normal_name
  - id: reference
    source: reference
  - id: cutadapt_adapters
    source: cutadapt_adapters
  - id: gatk_intervals
    source: gatk_intervals
  - id: genome_file
    source: genome_file
  - id: snps_dbsnp
    source: snps_dbsnp
  - id: snps_1000gp
    source: snps_1000gp
  - id: known_indels
    source: known_indels
  - id: mills_indels
    source: mills_indels
  run: tools/somatic_subpipeline.cwl
  out:
  - id: out
  - id: bqsr_bam
  - id: reports
  - id: depth_of_coverage
  - id: summary
- id: vc_gridss
  label: Gridss
  in:
  - id: bams
    source:
    - normal/out
    - tumor/out
  - id: reference
    source: reference
  - id: blacklist
    source: gridss_blacklist
  run: tools/gridss_v2_6_2.cwl
  out:
  - id: out
  - id: assembly
- id: vc_gatk
  label: GATK4 Somatic Variant Caller
  in:
  - id: normal_bam
    source: normal/bqsr_bam
  - id: tumor_bam
    source: tumor/bqsr_bam
  - id: normal_name
    source: normal_name
  - id: intervals
    source: gatk_intervals
  - id: reference
    source: reference
  - id: gnomad
    source: gnomad
  - id: panel_of_normals
    source: panel_of_normals
  scatter:
  - intervals
  run: tools/GATK4_SomaticVariantCaller_4_1_3_0.cwl
  out:
  - id: variants
  - id: out_bam
  - id: out
- id: vc_gatk_merge
  label: 'GATK4: Gather VCFs'
  in:
  - id: vcfs
    source: vc_gatk/out
  run: tools/Gatk4GatherVcfs_4_1_3_0.cwl
  out:
  - id: out
- id: vc_gatk_compressvcf
  label: BGZip
  in:
  - id: file
    source: vc_gatk_merge/out
  run: tools/bgzip_1_2_1.cwl
  out:
  - id: out
- id: vc_gatk_sort_combined
  label: 'BCFTools: Sort'
  in:
  - id: vcf
    source: vc_gatk_compressvcf/out
  run: tools/bcftoolssort_v1_9.cwl
  out:
  - id: out
- id: vc_gatk_uncompressvcf
  label: UncompressArchive
  in:
  - id: file
    source: vc_gatk_sort_combined/out
  run: tools/UncompressArchive_v1_0_0.cwl
  out:
  - id: out
- id: vc_strelka
  label: Strelka Somatic Variant Caller
  in:
  - id: normal_bam
    source: normal/out
  - id: tumor_bam
    source: tumor/out
  - id: reference
    source: reference
  - id: intervals
    source: strelka_intervals
  run: tools/strelkaSomaticVariantCaller_v0_1_1.cwl
  out:
  - id: sv
  - id: variants
  - id: out
- id: generate_vardict_headerlines
  label: GenerateVardictHeaderLines
  in:
  - id: reference
    source: reference
  run: tools/GenerateVardictHeaderLines_v0_1_0.cwl
  out:
  - id: out
- id: vc_vardict
  label: Vardict Somatic Variant Caller
  in:
  - id: normal_bam
    source: normal/out
  - id: tumor_bam
    source: tumor/out
  - id: normal_name
    source: normal_name
  - id: tumor_name
    source: tumor_name
  - id: intervals
    source: vardict_intervals
  - id: allele_freq_threshold
    source: allele_freq_threshold
  - id: header_lines
    source: generate_vardict_headerlines/out
  - id: reference
    source: reference
  scatter:
  - intervals
  run: tools/vardictSomaticVariantCaller_v0_1_0.cwl
  out:
  - id: variants
  - id: out
- id: vc_vardict_merge
  label: 'GATK4: Gather VCFs'
  in:
  - id: vcfs
    source: vc_vardict/out
  run: tools/Gatk4GatherVcfs_4_1_3_0.cwl
  out:
  - id: out
- id: vc_vardict_compressvcf
  label: BGZip
  in:
  - id: file
    source: vc_vardict_merge/out
  run: tools/bgzip_1_2_1.cwl
  out:
  - id: out
- id: vc_vardict_sort_combined
  label: 'BCFTools: Sort'
  in:
  - id: vcf
    source: vc_vardict_compressvcf/out
  run: tools/bcftoolssort_v1_9.cwl
  out:
  - id: out
- id: vc_vardict_uncompressvcf
  label: UncompressArchive
  in:
  - id: file
    source: vc_vardict_sort_combined/out
  run: tools/UncompressArchive_v1_0_0.cwl
  out:
  - id: out
- id: combine_variants
  label: Combine Variants
  in:
  - id: vcfs
    source:
    - vc_gatk_uncompressvcf/out
    - vc_strelka/out
    - vc_vardict_uncompressvcf/out
  - id: type
    source: combine_variants_type
  - id: columns
    source: combine_variants_columns
  - id: normal
    source: normal_name
  - id: tumor
    source: tumor_name
  run: tools/combinevariants_0_0_8.cwl
  out:
  - id: out
- id: combined_compress
  label: BGZip
  in:
  - id: file
    source: combine_variants/out
  run: tools/bgzip_1_2_1.cwl
  out:
  - id: out
- id: combined_sort
  label: 'BCFTools: Sort'
  in:
  - id: vcf
    source: combined_compress/out
  run: tools/bcftoolssort_v1_9.cwl
  out:
  - id: out
- id: combined_uncompress
  label: UncompressArchive
  in:
  - id: file
    source: combined_sort/out
  run: tools/UncompressArchive_v1_0_0.cwl
  out:
  - id: out
- id: addbamstats
  label: Annotate Bam Stats to Somatic Vcf Workflow
  in:
  - id: normal_id
    source: normal_name
  - id: tumor_id
    source: tumor_name
  - id: normal_bam
    source: normal/out
  - id: tumor_bam
    source: tumor/out
  - id: vcf
    source: combined_uncompress/out
  run: tools/AddBamStatsSomatic_v0_1_0.cwl
  out:
  - id: out
id: WGSSomaticMultiCallers
