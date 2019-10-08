arguments:
- position: 2
  valueFrom: -S
- position: 3
  valueFrom: -h
- position: 4
  valueFrom: -b
baseCommand:
- samtools
- view
class: CommandLineTool
cwlVersion: v1.0
doc: "Ensure SAMTOOLS.SORT is inheriting from parent metadata\n        \n---------------------------------------------------------------------------------------------------\n\
  \    \nWith no options or regions specified, prints all alignments in the specified\
  \ input alignment file \n(in SAM, BAM, or CRAM format) to standard output in SAM\
  \ format (with no header).\n\nYou may specify one or more space-separated region\
  \ specifications after the input filename to \nrestrict output to only those alignments\
  \ which overlap the specified region(s). \nUse of region specifications requires\
  \ a coordinate-sorted and indexed input file (in BAM or CRAM format)."
id: SamToolsView
inputs:
- doc: Output in the CRAM format (requires -T).
  id: cramOutput
  inputBinding:
    position: 5
    prefix: -C
  label: cramOutput
  type:
  - boolean
  - 'null'
- doc: Enable fast BAM compression (implies -b).
  id: compressedBam
  inputBinding:
    position: 5
    prefix: '-1'
  label: compressedBam
  type:
  - boolean
  - 'null'
- doc: Output uncompressed BAM. This option saves time spent on compression/decompression
    and is thus preferred when the output is piped to another samtools command.
  id: uncompressedBam
  inputBinding:
    position: 5
    prefix: -u
  label: uncompressedBam
  type:
  - boolean
  - 'null'
- doc: Output the header only.
  id: onlyOutputHeader
  inputBinding:
    position: 5
    prefix: -H
  label: onlyOutputHeader
  type:
  - boolean
  - 'null'
- doc: Instead of printing the alignments, only count them and print the total number.
    All filter options, such as -f, -F, and -q, are taken into account.
  id: countAlignments
  inputBinding:
    position: 5
    prefix: -c
  label: countAlignments
  type:
  - boolean
  - 'null'
- doc: Write alignments that are not selected by the various filter options to FILE.
    When this option is used, all alignments (or all alignments intersecting the regions
    specified) are written to either the output file or this file, but never both.
  id: writeAlignments
  inputBinding:
    position: 5
    prefix: -U
  label: writeAlignments
  type:
  - File
  - 'null'
- doc: "A tab-delimited FILE. Each line must contain the reference name in the first\
    \ column and the length of the reference in the second column, with one line for\
    \ each distinct reference. Any additional fields beyond the second column are\
    \ ignored. This file also defines the order of the reference sequences in sorting.\
    \ If you run: `samtools faidx <ref.fa>', the resulting index file <ref.fa>.fai\
    \ can be used as this FILE."
  id: inputTSV
  inputBinding:
    position: 5
    prefix: -t
  label: inputTSV
  type:
  - File
  - 'null'
- doc: Only output alignments overlapping the input BED FILE [null].
  id: onlyOverlapping
  inputBinding:
    position: 5
    prefix: -L
  label: onlyOverlapping
  type:
  - File
  - 'null'
- doc: Use the multi-region iterator on the union of the BED file and command-line
    region arguments. This avoids re-reading the same regions of files so can sometimes
    be much faster. Note this also removes duplicate sequences. Without this a sequence
    that overlaps multiple regions specified on the command line will be reported
    multiple times.
  id: useMultiRegionIterator
  inputBinding:
    position: 5
    prefix: -M
  label: useMultiRegionIterator
  type:
  - boolean
  - 'null'
- doc: Output alignments in read group STR [null]. Note that records with no RG tag
    will also be output when using this option. This behaviour may change in a future
    release.
  id: outputAlignmentsInReadGroup
  inputBinding:
    position: 5
    prefix: -r
  label: outputAlignmentsInReadGroup
  type:
  - string
  - 'null'
- doc: Output alignments in read groups listed in FILE [null]. Note that records with
    no RG tag will also be output when using this option. This behaviour may change
    in a future release.
  id: outputAlignmentsInFileReadGroups
  inputBinding:
    position: 5
    prefix: -R
  label: outputAlignmentsInFileReadGroups
  type:
  - File
  - 'null'
