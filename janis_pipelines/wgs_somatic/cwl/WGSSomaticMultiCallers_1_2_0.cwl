#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0

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
- id: vardict_header_lines
  doc: |
    As with chromosomal sequences it is highly recommended (but not required) that the header include tags describing the contigs referred to in the VCF file. This furthermore allows these contigs to come from different files. The format is identical to that of a reference sequence, but with an additional URL tag to indicate where that sequence can be found. For example:

    .. code-block:

       ##contig=<ID=ctg1,URL=ftp://somewhere.org/assembly.fa,...>

    Source: (1.2.5 Alternative allele field format) https://samtools.github.io/hts-specs/VCFv4.1.pdf (edited) 
  type: File
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
  doc: A zip file of the NORMAL FastQC quality reports.
  type:
    type: array
    items:
      type: array
      items: File
  outputSource: normal/reports
- id: tumor_report
  doc: A zip file of the TUMOR FastQC quality reports.
  type:
    type: array
    items:
      type: array
      items: File
  outputSource: tumor/reports
- id: normal_bam
  doc: Aligned and indexed NORMAL bam
  type: File
  secondaryFiles:
  - .bai
  outputSource: normal/out
- id: tumor_bam
  doc: Aligned and indexed TUMOR bam
  type: File
  secondaryFiles:
  - .bai
  outputSource: tumor/out
- id: gridss_assembly
  doc: Assembly returned by GRIDSS
  type: File
  outputSource: vc_gridss/assembly
- id: variants_gatk
  doc: Merged variants from the GATK caller
  type: File
  outputSource: vc_gatk_merge/out
- id: variants_strelka
  doc: Variants from the Strelka variant caller
  type: File
  outputSource: vc_strelka/out
- id: variants_vardict
  doc: Merged variants from the VarDict caller
  type: File
  outputSource: vc_vardict_merge/out
- id: variants_gridss
  doc: Variants from the GRIDSS variant caller
  type: File
  outputSource: vc_gridss/out
- id: variants
  doc: Combined variants from all 3 callers
  type: File
  outputSource: combine_variants/vcf

steps:
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
- id: vc_strelka
  in:
  - id: normal_bam
    source: normal/out
  - id: tumor_bam
    source: tumor/out
  - id: reference
    source: reference
  - id: intervals
    source: strelka_intervals
  run: tools/strelkaSomaticVariantCaller_v0_1_0.cwl
  out:
  - id: diploid
  - id: variants
  - id: out
- id: vc_gridss
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
- id: vc_vardict
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
    source: vardict_intervals
  - id: allele_freq_threshold
    source: allele_freq_threshold
  - id: header_lines
    source: vardict_header_lines
  - id: reference
    source: reference
  scatter:
  - intervals
  run: tools/vardictSomaticVariantCaller_v0_1_0.cwl
  out:
  - id: vardict_variants
  - id: out
- id: vc_vardict_merge
  in:
  - id: vcfs
    source: vc_vardict/out
  run: tools/Gatk4GatherVcfs_4_1_3_0.cwl
  out:
  - id: out
- id: combine_variants
  in:
  - id: vcfs
    source:
    - vc_gatk_merge/out
    - vc_strelka/out
    - vc_vardict_merge/out
  - id: type
    source: combine_variants_type
  - id: columns
    source: combine_variants_columns
  - id: normal
    source: normal_name
  - id: tumor
    source: tumor_name
  run: tools/combinevariants_0_0_4.cwl
  out:
  - id: vcf
  - id: tsv
- id: sortCombined
  in:
  - id: vcf
    source: combine_variants/vcf
  run: tools/bcftoolssort_v1_9.cwl
  out:
  - id: out
