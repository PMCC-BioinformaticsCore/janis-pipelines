baseCommand:
- gatk
- MarkDuplicates
class: CommandLineTool
cwlVersion: v1.0
doc: "MarkDuplicates (Picard): Identifies duplicate reads.\n\nThis tool locates and\
  \ tags duplicate reads in a BAM or SAM file, where duplicate reads are \ndefined\
  \ as originating from a single fragment of DNA. Duplicates can arise during sample\
  \ \npreparation e.g. library construction using PCR. See also EstimateLibraryComplexity\
  \ for \nadditional notes on PCR duplication artifacts. Duplicate reads can also\
  \ result from a single \namplification cluster, incorrectly detected as multiple\
  \ clusters by the optical sensor of the \nsequencing instrument. These duplication\
  \ artifacts are referred to as optical duplicates.\n\nThe MarkDuplicates tool works\
  \ by comparing sequences in the 5 prime positions of both reads \nand read-pairs\
  \ in a SAM/BAM file. An BARCODE_TAG option is available to facilitate duplicate\n\
  marking using molecular barcodes. After duplicate reads are collected, the tool\
  \ differentiates \nthe primary and duplicate reads using an algorithm that ranks\
  \ reads by the sums of their \nbase-quality scores (default method).\n\nThe tool's\
  \ main output is a new SAM or BAM file, in which duplicates have been identified\
  \ \nin the SAM flags field for each read. Duplicates are marked with the hexadecimal\
  \ value of 0x0400, \nwhich corresponds to a decimal value of 1024. If you are not\
  \ familiar with this type of annotation, \nplease see the following blog post for\
  \ additional information.\n\nAlthough the bitwise flag annotation indicates whether\
  \ a read was marked as a duplicate, \nit does not identify the type of duplicate.\
  \ To do this, a new tag called the duplicate type (DT) \ntag was recently added\
  \ as an optional output in the 'optional field' section of a SAM/BAM file. \nInvoking\
  \ the TAGGING_POLICY option, you can instruct the program to mark all the duplicates\
  \ (All), \nonly the optical duplicates (OpticalOnly), or no duplicates (DontTag).\
  \ The records within the \noutput of a SAM/BAM file will have values for the 'DT'\
  \ tag (depending on the invoked TAGGING_POLICY), \nas either library/PCR-generated\
  \ duplicates (LB), or sequencing-platform artifact duplicates (SQ). \nThis tool\
  \ uses the READ_NAME_REGEX and the OPTICAL_DUPLICATE_PIXEL_DISTANCE options as the\
  \ \nprimary methods to identify and differentiate duplicate types. Set READ_NAME_REGEX\
  \ to null to \nskip optical duplicate detection, e.g. for RNA-seq or other data\
  \ where duplicate sets are \nextremely large and estimating library complexity is\
  \ not an aim. Note that without optical \nduplicate counts, library size estimation\
  \ will be inaccurate.\n\nMarkDuplicates also produces a metrics file indicating\
  \ the numbers \nof duplicates for both single- and paired-end reads.\n\nThe program\
  \ can take either coordinate-sorted or query-sorted inputs, however the behavior\
  \ \nis slightly different. When the input is coordinate-sorted, unmapped mates of\
  \ mapped records \nand supplementary/secondary alignments are not marked as duplicates.\
  \ However, when the input \nis query-sorted (actually query-grouped), then unmapped\
  \ mates and secondary/supplementary \nreads are not excluded from the duplication\
  \ test and can be marked as duplicate reads.\n\nIf desired, duplicates can be removed\
  \ using the REMOVE_DUPLICATE and REMOVE_SEQUENCING_DUPLICATES options."
id: Gatk4MarkDuplicates
inputs:
- doc: One or more input SAM or BAM files to analyze. Must be coordinate sorted.
  id: bam
  inputBinding:
    position: 10
    prefix: -I
  label: bam
  secondaryFiles:
  - ^.bai
  type: File
- default: generated-8c02e8ce-cf9f-11e9-b76d-acde48001122.bam
  doc: File to write duplication metrics to
  id: outputFilename
  inputBinding:
    position: 10
    prefix: -O
  label: outputFilename
  type: string
- default: generated-8c02e928-cf9f-11e9-b76d-acde48001122.metrics.txt
  doc: The output file to write marked records to.
  id: metricsFilename
  inputBinding:
    position: 10
    prefix: -M
  label: metricsFilename
  type: string
- doc: read one or more arguments files and add them to the command line
  id: argumentsFile
  inputBinding:
    itemSeparator: ' '
    position: 10
    prefix: --arguments_file
  label: argumentsFile
  type:
  - items: File
    type: array
  - 'null'
- doc: 'If not null, assume that the input file has this order even if the header
    says otherwise. Exclusion: This argument cannot be used at the same time as ASSUME_SORTED.
    The --ASSUME_SORT_ORDER argument is an enumerated type (SortOrder), which can
    have one of the following values: [unsorted, queryname, coordinate, duplicate,
    unknown]'
  id: assumeSortOrder
  inputBinding:
    prefix: -ASO
  label: assumeSortOrder
  type:
  - string
  - 'null'
- doc: Barcode SAM tag (ex. BC for 10X Genomics)
  id: barcodeTag
  inputBinding:
    prefix: --BARCODE_TAG
  label: barcodeTag
  type:
  - string
  - 'null'
- doc: Comment(s) to include in the output file's header.
  id: comment
  inputBinding:
    itemSeparator: ' '
    prefix: -CO
  label: comment
  type:
  - items: string
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
- default: tmp/
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
label: Gatk4MarkDuplicates
outputs:
- id: out
  label: out
  outputBinding:
    glob: $(inputs.outputFilename)
  secondaryFiles:
  - ^.bai
  type: File
- id: metrics
  label: metrics
  outputBinding:
    glob: $(inputs.metricsFilename)
  type: File
requirements:
  DockerRequirement:
    dockerPull: broadinstitute/gatk:4.0.12.0
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
