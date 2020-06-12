#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0

requirements:
- class: InlineJavascriptRequirement
- class: StepInputExpressionRequirement
- class: ScatterFeatureRequirement
- class: SubworkflowFeatureRequirement

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

outputs:
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
- id: variants
  doc: Merged variants from the GATK caller
  type: File
  outputSource: sorted/out
- id: variants_split
  doc: Unmerged variants from the GATK caller (by interval)
  type:
    type: array
    items: File
  outputSource: vc_gatk/out

steps:
- id: tumor
  in:
  - id: reference
    source: reference
  - id: reads
    source: tumor_inputs
  - id: cutadapt_adapters
    source: cutadapt_adapters
  - id: sample_name
    source: tumor_name
  run: tools/somatic_subpipeline.cwl
  out:
  - id: out
  - id: reports
- id: normal
  in:
  - id: reference
    source: reference
  - id: reads
    source: normal_inputs
  - id: cutadapt_adapters
    source: cutadapt_adapters
  - id: sample_name
    source: normal_name
  run: tools/somatic_subpipeline.cwl
  out:
  - id: out
  - id: reports
- id: vc_gatk
  in:
  - id: normal_bam
    source: tumor/out
  - id: tumor_bam
    source: normal/out
  - id: normal_name
    source: normal_name
  - id: tumor_name
    source: tumor_name
  - id: intervals
    source: gatk_intervals
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
  run: tools/GATK4_SomaticVariantCaller_4_1_3_0.cwl
  out:
  - id: out
- id: vc_gatk_merge
  in:
  - id: vcfs
    source: vc_gatk/out
  run: tools/Gatk4GatherVcfs_4_1_3_0.cwl
  out:
  - id: out
- id: sorted
  in:
  - id: vcf
    source: vc_gatk_merge/out
  run: tools/bcftoolssort_v1_9.cwl
  out:
  - id: out
