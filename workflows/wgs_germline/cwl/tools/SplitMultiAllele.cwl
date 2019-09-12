arguments:
- position: 1
  shellQuote: false
  valueFrom: sed 's/ID=AD,Number=./ID=AD,Number=R/' <
- position: 3
  shellQuote: false
  valueFrom: '|'
- position: 4
  shellQuote: false
  valueFrom: vt decompose -s - -o -
- position: 5
  shellQuote: false
  valueFrom: '|'
- position: 6
  shellQuote: false
  valueFrom: vt normalize -n -q - -o -
- position: 8
  shellQuote: false
  valueFrom: '|'
- position: 9
  shellQuote: false
  valueFrom: sed 's/ID=AD,Number=./ID=AD,Number=1/'
class: CommandLineTool
cwlVersion: v1.0
id: SplitMultiAllele
inputs:
- id: vcf
  inputBinding:
    position: 2
    shellQuote: false
  label: vcf
  type: File
- id: reference
  inputBinding:
    position: 7
    prefix: -r
    shellQuote: false
  label: reference
  secondaryFiles:
  - .amb
  - .ann
  - .bwt
  - .pac
  - .sa
  - .fai
  - ^.dict
  type: File
- default: generated-d8f8b07e-d5b6-11e9-a585-f218985ebfa7.norm.vcf
  id: outputFilename
  inputBinding:
    position: 10
    prefix: '>'
    shellQuote: false
  label: outputFilename
  type: string
label: SplitMultiAllele
outputs:
- id: out
  label: out
  outputBinding:
    glob: $(inputs.outputFilename)
  type: File
requirements:
  DockerRequirement:
    dockerPull: heuermh/vt
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
