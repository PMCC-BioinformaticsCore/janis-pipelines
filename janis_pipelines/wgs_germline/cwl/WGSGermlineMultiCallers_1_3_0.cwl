#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: WGS Germline (Multi callers)
doc: |
  This is a genomics pipeline to align sequencing data (Fastq pairs) into BAMs and call variants using:

  This workflow is a reference pipeline using the Janis Python framework (pipelines assistant).

  - Takes raw sequence data in the FASTQ format;
  - align to the reference genome using BWA MEM;
  - Marks duplicates using Picard;
  - Call the appropriate variant callers (GATK / Strelka / VarDict);
  - Outputs the final variants in the VCF format.

requirements:
- class: InlineJavascriptRequirement
- class: StepInputExpressionRequirement
- class: ScatterFeatureRequirement
- class: SubworkflowFeatureRequirement
- class: MultipleInputFeatureRequirement

inputs:
- id: sample_name
  doc: Sample name from which to generate the readGroupHeaderLine for BwaMem
  type: string
- id: fastqs
  doc: |-
    An array of FastqGz pairs. These are aligned separately and merged to create higher depth coverages from multiple sets of reads
  type:
    type: array
    items:
      type: array
      items: File
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
- id: genome_file
  doc: Genome file for bedtools query
  type: File
- id: gridss_blacklist
  doc: BED file containing regions to ignore.
  type: File
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
- id: align_and_sort_sortsam_tmpDir
  doc: Undocumented option
  type: string
  default: ./tmp
- id: coverage_omitDepthOutputAtEachBase
  doc: Do not output depth of coverage at each base
  type: boolean
  default: true
- id: coverage_summaryCoverageThreshold
  doc: Coverage threshold (in percent) for summarizing statistics
  type:
    type: array
    items: int
  default:
  - 1
  - 50
  - 100
  - 300
  - 500
- id: combine_variants_type
  doc: germline | somatic
  type: string
  default: germline
- id: combine_variants_columns
  doc: Columns to keep, seperated by space output vcf (unsorted)
  type:
    type: array
    items: string
  default:
  - AC
  - AN
  - AF
  - AD
  - DP
  - GT

outputs:
- id: reports
  doc: A zip file of the FastQC quality report.
  type:
    type: array
    items:
      type: array
      items: File
  outputSource: fastqc/out
- id: sample_coverage
  doc: A text file of depth of coverage summary of bam
  type: File
  outputSource: coverage/out_sampleSummary
- id: summary
  doc: A text file of performance summary of bam
  type: File
  outputSource: performance_summary/performanceSummaryOut
- id: gridss_assembly
  doc: Assembly returned by GRIDSS
  type: File
  outputSource: vc_gridss/assembly
- id: variants_gridss
  doc: Variants from the GRIDSS variant caller
  type: File
  outputSource: vc_gridss/out
- id: bam
  doc: Aligned and indexed bam.
  type: File
  secondaryFiles:
  - .bai
  outputSource: merge_and_mark/out
- id: variants_combined
  doc: Combined variants from all 3 callers
  type: File
  outputSource: addbamstats/out
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
- id: fastqc
  label: FastQC
  in:
  - id: reads
    source: fastqs
  scatter:
  - reads
  run: tools/fastqc_v0_11_5.cwl
  out:
  - id: out
  - id: datafile
- id: getfastqc_adapters
  label: Parse FastQC Adaptors
  in:
  - id: fastqc_datafiles
    source: fastqc/datafile
  - id: cutadapt_adaptors_lookup
    source: cutadapt_adapters
  scatter:
  - fastqc_datafiles
  run: tools/ParseFastqcAdaptors_v0_1_0.cwl
  out:
  - id: adaptor_sequences