- doc: Skip alignments with MAPQ smaller than INT [0].
  id: mapqThreshold
  inputBinding:
    position: 5
    prefix: -q
  label: mapqThreshold
  type:
  - int
  - 'null'
- doc: Only output alignments in library STR [null].
  id: outputAlignmentsInLibrary
  inputBinding:
    position: 5
    prefix: -l
  label: outputAlignmentsInLibrary
  type:
  - string
  - 'null'
- doc: "Only output alignments with number of CIGAR bases consuming query sequence\
    \ \u2265 INT [0]"
  id: outputAlignmentsMeetingCIGARThreshold
  inputBinding:
    position: 5
    prefix: -m
  label: outputAlignmentsMeetingCIGARThreshold
  type:
  - int
  - 'null'
- doc: Only output alignments with all bits set in INT present in the FLAG field.
    INT can be specified in hex by beginning with `0x' (i.e. /^0x[0-9A-F]+/) or in
    octal by beginning with `0' (i.e. /^0[0-7]+/) [0].
  id: outputAlignmentsWithBitsSet
  inputBinding:
    position: 5
    prefix: -f
  label: outputAlignmentsWithBitsSet
  type:
  - string
  - 'null'
- doc: Do not output alignments with any bits set in INT present in the FLAG field.
    INT can be specified in hex by beginning with `0x' (i.e. /^0x[0-9A-F]+/) or in
    octal by beginning with `0' (i.e. /^0[0-7]+/) [0].
  id: doNotOutputAlignmentsWithBitsSet
  inputBinding:
    position: 5
    prefix: -F
  label: doNotOutputAlignmentsWithBitsSet
  type:
  - string
  - 'null'
- doc: Do not output alignments with all bits set in INT present in the FLAG field.
    This is the opposite of -f such that -f12 -G12 is the same as no filtering at
    all. INT can be specified in hex by beginning with `0x' (i.e. /^0x[0-9A-F]+/)
    or in octal by beginning with `0' (i.e. /^0[0-7]+/) [0].
  id: doNotOutputAlignmentsWithAllBitsSet
  inputBinding:
    position: 5
    prefix: -G
  label: doNotOutputAlignmentsWithAllBitsSet
  type:
  - string
  - 'null'
- doc: Read tag to exclude from output (repeatable) [null]
  id: readTagToExclude
  inputBinding:
    position: 5
    prefix: -x
  label: readTagToExclude
  type:
  - string
  - 'null'
- doc: Collapse the backward CIGAR operation.
  id: collapseBackwardCIGAR
  inputBinding:
    position: 5
    prefix: -B
  label: collapseBackwardCIGAR
  type:
  - boolean
  - 'null'
- doc: 'Output only a proportion of the input alignments. This subsampling acts in
    the same way on all of the alignment records in the same template or read pair,
    so it never keeps a read but not its mate. The integer and fractional parts of
    the -s INT.FRAC option are used separately: the part after the decimal point sets
    the fraction of templates/pairs to be kept, while the integer part is used as
    a seed that influences which subset of reads is kept.'
  id: subsamplingProportion
  inputBinding:
    position: 5
    prefix: -s
  label: subsamplingProportion
  type:
  - float
  - 'null'
- doc: Number of BAM compression threads to use in addition to main thread [0].
  id: threads
  inputBinding:
    position: 5
    prefix: -@
  label: threads
  type:
  - int
  - 'null'
- id: sam
  inputBinding:
    position: 10
  label: sam
  type: File
- doc: A FASTA format reference FILE, optionally compressed by bgzip and ideally indexed
    by samtools faidx. If an index is not present, one will be generated for you.
  id: reference
  inputBinding:
    position: 6
    prefix: -T
  label: reference
  secondaryFiles:
  - .amb
  - .ann
  - .bwt
  - .pac
  - .sa
  - .fai
  - ^.dict
  type:
  - File
  - 'null'
- default: generated-543a2dea-cf9e-11e9-97c1-acde48001122.bam
  doc: Output to FILE [stdout].
  id: outputFilename
  inputBinding:
    position: 5
    prefix: -o
  label: outputFilename
  type: string
label: SamToolsView
outputs:
- id: out
  label: out
  outputBinding:
    glob: $(inputs.outputFilename)
  type: File
requirements:
  DockerRequirement:
    dockerPull: biocontainers/samtools:v1.7.0_cv3
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
