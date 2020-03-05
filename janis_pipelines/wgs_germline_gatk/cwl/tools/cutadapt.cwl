#!/usr/bin/env cwl-runner
baseCommand: cutadapt
class: CommandLineTool
cwlVersion: v1.0
doc: "cutadapt version 2.4\nCopyright (C) 2010-2019 Marcel Martin <marcel.martin@scilifelab.se>\n\
  cutadapt removes adapter sequences from high-throughput sequencing reads.\nUsage:\n\
  \    cutadapt -a ADAPTER [options] [-o output.fastq] input.fastq\nFor paired-end\
  \ reads:\n    cutadapt -a ADAPT1 -A ADAPT2 [options] -o out1.fastq -p out2.fastq\
  \ in1.fastq in2.fastq\nReplace \"ADAPTER\" with the actual sequence of your 3' adapter.\
  \ IUPAC wildcard\ncharacters are supported. The reverse complement is *not* automatically\n\
  searched. All reads from input.fastq will be written to output.fastq with the\n\
  adapter sequence removed. Adapter matching is error-tolerant. Multiple adapter\n\
  sequences can be given (use further -a options), but only the best-matching\nadapter\
  \ will be removed.\nInput may also be in FASTA format. Compressed input and output\
  \ is supported and\nauto-detected from the file name (.gz, .xz, .bz2). Use the file\
  \ name '-' for\nstandard input/output. Without the -o option, output is sent to\
  \ standard output.\nCitation:\nMarcel Martin. Cutadapt removes adapter sequences\
  \ from high-throughput\nsequencing reads. EMBnet.Journal, 17(1):10-12, May 2011.\n\
  http://dx.doi.org/10.14806/ej.17.1.200\nRun \"cutadapt - -help\" to see all command-line\
  \ options.\nSee https://cutadapt.readthedocs.io/ for full documentation.\n"
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
  label: adapter
  type:
  - inputBinding:
      prefix: -a
    items: string
    type: array
  - 'null'
- default: generated--R1.fastq.gz
  doc: "Write trimmed reads to FILE. FASTQ or FASTA format is chosen depending on\
    \ input. The summary report is sent to standard output. Use '{name}' in FILE to\
    \ demultiplex reads into multiple files. Default: write to standard output"
  id: outputFilename
  inputBinding:
    prefix: -o
  label: outputFilename
  type: string
- default: generated--R2.fastq.gz
  doc: Write second read in a pair to FILE.
  id: secondReadFile
  inputBinding:
    prefix: -p
  label: secondReadFile
  type: string
- doc: '(-j)  Number of CPU cores to use. Use 0 to auto-detect. Default: 1'
  id: cores
  inputBinding:
    prefix: --cores
    separate: true
  label: cores
  type:
  - int
  - 'null'
- doc: "(-g)  Sequence of an adapter ligated to the 5' end (paired data: of the first\
    \ read). The adapter and any preceding bases are trimmed. Partial matches at the\
    \ 5' end are allowed. If a '^' character is prepended ('anchoring'), the adapter\
    \ is only found if it is a prefix of the read."
  id: front
  inputBinding:
    prefix: --front
    separate: true
  label: front
  type:
  - string
  - 'null'
- doc: "(-b)  Sequence of an adapter that may be ligated to the 5' or 3' end (paired\
    \ data: of the first read). Both types of matches as described under -a und -g\
    \ are allowed. If the first base of the read is part of the match, the behavior\
    \ is as with -g, otherwise as with -a. This option is mostly for rescuing failed\
    \ library preparations - do not use if you know which end your adapter was ligated\
    \ to!"
  id: anywhere
  inputBinding:
    prefix: --anywhere
    separate: true
  label: anywhere
  type:
  - string
  - 'null'
- doc: '(-e)  Maximum allowed error rate as value between 0 and 1 (no. of errors divided
    by length of matching region). Default: 0.1 (=10%)'
  id: errorRate
  inputBinding:
    prefix: --error-rate
    separate: true
  label: errorRate
  type:
  - float
  - 'null'
- doc: 'Allow only mismatches in alignments. Default: allow both mismatches and indels'
  id: noIndels
  inputBinding:
    prefix: --no-indels
    separate: true
  label: noIndels
  type:
  - boolean
  - 'null'
- doc: '(-n)  Remove up to COUNT adapters from each read. Default: 1'
  id: times
  inputBinding:
    prefix: --times
    separate: true
  label: times
  type:
  - int
  - 'null'
- doc: '(-O)  Require MINLENGTH overlap between read and adapter for an adapter to
    be found. Default: 3'
  id: overlap
  inputBinding:
    prefix: --overlap
    separate: true
  label: overlap
  type:
  - int
  - 'null'
- doc: ' Interpret IUPAC wildcards in reads. Default: False'
  id: matchReadWildcards
  inputBinding:
    prefix: --match-read-wildcards
    separate: true
  label: matchReadWildcards
  type:
  - boolean
  - 'null'
