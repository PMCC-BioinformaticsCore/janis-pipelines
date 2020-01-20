baseCommand: gridss.sh
class: CommandLineTool
cwlVersion: v1.0
doc: "GRIDSS: the Genomic Rearrangement IDentification Software Suite\n\nGRIDSS is\
  \ a module software suite containing tools useful for the detection of genomic rearrangements.\n\
  GRIDSS includes a genome-wide break-end assembler, as well as a structural variation\
  \ caller for Illumina\nsequencing data. GRIDSS calls variants based on alignment-guided\
  \ positional de Bruijn graph genome-wide\nbreak-end assembly, split read, and read\
  \ pair evidence.\n\nGRIDSS makes extensive use of the standard tags defined by SAM\
  \ specifications. Due to the modular design,\nany step (such as split read identification)\
  \ can be replaced by another implementation that also outputs\nusing the standard\
  \ tags. It is hoped that GRIDSS can serve as an exemplar modular structural variant\n\
  pipeline designed for interoperability with other tools.\n\nIf you have any trouble\
  \ running GRIDSS, please raise an issue using the Issues tab above. Based on feedback\n\
  from users, a user guide will be produced outlining common workflows, pitfalls,\
  \ and use cases.\n"
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
- default: generated.vcf
  id: outputFilename
  inputBinding:
    position: 2
    prefix: --output
  label: outputFilename
  type: string
- default: generated.bam
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
