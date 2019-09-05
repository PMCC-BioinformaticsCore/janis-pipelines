baseCommand: cutadapt
class: CommandLineTool
cwlVersion: v1.0
id: cutadapt
inputs:
- id: fastq
  inputBinding:
    position: 5
  label: fastq
  type:
    items: File
    type: array
- doc: "Sequence of an adapter ligated to the 3' end (paired data: of the first read).\
    \ The adapter and subsequent bases are trimmed. If a '$' character is appended\
    \ ('anchoring'), the adapter is only found if it is a suffix of the read."
  id: adapter
  inputBinding:
    prefix: -a
  label: adapter
  type:
  - string
  - 'null'
- default: generated-7edd9da4-cf83-11e9-907b-acde48001122-R1.fastq.gz
  doc: "Write trimmed reads to FILE. FASTQ or FASTA format is chosen depending on\
    \ input. The summary report is sent to standard output. Use '{name}' in FILE to\
    \ demultiplex reads into multiple files. Default: write to standard output"
  id: outputFilename
  inputBinding:
    prefix: -o
  label: outputFilename
  type: string
- default: generated-7edd9da4-cf83-11e9-907b-acde48001122-R2.fastq.gz
  doc: Write second read in a pair to FILE.
  id: secondReadFile
  inputBinding:
    prefix: -p
  label: secondReadFile
  type: string
- doc: Print debugging information.
  id: debug
  inputBinding:
    prefix: --debug
  label: debug
  type:
  - boolean
  - 'null'
- doc: 'Allow only mismatches in alignments. Default: allow both mismatches and indels'
  id: noIndels
  inputBinding:
    prefix: --no-indels
  label: noIndels
  type:
  - boolean
  - 'null'
- doc: 'Interpret IUPAC wildcards in reads. Default: False'
  id: matchReadWildcards
  inputBinding:
    prefix: --match-read-wildcards
  label: matchReadWildcards
  type:
  - boolean
  - 'null'
- doc: Trim N's on ends of reads.
  id: trimN
  inputBinding:
    prefix: --trim-n
  label: trimN
  type:
  - boolean
  - 'null'
- doc: Discard reads that did not pass CASAVA filtering (header has :Y:).
  id: discardCasava
  inputBinding:
    prefix: --discard-casava
  label: discardCasava
  type:
  - boolean
  - 'null'
- doc: Print only error messages.
  id: quiet
  inputBinding:
    prefix: --quiet
  label: quiet
  type:
  - boolean
  - 'null'
- doc: Strip the _F3 suffix of read names
  id: stripF3
  inputBinding:
    prefix: --strip-f3
  label: stripF3
  type:
  - boolean
  - 'null'
- doc: Disable zero capping
  id: noZeroCap
  inputBinding:
    prefix: --no-zero-cap
  label: noZeroCap
  type:
  - boolean
  - 'null'
- doc: Read and write interleaved paired-end reads.
  id: interleaved
  inputBinding:
    prefix: --interleaved
  label: interleaved
  type:
  - boolean
  - 'null'
- doc: Discard reads that contain an adapter. Also use -O to avoid discarding too
    many randomly matching reads!
  id: discardTrimmed
  inputBinding:
    prefix: --discard-trimmed
  label: discardTrimmed
  type:
  - boolean
  - 'null'
- doc: Discard reads that do not contain an adapter.
  id: discardUntrimmed
  inputBinding:
    prefix: --discard-untrimmed
  label: discardUntrimmed
  type:
  - boolean
  - 'null'
- doc: MAQ- and BWA-compatible colorspace output. This enables -c, -d, -t, --strip-f3
    and -y '/1'.
  id: maq
  inputBinding:
    prefix: --maq
  label: maq
  type:
  - boolean
  - 'null'
- doc: '(any|both|first) Which of the reads in a paired-end read have to match the
    filtering criterion in order for the pair to be filtered. Default: any'
  id: pairFilter
  inputBinding:
    prefix: --pair-filter=
  label: pairFilter
  type:
  - string
  - 'null'
- doc: NextSeq-specific quality trimming (each read). Trims also dark cycles appearing
    as high-quality G bases.
  id: nextseqTrim
  inputBinding:
    prefix: --nextseq-trim=
  label: nextseqTrim
  type:
  - string
  - 'null'
- doc: "What to do with found adapters. trim: remove; mask: replace with 'N' characters;\
    \ none: leave unchanged (useful with --discard-untrimmed). Default: trim"
  id: action
  inputBinding:
    prefix: --action=
  label: action
  type:
  - string
  - 'null'
- doc: 'Assume that quality values in FASTQ are encoded as ascii(quality + N). This
    needs to be set to 64 for some old Illumina FASTQ files. Default: 33'
  id: qualityBase
  inputBinding:
    prefix: --quality-base=
  label: qualityBase
  type:
  - string
  - 'null'
