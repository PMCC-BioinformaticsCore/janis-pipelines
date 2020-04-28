#!/usr/bin/env cwl-runner
class: CommandLineTool
cwlVersion: v1.0
label: trimIUPAC
requirements:
  DockerRequirement:
    dockerPull: michaelfranklin/pmacutil:0.0.5
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
inputs:
- id: vcf
  label: vcf
  doc: The VCF to remove the IUPAC bases from
  type: File
  inputBinding:
    position: 0
- id: outputFilename
  label: outputFilename
  type: string
  default: generated-.trimmed.vcf
  inputBinding:
    position: 2
outputs:
- id: out
  label: out
  type: File
  outputBinding:
    glob: $(inputs.outputFilename)
baseCommand: trimIUPAC.py
id: trimIUPAC
