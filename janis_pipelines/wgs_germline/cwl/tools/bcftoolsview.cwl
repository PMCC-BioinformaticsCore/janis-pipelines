baseCommand:
- bcftools
- view
class: CommandLineTool
cwlVersion: v1.0
doc: "________________________________\n \n        View, subset and filter VCF or\
  \ BCF files by position and filtering expression\n        Convert between VCF and\
  \ BCF. Former bcftools subset."
id: bcftoolsview
inputs:
- id: file
  inputBinding:
    position: 2
  label: file
  type: File
- doc: (-G) drop individual genotype information (after subsetting if -s option set)
  id: dropGenotypes
  inputBinding:
    position: 1
    prefix: --drop-genotypes
  label: dropGenotypes
  type:
  - boolean
  - 'null'
- doc: (-h) print the header only
  id: headerOnly
  inputBinding:
    position: 1
    prefix: --header-only
  label: headerOnly
  type:
  - boolean
  - 'null'
- doc: (-H) suppress the header in VCF output
  id: noHeader
  inputBinding:
    position: 1
    prefix: --no-header
  label: noHeader
  type:
  - boolean
  - 'null'
- doc: '(-l) compression level: 0 uncompressed, 1 best speed, 9 best compression [-1]'
  id: compressionLevel
  inputBinding:
    position: 1
    prefix: --compression-level
  label: compressionLevel
  type:
  - int
  - 'null'
- doc: do not append version and command line to the header
  id: noVersion
  inputBinding:
    position: 1
    prefix: --no-version
  label: noVersion
  type:
  - boolean
  - 'null'
- doc: (-o) output file name [stdout]
  id: outputFilename
  inputBinding:
    position: 1
    prefix: --output-file
  label: outputFilename
  type:
  - File
  - 'null'
- doc: '(-O) [<b|u|z|v>] b: compressed BCF, u: uncompressed BCF, z: compressed VCF,
    v: uncompressed VCF [v]'
  id: outputType
  inputBinding:
    position: 1
    prefix: --output-type
  label: outputType
  type:
  - string
  - 'null'
- doc: (-r) restrict to comma-separated list of regions
  id: regions
  inputBinding:
    position: 1
    prefix: --regions
  label: regions
  type:
  - string
  - 'null'
- doc: (-R) restrict to regions listed in a file
  id: regionsFile
  inputBinding:
    position: 1
    prefix: --regions-file
  label: regionsFile
  type:
  - File
  - 'null'
- doc: (-t) similar to -r but streams rather than index-jumps. Exclude regions with
    '^' prefix
  id: targets
  inputBinding:
    position: 1
    prefix: --targets
  label: targets
  type:
  - string
  - 'null'
- doc: (-T) similar to -R but streams rather than index-jumps. Exclude regions with
    '^' prefix
  id: targetsFile
  inputBinding:
    position: 1
    prefix: --targets-file
  label: targetsFile
  type:
  - File
  - 'null'
- doc: number of extra output compression threads [0]
  id: threads
  inputBinding:
    position: 1
    prefix: --threads
  label: threads
  type:
  - int
  - 'null'
- doc: (-a) trim alternate alleles not seen in the subset
  id: trimAltAlleles
  inputBinding:
    position: 1
    prefix: --trim-alt-alleles
  label: trimAltAlleles
  type:
  - boolean
  - 'null'
- doc: (-I) do not (re)calculate INFO fields for the subset (currently INFO/AC and
    INFO/AN)
  id: noUpdate
  inputBinding:
    position: 1
    prefix: --no-update
  label: noUpdate
  type:
  - boolean
  - 'null'
- doc: (-s) comma separated list of samples to include (or exclude with '^' prefix)
  id: samples
  inputBinding:
    position: 1
    prefix: --samples
  label: samples
  type:
  - items: string
    type: array
  - 'null'
- doc: (-S) file of samples to include (or exclude with '^' prefix)
  id: samplesFile
  inputBinding:
    position: 1
    prefix: --samples-file
  label: samplesFile
  type:
  - File
  - 'null'
- doc: only warn about unknown subset samples
  id: forceSamples
  inputBinding:
    position: 1
    prefix: --force-samples
  label: forceSamples
  type:
  - boolean
  - 'null'
- doc: (-c) minimum count for non-reference (nref), 1st alternate (alt1), least frequent
    (minor), most frequent (major) or sum of all but most frequent (nonmajor) alleles
    [nref]
  id: minAc
  inputBinding:
    position: 1
    prefix: --min-ac
  label: minAc
  type:
  - int
  - 'null'
