baseCommand:
- gatk
- ApplyBQSR
class: CommandLineTool
cwlVersion: v1.0
doc: "Apply base quality score recalibration: This tool performs the second pass in\
  \ a two-stage \nprocess called Base Quality Score Recalibration (BQSR). Specifically,\
  \ it recalibrates the \nbase qualities of the input reads based on the recalibration\
  \ table produced by the \nBaseRecalibrator tool, and outputs a recalibrated BAM\
  \ or CRAM file.\n\nSummary of the BQSR procedure: The goal of this procedure is\
  \ to correct for systematic bias \nthat affect the assignment of base quality scores\
  \ by the sequencer. The first pass consists \nof calculating error empirically and\
  \ finding patterns in how error varies with basecall \nfeatures over all bases.\
  \ The relevant observations are written to a recalibration table. \nThe second pass\
  \ consists of applying numerical corrections to each individual basecall \nbased\
  \ on the patterns identified in the first step (recorded in the recalibration table)\
  \ \nand write out the recalibrated data to a new BAM or CRAM file.\n\n- This tool\
  \ replaces the use of PrintReads for the application of base quality score \n  \
  \  recalibration as practiced in earlier versions of GATK (2.x and 3.x).\n- You\
  \ should only run ApplyBQSR with the covariates table created from the input BAM\
  \ or CRAM file(s).\n- Original qualities can be retained in the output file under\
  \ the \"OQ\" tag if desired. \n    See the `--emit-original-quals` argument for\
  \ details."
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
- default: generated-966c6a24-cf9f-11e9-a6a4-acde48001122.bam
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