- doc: Search for TAG followed by a decimal number in the description field of the
    read. Replace the decimal number with the correct length of the trimmed read.
    For example, use --length-tag 'length=' to correct fields like 'length=123'.
  id: lengthTag
  inputBinding:
    prefix: --length-tag=
  label: lengthTag
  type:
  - string
  - 'null'
- doc: Remove this suffix from read names if present. Can be given multiple times.
  id: stripSuffix
  inputBinding:
    prefix: --strip-suffix=
  label: stripSuffix
  type:
  - string
  - 'null'
- doc: Discard reads with more than COUNT 'N' bases. If COUNT is a number between
    0 and 1, it is interpreted as a fraction of the read length.
  id: maxN
  inputBinding:
    prefix: --max-n=
  label: maxN
  type:
  - int
  - 'null'
- doc: 'Which type of report to print. Default: full'
  id: report
  inputBinding:
    prefix: --report=
  label: report
  type:
  - string
  - 'null'
- doc: Write information about each read and its adapter matches into FILE. See the
    documentation for the file format.
  id: infoFile
  inputBinding:
    prefix: --info-file=
  label: infoFile
  type:
  - string
  - 'null'
- doc: When the adapter has N wildcard bases, write adapter bases matching wildcard
    positions to FILE. (Inaccurate with indels.)
  id: wildcardFile
  inputBinding:
    prefix: --wildcard-file=
  label: wildcardFile
  type:
  - string
  - 'null'
- doc: 'Write reads that are too short (according to length specified by -m) to FILE.
    Default: discard reads'
  id: tooShortOutput
  inputBinding:
    prefix: --too-short-output=
  label: tooShortOutput
  type:
  - string
  - 'null'
- doc: 'Write reads that are too long (according to length specified by -M) to FILE.
    Default: discard reads'
  id: tooLongOutput
  inputBinding:
    prefix: --too-long-output=
  label: tooLongOutput
  type:
  - string
  - 'null'
- doc: 'Write reads that do not contain any adapter to FILE. Default: output to same
    file as trimmed reads'
  id: untrimmedOutput
  inputBinding:
    prefix: --untrimmed-output=
  label: untrimmedOutput
  type:
  - string
  - 'null'
- doc: 'Write second read in a pair to this FILE when no adapter was found. Use with
    --untrimmed-output. Default: output to same file as trimmed reads'
  id: untrimmedPairedOutput
  inputBinding:
    prefix: --untrimmed-paired-output=
  label: untrimmedPairedOutput
  type:
  - string
  - 'null'
- doc: Write second read in a pair to this file if pair is too short. Use also --too-short-output.
  id: tooShortPairedOutput
  inputBinding:
    prefix: --too-short-paired-output=
  label: tooShortPairedOutput
  type:
  - string
  - 'null'
- doc: Write second read in a pair to this file if pair is too long. Use also --too-long-output.
  id: tooLongPairedOutput
  inputBinding:
    prefix: --too-long-paired-output=
  label: tooLongPairedOutput
  type:
  - string
  - 'null'
- doc: "Input file format; can be either 'fasta', 'fastq' or 'sra-fastq'. Ignored\
    \ when reading csfasta/qual files. Default: auto-detect from file name extension."
  id: inputFileFormat
  inputBinding:
    prefix: -f
  label: inputFileFormat
  type:
  - string
  - 'null'
- default: 0
  doc: 'Number of CPU cores to use. Use 0 to auto-detect. Default: 1'
  id: cores
  inputBinding:
    prefix: -j
  label: cores
  type: int
- doc: "Sequence of an adapter ligated to the 5' end (paired data: of the first read).\
    \ The adapter and any preceding bases are trimmed. Partial matches at the 5' end\
    \ are allowed. If a '^' character is prepended ('anchoring'), the adapter is only\
    \ found if it is a prefix of the read."
  id: adapter_g
  inputBinding:
    prefix: -g
  label: adapter_g
  type:
  - string
  - 'null'
- doc: "Sequence of an adapter that may be ligated to the 5' or 3' end (paired data:\
    \ of the first read). Both types of matches as described under -a und -g are allowed.\
    \ If the first base of the read is part of the match, the behavior is as with\
    \ -g, otherwise as with -a. This option is mostly for rescuing failed library\
    \ preparations - do not use if you know which end your adapter was ligated to!"
  id: adapter_both
  inputBinding:
    prefix: -b
  label: adapter_both
  type:
  - string
  - 'null'
- doc: 'Maximum allowed error rate as value between 0 and 1 (no. of errors divided
    by length of matching region). Default: 0.1 (=10%)'
  id: maximumErrorRate
  inputBinding:
    prefix: -e
  label: maximumErrorRate
  type:
  - float
  - 'null'
