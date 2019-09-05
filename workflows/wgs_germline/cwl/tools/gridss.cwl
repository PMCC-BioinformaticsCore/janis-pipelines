baseCommand: gridss.sh
class: CommandLineTool
cwlVersion: v1.0
id: gridss
inputs:
- id: bams
  inputBinding:
    position: 10
  label: bams
  type:
    items: File
    type: array
- id: reference
  inputBinding:
    position: 1
    prefix: --reference
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
- default: generated-6516cf1c-cf83-11e9-b4cb-acde48001122.vcf
  id: outputFilename
  inputBinding:
    position: 2
    prefix: --output
  label: outputFilename
  type: string
- default: generated-6516cf76-cf83-11e9-b4cb-acde48001122.bam
  id: assemblyFilename
  inputBinding:
    position: 3
    prefix: --assembly
  label: assemblyFilename
  type: string
- id: threads
  inputBinding:
    prefix: --threads
    valueFrom: $(inputs.runtime_cpu)
  label: threads
  type:
  - int
  - 'null'
- id: blacklist
  inputBinding:
    position: 4
    prefix: --blacklist
  label: blacklist
  type:
  - File
  - 'null'
label: gridss
outputs:
- id: out
  label: out
  outputBinding:
    glob: $(inputs.outputFilename)
  type: File
- id: assembly
  label: assembly
  outputBinding:
    glob: $(inputs.assemblyFilename)
  type: File
requirements:
  DockerRequirement:
    dockerPull: michaelfranklin/gridss:2.5.1-dev2
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
