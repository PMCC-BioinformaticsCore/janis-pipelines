baseCommand:
- gatk
- SortSam
class: CommandLineTool
cwlVersion: v1.0
doc: Sorts a SAM/BAM/CRAM file.
id: gatk4sortsam
inputs:
- doc: The SAM/BAM/CRAM file to sort.
  id: bam
  inputBinding:
    position: 10
    prefix: -I
  label: bam
  type: File
- default: generated-67f9257c-0fca-11ea-926e-acde48001122.bam
  doc: The sorted SAM/BAM/CRAM output file.
  id: outputFilename
  inputBinding:
    position: 10
    prefix: -O
  label: outputFilename
  type: string
- doc: 'The --SORT_ORDER argument is an enumerated type (SortOrder), which can have
    one of the following values: [unsorted, queryname, coordinate, duplicate, unknown]'
  id: sortOrder
  inputBinding:
    position: 10
    prefix: -SO
  label: sortOrder
  type: string
- doc: read one or more arguments files and add them to the command line
  id: argumentsFile
  inputBinding:
    position: 10
  label: argumentsFile
  type:
  - inputBinding:
      prefix: --arguments_file
    items: File
    type: array
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
label: gatk4sortsam
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
    dockerPull: broadinstitute/gatk:4.1.3.0
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
