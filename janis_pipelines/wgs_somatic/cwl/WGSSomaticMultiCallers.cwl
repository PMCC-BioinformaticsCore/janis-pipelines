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
id: WGSSomaticMultiCallers
inputs:
  allele_freq_threshold:
    default: 0.05
    doc: "The threshold for VarDict's allele frequency, default: 0.05 or 5%"
    id: allele_freq_threshold
    type: float
  combine_variants_columns:
    default:
    - AD
    - DP
    - GT
    doc: Columns to keep, seperated by space output vcf (unsorted)
    id: combine_variants_columns
    type:
      items: string
      type: array
  combine_variants_type:
    default: somatic
    doc: germline | somatic
    id: combine_variants_type
    type: string
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
  gridss_blacklist:
    doc: BED file containing regions to ignore.
    id: gridss_blacklist
    type: File
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
    - .fai
    - .amb
    - .ann
    - .bwt
    - .pac
    - .sa
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
  strelka_intervals:
    doc: An interval for which to restrict the analysis to.
    id: strelka_intervals
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
  vardict_header_lines:
    doc: "As with chromosomal sequences it is highly recommended (but not required)\
      \ that the header include tags describing the contigs referred to in the VCF\
      \ file. This furthermore allows these contigs to come from different files.\
      \ The format is identical to that of a reference sequence, but with an additional\
      \ URL tag to indicate where that sequence can be found. For example:\n\n.. code-block:\n\
      \n   ##contig=<ID=ctg1,URL=ftp://somewhere.org/assembly.fa,...>\n\nSource: (1.2.5\
      \ Alternative allele field format) https://samtools.github.io/hts-specs/VCFv4.1.pdf\
      \ (edited) \n"
    id: vardict_header_lines
    type: File
  vardict_intervals:
    doc: List of intervals over which to split the VarDict variant calling
    id: vardict_intervals
    type:
      items: File
      type: array
label: WGS Somatic (Multi callers)
outputs:
  gridss_assembly:
    doc: Assembly returned by GRIDSS
    id: gridss_assembly
    outputSource: vc_gridss/out
    type: File
  normal_bam:
    doc: Aligned and indexed NORMAL bam
    id: normal_bam
    outputSource: normal/out
    secondaryFiles:
    - .bai
    type: File
  normal_report:
    doc: A zip file of the NORMAL FastQC quality reports.
    id: normal_report
    outputSource: normal/reports
    type:
      items:
        items: File
        type: array
      type: array
  tumor_bam:
    doc: Aligned and indexed TUMOR bam
    id: tumor_bam
    outputSource: tumor/out
    secondaryFiles:
    - .bai
    type: File
  tumor_report:
    doc: A zip file of the TUMOR FastQC quality reports.
    id: tumor_report
    outputSource: tumor/reports
    type:
      items:
        items: File
        type: array
      type: array
  variants:
    doc: Combined variants from all 3 callers
    id: variants
    outputSource: combine_variants/vcf
    type: File
  variants_gatk:
    doc: Merged variants from the GATK caller
    id: variants_gatk
    outputSource: vc_gatk_merge/out
    type: File
  variants_gridss:
    doc: Variants from the GRIDSS variant caller
    id: variants_gridss
    outputSource: vc_gridss/out
    type: File
  variants_strelka:
    doc: Variants from the Strelka variant caller
    id: variants_strelka
    outputSource: vc_strelka/out
    type: File
  variants_vardict:
    doc: Merged variants from the VarDict caller
    id: variants_vardict
    outputSource: vc_vardict_merge/out
    type: File
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}
steps:
  combine_variants:
    in:
      columns:
        id: columns
        source: combine_variants_columns
      normal:
        id: normal
        source: normal_name
      tumor:
        id: tumor
        source: tumor_name
      type:
        id: type
        source: combine_variants_type
      vcfs:
        id: vcfs
        source:
        - vc_gatk_merge/out
        - vc_strelka/out
        - vc_vardict_merge/out
    out:
    - vcf
    - tsv
    run: tools/combinevariants.cwl
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
    out:
    - out
    - reports
    run: tools/somatic_subpipeline.cwl
  sortCombined:
    in:
      vcf:
        id: vcf
        source: combine_variants/vcf
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
    out:
    - out
    - assembly
    run: tools/gridss.cwl
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
    out:
    - diploid
    - variants
    - out
    run: tools/strelkaSomaticVariantCaller.cwl
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
    out:
    - vardict_variants
    - out
    run: tools/vardictSomaticVariantCaller.cwl
    scatter:
    - intervals
  vc_vardict_merge:
    in:
      vcfs:
        id: vcfs
        source: vc_vardict/out
    out:
    - out
    run: tools/Gatk4GatherVcfs.cwl
