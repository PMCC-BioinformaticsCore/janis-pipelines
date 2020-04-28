#!/usr/bin/env cwl-runner
class: CommandLineTool
cwlVersion: v1.0
label: SplitMultiAllele
requirements:
  DockerRequirement:
    dockerPull: heuermh/vt
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
inputs:
- id: vcf
  label: vcf
  type: File
  inputBinding:
    position: 3
    shellQuote: false
- id: reference
  label: reference
  type: File
  secondaryFiles:
  - .fai
  - .amb
  - .ann
  - .bwt
  - .pac
  - .sa
  - ^.dict
  inputBinding:
    prefix: -r
    position: 8
    shellQuote: false
- id: outputFilename
  label: outputFilename
  type: string
  default: generated-.norm.vcf
  inputBinding:
    prefix: '>'
    position: 10
    shellQuote: false
outputs:
- id: out
  label: out
  type: File
  outputBinding:
    glob: $(inputs.outputFilename)
arguments:
- position: 0
  valueFrom: zcat
  shellQuote: false
- position: 1
  valueFrom: '|'
  shellQuote: false
- position: 2
  valueFrom: sed 's/ID=AD,Number=./ID=AD,Number=R/' <
  shellQuote: false
- position: 4
  valueFrom: '|'
  shellQuote: false
- position: 5
  valueFrom: vt decompose -s - -o -
  shellQuote: false
- position: 6
  valueFrom: '|'
  shellQuote: false
- position: 7
  valueFrom: vt normalize -n -q - -o -
  shellQuote: false
- position: 9
  valueFrom: '|'
  shellQuote: false
- position: 10
  valueFrom: sed 's/ID=AD,Number=./ID=AD,Number=1/'
  shellQuote: false
id: SplitMultiAllele
