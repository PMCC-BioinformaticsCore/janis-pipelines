arguments:
- position: 3
  shellQuote: false
  valueFrom: '| teststrandbias.R |'
- position: 4
  shellQuote: false
  valueFrom: var2vcf_valid.pl
baseCommand: VarDict
class: CommandLineTool
cwlVersion: v1.0
id: vardict_germline
inputs:
- id: intervals
  inputBinding:
    position: 2
    shellQuote: false
  label: intervals
  type: File
- default: generated-65169ac4-cf83-11e9-b4cb-acde48001122.vardict.vcf
  id: outputFilename
  inputBinding:
    position: 6
    prefix: '>'
    shellQuote: false
  label: outputFilename
  type: string
- doc: The indexed BAM file
  id: bam
  inputBinding:
    position: 1
    prefix: -b
    shellQuote: false
  label: bam
  secondaryFiles:
  - ^.bai
  type: File
- doc: 'The reference fasta. Should be indexed (.fai). Defaults to: /ngs/reference_data/genomes/Hsapiens/hg19/seq/hg19.fa'
  id: reference
  inputBinding:
    position: 1
    prefix: -G
    shellQuote: false
  label: reference
  secondaryFiles:
  - .fai
  type: File
- doc: Indicate to move indels to 3-prime if alternative alignment can be achieved.
  id: indels3prime
  inputBinding:
    position: 1
    prefix: '-3'
    shellQuote: false
  label: indels3prime
  type:
  - boolean
  - 'null'
- doc: "Indicate it's amplicon based calling.  Reads that don't map to the amplicon\
    \ will be skipped.  A read pair is considered belonging  to the amplicon if the\
    \ edges are less than int bp to the amplicon, and overlap fraction is at least\
    \ float.  Default: 10:0.95"
  id: amplicon
  inputBinding:
    position: 1
    prefix: -a
    shellQuote: false
  label: amplicon
  type:
  - float
  - 'null'
- doc: 'The minimum # of reads to determine strand bias, default 2'
  id: minReads
  inputBinding:
    position: 1
    prefix: -B
    shellQuote: false
  label: minReads
  type:
  - int
  - 'null'
- doc: Indicate the chromosome names are just numbers, such as 1, 2, not chr1, chr2
  id: chromNamesAreNumbers
  inputBinding:
    position: 1
    prefix: -C
    shellQuote: false
  label: chromNamesAreNumbers
  type:
  - boolean
  - 'null'
- doc: The column for chromosome
  id: chromColumn
  inputBinding:
    position: 1
    prefix: -c
    shellQuote: false
  label: chromColumn
  type:
  - int
  - 'null'
- doc: Debug mode.  Will print some error messages and append full genotype at the
    end.
  id: debug
  inputBinding:
    position: 1
    prefix: -D
    shellQuote: false
  label: debug
  type:
  - boolean
  - 'null'
- doc: "The delimiter for split region_info, default to tab \"\t\""
  id: splitDelimeter
  inputBinding:
    position: 1
    prefix: -d
    shellQuote: false
  label: splitDelimeter
  type:
  - string
  - 'null'
- doc: The column for region end, e.g. gene end
  id: geneEndCol
  inputBinding:
    position: 1
    prefix: -E
    shellQuote: false
  label: geneEndCol
  type:
  - int
  - 'null'
- doc: The column for segment ends in the region, e.g. exon ends
  id: segEndCol
  inputBinding:
    position: 1
    prefix: -e
    shellQuote: false
  label: segEndCol
  type:
  - int
  - 'null'
- doc: 'The hexical to filter reads using samtools. Default: 0x500 (filter 2nd alignments
    and duplicates). Use -F 0 to turn it off.'
  id: filter
  inputBinding:
    position: 1
    prefix: -F
    shellQuote: false
  label: filter
  type:
  - string
  - 'null'
- doc: 'The threshold for allele frequency, default: 0.05 or 5%'
  id: alleleFreqThreshold
  inputBinding:
    position: 1
    prefix: -f
    shellQuote: false
  label: alleleFreqThreshold
  type:
  - float
  - 'null'
- doc: The column for gene name, or segment annotation
  id: geneNameCol
  inputBinding:
    position: 1
    prefix: -g
    shellQuote: false
  label: geneNameCol
  type:
  - int
  - 'null'