- id: align_and_sort
  label: Align and sort reads
  in:
  - id: sample_name
    source: sample_name
  - id: reference
    source: reference
  - id: fastq
    source: fastqs
  - id: cutadapt_adapter
    source: getfastqc_adapters/adaptor_sequences
  - id: cutadapt_removeMiddle3Adapter
    source: getfastqc_adapters/adaptor_sequences
  - id: sortsam_tmpDir
    source: align_and_sort_sortsam_tmpDir
  scatter:
  - fastq
  - cutadapt_adapter
  - cutadapt_removeMiddle3Adapter
  scatterMethod: dotproduct
  run: tools/BwaAligner_1_0_0.cwl
  out:
  - id: out
- id: merge_and_mark
  label: Merge and Mark Duplicates
  in:
  - id: bams
    source: align_and_sort/out
  - id: sampleName
    source: sample_name
  run: tools/mergeAndMarkBams_4_1_3.cwl
  out:
  - id: out
- id: coverage
  label: 'GATK4: Generate coverage summary information for reads data'
  in:
  - id: bam
    source: merge_and_mark/out
  - id: reference
    source: reference
  - id: outputPrefix
    source: sample_name
  - id: intervals
    source: gatk_intervals
  - id: summaryCoverageThreshold
    source: coverage_summaryCoverageThreshold
  - id: omitDepthOutputAtEachBase
    source: coverage_omitDepthOutputAtEachBase
  run: tools/Gatk4DepthOfCoverage_4_1_6_0.cwl
  out:
  - id: out_sample
  - id: out_sampleCumulativeCoverageCounts
  - id: out_sampleCumulativeCoverageProportions
  - id: out_sampleIntervalStatistics
  - id: out_sampleIntervalSummary
  - id: out_sampleStatistics
  - id: out_sampleSummary
- id: performance_summary
  label: Performance summary workflow (whole genome)
  in:
  - id: bam
    source: merge_and_mark/out
  - id: sample_name
    source: sample_name
  - id: genome_file
    source: genome_file
  run: tools/PerformanceSummaryGenome_v0_1_0.cwl
  out:
  - id: performanceSummaryOut
- id: vc_gridss
  label: Gridss
  in:
  - id: bams
    source:
    - merge_and_mark/out
    linkMerge: merge_nested
  - id: reference
    source: reference
  - id: blacklist
    source: gridss_blacklist
  run: tools/gridss_v2_6_2.cwl
  out:
  - id: out
  - id: assembly
- id: bqsr
  label: GATK Base Recalibration on Bam
  in:
  - id: bam
    source: merge_and_mark/out
  - id: reference
    source: reference
  - id: snps_dbsnp
    source: snps_dbsnp
  - id: snps_1000gp
    source: snps_1000gp
  - id: known_indels
    source: known_indels
  - id: mills_indels
    source: mills_indels
  run: tools/GATKBaseRecalBQSRWorkflow_4_1_3.cwl
  out:
  - id: out
- id: vc_gatk
  label: GATK4 Germline Variant Caller
  in:
  - id: bam
    source: bqsr/out
  - id: intervals
    source: gatk_intervals
  - id: reference
    source: reference
  - id: snps_dbsnp
    source: snps_dbsnp
  scatter:
  - intervals
  run: tools/GATK4_GermlineVariantCaller_4_1_3_0.cwl
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
  label: Strelka Germline Variant Caller
  in:
  - id: bam
    source: merge_and_mark/out
  - id: reference
    source: reference
  - id: intervals
    source: strelka_intervals
  run: tools/strelkaGermlineVariantCaller_v0_1_1.cwl
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
  label: Vardict Germline Variant Caller
  in:
  - id: bam
    source: merge_and_mark/out
  - id: intervals
    source: vardict_intervals
  - id: sample_name
    source: sample_name
  - id: allele_freq_threshold
    source: allele_freq_threshold
  - id: header_lines
    source: generate_vardict_headerlines/out
  - id: reference
    source: reference
  scatter:
  - intervals
  run: tools/vardictGermlineVariantCaller_v0_1_1.cwl
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
  label: Annotate Bam Stats to Germline Vcf Workflow
  in:
  - id: bam
    source: merge_and_mark/out
  - id: vcf
    source: combined_uncompress/out
  run: tools/AddBamStatsGermline_v0_1_0.cwl
  out:
  - id: out
id: WGSGermlineMultiCallers
