#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
doc: "This is a genomics pipeline to align sequencing data (Fastq pairs) into BAMs\
  \ and call variants using GATK. The final variants are outputted in the VCF format.\n\
  \n**Resources**\n\nThis pipeline has been tested using the HG38 reference set, available\
  \ on Google Cloud Storage through:\n\n- https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/\n\
  \nThis pipeline expects the assembly references to be as they appear in that storage\
  \     (\".fai\", \".amb\", \".ann\", \".bwt\", \".pac\", \".sa\", \"^.dict\").\n\
  The known sites (snps_dbsnp, snps_1000gp, known_indels, mills_indels) should be\
  \ gzipped and tabix indexed.\n"
id: WGSGermlineGATK
inputs:
  align_and_sort_sortsam_tmpDir:
    default: .
    doc: Undocumented option
    id: align_and_sort_sortsam_tmpDir
    type: string
  cutadapt_adapters:
    doc: Specifies a file which contains a list of sequences to determine valid overrepresented
      sequences from the FastQC report to trim with Cuatadapt. The file must contain
      sets of named adapters in the form name[tab]sequence. Lines prefixed with a
      hash will be ignored.
    id: cutadapt_adapters
    type:
    - File
    - 'null'
  fastqs:
    doc: An array of FastqGz pairs. These are aligned separately and merged to create
      higher depth coverages from multiple sets of reads
    id: fastqs
    type:
      items:
        items: File
        type: array
      type: array
  gatk_intervals:
    doc: List of intervals over which to split the GATK variant calling
    id: gatk_intervals
    type:
      items: File
      type: array
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
label: WGS Germline (GATK only)
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
  variants:
    id: variants
    outputSource: sort_combined/out
    type: File
  variants_split:
    id: variants_split
    outputSource: vc_gatk/out
    type:
      items: File
      type: array
requirements:
  InlineJavascriptRequirement: {}
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
        source: vc_gatk_merge/out
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
