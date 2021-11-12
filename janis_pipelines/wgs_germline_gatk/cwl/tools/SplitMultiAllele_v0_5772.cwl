#!/usr/bin/env cwl-runner
class: CommandLineTool
cwlVersion: v1.2
label: Split Multiple Alleles
doc: ''

requirements:
- class: ShellCommandRequirement
- class: InlineJavascriptRequirement
- class: DockerRequirement
  dockerPull: heuermh/vt

inputs:
- id: vcf
  label: vcf
  type: File
  inputBinding:
    position: 1
    shellQuote: false
- id: reference
  label: reference
  type: File
  secondaryFiles:
  - pattern: .fai
  - pattern: .amb
  - pattern: .ann
  - pattern: .bwt
  - pattern: .pac
  - pattern: .sa
  - pattern: ^.dict
  inputBinding:
    prefix: -r
    position: 4
    shellQuote: false
- id: outputFilename
  label: outputFilename
  type:
  - string
  - 'null'
  default: generated.norm.vcf
  inputBinding:
    prefix: -o
    position: 6
    valueFrom: $(inputs.vcf.basename.replace(/.vcf.gz$/, "").replace(/.vcf$/, "")).norm.vcf
    shellQuote: false

outputs:
- id: out
  label: out
  type: File
  outputBinding:
    glob: $(inputs.vcf.basename.replace(/.vcf.gz$/, "").replace(/.vcf$/, "")).norm.vcf
    loadContents: false
stdout: _stdout
stderr: _stderr
arguments:
- position: 0
  valueFrom: 'vt decompose -s '
  shellQuote: false
- position: 2
  valueFrom: '| vt normalize -n -q - '
  shellQuote: false

hints:
- class: ToolTimeLimit
  timelimit: |-
    $([inputs.runtime_seconds, 86400].filter(function (inner) { return inner != null })[0])
id: SplitMultiAllele
