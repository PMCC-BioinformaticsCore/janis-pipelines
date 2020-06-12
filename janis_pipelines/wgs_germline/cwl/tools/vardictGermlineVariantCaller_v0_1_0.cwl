#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0

requirements:
- class: InlineJavascriptRequirement
- class: StepInputExpressionRequirement

inputs:
- id: bam
  type: File
  secondaryFiles:
  - .bai
- id: intervals
  type: File
- id: sample_name
  type: string
- id: allele_freq_threshold
  type: float
  default: 0.5
- id: header_lines
  type: File
- id: reference
  type: File
  secondaryFiles:
  - .fai
  - .amb
  - .ann
  - .bwt
  - .pac
  - .sa
  - ^.dict
- id: vardict_chromNamesAreNumbers
  doc: Indicate the chromosome names are just numbers, such as 1, 2, not chr1, chr2
  type: boolean
  default: true
- id: vardict_vcfFormat
  doc: VCF format output
  type: boolean
  default: true
- id: vardict_chromColumn
  doc: The column for chromosome
  type: int
  default: 1
- id: vardict_regStartCol
  doc: The column for region start, e.g. gene start
  type: int
  default: 2
- id: vardict_geneEndCol
  doc: The column for region end, e.g. gene end
  type: int
  default: 3

outputs:
- id: vardict_variants
  type: File
  outputSource: vardict/out
- id: out
  type: File
  outputSource: trim/out

steps:
- id: vardict
  in:
  - id: intervals
    source: intervals
  - id: bam
    source: bam
  - id: reference
    source: reference
  - id: chromNamesAreNumbers
    source: vardict_chromNamesAreNumbers
  - id: chromColumn
    source: vardict_chromColumn
  - id: geneEndCol
    source: vardict_geneEndCol
  - id: alleleFreqThreshold
    source: allele_freq_threshold
  - id: sampleName
    source: sample_name
  - id: regStartCol
    source: vardict_regStartCol
  - id: vcfFormat
    source: vardict_vcfFormat
  - id: var2vcfSampleName
    source: sample_name
  - id: var2vcfAlleleFreqThreshold
    source: allele_freq_threshold
  run: vardict_germline_1_6_0.cwl
  out:
  - id: out
- id: annotate
  in:
  - id: file
    source: vardict/out
  - id: headerLines
    source: header_lines
  run: bcftoolsAnnotate_v1_5.cwl
  out:
  - id: out
- id: split_multi_allele
  in:
  - id: vcf
    source: annotate/out
  - id: reference
    source: reference
  run: SplitMultiAllele_v0_5772.cwl
  out:
  - id: out
- id: trim
  in:
  - id: vcf
    source: split_multi_allele/out
  run: trimIUPAC_0_0_5.cwl
  out:
  - id: out
