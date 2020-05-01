#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: WGS Somatic (GATK only)
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
  InlineJavascriptRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
inputs:
  cutadapt_adapters:
    id: cutadapt_adapters
    doc: |-
      Specifies a containment list for cutadapt, which contains a list of sequences to determine valid overrepresented sequences from the FastQC report to trim with Cuatadapt. The file must contain sets of named adapters in the form: ``name[tab]sequence``. Lines prefixed with a hash will be ignored.
    type:
    - File
    - 'null'
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
  normal_inputs:
    id: normal_inputs
    doc: |-
      An array of NORMAL FastqGz pairs. These are aligned separately and merged to create higher depth coverages from multiple sets of reads
    type:
      type: array
      items:
        type: array
        items: File
  normal_name:
    id: normal_name
    doc: |-
      Sample name for the NORMAL sample from which to generate the readGroupHeaderLine for BwaMem
    type: string
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
  tumor_inputs:
    id: tumor_inputs
    doc: |-
      An array of TUMOR FastqGz pairs. These are aligned separately and merged to create higher depth coverages from multiple sets of reads
    type:
      type: array
      items:
        type: array
        items: File
  tumor_name:
    id: tumor_name
    doc: |-
      Sample name for the TUMOR sample from which to generate the readGroupHeaderLine for BwaMem
    type: string
outputs:
  normal_bam:
    id: normal_bam
    type: File
    secondaryFiles:
    - .bai
    outputSource: normal/out
  normal_report:
    id: normal_report
    type:
      type: array
      items:
        type: array
        items: File
    outputSource: normal/reports
  tumor_bam:
    id: tumor_bam
    type: File
    secondaryFiles:
    - .bai
    outputSource: tumor/out
  tumor_report:
    id: tumor_report
    type:
      type: array
      items:
        type: array
        items: File
    outputSource: tumor/reports
  variants:
    id: variants
    doc: Merged variants from the GATK caller
    type: File
    outputSource: sorted/out
  variants_split:
    id: variants_split
    doc: Unmerged variants from the GATK caller (by interval)
    type:
      type: array
      items: File
    outputSource: vc_gatk/out
steps:
  normal:
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
    run: tools/somatic_subpipeline.cwl
    out:
    - out
    - reports
  sorted:
    in:
      vcf:
        id: vcf
        source: vc_gatk_merge/out
    run: tools/bcftoolssort.cwl
    out:
    - out
  tumor:
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
    run: tools/somatic_subpipeline.cwl
    out:
    - out
    - reports
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
    scatter:
    - intervals
    run: tools/GATK4_SomaticVariantCaller.cwl
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
id: WGSSomaticGATK
