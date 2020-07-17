#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0

requirements:
- class: InlineJavascriptRequirement
- class: StepInputExpressionRequirement
- class: ScatterFeatureRequirement
- class: SubworkflowFeatureRequirement

inputs:
- id: reads
  type:
    type: array
    items:
      type: array
      items: File
- id: sample_name
  type: string
- id: reference
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
  type:
  - File
  - 'null'
- id: genome_file
  type: File
- id: gatk_intervals
  type:
    type: array
    items: File
- id: snps_dbsnp
  type: File
  secondaryFiles:
  - .tbi
- id: snps_1000gp
  type: File
  secondaryFiles:
  - .tbi
- id: known_indels
  type: File
  secondaryFiles:
  - .tbi
- id: mills_indels
  type: File
  secondaryFiles:
  - .tbi
- id: align_and_sort_sortsam_tmpDir
  type:
  - string
  - 'null'
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
- id: out
  type: File
  secondaryFiles:
  - .bai
  outputSource: merge_and_mark/out
- id: bqsr_bam
  type: File
  secondaryFiles:
  - .bai
  outputSource: bqsr/out
- id: reports
  type:
    type: array
    items:
      type: array
      items: File
  outputSource: fastqc/out
- id: depth_of_coverage
  type: File
  outputSource: coverage/out_sampleSummary
- id: summary
  type: File
  outputSource: performance_summary/performanceSummaryOut

steps:
- id: fastqc
  label: FastQC
  in:
  - id: reads
    source: reads
  scatter:
  - reads
  run: fastqc_v0_11_5.cwl
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
  run: ParseFastqcAdaptors_v0_1_0.cwl
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
    source: reads
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
  run: BwaAligner_1_0_0.cwl
  out:
  - id: out
- id: merge_and_mark
  label: Merge and Mark Duplicates
  in:
  - id: bams
    source: align_and_sort/out
  - id: sampleName
    source: sample_name
  run: mergeAndMarkBams_4_1_3.cwl
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
  run: Gatk4DepthOfCoverage_4_1_6_0.cwl
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
  run: PerformanceSummaryGenome_v0_1_0.cwl
  out:
  - id: performanceSummaryOut
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
  run: GATKBaseRecalBQSRWorkflow_4_1_3.cwl
  out:
  - id: out
id: somatic_subpipeline
