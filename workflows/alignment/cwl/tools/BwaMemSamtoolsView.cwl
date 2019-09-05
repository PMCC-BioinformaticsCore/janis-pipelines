arguments:
- position: 0
  shellQuote: false
  valueFrom: bwa
- position: 1
  shellQuote: false
  valueFrom: mem
- position: 5
  shellQuote: false
  valueFrom: '|'
- position: 6
  shellQuote: false
  valueFrom: samtools
- position: 7
  shellQuote: false
  valueFrom: view
- position: 8
  prefix: -T
  shellQuote: false
  valueFrom: $(inputs.reference)
- position: 8
  prefix: --threads
  shellQuote: false
  valueFrom: $(inputs.runtime_cpu)
- position: 8
  shellQuote: false
  valueFrom: -h
- position: 8
  shellQuote: false
  valueFrom: -b
- position: 2
  prefix: -R
  valueFrom: $("@RG\\tID:{name}\\tSM:{name}\\tLB:{name}\\tPL:ILLUMINA".replace(/\{name\}/g,
    inputs.sampleName))
- position: 2
  prefix: -t
  shellQuote: false
  valueFrom: $(inputs.runtime_cpu)
class: CommandLineTool
cwlVersion: v1.0
id: BwaMemSamtoolsView
inputs:
- id: reference
  inputBinding:
    position: 2
    shellQuote: false
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
- id: reads
  inputBinding:
    itemSeparator: ' '
    position: 3
    shellQuote: false
  label: reads
  type:
    items: File
    type: array
- id: mates
  inputBinding:
    itemSeparator: ' '
    position: 4
    shellQuote: false
  label: mates
  type:
  - items: File
    type: array
  - 'null'
- default: generated-57ab2f16-cf9d-11e9-938d-acde48001122.bam
  doc: output file name [stdout]
  id: outputFilename
  inputBinding:
    position: 8
    prefix: -o
    shellQuote: false
  label: outputFilename
  type: string
- doc: "Used to construct the readGroupHeaderLine with format: '@RG\\tID:{name}\\\
    tSM:{name}\\tLB:{name}\\tPL:ILLUMINA'"
  id: sampleName
  label: sampleName
  type: string
- doc: 'Matches shorter than INT will be missed. The alignment speed is usually insensitive
    to this value unless it significantly deviates 20. (Default: 19)'
  id: minimumSeedLength
  inputBinding:
    position: 2
    prefix: -k
    shellQuote: false
  label: minimumSeedLength
  type:
  - int
  - 'null'
- doc: 'Essentially, gaps longer than ${bandWidth} will not be found. Note that the
    maximum gap length is also affected by the scoring matrix and the hit length,
    not solely determined by this option. (Default: 100)'
  id: bandwidth
  inputBinding:
    position: 2
    prefix: -w
    shellQuote: false
  label: bandwidth
  type:
  - int
  - 'null'
- doc: "(Z-dropoff): Stop extension when the difference between the best and the current\
    \ extension score is above |i-j|*A+INT, where i and j are the current positions\
    \ of the query and reference, respectively, and A is the matching score. Z-dropoff\
    \ is similar to BLAST\u2019s X-dropoff except that it doesn\u2019t penalize gaps\
    \ in one of the sequences in the alignment. Z-dropoff not only avoids unnecessary\
    \ extension, but also reduces poor alignments inside a long good alignment. (Default:\
    \ 100)"
  id: offDiagonalXDropoff
  inputBinding:
    position: 2
    prefix: -d
    shellQuote: false
  label: offDiagonalXDropoff
  type:
  - int
  - 'null'
- doc: 'Trigger re-seeding for a MEM longer than minSeedLen*FLOAT. This is a key heuristic
    parameter for tuning the performance. Larger value yields fewer seeds, which leads
    to faster alignment speed but lower accuracy. (Default: 1.5)'
  id: reseedTrigger
  inputBinding:
    position: 2
    prefix: -r
    shellQuote: false
  label: reseedTrigger
  type:
  - float
  - 'null'
- doc: 'Discard a MEM if it has more than INT occurence in the genome. This is an
    insensitive parameter. (Default: 10000)'
  id: occurenceDiscard
  inputBinding:
    position: 2
    prefix: -c
    shellQuote: false
  label: occurenceDiscard
  type:
  - int
  - 'null'
- doc: In the paired-end mode, perform SW to rescue missing hits only but do not try
    to find hits that fit a proper pair.
  id: performSW
  inputBinding:
    position: 2
    prefix: -P
    shellQuote: false
  label: performSW
  type:
  - boolean
  - 'null'
