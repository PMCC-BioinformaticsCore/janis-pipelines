#!/usr/bin/env cwl-runner
class: CommandLineTool
cwlVersion: v1.2
label: 'GATK4: Merge SAM Files'
doc: Merges multiple SAM/BAM files into one file

requirements:
- class: ShellCommandRequirement
- class: InlineJavascriptRequirement
- class: DockerRequirement
  dockerPull: broadinstitute/gatk:4.1.3.0

inputs:
- id: javaOptions
  label: javaOptions
  type:
  - type: array
    items: string
  - 'null'
- id: compression_level
  label: compression_level
  doc: |-
    Compression level for all compressed files created (e.g. BAM and VCF). Default value: 2.
  type:
  - int
  - 'null'
- id: bams
  label: bams
  doc: The SAM/BAM file to sort.
  type:
    type: array
    inputBinding:
      prefix: -I
    items: File
  inputBinding:
    position: 10
- id: sampleName
  label: sampleName
  doc: Used for naming purposes only
  type:
  - string
  - 'null'
- id: outputFilename
  label: outputFilename
  doc: SAM/BAM file to write merged result to
  type:
  - string
  - 'null'
  default: generated.merged.bam
  inputBinding:
    prefix: -O
    position: 10
    valueFrom: '$(inputs.sampleName ? inputs.sampleName : "generated").merged.bam'
- id: argumentsFile
  label: argumentsFile
  doc: read one or more arguments files and add them to the command line
  type:
  - type: array
    items: File
  - 'null'
  inputBinding:
    prefix: --arguments_file
    position: 10
- id: assumeSorted
  label: assumeSorted
  doc: |-
    If true, assume that the input files are in the same sort order as the requested output sort order, even if their headers say otherwise.
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: -AS
- id: comment
  label: comment
  doc: Comment(s) to include in the merged output file's header.
  type:
  - type: array
    items: string
  - 'null'
  inputBinding:
    prefix: -CO
- id: mergeSequenceDictionaries
  label: mergeSequenceDictionaries
  doc: Merge the sequence dictionaries
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: -MSD
- id: sortOrder
  label: sortOrder
  doc: |-
    The --SORT_ORDER argument is an enumerated type (SortOrder), which can have one of the following values: [unsorted, queryname, coordinate, duplicate, unknown]
  type:
  - string
  - 'null'
  inputBinding:
    prefix: -SO
    position: 10
- id: useThreading
  label: useThreading
  doc: |-
    Option to create a background thread to encode, compress and write to disk the output file. The threaded version uses about 20% more CPU and decreases runtime by ~20% when writing out a compressed BAM file.
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --USE_THREADING
- id: compressionLevel
  label: compressionLevel
  doc: Compression level for all compressed files created (e.g. BAM and GELI).
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --COMPRESSION_LEVEL
    position: 11
- id: createIndex
  label: createIndex
  doc: Whether to create a BAM index when writing a coordinate-sorted BAM file.
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --CREATE_INDEX
    position: 11
- id: createMd5File
  label: createMd5File
  doc: Whether to create an MD5 digest for any BAM or FASTQ files created.
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --CREATE_MD5_FILE
    position: 11
- id: maxRecordsInRam
  label: maxRecordsInRam
  doc: |-
    When writing SAM files that need to be sorted, this will specify the number of records stored in RAM before spilling to disk. Increasing this number reduces the number of file handles needed to sort a SAM file, and increases the amount of RAM needed.
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --MAX_RECORDS_IN_RAM
    position: 11
- id: quiet
  label: quiet
  doc: Whether to suppress job-summary info on System.err.
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --QUIET
    position: 11
- id: reference
  label: reference
  doc: Reference sequence file.
  type:
  - File
  - 'null'
  secondaryFiles:
  - pattern: .fai
  - pattern: .amb
  - pattern: .ann
  - pattern: .bwt
  - pattern: .pac
  - pattern: .sa
  - pattern: ^.dict
  inputBinding:
    prefix: --reference
    position: 11
- id: tmpDir
  label: tmpDir
  doc: Undocumented option
  type: string
  default: /tmp/
  inputBinding:
    prefix: --TMP_DIR
    position: 11
- id: useJdkDeflater
  label: useJdkDeflater
  doc: Whether to use the JdkDeflater (as opposed to IntelDeflater)
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --use_jdk_deflater
    position: 11
- id: useJdkInflater
  label: useJdkInflater
  doc: Whether to use the JdkInflater (as opposed to IntelInflater)
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --use_jdk_inflater
    position: 11
- id: validationStringency
  label: validationStringency
  doc: |-
    Validation stringency for all SAM files read by this program. Setting stringency to SILENT can improve performance when processing a BAM file in which variable-length data (read, qualities, tags) do not otherwise need to be decoded.The --VALIDATION_STRINGENCY argument is an enumerated type (ValidationStringency), which can have one of the following values: [STRICT, LENIENT, SILENT]
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --VALIDATION_STRINGENCY
    position: 11
- id: verbosity
  label: verbosity
  doc: |-
    The --verbosity argument is an enumerated type (LogLevel), which can have one of the following values: [ERROR, WARNING, INFO, DEBUG]
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --verbosity
    position: 11

outputs:
- id: out
  label: out
  type: File
  secondaryFiles:
  - |-
    ${

            function resolveSecondary(base, secPattern) {
              if (secPattern[0] == "^") {
                var spl = base.split(".");
                var endIndex = spl.length > 1 ? spl.length - 1 : 1;
                return resolveSecondary(spl.slice(undefined, endIndex).join("."), secPattern.slice(1));
              }
              return base + secPattern
            }
            return [
                    {
                        path: resolveSecondary(self.path, "^.bai"),
                        basename: resolveSecondary(self.basename, ".bai"),
                        class: "File",
                    }
            ];

    }
  outputBinding:
    glob: '$(inputs.sampleName ? inputs.sampleName : "generated").merged.bam'
    loadContents: false
stdout: _stdout
stderr: _stderr

baseCommand:
- gatk
- MergeSamFiles
arguments:
- prefix: --java-options
  position: -1
  valueFrom: |-
    $("-Xmx{memory}G {compression} {otherargs}".replace(/\{memory\}/g, (([inputs.runtime_memory, 8, 4].filter(function (inner) { return inner != null })[0] * 3) / 4)).replace(/\{compression\}/g, (inputs.compression_level != null) ? ("-Dsamjdk.compress_level=" + inputs.compression_level) : "").replace(/\{otherargs\}/g, [inputs.javaOptions, []].filter(function (inner) { return inner != null })[0].join(" ")))

hints:
- class: ToolTimeLimit
  timelimit: |-
    $([inputs.runtime_seconds, 86400].filter(function (inner) { return inner != null })[0])
id: Gatk4MergeSamFiles