- doc: Print a header row describing columns
  id: printHeaderRow
  inputBinding:
    position: 1
    prefix: -h
    shellQuote: false
  label: printHeaderRow
  type:
  - boolean
  - 'null'
- doc: 'The indel size.  Default: 120bp'
  id: indelSize
  inputBinding:
    position: 1
    prefix: -I
    shellQuote: false
  label: indelSize
  type:
  - int
  - 'null'
- doc: Output splicing read counts
  id: outputSplice
  inputBinding:
    position: 1
    prefix: -i
    shellQuote: false
  label: outputSplice
  type:
  - boolean
  - 'null'
- doc: 'Indicate whether to perform local realignment.  Default: 1.  Set to 0 to disable
    it. For Ion or PacBio, 0 is recommended.'
  id: performLocalRealignment
  inputBinding:
    position: 1
    prefix: -k
    shellQuote: false
  label: performLocalRealignment
  type:
  - int
  - 'null'
- doc: "The minimum matches for a read to be considered. If, after soft-clipping,\
    \ the matched bp is less than INT, then the read is discarded. It's meant for\
    \ PCR based targeted sequencing where there's no insert and the matching is only\
    \ the primers. Default: 0, or no filtering"
  id: minMatches
  inputBinding:
    position: 1
    prefix: -M
    shellQuote: false
  label: minMatches
  type:
  - int
  - 'null'
- doc: 'If set, reads with mismatches more than INT will be filtered and ignored.
    Gaps are not counted as mismatches. Valid only for bowtie2/TopHat or BWA aln followed
    by sampe. BWA mem is calculated as NM - Indels. Default: 8, or reads with more
    than 8 mismatches will not be used.'
  id: maxMismatches
  inputBinding:
    position: 1
    prefix: -m
    shellQuote: false
  label: maxMismatches
  type:
  - int
  - 'null'
- doc: The sample name to be used directly.  Will overwrite -n option
  id: sampleName
  inputBinding:
    position: 1
    prefix: -N
    shellQuote: false
  label: sampleName
  type: string
- doc: 'The regular expression to extract sample name from BAM filenames. Default
    to: /([^\/\._]+?)_[^\/]*.bam/'
  id: regexSampleName
  inputBinding:
    position: 1
    prefix: -n
    shellQuote: false
  label: regexSampleName
  type:
  - string
  - 'null'
- doc: 'The reads should have at least mean MapQ to be considered a valid variant.
    Default: no filtering'
  id: mapq
  inputBinding:
    position: 1
    prefix: -O
    shellQuote: false
  label: mapq
  type:
  - string
  - 'null'
- doc: 'The Qratio of (good_quality_reads)/(bad_quality_reads+0.5). The quality is
    defined by -q option.  Default: 1.5'
  id: qratio
  inputBinding:
    position: 1
    prefix: -o
    shellQuote: false
  label: qratio
  type:
  - float
  - 'null'
- doc: "The read position filter. If the mean variants position is less that specified,\
    \ it's considered false positive.  Default: 5"
  id: readPosition
  inputBinding:
    position: 1
    prefix: -P
    shellQuote: false
  label: readPosition
  type:
  - float
  - 'null'
- doc: Do pileup regardless of the frequency
  id: pileup
  inputBinding:
    position: 1
    prefix: -p
    shellQuote: false
  label: pileup
  type:
  - boolean
  - 'null'
- doc: If set, reads with mapping quality less than INT will be filtered and ignored
  id: minMappingQual
  inputBinding:
    position: 1
    prefix: -Q
    shellQuote: false
  label: minMappingQual
  type:
  - int
  - 'null'
- doc: 'The phred score for a base to be considered a good call.  Default: 25 (for
    Illumina) For PGM, set it to ~15, as PGM tends to under estimate base quality.'
  id: phredScore
  inputBinding:
    position: 1
    prefix: -q
    shellQuote: false
  label: phredScore
  type:
  - int
  - 'null'
- doc: The region of interest.  In the format of chr:start-end.  If end is omitted,
    then a single position.  No BED is needed.
  id: region
  inputBinding:
    position: 1
    prefix: -R
    shellQuote: false
  label: region
  type:
  - string
  - 'null'
