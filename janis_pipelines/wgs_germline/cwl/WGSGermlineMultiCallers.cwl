#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: WGS Germline (Multi callers)
doc: |
  This is a genomics pipeline to align sequencing data (Fastq pairs) into BAMs and call variants using:

  This workflow is a reference pipeline using the Janis Python framework (pipelines assistant).

  - Takes raw sequence data in the FASTQ format;
  - align to the reference genome using BWA MEM;
  - Marks duplicates using Picard;
  - Call the appropriate variant callers (GATK / Strelka / VarDict);
  - Outputs the final variants in the VCF format.
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
inputs:
  align_and_sort_sortsam_tmpDir:
    id: align_and_sort_sortsam_tmpDir
    doc: Undocumented option
    type: string
    default: ./tmp
  allele_freq_threshold:
    id: allele_freq_threshold
    doc: "The threshold for VarDict's allele frequency, default: 0.05 or 5%"
    type: float
    default: 0.05
  combine_variants_columns:
    id: combine_variants_columns
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
  combine_variants_type:
    id: combine_variants_type
    doc: germline | somatic
    type: string
    default: germline
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
  strelka_intervals:
    id: strelka_intervals
    doc: An interval for which to restrict the analysis to.
    type: File
    secondaryFiles:
    - .tbi
  vardict_header_lines:
    id: vardict_header_lines
    doc: |
      As with chromosomal sequences it is highly recommended (but not required) that the header include tags describing the contigs referred to in the VCF file. This furthermore allows these contigs to come from different files. The format is identical to that of a reference sequence, but with an additional URL tag to indicate where that sequence can be found. For example:

      .. code-block:

         ##contig=<ID=ctg1,URL=ftp://somewhere.org/assembly.fa,...>

      Source: (1.2.5 Alternative allele field format) https://samtools.github.io/hts-specs/VCFv4.1.pdf (edited) 
    type: File
  vardict_intervals:
    id: vardict_intervals
    doc: List of intervals over which to split the VarDict variant calling
    type:
      type: array
      items: File
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
    doc: Combined variants from all 3 callers
    type: File
    outputSource: sort_combined/out
  variants_gatk:
    id: variants_gatk
    doc: Merged variants from the GATK caller
    type: File
    outputSource: vc_gatk_merge/out
  variants_gatk_split:
    id: variants_gatk_split
    doc: Unmerged variants from the GATK caller (by interval)
    type:
      type: array
      items: File
    outputSource: vc_gatk/out
  variants_strelka:
    id: variants_strelka
    doc: Variants from the Strelka variant caller
    type: File
    outputSource: vc_strelka/out
  variants_vardict:
    id: variants_vardict
    doc: Merged variants from the VarDict caller
    type: File
    outputSource: vc_vardict_merge/out
  variants_vardict_split:
    id: variants_vardict_split
    doc: Unmerged variants from the VarDict caller (by interval)
    type:
      type: array
      items: File
    outputSource: vc_vardict/out
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
  combine_variants:
    in:
      type:
        id: type
        source: combine_variants_type
      columns:
        id: columns
        source: combine_variants_columns
      vcfs:
        id: vcfs
        source:
        - vc_gatk_merge/out
        - vc_strelka/out
        - vc_vardict_merge/out
    run: tools/combinevariants.cwl
    out:
    - vcf
    - tsv
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
        source: combine_variants/vcf
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
  vc_strelka:
    in:
      bam:
        id: bam
        source: merge_and_mark/out
      intervals:
        id: intervals
        source: strelka_intervals
      reference:
        id: reference
        source: reference
    run: tools/strelkaGermlineVariantCaller.cwl
    out:
    - diploid
    - variants
    - out
  vc_vardict:
    in:
      allele_freq_threshold:
        id: allele_freq_threshold
        source: allele_freq_threshold
      bam:
        id: bam
        source: merge_and_mark/out
      header_lines:
        id: header_lines
        source: vardict_header_lines
      intervals:
        id: intervals
        source: vardict_intervals
      reference:
        id: reference
        source: reference
      sample_name:
        id: sample_name
        source: sample_name
    scatter:
    - intervals
    run: tools/vardictGermlineVariantCaller.cwl
    out:
    - vardict_variants
    - out
  vc_vardict_merge:
    in:
      vcfs:
        id: vcfs
        source: vc_vardict/out
    run: tools/Gatk4GatherVcfs.cwl
    out:
    - out
id: WGSGermlineMultiCallers
