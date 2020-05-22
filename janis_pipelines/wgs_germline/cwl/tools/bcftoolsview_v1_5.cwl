#!/usr/bin/env cwl-runner
class: CommandLineTool
cwlVersion: v1.0
label: 'BCFTools: View'
doc: |-
  ________________________________
   
          View, subset and filter VCF or BCF files by position and filtering expression
          Convert between VCF and BCF. Former bcftools subset.

requirements:
- class: ShellCommandRequirement
- class: InlineJavascriptRequirement
- class: DockerRequirement
  dockerPull: biocontainers/bcftools:v1.5_cv2

inputs:
- id: file
  label: file
  type: File
  inputBinding:
    position: 2
- id: dropGenotypes
  label: dropGenotypes
  doc: (-G) drop individual genotype information (after subsetting if -s option set)
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --drop-genotypes
    position: 1
- id: headerOnly
  label: headerOnly
  doc: (-h) print the header only
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --header-only
    position: 1
- id: noHeader
  label: noHeader
  doc: (-H) suppress the header in VCF output
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --no-header
    position: 1
- id: compressionLevel
  label: compressionLevel
  doc: '(-l) compression level: 0 uncompressed, 1 best speed, 9 best compression [-1]'
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --compression-level
    position: 1
- id: noVersion
  label: noVersion
  doc: do not append version and command line to the header
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --no-version
    position: 1
- id: regions
  label: regions
  doc: (-r) restrict to comma-separated list of regions
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --regions
    position: 1
- id: regionsFile
  label: regionsFile
  doc: (-R) restrict to regions listed in a file
  type:
  - File
  - 'null'
  inputBinding:
    prefix: --regions-file
    position: 1
- id: targets
  label: targets
  doc: |-
    (-t) similar to -r but streams rather than index-jumps. Exclude regions with '^' prefix
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --targets
    position: 1
- id: targetsFile
  label: targetsFile
  doc: |-
    (-T) similar to -R but streams rather than index-jumps. Exclude regions with '^' prefix
  type:
  - File
  - 'null'
  inputBinding:
    prefix: --targets-file
    position: 1
- id: threads
  label: threads
  doc: number of extra output compression threads [0]
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --threads
    position: 1
- id: trimAltAlleles
  label: trimAltAlleles
  doc: (-a) trim alternate alleles not seen in the subset
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --trim-alt-alleles
    position: 1
- id: noUpdate
  label: noUpdate
  doc: |-
    (-I) do not (re)calculate INFO fields for the subset (currently INFO/AC and INFO/AN)
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --no-update
    position: 1
- id: samples
  label: samples
  doc: (-s) comma separated list of samples to include (or exclude with '^' prefix)
  type:
  - type: array
    items: string
  - 'null'
  inputBinding:
    prefix: --samples
    position: 1
- id: samplesFile
  label: samplesFile
  doc: (-S) file of samples to include (or exclude with '^' prefix)
  type:
  - File
  - 'null'
  inputBinding:
    prefix: --samples-file
    position: 1
- id: forceSamples
  label: forceSamples
  doc: only warn about unknown subset samples
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --force-samples
    position: 1
- id: minAc
  label: minAc
  doc: |-
    (-c) minimum count for non-reference (nref), 1st alternate (alt1), least frequent (minor), most frequent (major) or sum of all but most frequent (nonmajor) alleles [nref]
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --min-ac
    position: 1
- id: maxAc
  label: maxAc
  doc: |-
    (-C) maximum count for non-reference (nref), 1st alternate (alt1), least frequent (minor), most frequent (major) or sum of all but most frequent (nonmajor) alleles [nref]
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --max-ac
    position: 1
- id: applyFilters
  label: applyFilters
  doc: (-f) require at least one of the listed FILTER strings (e.g. 'PASS,.'')
  type:
  - type: array
    items: string
  - 'null'
  inputBinding:
    prefix: --apply-filters
    position: 1
- id: genotype
  label: genotype
  doc: |-
    (-g) [<hom|het|miss>] require one or more hom/het/missing genotype or, if prefixed with '^', exclude sites with hom/het/missing genotypes
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --genotype
    position: 1
- id: include
  label: include
  doc: (-i) select sites for which the expression is true (see man page for details)
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --include
    position: 1
- id: exclude
  label: exclude
  doc: (-e) exclude sites for which the expression is true (see man page for details)
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --exclude
    position: 1
- id: known
  label: known
  doc: (-k) select known sites only (ID is not/is '.')
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --known
    position: 1
- id: novel
  label: novel
  doc: (-n) select novel sites only (ID is not/is '.')
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --novel
    position: 1
- id: minAlleles
  label: minAlleles
  doc: |-
    (-m) minimum number of alleles listed in REF and ALT (e.g. -m2 -M2 for biallelic sites)
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --min-alleles
    position: 1
- id: maxAlleles
  label: maxAlleles
  doc: |-
    (-M) maximum number of alleles listed in REF and ALT (e.g. -m2 -M2 for biallelic sites)
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --max-alleles
    position: 1
- id: phased
  label: phased
  doc: (-p) select sites where all samples are phased
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --phased
    position: 1
- id: excludePhased
  label: excludePhased
  doc: (-P) exclude sites where all samples are phased
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --exclude-phased
    position: 1
- id: minAf
  label: minAf
  doc: |-
    (-q) minimum frequency for non-reference (nref), 1st alternate (alt1), least frequent (minor), most frequent (major) or sum of all but most frequent (nonmajor) alleles [nref]
  type:
  - float
  - 'null'
  inputBinding:
    prefix: --min-af
    position: 1
- id: maxAf
  label: maxAf
  doc: |-
    (-Q) maximum frequency for non-reference (nref), 1st alternate (alt1), least frequent (minor), most frequent (major) or sum of all but most frequent (nonmajor) alleles [nref]
  type:
  - float
  - 'null'
  inputBinding:
    prefix: --max-af
    position: 1
- id: uncalled
  label: uncalled
  doc: (-u) select sites without a called genotype
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --uncalled
    position: 1
- id: excludeUncalled
  label: excludeUncalled
  doc: (-U) exclude sites without a called genotype
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --exclude-uncalled
    position: 1
- id: types
  label: types
  doc: '(-v) select comma-separated list of variant types: snps,indels,mnps,other
    [null]'
  type:
  - type: array
    items: string
  - 'null'
  inputBinding:
    prefix: --types
    position: 1
- id: excludeTypes
  label: excludeTypes
  doc: |-
    (-V) exclude comma-separated list of variant types: snps,indels,mnps,other [null]
  type:
  - type: array
    items: string
  - 'null'
  inputBinding:
    prefix: --exclude-types
    position: 1
- id: private
  label: private
  doc: |-
    (-x) select sites where the non-reference alleles are exclusive (private) to the subset samples
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --private
    position: 1
- id: excludePrivate
  label: excludePrivate
  doc: |-
    (-X) exclude sites where the non-reference alleles are exclusive (private) to the subset samples
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --exclude-private
    position: 1

outputs:
- id: out
  label: out
  type: stdout

baseCommand:
- bcftools
- view
arguments:
- prefix: --output-type
  position: 1
  valueFrom: z
id: bcftoolsview