- doc: 'The minimum # of variant reads, default 2'
  id: minVariantReads
  inputBinding:
    position: 1
    prefix: -r
    shellQuote: false
  label: minVariantReads
  type:
  - int
  - 'null'
- doc: The column for region start, e.g. gene start
  id: regStartCol
  inputBinding:
    position: 1
    prefix: -S
    shellQuote: false
  label: regStartCol
  type:
  - int
  - 'null'
- doc: The column for segment starts in the region, e.g. exon starts
  id: segStartCol
  inputBinding:
    position: 1
    prefix: -s
    shellQuote: false
  label: segStartCol
  type:
  - int
  - 'null'
- doc: Trim bases after [INT] bases in the reads
  id: minReadsBeforeTrim
  inputBinding:
    position: 1
    prefix: -T
    shellQuote: false
  label: minReadsBeforeTrim
  type:
  - int
  - 'null'
- doc: Indicate to remove duplicated reads.  Only one pair with same start positions
    will be kept
  id: removeDuplicateReads
  inputBinding:
    position: 1
    prefix: -t
    shellQuote: false
  label: removeDuplicateReads
  type:
  - boolean
  - 'null'
- doc: Threads count.
  id: threads
  inputBinding:
    position: 1
    prefix: -th
    shellQuote: false
    valueFrom: $(inputs.runtime_cpu)
  label: threads
  type:
  - int
  - 'null'
- doc: The lowest frequency in the normal sample allowed for a putative somatic mutation.
    Defaults to 0.05
  id: freq
  inputBinding:
    position: 1
    prefix: -V
    shellQuote: false
  label: freq
  type:
  - int
  - 'null'
- doc: VCF format output
  id: vcfFormat
  inputBinding:
    position: 1
    prefix: -v
    shellQuote: false
  label: vcfFormat
  type:
  - boolean
  - 'null'
- doc: "[STRICT | LENIENT | SILENT] How strict to be when reading a SAM or BAM: STRICT\
    \   - throw an exception if something looks wrong. LENIENT\t- Emit warnings but\
    \ keep going if possible. SILENT\t- Like LENIENT, only don't emit warning messages.\
    \ Default: LENIENT"
  id: vs
  inputBinding:
    position: 1
    prefix: -VS
    shellQuote: false
  label: vs
  type:
  - string
  - 'null'
- doc: Extension of bp to look for mismatches after insersion or deletion.  Default
    to 3 bp, or only calls when they're within 3 bp.
  id: bp
  inputBinding:
    position: 1
    prefix: -X
    shellQuote: false
  label: bp
  type:
  - int
  - 'null'
- doc: 'The number of nucleotide to extend for each segment, default: 0'
  id: extensionNucleotide
  inputBinding:
    position: 1
    prefix: -x
    shellQuote: false
  label: extensionNucleotide
  type:
  - int
  - 'null'
- doc: <No content>
  id: yy
  inputBinding:
    position: 1
    prefix: -y
    shellQuote: false
  label: yy
  type:
  - boolean
  - 'null'
- doc: 'For downsampling fraction.  e.g. 0.7 means roughly 70% downsampling.  Default:
    No downsampling.  Use with caution.  The downsampling will be random and non-reproducible.'
  id: downsamplingFraction
  inputBinding:
    position: 1
    prefix: -Z
    shellQuote: false
  label: downsamplingFraction
  type:
  - int
  - 'null'
- doc: "0/1  Indicate whether coordinates are zero-based, as IGV uses.  Default: 1\
    \ for BED file or amplicon BED file. Use 0 to turn it off. When using the -R option,\
    \ it's set to 0"
  id: zeroBasedCoords
  inputBinding:
    position: 1
    prefix: -z
    shellQuote: false
  label: zeroBasedCoords
  type:
  - int
  - 'null'
- id: var2vcfSampleName
  inputBinding:
    position: 5
    prefix: -N
    shellQuote: false
  label: var2vcfSampleName
  type: string
- id: var2vcfAlleleFreqThreshold
  inputBinding:
    position: 5
    prefix: -f
    shellQuote: false
  label: var2vcfAlleleFreqThreshold
  type: float
label: vardict_germline
outputs:
- id: out
  label: out
  outputBinding:
    glob: $(inputs.outputFilename)
  type: File
requirements:
  DockerRequirement:
    dockerPull: michaelfranklin/vardict:1.5.8
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