- doc: 'Matching score. (Default: 1)'
  id: matchingScore
  inputBinding:
    position: 2
    prefix: -A
    shellQuote: false
  label: matchingScore
  type:
  - int
  - 'null'
- doc: 'Mismatch penalty. The sequence error rate is approximately: {.75 * exp[-log(4)
    * B/A]}. (Default: 4)'
  id: mismatchPenalty
  inputBinding:
    position: 2
    prefix: -B
    shellQuote: false
  label: mismatchPenalty
  type:
  - int
  - 'null'
- doc: 'Gap open penalty. (Default: 6)'
  id: openGapPenalty
  inputBinding:
    position: 2
    prefix: -O
    shellQuote: false
  label: openGapPenalty
  type:
  - int
  - 'null'
- doc: 'Gap extension penalty. A gap of length k costs O + k*E (i.e. -O is for opening
    a zero-length gap). (Default: 1)'
  id: gapExtensionPenalty
  inputBinding:
    position: 2
    prefix: -E
    shellQuote: false
  label: gapExtensionPenalty
  type:
  - int
  - 'null'
- doc: 'Clipping penalty. When performing SW extension, BWA-MEM keeps track of the
    best score reaching the end of query. If this score is larger than the best SW
    score minus the clipping penalty, clipping will not be applied. Note that in this
    case, the SAM AS tag reports the best SW score; clipping penalty is not deducted.
    (Default: 5)'
  id: clippingPenalty
  inputBinding:
    position: 2
    prefix: -L
    shellQuote: false
  label: clippingPenalty
  type:
  - int
  - 'null'
- doc: 'Penalty for an unpaired read pair. BWA-MEM scores an unpaired read pair as
    scoreRead1+scoreRead2-INT and scores a paired as scoreRead1+scoreRead2-insertPenalty.
    It compares these two scores to determine whether we should force pairing. (Default:
    9)'
  id: unpairedReadPenalty
  inputBinding:
    position: 2
    prefix: -U
    shellQuote: false
  label: unpairedReadPenalty
  type:
  - int
  - 'null'
- doc: 'Assume the first input query file is interleaved paired-end FASTA/Q. '
  id: assumeInterleavedFirstInput
  inputBinding:
    position: 2
    prefix: -p
    shellQuote: false
  label: assumeInterleavedFirstInput
  type:
  - boolean
  - 'null'
- doc: "Don\u2019t output alignment with score lower than INT. Only affects output.\
    \ (Default: 30)"
  id: outputAlignmentThreshold
  inputBinding:
    position: 2
    prefix: -T
    shellQuote: false
  label: outputAlignmentThreshold
  type:
  - int
  - 'null'
- doc: Output all found alignments for single-end or unpaired paired-end reads. These
    alignments will be flagged as secondary alignments.
  id: outputAllElements
  inputBinding:
    position: 2
    prefix: -a
    shellQuote: false
  label: outputAllElements
  type:
  - boolean
  - 'null'
- doc: Append append FASTA/Q comment to SAM output. This option can be used to transfer
    read meta information (e.g. barcode) to the SAM output. Note that the FASTA/Q
    comment (the string after a space in the header line) must conform the SAM spec
    (e.g. BC:Z:CGTAC). Malformated comments lead to incorrect SAM output.
  id: appendComments
  inputBinding:
    position: 2
    prefix: -C
    shellQuote: false
  label: appendComments
  type:
  - boolean
  - 'null'
- doc: "Use hard clipping \u2019H\u2019 in the SAM output. This option may dramatically\
    \ reduce the redundancy of output when mapping long contig or BAC sequences."
  id: hardClipping
  inputBinding:
    position: 2
    prefix: -H
    shellQuote: false
  label: hardClipping
  type:
  - boolean
  - 'null'
- doc: Mark shorter split hits as secondary (for Picard compatibility).
  id: markShorterSplits
  inputBinding:
    position: 2
    prefix: -M
    shellQuote: false
  label: markShorterSplits
  type:
  - boolean
  - 'null'
- doc: 'Control the verbose level of the output. This option has not been fully supported
    throughout BWA. Ideally, a value: 0 for disabling all the output to stderr; 1
    for outputting errors only; 2 for warnings and errors; 3 for all normal messages;
    4 or higher for debugging. When this option takes value 4, the output is not SAM.
    (Default: 3)'
  id: verboseLevel
  inputBinding:
    position: 2
    prefix: -v
    shellQuote: false
  label: verboseLevel
  type:
  - int
  - 'null'