- doc: 'Remove up to COUNT adapters from each read. Default: 1'
  id: removeNAdapters
  inputBinding:
    prefix: -n
  label: removeNAdapters
  type:
  - int
  - 'null'
- doc: 'Require MINLENGTH overlap between read and adapter for an adapter to be found.
    Default: 3'
  id: overlapRequirement
  inputBinding:
    prefix: -O
  label: overlapRequirement
  type:
  - int
  - 'null'
- doc: Remove bases from each read (first read only if paired). If LENGTH is positive,
    remove bases from the beginning. If LENGTH is negative, remove bases from the
    end. Can be used twice if LENGTHs have different signs. This is applied *before*
    adapter trimming.
  id: removeNBases
  inputBinding:
    prefix: -u
  label: removeNBases
  type:
  - int
  - 'null'
- doc: --quality-cutoff=[5'CUTOFF,]3'CUTOFF Trim low-quality bases from 5' and/or
    3' ends of each read before adapter removal. Applied to both reads if data is
    paired. If one value is given, only the 3' end is trimmed. If two comma-separated
    cutoffs are given, the 5' end is trimmed with the first cutoff, the 3' end with
    the second.
  id: qualityCutoff
  inputBinding:
    prefix: -q
  label: qualityCutoff
  type:
  - int
  - 'null'
- doc: Shorten reads to LENGTH. Positive values remove bases at the end while negative
    ones remove bases at the beginning. This and the following modifications are applied
    after adapter trimming.
  id: shortenReadsToLength
  inputBinding:
    prefix: -l
  label: shortenReadsToLength
  type:
  - int
  - 'null'
- doc: Add this prefix to read names. Use {name} to insert the name of the matching
    adapter.
  id: readNamesPrefix
  inputBinding:
    prefix: -x
  label: readNamesPrefix
  type:
  - string
  - 'null'
- doc: Add this suffix to read names; can also include {name}
  id: readNamesSuffix
  inputBinding:
    prefix: -y
  label: readNamesSuffix
  type:
  - string
  - 'null'
- doc: '--minimum-length=LEN[:LEN2] Discard reads shorter than LEN. Default: 0'
  id: minReadLength
  inputBinding:
    prefix: -m
  label: minReadLength
  type:
  - int
  - 'null'
- doc: '--maximum-length=LEN[:LEN2] Discard reads longer than LEN. Default: no limit'
  id: maxReadsLength
  inputBinding:
    prefix: -M
  label: maxReadsLength
  type:
  - int
  - 'null'
- doc: When the adapter matches in the middle of a read, write the rest (after the
    adapter) to FILE.
  id: middleReadMatchFile
  inputBinding:
    prefix: -r
  label: middleReadMatchFile
  type:
  - string
  - 'null'
- doc: 3' adapter to be removed from second read in a pair.
  id: removeMiddle3Adapter
  inputBinding:
    prefix: -A
  label: removeMiddle3Adapter
  type:
  - string
  - 'null'
- doc: 5' adapter to be removed from second read in a pair.
  id: removeMiddle5Adapter
  inputBinding:
    prefix: -G
  label: removeMiddle5Adapter
  type:
  - string
  - 'null'
- doc: 5'/3 adapter to be removed from second read in a pair.
  id: removeMiddleBothAdapter
  inputBinding:
    prefix: -B
  label: removeMiddleBothAdapter
  type:
  - string
  - 'null'
- doc: Remove LENGTH bases from second read in a pair.
  id: removeNBasesFromSecondRead
  inputBinding:
    prefix: -U
  label: removeNBasesFromSecondRead
  type:
  - int
  - 'null'
- doc: Do not interpret IUPAC wildcards in adapters.
  id: noMatchAdapterWildcards
  inputBinding:
    prefix: -N
  label: noMatchAdapterWildcards
  type:
  - boolean
  - 'null'
- doc: Enable colorspace mode
  id: colorspace
  inputBinding:
    prefix: -c
  label: colorspace
  type:
  - boolean
  - 'null'
- doc: Double-encode colors (map 0,1,2,3,4 to A,C,G,T,N).
  id: doubleEncode
  inputBinding:
    prefix: -d
  label: doubleEncode
  type:
  - boolean
  - 'null'
- doc: Trim primer base and the first color
  id: trimPrimer
  inputBinding:
    prefix: -t
  label: trimPrimer
  type:
  - boolean
  - 'null'
- doc: Change negative quality values to zero. Enabled by default in colorspace mode
    since many tools have problems with negative qualities
  id: zeroCap
  inputBinding:
    prefix: -z
  label: zeroCap
  type:
  - boolean
  - 'null'
label: cutadapt
outputs:
- id: out
  label: out
  outputBinding:
    glob: '*.fastq.gz'
  type:
    items: File
    type: array
requirements:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/cutadapt:1.18--py37h14c3975_1
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
