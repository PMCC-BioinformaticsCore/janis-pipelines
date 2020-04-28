#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: WGS Somatic (Multi callers)
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
  MultipleInputFeatureRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
inputs:
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
    - AD
    - DP
    - GT
  combine_variants_type:
    id: combine_variants_type
    doc: germline | somatic
    type: string
    default: somatic
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
  gridss_blacklist:
    id: gridss_blacklist
    doc: BED file containing regions to ignore.
    type: File
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
  strelka_intervals:
    id: strelka_intervals
    doc: An interval for which to restrict the analysis to.
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
  gridss_assembly:
    id: gridss_assembly
    doc: Assembly returned by GRIDSS
    type: File
    outputSource: vc_gridss/out
  normal_bam:
    id: normal_bam
    doc: Aligned and indexed NORMAL bam
    type: File
    secondaryFiles:
    - .bai
    outputSource: normal/out
  normal_report:
    id: normal_report
    doc: A zip file of the NORMAL FastQC quality reports.
    type:
      type: array
      items:
        type: array
        items: File
    outputSource: normal/reports
  tumor_bam:
    id: tumor_bam
    doc: Aligned and indexed TUMOR bam
    type: File
    secondaryFiles:
    - .bai
    outputSource: tumor/out
  tumor_report:
    id: tumor_report
    doc: A zip file of the TUMOR FastQC quality reports.
    type:
      type: array
      items:
        type: array
        items: File
    outputSource: tumor/reports
  variants:
    id: variants
    doc: Combined variants from all 3 callers
    type: File
    outputSource: combine_variants/vcf
  variants_gatk:
    id: variants_gatk
    doc: Merged variants from the GATK caller
    type: File
    outputSource: vc_gatk_merge/out
  variants_gridss:
    id: variants_gridss
    doc: Variants from the GRIDSS variant caller
    type: File
    outputSource: vc_gridss/out
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
steps:
  combine_variants:
    in:
      type:
        id: type
        source: combine_variants_type
      columns:
        id: columns
        source: combine_variants_columns
      normal:
        id: normal
        source: normal_name
      tumor:
        id: tumor
        source: tumor_name
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
  sortCombined:
    in:
      vcf:
        id: vcf
        source: combine_variants/vcf
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
  vc_gridss:
    in:
      bams:
        id: bams
        source:
        - normal/out
        - tumor/out
      blacklist:
        id: blacklist
        source: gridss_blacklist
      reference:
        id: reference
        source: reference
    run: tools/gridss.cwl
    out:
    - out
    - assembly
  vc_strelka:
    in:
      intervals:
        id: intervals
        source: strelka_intervals
      normal_bam:
        id: normal_bam
        source: normal/out
      reference:
        id: reference
        source: reference
      tumor_bam:
        id: tumor_bam
        source: tumor/out
    run: tools/strelkaSomaticVariantCaller.cwl
    out:
    - diploid
    - variants
    - out
  vc_vardict:
    in:
      allele_freq_threshold:
        id: allele_freq_threshold
        source: allele_freq_threshold
      header_lines:
        id: header_lines
        source: vardict_header_lines
      intervals:
        id: intervals
        source: vardict_intervals
      normal_bam:
        id: normal_bam
        source: tumor/out
      normal_name:
        id: normal_name
        source: normal_name
      reference:
        id: reference
        source: reference
      tumor_bam:
        id: tumor_bam
        source: normal/out
      tumor_name:
        id: tumor_name
        source: tumor_name
    scatter:
    - intervals
    run: tools/vardictSomaticVariantCaller.cwl
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
id: WGSSomaticMultiCallers
