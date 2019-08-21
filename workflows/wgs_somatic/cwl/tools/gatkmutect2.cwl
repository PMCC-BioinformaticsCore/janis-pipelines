baseCommand:
- gatk
- Mutect2
class: CommandLineTool
cwlVersion: v1.0
doc: "Call somatic short variants via local assembly of haplotypes. Short variants\
  \ include single nucleotide (SNV) \nand insertion and deletion (indel) variants.\
  \ The caller combines the DREAM challenge-winning somatic \ngenotyping engine of\
  \ the original MuTect (Cibulskis et al., 2013) with the assembly-based machinery\
  \ of HaplotypeCaller.\n\nThis tool is featured in the Somatic Short Mutation calling\
  \ Best Practice Workflow. See Tutorial#11136 \nfor a step-by-step description of\
  \ the workflow and Article#11127 for an overview of what traditional \nsomatic calling\
  \ entails. For the latest pipeline scripts, see the Mutect2 WDL scripts directory.\
  \ \nAlthough we present the tool for somatic calling, it may apply to other contexts,\
  \ \nsuch as mitochondrial variant calling."
id: gatkmutect2
inputs:
- doc: BAM/SAM/CRAM file containing reads
  id: tumor
  inputBinding:
    position: 6
    prefix: -I
  label: tumor
  secondaryFiles:
  - ^.bai
  type: File
- doc: BAM sample name of tumor. May be URL-encoded as output by GetSampleName with
    -encode.
  id: tumorName
  inputBinding:
    position: 6
    prefix: -tumor
  label: tumorName
  type: string
- doc: BAM/SAM/CRAM file containing reads
  id: normal
  inputBinding:
    position: 5
    prefix: -I
  label: normal
  secondaryFiles:
  - ^.bai
  type: File
- doc: BAM sample name of normal. May be URL-encoded as output by GetSampleName with
    -encode.
  id: normalName
  inputBinding:
    position: 6
    prefix: -normal
  label: normalName
  type: string
- doc: One or more genomic intervals over which to operate
  id: intervals
  inputBinding:
    position: 7
    prefix: -L
  label: intervals
  type:
  - File
  - 'null'
- doc: Reference sequence file
  id: reference
  inputBinding:
    position: 8
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
- default: generated-4343d6f2-c3b0-11e9-af7e-f218985ebfa7.vcf.gz
  id: outputFilename
  inputBinding:
    position: 20
    prefix: -O
  label: outputFilename
  type: string
- id: germlineResource
  inputBinding:
    position: 10
    prefix: --germline-resource
  label: germlineResource
  secondaryFiles:
  - .idx
  type:
  - File
  - 'null'
- doc: Population allele fraction assigned to alleles not found in germline resource.
    Please see docs/mutect/mutect2.pdf fora derivation of the default value.
  id: afOfAllelesNotInResource
  inputBinding:
    position: 11
    prefix: --af-of-alleles-not-in-resource
  label: afOfAllelesNotInResource
  type:
  - float
  - 'null'
- doc: A panel of normals can be a useful (optional) input to help filter out commonly
    seen sequencing noise that may appear as low allele-fraction somatic variants.
  id: panelOfNormals
  inputBinding:
    position: 10
    prefix: --panel-of-normals
  label: panelOfNormals
  secondaryFiles:
  - .idx
  type:
  - File
  - 'null'
label: gatkmutect2
outputs:
- doc: To determine type
  id: out
  label: out
  outputBinding:
    glob: $(inputs.outputFilename)
  secondaryFiles:
  - .tbi
  type: File
requirements:
  DockerRequirement:
    dockerPull: broadinstitute/gatk:4.0.12.0
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