- doc: (-N)  Do not interpret IUPAC wildcards in adapters.
  id: noMatchAdapterWildcards
  inputBinding:
    prefix: --no-match-adapter-wildcards
    separate: true
  label: noMatchAdapterWildcards
  type:
  - boolean
  - 'null'
- doc: "(trim,mask,lowercase,none}  What to do with found adapters. mask: replace\
    \ with 'N' characters; lowercase: convert to lowercase; none: leave unchanged\
    \ (useful with --discard-untrimmed). Default: trim"
  id: action
  inputBinding:
    prefix: --action
    separate: true
  label: action
  type:
  - string
  - 'null'
- doc: (-u)  Remove bases from each read (first read only if paired). If LENGTH is
    positive, remove bases from the beginning. If LENGTH is negative, remove bases
    from the end. Can be used twice if LENGTHs have different signs. This is applied
    *before* adapter trimming.
  id: cut
  inputBinding:
    prefix: --cut
    separate: true
  label: cut
  type:
  - int
  - 'null'
- doc: ' NextSeq-specific quality trimming (each read). Trims also dark cycles appearing
    as high-quality G bases.'
  id: nextseqTrim
  inputBinding:
    prefix: --nextseq-trim
    separate: true
  label: nextseqTrim
  type:
  - string
  - 'null'
- doc: (]3'CUTOFF, ]3'CUTOFF, -q)  Trim low-quality bases from 5' and/or 3' ends of
    each read before adapter removal. Applied to both reads if data is paired. If
    one value is given, only the 3' end is trimmed. If two comma-separated cutoffs
    are given, the 5' end is trimmed with the first cutoff, the 3' end with the second.
  id: qualityCutoff
  inputBinding:
    prefix: --quality-cutoff
    separate: true
  label: qualityCutoff
  type:
  - int
  - 'null'
- doc: 'Assume that quality values in FASTQ are encoded as ascii(quality + N). This
    needs to be set to 64 for some old Illumina FASTQ files. Default: 33'
  id: qualityBase
  inputBinding:
    prefix: --quality-base
    separate: true
  label: qualityBase
  type:
  - boolean
  - 'null'
- doc: (-l)  Shorten reads to LENGTH. Positive values remove bases at the end while
    negative ones remove bases at the beginning. This and the following modifications
    are applied after adapter trimming.
  id: length
  inputBinding:
    prefix: --length
    separate: true
  label: length
  type:
  - int
  - 'null'
- doc: Trim N's on ends of reads.
  id: trimN
  inputBinding:
    prefix: --trim-n
    separate: true
  label: trimN
  type:
  - int
  - 'null'
- doc: Search for TAG followed by a decimal number in the description field of the
    read. Replace the decimal number with the correct length of the trimmed read.
    For example, use --length-tag 'length=' to correct fields like 'length=123'.
  id: lengthTag
  inputBinding:
    prefix: --length-tag
    separate: true
  label: lengthTag
  type:
  - int
  - 'null'
- doc: ' Remove this suffix from read names if present. Can be given multiple times.'
  id: stripSuffix
  inputBinding:
    prefix: --strip-suffix
    separate: true
  label: stripSuffix
  type:
  - string
  - 'null'
- doc: (-x)  Add this prefix to read names. Use {name} to insert the name of the matching
    adapter.
  id: prefix
  inputBinding:
    prefix: --prefix
    separate: true
  label: prefix
  type:
  - string
  - 'null'
- doc: (-y)  Add this suffix to read names; can also include {name}
  id: suffix
  inputBinding:
    prefix: --suffix
    separate: true
  label: suffix
  type:
  - string
  - 'null'
- doc: (-z) Change negative quality values to zero.
  id: zeroCap
  inputBinding:
    prefix: --zero-cap
    separate: true
  label: zeroCap
  type:
  - boolean
  - 'null'
- doc: '(-m)  Discard reads shorter than LEN. Default: 0'
  id: minimumLength
  inputBinding:
    prefix: --minimum-length
    separate: true
  label: minimumLength
  type:
  - int
  - 'null'
- doc: '(-M)  Discard reads longer than LEN. Default: no limit'
  id: maximumLength
  inputBinding:
    prefix: --maximum-length
    separate: true
  label: maximumLength
  type:
  - int
  - 'null'
- doc: Discard reads with more than COUNT 'N' bases. If COUNT is a number between
    0 and 1, it is interpreted as a fraction of the read length.
  id: maxN
  inputBinding:
    prefix: --max-n
    separate: true
  label: maxN
  type:
  - float
  - 'null'
- doc: (--discard)  Discard reads that contain an adapter. Use also -O to avoid discarding
    too many randomly matching reads.
  id: discardTrimmed
  inputBinding:
    prefix: --discard-trimmed
    separate: true
  label: discardTrimmed
  type:
  - boolean
  - 'null'
- doc: (--trimmed-only)  Discard reads that do not contain an adapter.
  id: discardUntrimmed
  inputBinding:
    prefix: --discard-untrimmed
    separate: true
  label: discardUntrimmed
  type:
  - boolean
  - 'null'