- doc: output reads not selected by filters to FILE [null]
  id: skippedReadsOutputFilename
  inputBinding:
    position: 8
    prefix: -U
    shellQuote: false
  label: skippedReadsOutputFilename
  type:
  - string
  - 'null'
- doc: FILE listing reference names and lengths (see long help) [null]
  id: referenceIndex
  inputBinding:
    position: 8
    prefix: -t
    shellQuote: false
  label: referenceIndex
  type:
  - File
  - 'null'
- doc: only include reads overlapping this BED FILE [null]
  id: intervals
  inputBinding:
    position: 8
    prefix: -L
    shellQuote: false
  label: intervals
  type:
  - File
  - 'null'
- doc: only include reads in read group STR [null]
  id: includeReadsInReadGroup
  inputBinding:
    position: 8
    prefix: -r
    shellQuote: false
  label: includeReadsInReadGroup
  type:
  - string
  - 'null'
- doc: only include reads with read group listed in FILE [null]
  id: includeReadsInFile
  inputBinding:
    position: 8
    prefix: -R
    shellQuote: false
  label: includeReadsInFile
  type:
  - File
  - 'null'
- doc: only include reads with mapping quality >= INT [0]
  id: includeReadsWithQuality
  inputBinding:
    position: 8
    prefix: -q
    shellQuote: false
  label: includeReadsWithQuality
  type:
  - int
  - 'null'
- doc: only include reads in library STR [null]
  id: includeReadsInLibrary
  inputBinding:
    position: 8
    prefix: -l
    shellQuote: false
  label: includeReadsInLibrary
  type:
  - string
  - 'null'
- doc: only include reads with number of CIGAR operations consuming query sequence
    >= INT [0]
  id: includeReadsWithCIGAROps
  inputBinding:
    position: 8
    prefix: -m
    shellQuote: false
  label: includeReadsWithCIGAROps
  type:
  - int
  - 'null'
- doc: only include reads with all of the FLAGs in INT present [0]
  id: includeReadsWithAllFLAGs
  inputBinding:
    itemSeparator: ' '
    position: 8
    prefix: -f
    shellQuote: false
  label: includeReadsWithAllFLAGs
  type:
  - items: int
    type: array
  - 'null'
- doc: only include reads with none of the FLAGS in INT present [0]
  id: includeReadsWithoutFLAGs
  inputBinding:
    itemSeparator: ' '
    position: 8
    prefix: -F
    shellQuote: false
  label: includeReadsWithoutFLAGs
  type:
  - items: int
    type: array
  - 'null'
- doc: only EXCLUDE reads with all of the FLAGs in INT present [0] fraction of templates/read
    pairs to keep; INT part sets seed)
  id: excludeReadsWithAllFLAGs
  inputBinding:
    itemSeparator: ' '
    position: 8
    prefix: -G
    shellQuote: false
  label: excludeReadsWithAllFLAGs
  type:
  - items: int
    type: array
  - 'null'
- doc: use the multi-region iterator (increases the speed, removes duplicates and
    outputs the reads as they are ordered in the file)
  id: useMultiRegionIterator
  inputBinding:
    position: 8
    prefix: -M
    shellQuote: false
  label: useMultiRegionIterator
  type:
  - boolean
  - 'null'
- doc: read tag to strip (repeatable) [null]
  id: readTagToStrip
  inputBinding:
    position: 8
    prefix: -x
    shellQuote: false
  label: readTagToStrip
  type:
  - string
  - 'null'
- doc: collapse the backward CIGAR operation Specify a single input file format option
    in the form of OPTION or OPTION=VALUE
  id: collapseBackwardCIGAROps
  inputBinding:
    position: 8
    prefix: -B
    shellQuote: false
  label: collapseBackwardCIGAROps
  type:
  - boolean
  - 'null'
- doc: (OPT[, -O)  Specify output format (SAM, BAM, CRAM) Specify a single output
    file format option in the form of OPTION or OPTION=VALUE
  id: outputFmt
  inputBinding:
    position: 8
    prefix: --output-fmt
    shellQuote: false
  label: outputFmt
  type:
  - string
  - 'null'
label: BwaMemSamtoolsView
outputs:
- id: out
  label: out
  outputBinding:
    glob: $(inputs.outputFilename)
  type: File
requirements:
  DockerRequirement:
    dockerPull: michaelfranklin/bwasamtools:0.7.17-1.9
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
