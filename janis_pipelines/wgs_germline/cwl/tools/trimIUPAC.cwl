baseCommand: trimIUPAC.py
class: CommandLineTool
cwlVersion: v1.0
id: trimIUPAC
inputs:
- doc: The VCF to remove the IUPAC bases from
  id: vcf
  inputBinding:
    position: 0
  label: vcf
  type: File
- default: generated-546da88e-0fca-11ea-99c5-acde48001122.trimmed.vcf
  id: outputFilename
  inputBinding:
    position: 2
  label: outputFilename
  type: string
label: trimIUPAC
outputs:
- id: out
  label: out
  outputBinding:
    glob: $(inputs.outputFilename)
  type: File
requirements:
  DockerRequirement:
    dockerPull: michaelfranklin/pmacutil:0.0.4
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
