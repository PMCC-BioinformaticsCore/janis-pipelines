baseCommand:
- gatk
- GatherVcfs
class: CommandLineTool
cwlVersion: v1.0
doc: "GatherVcfs (Picard)\n            \nGathers multiple VCF files from a scatter\
  \ operation into a single VCF file. \nInput files must be supplied in genomic order\
  \ and must not have events at overlapping positions."
id: Gatk4GatherVcfs
inputs:
- doc: '[default: []] (-I) Input VCF file(s).'
  id: vcfs
  inputBinding:
    prefix: --INPUT
  label: vcfs
  type:
    items: File
    type: array
- default: generated-2e98e504-d5c0-11e9-96ee-f218985ebfa7.gathered.vcf
  doc: '[default: null] (-O) Output VCF file.'
  id: outputFilename
  inputBinding:
    prefix: --OUTPUT
  label: outputFilename
  type: string
- doc: '[default: []] read one or more arguments files and add them to the command
    line'
  id: argumentsFile
  inputBinding:
    prefix: --arguments_file
  label: argumentsFile
  type:
  - items: File
    type: array
  - 'null'
- doc: '[default: 5] Compression level for all compressed files created (e.g. BAM
    and VCF).'
  id: compressionLevel
  inputBinding:
    prefix: --COMPRESSION_LEVEL
  label: compressionLevel
  type:
  - int
  - 'null'
- doc: '[default: TRUE] Whether to create a BAM index when writing a coordinate-sorted
    BAM file.'
  id: createIndex
  inputBinding:
    prefix: --CREATE_INDEX
  label: createIndex
  type:
  - boolean
  - 'null'
- doc: '[default: FALSE] Whether to create an MD5 digest for any BAM or FASTQ files
    created.'
  id: createMd5File
  inputBinding:
    prefix: --CREATE_MD5_FILE
  label: createMd5File
  type:
  - boolean
  - 'null'
- doc: '[default: client_secrets.json] Google Genomics API client_secrets.json file
    path.'
  id: ga4ghClientSecrets
  inputBinding:
    prefix: --GA4GH_CLIENT_SECRETS
  label: ga4ghClientSecrets
  type:
  - File
  - 'null'
- doc: '[default: 500000] When writing files that need to be sorted, this will specify
    the number of records stored in RAM before spilling to disk. Increasing this number
    reduces the number of file handles needed to sort the file, and increases the
    amount of RAM needed.'
  id: maxRecordsInRam
  inputBinding:
    prefix: --MAX_RECORDS_IN_RAM
  label: maxRecordsInRam
  type:
  - int
  - 'null'
- doc: '[default: FALSE] Whether to suppress job-summary info on System.err.'
  id: quiet
  inputBinding:
    prefix: --QUIET
  label: quiet
  type:
  - boolean
  - 'null'
- doc: '[default: null] Reference sequence file.'
  id: referenceSequence
  inputBinding:
    prefix: --REFERENCE_SEQUENCE
  label: referenceSequence
  type:
  - File
  - 'null'
- default: /tmp
  doc: '[default: []] One or more directories with space available to be used by this
    program for temporary storage of working files'
  id: tmpDir
  inputBinding:
    prefix: --TMP_DIR
  label: tmpDir
  type: string
- doc: '[default: FALSE] (-use_jdk_deflater) Use the JDK Deflater instead of the Intel
    Deflater for writing compressed output'
  id: useJdkDeflater
  inputBinding:
    prefix: --USE_JDK_DEFLATER
  label: useJdkDeflater
  type:
  - boolean
  - 'null'
- doc: '[default: FALSE] (-use_jdk_inflater) Use the JDK Inflater instead of the Intel
    Inflater for reading compressed input'
  id: useJdkInflater
  inputBinding:
    prefix: --USE_JDK_INFLATER
  label: useJdkInflater
  type:
  - boolean
  - 'null'
- doc: '[default: STRICT] Validation stringency for all SAM files read by this program.
    Setting stringency to SILENT can improve performance when processing a BAM file
    in which variable-length data (read, qualities, tags) do not otherwise need to
    be decoded.'
  id: validationStringency
  inputBinding:
    prefix: --VALIDATION_STRINGENCY
  label: validationStringency
  type:
  - string
  - 'null'
- doc: '[default: INFO] Control verbosity of logging.'
  id: verbosity
  inputBinding:
    prefix: --VERBOSITY
  label: verbosity
  type:
  - boolean
  - 'null'
label: Gatk4GatherVcfs
outputs:
- id: out
  label: out
  outputBinding:
    glob: $(inputs.outputFilename)
  type: File
requirements:
  DockerRequirement:
    dockerPull: broadinstitute/gatk:4.1.3.0
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
