baseCommand:
- gatk
- ApplyBQSR
class: CommandLineTool
cwlVersion: v1.0
id: GATK4ApplyBQSR
inputs:
- doc: The SAM/BAM/CRAM file containing reads.
  id: bam
  inputBinding:
    position: 10
    prefix: -I
  label: bam
  secondaryFiles:
  - ^.bai
  type: File
- doc: Reference sequence
  id: reference
  inputBinding:
    prefix: -R
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
- default: generated-7ede0172-cf83-11e9-907b-acde48001122.bam
  doc: Write output to this file
  id: outputFilename
  inputBinding:
    prefix: -O
  label: outputFilename
  type: string
- doc: Input recalibration table for BQSR
  id: recalFile
  inputBinding:
    prefix: --bqsr-recal-file
  label: recalFile
  type:
  - File
  - 'null'
- doc: -L (BASE) One or more genomic intervals over which to operate
  id: intervals
  inputBinding:
    prefix: --intervals
  label: intervals
  type:
  - File
  - 'null'
- default: /tmp/
  doc: Temp directory to use.
  id: tmpDir
  inputBinding:
    position: 11
    prefix: --tmp-dir
  label: tmpDir
  type: string
label: GATK4ApplyBQSR
outputs:
- id: out
  label: out
  outputBinding:
    glob: $(inputs.outputFilename)
  secondaryFiles:
  - ^.bai
  type: File
requirements:
  DockerRequirement:
    dockerPull: broadinstitute/gatk:4.0.12.0
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
