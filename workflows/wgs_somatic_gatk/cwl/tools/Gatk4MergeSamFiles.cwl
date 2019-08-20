baseCommand:
- gatk
- MergeSamFiles
class: CommandLineTool
cwlVersion: v1.0
doc: Merges multiple SAM/BAM files into one file
id: Gatk4MergeSamFiles
inputs:
- doc: The SAM/BAM file to sort.
  id: bams
  inputBinding:
    position: 10
    prefix: -I
  label: bams
  type:
    items: File
    type: array
- default: generated-9c0b2b94-c2e5-11e9-91cd-f218985ebfa7.bam
  doc: SAM/BAM file to write merged result to
  id: outputFilename
  inputBinding:
    position: 10
    prefix: -O
  label: outputFilename
  type: string
- doc: read one or more arguments files and add them to the command line
  id: argumentsFile
  inputBinding:
    position: 10
    prefix: --arguments_file
  label: argumentsFile
  type:
  - items: File
    type: array
  - 'null'
- doc: If true, assume that the input files are in the same sort order as the requested
    output sort order, even if their headers say otherwise.
  id: assumeSorted
  inputBinding:
    prefix: -AS
  label: assumeSorted
  type:
  - boolean
  - 'null'
- doc: Comment(s) to include in the merged output file's header.
  id: comment
  inputBinding:
    prefix: -CO
  label: comment
  type:
  - items: string
    type: array
  - 'null'
- doc: Merge the sequence dictionaries
  id: mergeSequenceDictionaries
  inputBinding:
    prefix: -MSD
  label: mergeSequenceDictionaries
  type:
  - boolean
  - 'null'
- doc: 'The --SORT_ORDER argument is an enumerated type (SortOrder), which can have
    one of the following values: [unsorted, queryname, coordinate, duplicate, unknown]'
  id: sortOrder
  inputBinding:
    position: 10
    prefix: -SO
  label: sortOrder
  type:
  - string
  - 'null'
- doc: Option to create a background thread to encode, compress and write to disk
    the output file. The threaded version uses about 20% more CPU and decreases runtime
    by ~20% when writing out a compressed BAM file.
  id: useThreading
  inputBinding:
    prefix: --USE_THREADING
  label: useThreading
  type:
  - boolean
  - 'null'
- doc: Compression level for all compressed files created (e.g. BAM and GELI).
  id: compressionLevel
  inputBinding:
    position: 11
    prefix: --COMPRESSION_LEVEL
  label: compressionLevel
  type:
  - int
  - 'null'
- doc: Whether to create a BAM index when writing a coordinate-sorted BAM file.
  id: createIndex
  inputBinding:
    position: 11
    prefix: --CREATE_INDEX
  label: createIndex
  type:
  - boolean
  - 'null'
- doc: Whether to create an MD5 digest for any BAM or FASTQ files created.
  id: createMd5File
  inputBinding:
    position: 11
    prefix: --CREATE_MD5_FILE
  label: createMd5File
  type:
  - boolean
  - 'null'
- doc: When writing SAM files that need to be sorted, this will specify the number
    of records stored in RAM before spilling to disk. Increasing this number reduces
    the number of file handles needed to sort a SAM file, and increases the amount
    of RAM needed.
  id: maxRecordsInRam
  inputBinding:
    position: 11
    prefix: --MAX_RECORDS_IN_RAM
  label: maxRecordsInRam
  type:
  - int
  - 'null'
- doc: Whether to suppress job-summary info on System.err.
  id: quiet
  inputBinding:
    position: 11
    prefix: --QUIET
  label: quiet
  type:
  - boolean
  - 'null'
- doc: Reference sequence file.
  id: reference
  inputBinding:
    position: 11
    prefix: --reference
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
- default: /tmp/
  doc: Undocumented option
  id: tmpDir
  inputBinding:
    position: 11
    prefix: --TMP_DIR
  label: tmpDir
  type: string
- doc: Whether to use the JdkDeflater (as opposed to IntelDeflater)
  id: useJdkDeflater
  inputBinding:
    position: 11
    prefix: --use_jdk_deflater
  label: useJdkDeflater
  type:
  - boolean
  - 'null'
- doc: Whether to use the JdkInflater (as opposed to IntelInflater)
  id: useJdkInflater
  inputBinding:
    position: 11
    prefix: --use_jdk_inflater
  label: useJdkInflater
  type:
  - boolean
  - 'null'
- doc: 'Validation stringency for all SAM files read by this program. Setting stringency
    to SILENT can improve performance when processing a BAM file in which variable-length
    data (read, qualities, tags) do not otherwise need to be decoded.The --VALIDATION_STRINGENCY
    argument is an enumerated type (ValidationStringency), which can have one of the
    following values: [STRICT, LENIENT, SILENT]'
  id: validationStringency
  inputBinding:
    position: 11
    prefix: --VALIDATION_STRINGENCY
  label: validationStringency
  type:
  - string
  - 'null'
- doc: 'The --verbosity argument is an enumerated type (LogLevel), which can have
    one of the following values: [ERROR, WARNING, INFO, DEBUG]'
  id: verbosity
  inputBinding:
    position: 11
    prefix: --verbosity
  label: verbosity
  type:
  - string
  - 'null'
label: Gatk4MergeSamFiles
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
