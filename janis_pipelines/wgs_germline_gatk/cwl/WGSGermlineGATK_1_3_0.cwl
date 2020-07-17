#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: WGS Germline (GATK only)
doc: |
  This is a genomics pipeline to align sequencing data (Fastq pairs) into BAMs and call variants using GATK. The final variants are outputted in the VCF format.

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
  default: .
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
- id: variants
  doc: Merged variants from the GATK caller
  type: File
  outputSource: vc_gatk_sort_combined/out
- id: variants_split
  doc: Unmerged variants from the GATK caller (by interval)
  type:
    type: array
    items: File
  outputSource: vc_gatk/out
- id: variants_final
  doc: Final vcf
  type: File
  outputSource: addbamstats/out

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
- id: addbamstats
  label: Annotate Bam Stats to Germline Vcf Workflow
  in:
  - id: bam
    source: merge_and_mark/out
  - id: vcf
    source: vc_gatk_uncompressvcf/out
  run: tools/AddBamStatsGermline_v0_1_0.cwl
  out:
  - id: out
id: WGSGermlineGATK
