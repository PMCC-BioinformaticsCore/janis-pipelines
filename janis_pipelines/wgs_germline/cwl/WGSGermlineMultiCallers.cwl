#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
doc: "This is a genomics pipeline to align sequencing data (Fastq pairs) into BAMs\
  \ and call variants using:\n\nThis workflow is a reference pipeline using the Janis\
  \ Python framework (pipelines assistant).\n\n- Takes raw sequence data in the FASTQ\
  \ format;\n- align to the reference genome using BWA MEM;\n- Marks duplicates using\
  \ Picard;\n- Call the appropriate variant callers (GATK / Strelka / VarDict);\n\
  - Outputs the final variants in the VCF format.\n"
id: WGSGermlineMultiCallers
inputs:
  align_and_sort_sortsam_tmpDir:
    default: ./tmp
    doc: Undocumented option
    id: align_and_sort_sortsam_tmpDir
    type: string
  allele_freq_threshold:
    default: 0.05
    doc: "The threshold for VarDict's allele frequency, default: 0.05 or 5%"
    id: allele_freq_threshold
    type: float
  combine_variants_columns:
    default:
    - AC
    - AN
    - AF
    - AD
    - DP
    - GT
    doc: Columns to keep, seperated by space output vcf (unsorted)
    id: combine_variants_columns
    type:
      items: string
      type: array
  combine_variants_type:
    default: germline
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
  strelka_intervals:
    doc: An interval for which to restrict the analysis to.
    id: strelka_intervals
    secondaryFiles:
    - .tbi
    type: File
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
label: WGS Germline (Multi callers)
outputs:
  bam:
    doc: Aligned and indexed bam.
    id: bam
    outputSource: merge_and_mark/out
    secondaryFiles:
    - .bai
    type: File
  reports:
    doc: A zip file of the FastQC quality report.
    id: reports
    outputSource: fastqc/out
    type:
      items:
        items: File
        type: array
      type: array
  variants_combined:
    doc: Combined variants from all 3 callers
    id: variants_combined
    outputSource: sort_combined/out
    type: File
  variants_gatk:
    doc: Merged variants from the GATK caller
    id: variants_gatk
    outputSource: vc_gatk_merge/out
    type: File
  variants_gatk_split:
    doc: Unmerged variants from the GATK caller (by interval)
    id: variants_gatk_split
    outputSource: vc_gatk/out
    type:
      items: File
      type: array
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
  variants_vardict_split:
    doc: Unmerged variants from the VarDict caller (by interval)
    id: variants_vardict_split
    outputSource: vc_vardict/out
    type:
      items: File
      type: array
requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
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
  combine_variants:
    in:
      columns:
        id: columns
        source: combine_variants_columns
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
        source: combine_variants/vcf
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
    out:
    - diploid
    - variants
    - out
    run: tools/strelkaGermlineVariantCaller.cwl
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
    out:
    - vardict_variants
    - out
    run: tools/vardictGermlineVariantCaller.cwl
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
