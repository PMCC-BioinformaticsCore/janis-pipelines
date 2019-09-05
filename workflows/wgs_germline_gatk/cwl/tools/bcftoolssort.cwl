baseCommand:
- bcftools
- sort
class: CommandLineTool
cwlVersion: v1.0
id: bcftoolssort
inputs:
- doc: The VCF file to sort
  id: vcf
  inputBinding:
    position: 1
  label: vcf
  type: File
- default: generated-7ede21a2-cf83-11e9-907b-acde48001122.sorted.vcf
  doc: (-o) output file name [stdout]
  id: outputFilename
  inputBinding:
    prefix: --output-file
  label: outputFilename
  type: string
- doc: '(-O) b: compressed BCF, u: uncompressed BCF, z: compressed VCF, v: uncompressed
    VCF [v]'
  id: outputType
  inputBinding:
    prefix: --output-type
  label: outputType
  type:
  - string
  - 'null'
- doc: (-T) temporary files [/tmp/bcftools-sort.XXXXXX/]
  id: tempDir
  inputBinding:
    prefix: --temp-dir
  label: tempDir
  type:
  - string
  - 'null'
label: bcftoolssort
outputs:
- id: out
  label: out
  outputBinding:
    glob: $(inputs.outputFilename)
  type: File
requirements:
  DockerRequirement:
    dockerPull: michaelfranklin/bcftools:1.9
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
