baseCommand:
- bcftools
- annotate
class: CommandLineTool
cwlVersion: v1.0
id: bcftoolsAnnotate
inputs:
- id: file
  inputBinding:
    position: 100
  label: file
  type: File
- default: generated-34059bba-af85-11e9-a525-acde48001122.vcf
  doc: '[-o] see Common Options'
  id: outputFilename
  inputBinding:
    prefix: --output
  label: outputFilename
  type: string
- doc: '[-a] Bgzip-compressed and tabix-indexed file with annotations. The file can
    be VCF, BED, or a tab-delimited file with mandatory columns CHROM, POS (or, alternatively,
    FROM and TO), optional columns REF and ALT, and arbitrary number of annotation
    columns. BED files are expected to have the ".bed" or ".bed.gz" suffix (case-insensitive),
    otherwise a tab-delimited file is assumed. Note that in case of tab-delimited
    file, the coordinates POS, FROM and TO are one-based and inclusive. When REF and
    ALT are present, only matching VCF records will be annotated. When multiple ALT
    alleles are present in the annotation file (given as comma-separated list of alleles),
    at least one must match one of the alleles in the corresponding VCF record. Similarly,
    at least one alternate allele from a multi-allelic VCF record must be present
    in the annotation file. Missing values can be added by providing "." in place
    of actual value. Note that flag types, such as "INFO/FLAG", can be annotated by
    including a field with the value "1" to set the flag, "0" to remove it, or "."
    to keep existing flags. See also -c, --columns and -h, --header-lines.'
  id: annotations
  inputBinding:
    prefix: --annotations
  label: annotations
  type:
  - File
  - 'null'
- doc: (snps|indels|both|all|some|none) Controls how to match records from the annotation
    file to the target VCF. Effective only when -a is a VCF or BCF. See Common Options
    for more.
  id: collapse
  inputBinding:
    prefix: --collapse
  label: collapse
  type:
  - string
  - 'null'
- doc: '[-c] Comma-separated list of columns or tags to carry over from the annotation
    file (see also -a, --annotations). If the annotation file is not a VCF/BCF, list
    describes the columns of the annotation file and must include CHROM, POS (or,
    alternatively, FROM and TO), and optionally REF and ALT. Unused columns which
    should be ignored can be indicated by "-". If the annotation file is a VCF/BCF,
    only the edited columns/tags must be present and their order does not matter.
    The columns ID, QUAL, FILTER, INFO and FORMAT can be edited, where INFO tags can
    be written both as "INFO/TAG" or simply "TAG", and FORMAT tags can be written
    as "FORMAT/TAG" or "FMT/TAG". The imported VCF annotations can be renamed as "DST_TAG:=SRC_TAG"
    or "FMT/DST_TAG:=FMT/SRC_TAG". To carry over all INFO annotations, use "INFO".
    To add all INFO annotations except "TAG", use "^INFO/TAG". By default, existing
    values are replaced. To add annotations without overwriting existing values (that
    is, to add missing tags or add values to existing tags with missing values), use
    "+TAG" instead of "TAG". To append to existing values (rather than replacing or
    leaving untouched), use "=TAG" (instead of "TAG" or "+TAG"). To replace only existing
    values without modifying missing annotations, use "-TAG". If the annotation file
    is not a VCF/BCF, all new annotations must be defined via -h, --header-lines.'
  id: columns
  inputBinding:
    prefix: --columns
  label: columns
  type:
  - items: string
    type: array
  - 'null'
- doc: '[-e] exclude sites for which EXPRESSION is true. For valid expressions see
    EXPRESSIONS.'
  id: exclude
  inputBinding:
    prefix: --exclude
  label: exclude
  type:
  - string
  - 'null'
- doc: '[-h] Lines to append to the VCF header, see also -c, --columns and -a, --annotations.'
  id: headerLines
  inputBinding:
    prefix: --header-lines
  label: headerLines
  type:
  - File
  - 'null'
- doc: "[-I] assign ID on the fly. The format is the same as in the query command\
    \ (see below). By default all existing IDs are replaced. If the format string\
    \ is preceded by \"+\", only missing IDs will be set. For example, one can use\
    \ # bcftools annotate --set-id +' % CHROM\\_ % POS\\_ % REF\\_ % FIRST_ALT' file.vcf"
  id: setId
  inputBinding:
    prefix: --set-id
  label: setId
  type:
  - string
  - 'null'
- doc: '[-i] include only sites for which EXPRESSION is true. For valid expressions
    see EXPRESSIONS.'
  id: include
  inputBinding:
    prefix: --include
  label: include
  type:
  - string
  - 'null'
- doc: keep sites wich do not pass -i and -e expressions instead of discarding them(
  id: keepSites
  inputBinding:
    prefix: --keep-sites
  label: keepSites
  type:
  - boolean
  - 'null'
- doc: '[-m] (+|-)annotate sites which are present ("+") or absent ("-") in the -a
    file with a new INFO/TAG flag'
  id: markSites
  inputBinding:
    prefix: --mark-sites
  label: markSites
  type:
  - string
  - 'null'
- doc: '[-O] (b|u|z|v) see Common Options'
  id: outputType
  inputBinding:
    prefix: --output-type
  label: outputType
  type:
  - string
  - 'null'
- doc: "([-r] chr|chr:pos|chr:from-to|chr:from-[,\u2026]) see Common Options"
  id: regions
  inputBinding:
    prefix: --regions
  label: regions
  type:
  - string
  - 'null'
- doc: '[-R] see Common Options'
  id: regionsFile
  inputBinding:
    prefix: --regions-file
  label: regionsFile
  type:
  - File
  - 'null'
- doc: rename chromosomes according to the map in file, with "old_name new_name\n"
    pairs separated by whitespaces, each on a separate line.
  id: renameChrs
  inputBinding:
    prefix: --rename-chrs
  label: renameChrs
  type:
  - File
  - 'null'
- doc: '[-s] subset of samples to annotate, see also Common Options'
  id: samples
  inputBinding:
    prefix: --samples
  label: samples
  type:
  - items: File
    type: array
  - 'null'
- doc: '[-S] subset of samples to annotate. If the samples are named differently in
    the target VCF and the -a, --annotations VCF, the name mapping can be given as
    "src_name dst_name\n", separated by whitespaces, each pair on a separate line.'
  id: samplesFile
  inputBinding:
    prefix: --samples-file
  label: samplesFile
  type:
  - File
  - 'null'
- doc: see Common Options
  id: threads
  inputBinding:
    prefix: --threads
  label: threads
  type:
  - int
  - 'null'
- doc: '[-x] List of annotations to remove. Use "FILTER" to remove all filters or
    "FILTER/SomeFilter" to remove a specific filter. Similarly, "INFO" can be used
    to remove all INFO tags and "FORMAT" to remove all FORMAT tags except GT. To remove
    all INFO tags except "FOO" and "BAR", use "^INFO/FOO,INFO/BAR" (and similarly
    for FORMAT and FILTER). "INFO" can be abbreviated to "INF" and "FORMAT" to "FMT".'
  id: remove
  inputBinding:
    prefix: --remove
  label: remove
  type:
  - items: string
    type: array
  - 'null'
label: bcftoolsAnnotate
outputs:
- id: out
  label: out
  outputBinding:
    glob: $(inputs.outputFilename)
  type: File
requirements:
  DockerRequirement:
    dockerPull: biocontainers/bcftools:v1.5_cv2
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
