baseCommand: combine_vcf.py
class: CommandLineTool
cwlVersion: v1.0
doc: "\nusage: combine_vcf.py [-h] -i I --columns COLUMNS -o O --type\n          \
  \            {germline,somatic} [--regions REGIONS] [--normal NORMAL]\n        \
  \              [--tumor TUMOR] [--priority PRIORITY [PRIORITY ...]]\n\nExtracts\
  \ and combines the information from germline / somatic vcfs into one\n\nrequired\
  \ arguments:\n  -i I                  input vcfs, the priority of the vcfs will\
  \ be based on\n                        the order of the input. This parameter can\
  \ be\n                        specified more than once\n  --columns COLUMNS    \
  \ Columns to keep. This parameter can be specified more\n                      \
  \  than once\n  -o O                  output vcf (unsorted)\n  --type {germline,somatic}\n\
  \                        must be either germline or somatic\n  --regions REGIONS\
  \     Region file containing all the variants, used as\n                       \
  \ samtools mpileup\n  --normal NORMAL       Sample id of germline vcf, or normal\
  \ sample id of\n                        somatic vcf\n  --tumor TUMOR         tumor\
  \ sample ID, required if inputs are somatic vcfs\n  --priority PRIORITY [PRIORITY\
  \ ...]\n                        The priority of the callers, must match with the\n\
  \                        callers in the source header\n\noptional arguments:\n \
  \ -h, --help            show this help message and exit\n"
id: combinevariants
inputs:
- default: generated-d5e10f96-e018-11e9-851b-a0cec8186c53.combined.vcf
  id: outputFilename
  inputBinding:
    prefix: -o
  label: outputFilename
  type: string
- default: generated-d5e10ff0-e018-11e9-851b-a0cec8186c53.tsv
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
