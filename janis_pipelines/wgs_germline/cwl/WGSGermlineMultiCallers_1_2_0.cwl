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
- id: bam
  doc: Aligned and indexed bam.
  type: File
  secondaryFiles:
  - .bai
  outputSource: merge_and_mark/out
- id: variants
  doc: Combined variants from all 3 callers
  type: File
  outputSource: sort_combined/out
- id: variants_gatk
  doc: Merged variants from the GATK caller
  type: File
  outputSource: vc_gatk_merge/out
- id: variants_vardict
  doc: Merged variants from the VarDict caller
  type: File
  outputSource: vc_vardict_merge/out
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
  in:
  - id: bams
    source: align_and_sort/out
  - id: sampleName
    source: sample_name
  run: tools/mergeAndMarkBams_4_1_3.cwl
  out:
  - id: out
- id: vc_gatk
  in:
  - id: bam
    source: merge_and_mark/out
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
  run: tools/GATK4_GermlineVariantCaller_4_1_3_0.cwl
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
  - id: bam
    source: merge_and_mark/out
  - id: reference
    source: reference
  - id: intervals
    source: strelka_intervals
  run: tools/strelkaGermlineVariantCaller_v0_1_0.cwl
  out:
  - id: diploid
  - id: variants
  - id: out
- id: vc_vardict
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
    source: vardict_header_lines
  - id: reference
    source: reference
  scatter:
  - intervals
  run: tools/vardictGermlineVariantCaller_v0_1_0.cwl
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
  run: tools/combinevariants_0_0_4.cwl
  out:
  - id: vcf
  - id: tsv
- id: sort_combined
  in:
  - id: vcf
    source: combine_variants/vcf
  run: tools/bcftoolssort_v1_9.cwl
  out:
  - id: out
