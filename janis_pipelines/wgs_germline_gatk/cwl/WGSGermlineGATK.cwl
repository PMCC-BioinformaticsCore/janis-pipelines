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
  InlineJavascriptRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
inputs:
  align_and_sort_sortsam_tmpDir:
    id: align_and_sort_sortsam_tmpDir
    doc: Undocumented option
    type: string
    default: .
  cutadapt_adapters:
    id: cutadapt_adapters
    doc: |-
      Specifies a containment list for cutadapt, which contains a list of sequences to determine valid overrepresented sequences from the FastQC report to trim with Cuatadapt. The file must contain sets of named adapters in the form: ``name[tab]sequence``. Lines prefixed with a hash will be ignored.
    type:
    - File
    - 'null'
  fastqs:
    id: fastqs
    doc: |-
      An array of FastqGz pairs. These are aligned separately and merged to create higher depth coverages from multiple sets of reads
    type:
      type: array
      items:
        type: array
        items: File
  gatk_intervals:
    id: gatk_intervals
    doc: List of intervals over which to split the GATK variant calling
    type:
      type: array
      items: File
  known_indels:
    id: known_indels
    doc: From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``
    type: File
    secondaryFiles:
    - .tbi
  mills_indels:
    id: mills_indels
    doc: From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``
    type: File
    secondaryFiles:
    - .tbi
  reference:
    id: reference
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
  sample_name:
    id: sample_name
    doc: Sample name from which to generate the readGroupHeaderLine for BwaMem
    type: string
  snps_1000gp:
    id: snps_1000gp
    doc: From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``
    type: File
    secondaryFiles:
    - .tbi
  snps_dbsnp:
    id: snps_dbsnp
    doc: From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``
    type: File
    secondaryFiles:
    - .tbi
outputs:
  bam:
    id: bam
    doc: Aligned and indexed bam.
    type: File
    secondaryFiles:
    - .bai
    outputSource: merge_and_mark/out
  reports:
    id: reports
    doc: A zip file of the FastQC quality report.
    type:
      type: array
      items:
        type: array
        items: File
    outputSource: fastqc/out
  variants:
    id: variants
    doc: Merged variants from the GATK caller
    type: File
    outputSource: sort_combined/out
  variants_split:
    id: variants_split
    doc: Unmerged variants from the GATK caller (by interval)
    type:
      type: array
      items: File
    outputSource: vc_gatk/out
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
    scatter:
    - fastq
    - cutadapt_adapter
    - cutadapt_removeMiddle3Adapter
    scatterMethod: dotproduct
    run: tools/BwaAligner.cwl
    out:
    - out
  fastqc:
    in:
      reads:
        id: reads
        source: fastqs
    scatter:
    - reads
    run: tools/fastqc.cwl
    out:
    - out
    - datafile
  getfastqc_adapters:
    in:
      cutadapt_adaptors_lookup:
        id: cutadapt_adaptors_lookup
        source: cutadapt_adapters
      fastqc_datafiles:
        id: fastqc_datafiles
        source: fastqc/datafile
    scatter:
    - fastqc_datafiles
    run: tools/ParseFastqcAdaptors.cwl
    out:
    - adaptor_sequences
  merge_and_mark:
    in:
      bams:
        id: bams
        source: align_and_sort/out
      sampleName:
        id: sampleName
        source: sample_name
    run: tools/mergeAndMarkBams.cwl
    out:
    - out
  sort_combined:
    in:
      vcf:
        id: vcf
        source: vc_gatk_merge/out
    run: tools/bcftoolssort.cwl
    out:
    - out
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
    scatter:
    - intervals
    run: tools/GATK4_GermlineVariantCaller.cwl
    out:
    - out
  vc_gatk_merge:
    in:
      vcfs:
        id: vcfs
        source: vc_gatk/out
    run: tools/Gatk4GatherVcfs.cwl
    out:
    - out
id: WGSGermlineGATK
