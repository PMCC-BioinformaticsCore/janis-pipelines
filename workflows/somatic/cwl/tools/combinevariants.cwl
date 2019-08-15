baseCommand: combine_vcf.py
class: CommandLineTool
cwlVersion: v1.0
id: combinevariants
inputs:
- default: generated-b24e370a-b1b2-11e9-8f78-acde48001122.combined.vcf
  id: outputFilename
  inputBinding:
    prefix: -o
  label: outputFilename
  type: string
- default: generated-b24e3750-b1b2-11e9-8f78-acde48001122.tsv
  doc: Region file containing all the variants, used as samtools mpileup
  id: regions
  inputBinding:
    prefix: --regions
  label: regions
  type: string
- doc: input vcfs, the priority of the vcfs will be based on the order of the input
  id: vcfs
  label: vcfs
  type:
    inputBinding:
      prefix: -i
    items: File
    type: array
- doc: germline | somatic
  id: type
  inputBinding:
    prefix: --type
  label: type
  type: string
- doc: Columns to keep, seperated by space output vcf (unsorted)
  id: columns
  label: columns
  type:
  - inputBinding:
      prefix: --columns
    items: string
    type: array
  - 'null'
- doc: Sample id of germline vcf, or normal sample id of somatic vcf
  id: normal
  inputBinding:
    prefix: --normal
  label: normal
  type:
  - string
  - 'null'
- doc: tumor sample ID, required if inputs are somatic vcfs
  id: tumor
  inputBinding:
    prefix: --tumor
  label: tumor
  type:
  - string
  - 'null'
- doc: The priority of the callers, must match with the callers in the source header
  id: priority
  inputBinding:
    prefix: --priority
  label: priority
  type:
  - int
  - 'null'
label: combinevariants
outputs:
- id: vcf
  label: vcf
  outputBinding:
    glob: $(inputs.outputFilename)
  type: File
- id: tsv
  label: tsv
  outputBinding:
    glob: $(inputs.regions)
  type: File
requirements:
  DockerRequirement:
    dockerPull: michaelfranklin/pmacutil:0.0.4
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