- doc: (-C) maximum count for non-reference (nref), 1st alternate (alt1), least frequent
    (minor), most frequent (major) or sum of all but most frequent (nonmajor) alleles
    [nref]
  id: maxAc
  inputBinding:
    position: 1
    prefix: --max-ac
  label: maxAc
  type:
  - int
  - 'null'
- doc: (-f) require at least one of the listed FILTER strings (e.g. 'PASS,.'')
  id: applyFilters
  inputBinding:
    position: 1
    prefix: --apply-filters
  label: applyFilters
  type:
  - items: string
    type: array
  - 'null'
- doc: (-g) [<hom|het|miss>] require one or more hom/het/missing genotype or, if prefixed
    with '^', exclude sites with hom/het/missing genotypes
  id: genotype
  inputBinding:
    position: 1
    prefix: --genotype
  label: genotype
  type:
  - string
  - 'null'
- doc: (-i) select sites for which the expression is true (see man page for details)
  id: include
  inputBinding:
    position: 1
    prefix: --include
  label: include
  type:
  - string
  - 'null'
- doc: (-e) exclude sites for which the expression is true (see man page for details)
  id: exclude
  inputBinding:
    position: 1
    prefix: --exclude
  label: exclude
  type:
  - string
  - 'null'
- doc: (-k) select known sites only (ID is not/is '.')
  id: known
  inputBinding:
    position: 1
    prefix: --known
  label: known
  type:
  - boolean
  - 'null'
- doc: (-n) select novel sites only (ID is not/is '.')
  id: novel
  inputBinding:
    position: 1
    prefix: --novel
  label: novel
  type:
  - boolean
  - 'null'
- doc: (-m) minimum number of alleles listed in REF and ALT (e.g. -m2 -M2 for biallelic
    sites)
  id: minAlleles
  inputBinding:
    position: 1
    prefix: --min-alleles
  label: minAlleles
  type:
  - int
  - 'null'
- doc: (-M) maximum number of alleles listed in REF and ALT (e.g. -m2 -M2 for biallelic
    sites)
  id: maxAlleles
  inputBinding:
    position: 1
    prefix: --max-alleles
  label: maxAlleles
  type:
  - int
  - 'null'
- doc: (-p) select sites where all samples are phased
  id: phased
  inputBinding:
    position: 1
    prefix: --phased
  label: phased
  type:
  - boolean
  - 'null'
- doc: (-P) exclude sites where all samples are phased
  id: excludePhased
  inputBinding:
    position: 1
    prefix: --exclude-phased
  label: excludePhased
  type:
  - boolean
  - 'null'
- doc: (-q) minimum frequency for non-reference (nref), 1st alternate (alt1), least
    frequent (minor), most frequent (major) or sum of all but most frequent (nonmajor)
    alleles [nref]
  id: minAf
  inputBinding:
    position: 1
    prefix: --min-af
  label: minAf
  type:
  - float
  - 'null'
- doc: (-Q) maximum frequency for non-reference (nref), 1st alternate (alt1), least
    frequent (minor), most frequent (major) or sum of all but most frequent (nonmajor)
    alleles [nref]
  id: maxAf
  inputBinding:
    position: 1
    prefix: --max-af
  label: maxAf
  type:
  - float
  - 'null'
- doc: (-u) select sites without a called genotype
  id: uncalled
  inputBinding:
    position: 1
    prefix: --uncalled
  label: uncalled
  type:
  - boolean
  - 'null'
- doc: (-U) exclude sites without a called genotype
  id: excludeUncalled
  inputBinding:
    position: 1
    prefix: --exclude-uncalled
  label: excludeUncalled
  type:
  - boolean
  - 'null'
- doc: '(-v) select comma-separated list of variant types: snps,indels,mnps,other
    [null]'
  id: types
  inputBinding:
    position: 1
    prefix: --types
  label: types
  type:
  - items: string
    type: array
  - 'null'
- doc: '(-V) exclude comma-separated list of variant types: snps,indels,mnps,other
    [null]'
  id: excludeTypes
  inputBinding:
    position: 1
    prefix: --exclude-types
  label: excludeTypes
  type:
  - items: string
    type: array
  - 'null'
- doc: (-x) select sites where the non-reference alleles are exclusive (private) to
    the subset samples
  id: private
  inputBinding:
    position: 1
    prefix: --private
  label: private
  type:
  - boolean
  - 'null'
- doc: (-X) exclude sites where the non-reference alleles are exclusive (private)
    to the subset samples
  id: excludePrivate
  inputBinding:
    position: 1
    prefix: --exclude-private
  label: excludePrivate
  type:
  - boolean
  - 'null'
label: bcftoolsview
outputs:
- id: out
  label: out
  type: stdout
requirements:
  DockerRequirement:
    dockerPull: biocontainers/bcftools:v1.5_cv2
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