- doc: Discard reads that did not pass CASAVA filtering (header has :Y:).
  id: discardCasava
  inputBinding:
    prefix: --discard-casava
    separate: true
  label: discardCasava
  type:
  - boolean
  - 'null'
- doc: "Print only error messages. Which type of report to print: 'full' or 'minimal'.\
    \ Default: full"
  id: quiet
  inputBinding:
    prefix: --quiet
    separate: true
  label: quiet
  type:
  - boolean
  - 'null'
- doc: Use compression level 1 for gzipped output files (faster, but uses more space)
  id: compressionLevel
  inputBinding:
    prefix: -Z
    separate: true
  label: compressionLevel
  type:
  - string
  - 'null'
- doc: Write information about each read and its adapter matches into FILE. See the
    documentation for the file format.
  id: infoFile
  inputBinding:
    prefix: --info-file
    separate: true
  label: infoFile
  type:
  - string
  - 'null'
- doc: (-r)  When the adapter matches in the middle of a read, write the rest (after
    the adapter) to FILE.
  id: restFile
  inputBinding:
    prefix: --rest-file
    separate: true
  label: restFile
  type:
  - string
  - 'null'
- doc: When the adapter has N wildcard bases, write adapter bases matching wildcard
    positions to FILE. (Inaccurate with indels.)
  id: wildcardFile
  inputBinding:
    prefix: --wildcard-file
    separate: true
  label: wildcardFile
  type:
  - string
  - 'null'
- doc: ' Write reads that are too short (according to length specified by -m) to FILE.
    Default: discard reads'
  id: tooShortOutput
  inputBinding:
    prefix: --too-short-output
    separate: true
  label: tooShortOutput
  type:
  - string
  - 'null'
- doc: ' Write reads that are too long (according to length specified by -M) to FILE.
    Default: discard reads'
  id: tooLongOutput
  inputBinding:
    prefix: --too-long-output
    separate: true
  label: tooLongOutput
  type:
  - string
  - 'null'
- doc: ' Write reads that do not contain any adapter to FILE. Default: output to same
    file as trimmed reads'
  id: untrimmedOutput
  inputBinding:
    prefix: --untrimmed-output
    separate: true
  label: untrimmedOutput
  type:
  - string
  - 'null'
- doc: 3' adapter to be removed from second read in a pair.
  id: removeMiddle3Adapter
  label: removeMiddle3Adapter
  type:
  - inputBinding:
      prefix: -A
      separate: true
    items: string
    type: array
  - 'null'
- doc: 5' adapter to be removed from second read in a pair.
  id: removeMiddle5Adapter
  inputBinding:
    prefix: -G
    separate: true
  label: removeMiddle5Adapter
  type:
  - string
  - 'null'
- doc: 5'/3 adapter to be removed from second read in a pair.
  id: removeMiddleBothAdapter
  inputBinding:
    prefix: -B
    separate: true
  label: removeMiddleBothAdapter
  type:
  - string
  - 'null'
- doc: Remove LENGTH bases from second read in a pair.
  id: removeNBasesFromSecondRead
  inputBinding:
    prefix: -U
    separate: true
  label: removeNBasesFromSecondRead
  type:
  - string
  - 'null'
- doc: Treat adapters given with -a/-A etc. as pairs. Either both or none are removed
    from each read pair.
  id: pairAdapters
  inputBinding:
    prefix: --pair-adapters
    separate: true
  label: pairAdapters
  type:
  - string
  - 'null'
- doc: '{any,both,first} Which of the reads in a paired-end read have to match the
    filtering criterion in order for the pair to be filtered. Default: any'
  id: pairFilter
  inputBinding:
    prefix: --pair-filter
    separate: true
  label: pairFilter
  type:
  - string
  - 'null'
- doc: Read and write interleaved paired-end reads.
  id: interleaved
  inputBinding:
    prefix: --interleaved
    separate: true
  label: interleaved
  type:
  - boolean
  - 'null'
- doc: ' Write second read in a pair to this FILE when no adapter was found. Use with
    --untrimmed-output. Default: output to same file as trimmed reads'
  id: untrimmedPairedOutput
  inputBinding:
    prefix: --untrimmed-paired-output
    separate: true
  label: untrimmedPairedOutput
  type:
  - string
  - 'null'
- doc: ' Write second read in a pair to this file if pair is too short. Use also --too-short-output.'
  id: tooShortPairedOutput
  inputBinding:
    prefix: --too-short-paired-output
    separate: true
  label: tooShortPairedOutput
  type:
  - string
  - 'null'
- doc: ' Write second read in a pair to this file if pair is too long. Use also --too-long-output.'
  id: tooLongPairedOutput
  inputBinding:
    prefix: --too-long-paired-output
    separate: true
  label: tooLongPairedOutput
  type:
  - string
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
    dockerPull: quay.io/biocontainers/cutadapt:2.6--py36h516909a_0
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
