#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.2
label: Janis Germline Variant-Calling Workflow (GATK)
doc: |
  This is a genomics pipeline to do a single germline sample variant-calling, adapted from GATK Best Practice Workflow.

  This workflow is a reference pipeline for using the Janis Python framework (pipelines assistant).
  - Alignment: bwa-mem
  - Variant-Calling: GATK HaplotypeCaller
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
  doc: |2-
        The reference genome from which to align the reads. This requires a number indexes (can be generated     with the 'IndexFasta' pipeline This pipeline has been tested using the HG38 reference set.

        This pipeline expects the assembly references to be as they appear in the GCP example. For example:
            - HG38: https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/

        - (".fai", ".amb", ".ann", ".bwt", ".pac", ".sa", "^.dict").
  type: File
  secondaryFiles:
  - pattern: .fai
  - pattern: .amb
  - pattern: .ann
  - pattern: .bwt
  - pattern: .pac
  - pattern: .sa
  - pattern: ^.dict
- id: snps_dbsnp
  doc: From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``
  type: File
  secondaryFiles:
  - pattern: .tbi
- id: snps_1000gp
  doc: |-
    From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``. Accessible from the HG38 genomics-public-data google cloud bucket: https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/ 
  type: File
  secondaryFiles:
  - pattern: .tbi
- id: known_indels
  doc: From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``
  type: File
  secondaryFiles:
  - pattern: .tbi
- id: mills_indels
  doc: From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``
  type: File
  secondaryFiles:
  - pattern: .tbi
- id: gatk_intervals
  doc: |-
    List of intervals over which to split the GATK variant calling. If no interval is provided, one interval for each chromosome in the reference will be generated.
  type:
  - type: array
    items: File
  - 'null'
- id: cutadapt_adapters
  doc: |2-
                    Specifies a containment list for cutadapt, which contains a list of sequences to determine valid
                    overrepresented sequences from the FastQC report to trim with Cuatadapt. The file must contain sets
                    of named adapters in the form: ``name[tab]sequence``. Lines prefixed with a hash will be ignored.
  type: File
- id: align_and_sort_sortsam_tmpDir
  doc: Undocumented option
  type: string
  default: ./tmp

outputs:
- id: out_fastqc_reports
  doc: A zip file of the FastQC quality report.
  type:
    type: array
    items:
      type: array
      items: File
  outputSource: fastqc/out
- id: out_bam
  doc: Aligned and indexed bam.
  type: File
  secondaryFiles:
  - pattern: .bai
  outputSource: merge_and_mark/out
- id: out_performance_summary
  doc: A text file of performance summary of bam
  type: File
  outputSource: performance_summary/performanceSummaryOut
- id: out_variants_gatk
  doc: Merged variants from the GATK caller
  type: File
  outputSource: vc_gatk_sort_combined/out
- id: out_variants_gatk_split
  doc: Unmerged variants from the GATK caller (by interval)
  type:
    type: array
    items: File
  outputSource: vc_gatk/out
- id: out_variants_bamstats
  type: File
  outputSource: vc_gatk_addbamstats/out

steps:
- id: fastqc
  label: FastQC
  in:
  - id: reads
    source: fastqs
  scatter:
  - reads
  run: tools/fastqc_v0_11_8.cwl
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
- id: calculate_performancesummary_genomefile
  label: Generate genome for BedtoolsCoverage
  in:
  - id: reference
    source: reference
  run: tools/GenerateGenomeFileForBedtoolsCoverage_v0_1_0.cwl
  out:
  - id: out
- id: performance_summary
  label: Performance summary workflow (whole genome)
  in:
  - id: bam
    source: merge_and_mark/out
  - id: sample_name
    source: sample_name
  - id: genome_file
    source: calculate_performancesummary_genomefile/out
  run: tools/PerformanceSummaryGenome_v0_1_0.cwl
  out:
  - id: performanceSummaryOut
- id: generate_gatk_intervals
  label: Generating genomic intervals by chromosome
  in:
  - id: reference
    source: reference
  - id: __when_gatkintervals
    source: gatk_intervals
  run: tools/GenerateIntervalsByChromosome_v0_1_0.cwl
  when: $(!((inputs.__when_gatkintervals != null)))
  out:
  - id: out_regions
- id: _evaluate_prescatter-bqsr-intervals
  in:
  - id: _gatkintervals
    source: gatk_intervals
  - id: _generategatkintervalsoutregions
    source: generate_gatk_intervals/out_regions
  run:
    class: ExpressionTool

    inputs:
    - id: _gatkintervals
      type:
        type: array
        items: File
      loadContents: false
    - id: _generategatkintervalsoutregions
      type:
      - type: array
        items: File
      - 'null'
      loadContents: false

    outputs:
    - id: out
      type:
        type: array
        items: File
    expression: |-
      ${return {out: [inputs._gatkintervals, inputs._generategatkintervalsoutregions].filter(function (inner) { return inner != null })[0] }}
  out:
  - out
- id: bqsr
  label: GATK Base Recalibration on Bam
  doc: Perform base quality score recalibration
  in:
  - id: bam
    source: merge_and_mark/out
  - id: intervals
    source: _evaluate_prescatter-bqsr-intervals/out
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
  scatter:
  - intervals
  run: tools/GATKBaseRecalBQSRWorkflow_4_1_3.cwl
  out:
  - id: out
- id: _evaluate_prescatter-vc_gatk-intervals
  in:
  - id: _gatkintervals
    source: gatk_intervals
  - id: _generategatkintervalsoutregions
    source: generate_gatk_intervals/out_regions
  run:
    class: ExpressionTool

    inputs:
    - id: _gatkintervals
      type:
        type: array
        items: File
      loadContents: false
    - id: _generategatkintervalsoutregions
      type:
      - type: array
        items: File
      - 'null'
      loadContents: false

    outputs:
    - id: out
      type:
        type: array
        items: File
    expression: |-
      ${return {out: [inputs._gatkintervals, inputs._generategatkintervalsoutregions].filter(function (inner) { return inner != null })[0] }}
  out:
  - out
- id: vc_gatk
  label: GATK4 Germline Variant Caller
  in:
  - id: bam
    source: bqsr/out
  - id: intervals
    source: _evaluate_prescatter-vc_gatk-intervals/out
  - id: reference
    source: reference
  - id: snps_dbsnp
    source: snps_dbsnp
  scatter:
  - intervals
  - bam
  scatterMethod: dotproduct
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
- id: vc_gatk_uncompress
  label: UncompressArchive
  in:
  - id: file
    source: vc_gatk_sort_combined/out
  run: tools/UncompressArchive_v1_0_0.cwl
  out:
  - id: out
- id: vc_gatk_addbamstats
  label: Annotate Bam Stats to Germline Vcf Workflow
  in:
  - id: bam
    source: merge_and_mark/out
  - id: vcf
    source: vc_gatk_uncompress/out
  - id: reference
    source: reference
  run: tools/AddBamStatsGermline_v0_1_0.cwl
  out:
  - id: out
id: WGSGermlineGATK
