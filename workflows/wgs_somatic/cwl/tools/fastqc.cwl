baseCommand: fastqc
class: CommandLineTool
cwlVersion: v1.0
id: fastqc
inputs:
- id: reads
  inputBinding:
    position: 5
  label: reads
  type:
    items: File
    type: array
- default: .
  doc: (-o) Create all output files in the specified output directory. Please note
    that this directory must exist as the program will not create it.  If this option
    is not set then the output file for each sequence file is created in the same
    directory as the sequence file which was processed.
  id: outdir
  inputBinding:
    prefix: --outdir
  label: outdir
  type: string
- doc: Files come from raw casava output. Files in the same sample group (differing
    only by the group number) will be analysed as a set rather than individually.
    Sequences with the filter flag set in the header will be excluded from the analysis.
    Files must have the same names given to them by casava (including being gzipped
    and ending with .gz) otherwise they won't be grouped together correctly.
  id: casava
  inputBinding:
    prefix: --casava
  label: casava
  type:
  - boolean
  - 'null'
- doc: Files come from naopore sequences and are in fast5 format. In this mode you
    can pass in directories to process and the program will take in all fast5 files
    within those directories and produce a single output file from the sequences found
    in all files.
  id: nano
  inputBinding:
    prefix: --nano
  label: nano
  type:
  - boolean
  - 'null'
- doc: If running with --casava then don't remove read flagged by casava as poor quality
    when performing the QC analysis.
  id: nofilter
  inputBinding:
    prefix: --nofilter
  label: nofilter
  type:
  - boolean
  - 'null'
- doc: If set then the zipped output file will be uncompressed in the same directory
    after it has been created.  By default this option will be set if fastqc is run
    in non-interactive mode.
  id: extract
  inputBinding:
    prefix: --extract
  label: extract
  type:
  - boolean
  - 'null'
- doc: (-j) Provides the full path to the java binary you want to use to launch fastqc.
    If not supplied then java is assumed to be in your path.
  id: java
  inputBinding:
    prefix: --java
  label: java
  type:
  - string
  - 'null'
- default: true
  doc: 'Do not uncompress the output file after creating it.  You should set this
    option if you donot wish to uncompress the output when running in non-interactive
    mode. '
  id: noextract
  inputBinding:
    prefix: --noextract
  label: noextract
  type: boolean
- doc: 'Disable grouping of bases for reads >50bp. All reports will show data for
    every base in the read. WARNING: Using this option will cause fastqc to crash
    and burn if you use it on really long reads, and your plots may end up a ridiculous
    size. You have been warned! '
  id: nogroup
  inputBinding:
    prefix: --nogroup
  label: nogroup
  type:
  - boolean
  - 'null'
- doc: '(-f) Bypasses the normal sequence file format detection and forces the program
    to use the specified format.  Valid formats are bam,sam,bam_mapped,sam_mapped
    and fastq '
  id: format
  inputBinding:
    prefix: --format
  label: format
  type:
  - string
  - 'null'
- doc: (-t) Specifies the number of files which can be processed simultaneously. Each
    thread will be allocated 250MB of memory so you shouldn't run more threads than
    your available memory will cope with, and not more than 6 threads on a 32 bit
    machine
  id: threads
  inputBinding:
    prefix: --threads
    valueFrom: $(inputs.runtime_cpu)
  label: threads
  type:
  - int
  - 'null'
- doc: (-c) Specifies a non-default file which contains the list of contaminants to
    screen overrepresented sequences against. The file must contain sets of named
    contaminants in the form name[tab]sequence.  Lines prefixed with a hash will be
    ignored.
  id: contaminants
  inputBinding:
    prefix: --contaminants
  label: contaminants
  type:
  - File
  - 'null'
- doc: '(-a) Specifies a non-default file which contains the list of adapter sequences
    which will be explicity searched against the library. The file must contain sets
    of named adapters in the form name[tab]sequence.  Lines prefixed with a hash will
    be ignored. '
  id: adapters
  inputBinding:
    prefix: --adapters
  label: adapters
  type:
  - File
  - 'null'
- doc: (-l) Specifies a non-default file which contains a set of criteria which will
    be used to determine the warn/error limits for the various modules.  This file
    can also be used to selectively  remove some modules from the output all together.
    The format needs to mirror the default limits.txt file found in the Configuration
    folder.
  id: limits
  inputBinding:
    prefix: --limits
  label: limits
  type:
  - File
  - 'null'
- doc: '(-k) Specifies the length of Kmer to look for in the Kmer content module.
    Specified Kmer length must be between 2 and 10. Default length is 7 if not specified. '
  id: kmers
  inputBinding:
    prefix: --kmers
  label: kmers
  type:
  - int
  - 'null'
- doc: (-q) Supress all progress messages on stdout and only report errors.
  id: quiet
  inputBinding:
    prefix: --quiet
  label: quiet
  type:
  - boolean
  - 'null'
- doc: (-d) Selects a directory to be used for temporary files written when generating
    report images.Defaults to system temp directory if not specified.
  id: dir
  inputBinding:
    prefix: --dir
  label: dir
  type:
  - string
  - 'null'
label: fastqc
outputs:
- id: out
  label: out
  outputBinding:
    glob: '*.zip'
  type:
    items: File
    type: array
requirements:
  DockerRequirement:
    dockerPull: biocontainers/fastqc:v0.11.5_cv3
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
