#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
doc: "This is a genomics pipeline to align sequencing data (Fastq pairs) into BAMs:\n\
  \n- Takes raw sequence data in the FASTQ format;\n- align to the reference genome\
  \ using BWA MEM;\n- Marks duplicates using Picard;\n- Call the appropriate somatic\
  \ variant callers (GATK / Strelka / VarDict);\n- Outputs the final variants in the\
  \ VCF format.\n\n**Resources**\n\nThis pipeline has been tested using the HG38 reference\
  \ set, available on Google Cloud Storage through:\n\n- https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/\n\
  \nThis pipeline expects the assembly references to be as they appear in that storage\
  \     (\".fai\", \".amb\", \".ann\", \".bwt\", \".pac\", \".sa\", \"^.dict\").\n\
  The known sites (snps_dbsnp, snps_1000gp, known_indels, mills_indels) should be\
  \ gzipped and tabix indexed.\n"
id: WGSSomaticGATK
inputs:
  cutadapt_adapters:
    doc: 'Specifies a containment list for cutadapt, which contains a list of sequences
      to determine valid overrepresented sequences from the FastQC report to trim
      with Cuatadapt. The file must contain sets of named adapters in the form: ``name[tab]sequence``.
      Lines prefixed with a hash will be ignored.'
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
  normal_inputs:
    doc: An array of NORMAL FastqGz pairs. These are aligned separately and merged
      to create higher depth coverages from multiple sets of reads
    id: normal_inputs
    type:
      items:
        items: File
        type: array
      type: array
  normal_name:
    doc: Sample name for the NORMAL sample from which to generate the readGroupHeaderLine
      for BwaMem
    id: normal_name
    type: string
  reference:
    doc: "The reference genome from which to align the reads. This requires a number\
      \ indexes (can be generated with the 'IndexFasta' pipeline This pipeline has\
      \ been tested using the HG38 reference set.\n\nThis pipeline expects the assembly\
      \ references to be as they appear in the GCP example:\n\n- (\".fai\", \".amb\"\
      , \".ann\", \".bwt\", \".pac\", \".sa\", \"^.dict\")."
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
  tumor_inputs:
    doc: An array of TUMOR FastqGz pairs. These are aligned separately and merged
      to create higher depth coverages from multiple sets of reads
    id: tumor_inputs
    type:
      items:
        items: File
        type: array
      type: array
  tumor_name:
    doc: Sample name for the TUMOR sample from which to generate the readGroupHeaderLine
      for BwaMem
    id: tumor_name
    type: string
label: WGS Somatic (GATK only)
outputs:
  normal_bam:
    id: normal_bam
    outputSource: normal/out
    secondaryFiles:
    - .bai
    type: File
  normal_report:
    id: normal_report
    outputSource: normal/reports
    type:
      items:
        items: File
        type: array
      type: array
  tumor_bam:
    id: tumor_bam
    outputSource: tumor/out
    secondaryFiles:
    - .bai
    type: File
  tumor_report:
    id: tumor_report
    outputSource: tumor/reports
    type:
      items:
        items: File
        type: array
      type: array
  variants_gatk:
    id: variants_gatk
    outputSource: sorted/out
    type: File
requirements:
  InlineJavascriptRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
steps:
  normal:
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
    out:
    - out
    - reports
    run: tools/somatic_subpipeline.cwl
  sorted:
    in:
      vcf:
        id: vcf
        source: vc_gatk_merge/out
    out:
    - out
    run: tools/bcftoolssort.cwl
  tumor:
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
    out:
    - out
    - reports
    run: tools/somatic_subpipeline.cwl
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
    out:
    - out
    run: tools/GATK4_SomaticVariantCaller.cwl
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
