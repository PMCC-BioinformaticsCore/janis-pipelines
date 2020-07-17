#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.0
label: Annotate Bam Stats to Germline Vcf Workflow

requirements:
- class: InlineJavascriptRequirement
- class: StepInputExpressionRequirement

inputs:
- id: bam
  type: File
  secondaryFiles:
  - .bai
- id: vcf
  type: File
- id: samtoolsmpileup_countOrphans
  doc: do not discard anomalous read pairs
  type: boolean
  default: true
- id: samtoolsmpileup_noBAQ
  doc: disable BAQ (per-Base Alignment Quality)
  type: boolean
  default: true
- id: samtoolsmpileup_minBQ
  doc: Minimum base quality for a base to be considered [13]
  type: int
  default: 0
- id: samtoolsmpileup_maxDepth
  doc: max per-file depth; avoids excessive memory usage [8000]
  type: int
  default: 10000
- id: addbamstats_type
  doc: must be either germline or somatic
  type: string
  default: germline

outputs:
- id: out
  type: File
  outputSource: addbamstats/out

steps:
- id: samtoolsmpileup
  label: 'SamTools: Mpileup'
  in:
  - id: countOrphans
    source: samtoolsmpileup_countOrphans
  - id: noBAQ
    source: samtoolsmpileup_noBAQ
  - id: maxDepth
    source: samtoolsmpileup_maxDepth
  - id: positions
    source: vcf
  - id: minBQ
    source: samtoolsmpileup_minBQ
  - id: bam
    source: bam
  run: SamToolsMpileup_1_9_0.cwl
  out:
  - id: out
- id: addbamstats
  label: Add Bam Statistics to Vcf
  in:
  - id: mpileup
    source: samtoolsmpileup/out
  - id: inputVcf
    source: vcf
  - id: type
    source: addbamstats_type
  run: addBamStats_0_0_7.cwl
  out:
  - id: out
id: AddBamStatsGermline
