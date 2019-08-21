baseCommand:
- gatk
- BaseRecalibrator
class: CommandLineTool
cwlVersion: v1.0
doc: "First pass of the base quality score recalibration. Generates a recalibration\
  \ table based on various covariates. \nThe default covariates are read group, reported\
  \ quality score, machine cycle, and nucleotide context.\n\nThis walker generates\
  \ tables based on specified covariates. It does a by-locus traversal operating only\
  \ at sites \nthat are in the known sites VCF. ExAc, gnomAD, or dbSNP resources can\
  \ be used as known sites of variation. \nWe assume that all reference mismatches\
  \ we see are therefore errors and indicative of poor base quality. \nSince there\
  \ is a large amount of data one can then calculate an empirical probability of error\
  \ given the \nparticular covariates seen at this site, where p(error) = num mismatches\
  \ / num observations. The output file is a \ntable (of the several covariate values,\
  \ num observations, num mismatches, empirical quality score)."
id: Gatk4BaseRecalibrator
inputs:
- default: /tmp/
  doc: Temp directory to use.
  id: tmpDir
  inputBinding:
    prefix: --tmp-dir
  label: tmpDir
  type: string
- doc: BAM/SAM/CRAM file containing reads
  id: bam
  inputBinding:
    position: 6
    prefix: -I
  label: bam
  secondaryFiles:
  - ^.bai
  type: File
- doc: '**One or more databases of known polymorphic sites used to exclude regions
    around known polymorphisms from analysis.** This algorithm treats every reference
    mismatch as an indication of error. However, real genetic variation is expected
    to mismatch the reference, so it is critical that a database of known polymorphic
    sites is given to the tool in order to skip over those sites. This tool accepts
    any number of Feature-containing files (VCF, BCF, BED, etc.) for use as this database.
    For users wishing to exclude an interval list of known variation simply use -XL
    my.interval.list to skip over processing those sites. Please note however that
    the statistics reported by the tool will not accurately reflected those sites
    skipped by the -XL argument.'
  id: knownSites
  inputBinding:
    position: 28
  label: knownSites
  type:
    inputBinding:
      prefix: --known-sites
    items: File
    type: array
- doc: Reference sequence file
  id: reference
  inputBinding:
    position: 5
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
- default: generated-1c8f3358-c3b0-11e9-917e-f218985ebfa7.table
  doc: "**The output recalibration table filename to create.** After the header, data\
    \ records occur one per line until the end of the file. The first several items\
    \ on a line are the values of the individual covariates and will change depending\
    \ on which covariates were specified at runtime. The last three items are the\
    \ data- that is, number of observations for this combination of covariates, number\
    \ of reference mismatches, and the raw empirical quality score calculated by phred-scaling\
    \ the mismatch rate. Use '/dev/stdout' to print to standard out."
  id: outputFilename
  inputBinding:
    position: 8
    prefix: -O
  label: outputFilename
  type: string
- doc: -L (BASE) One or more genomic intervals over which to operate
  id: intervals
  inputBinding:
    prefix: --intervals
  label: intervals
  type:
  - File
  - 'null'
label: Gatk4BaseRecalibrator
outputs:
- id: out
  label: out
  outputBinding:
    glob: $(inputs.outputFilename)
  type: File
requirements:
  DockerRequirement:
    dockerPull: broadinstitute/gatk:4.0.12.0
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
