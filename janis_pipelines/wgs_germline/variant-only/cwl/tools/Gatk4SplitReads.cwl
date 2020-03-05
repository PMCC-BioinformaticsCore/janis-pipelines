#!/usr/bin/env cwl-runner
baseCommand:
- gatk
- SplitReads
class: CommandLineTool
cwlVersion: v1.0
id: Gatk4SplitReads
inputs:
- default: .
  doc: "The directory to output SAM/BAM/CRAM files. Default value: '.' "
  id: outputFilename
  inputBinding:
    prefix: --output
  label: outputFilename
  type: string
- doc: (-I:String) BAM/SAM/CRAM file containing reads  This argument must be specified
    at least once.
  id: bam
  inputBinding:
    position: 1
    prefix: --input
  label: bam
  secondaryFiles: "${\n\n        function resolveSecondary(base, secPattern) {\n \
    \         if (secPattern[0] == \"^\") {\n            var spl = base.split(\".\"\
    );\n            var endIndex = spl.length > 1 ? spl.length - 1 : 1;\n        \
    \    return resolveSecondary(spl.slice(undefined, endIndex).join(\".\"), secPattern.slice(1));\n\
    \          }\n          return base + secPattern\n        }\n\n        return\
    \ [\n                {\n                    location: resolveSecondary(self.location,\
    \ \"^.bai\"),\n                    basename: resolveSecondary(self.basename, \"\
    .bai\")\n                }\n        ];\n\n}"
  type: File
- doc: '(-L:String) One or more genomic intervals over which to operate This argument
    may be specified 0 or more times. Default value: null. '
  id: intervals
  inputBinding:
    prefix: --intervals
  label: intervals
  type:
  - File
  - 'null'
- doc: '(--add-output-sam-program-record)  If true, adds a PG tag to created SAM/BAM/CRAM
    files.  Default value: true. Possible values: {true, false} '
  id: addOutputSamProgramRecord
  inputBinding:
    prefix: -add-output-sam-program-record
  label: addOutputSamProgramRecord
  type:
  - boolean
  - 'null'
- doc: '(--add-output-vcf-command-line)  If true, adds a command line header line
    to created VCF files.  Default value: true. Possible values: {true, false} '
  id: addOutputVcfCommandLine
  inputBinding:
    prefix: -add-output-vcf-command-line
  label: addOutputVcfCommandLine
  type:
  - boolean
  - 'null'
- doc: 'read one or more arguments files and add them to the command line This argument
    may be specified 0 or more times. Default value: null. '
  id: arguments_file
  inputBinding:
    prefix: --arguments_file:File
  label: arguments_file
  type:
  - File
  - 'null'
- doc: '(-CIPB:Integer)  Size of the cloud-only prefetch buffer (in MB; 0 to disable).
    Defaults to cloudPrefetchBuffer if unset.  Default value: -1. '
  id: cloudIndexPrefetchBuffer
  inputBinding:
    prefix: --cloud-index-prefetch-buffer
  label: cloudIndexPrefetchBuffer
  type:
  - string
  - 'null'
- doc: '(-CPB:Integer)  Size of the cloud-only prefetch buffer (in MB; 0 to disable).  Default
    value: 40. '
  id: cloudPrefetchBuffer
  inputBinding:
    prefix: --cloud-prefetch-buffer
  label: cloudPrefetchBuffer
  type:
  - string
  - 'null'
- doc: '(-OBI:Boolean)  If true, create a BAM/CRAM index when writing a coordinate-sorted
    BAM/CRAM file.  Default value: true. Possible values: {true, false} '
  id: createOutputBamIndex
  inputBinding:
    prefix: --create-output-bam-index
  label: createOutputBamIndex
  type:
  - string
  - 'null'
- doc: '(-OBM:Boolean)  If true, create a MD5 digest for any BAM/SAM/CRAM file created  Default
    value: false. Possible values: {true, false} '
  id: createOutputBamMd5
  inputBinding:
    prefix: --create-output-bam-md5
  label: createOutputBamMd5
  type:
  - string
  - 'null'
- doc: '(-OVI:Boolean)  If true, create a VCF index when writing a coordinate-sorted
    VCF file.  Default value: true. Possible values: {true, false} '
  id: createOutputVariantIndex
  inputBinding:
    prefix: --create-output-variant-index
  label: createOutputVariantIndex
  type:
  - string
  - 'null'
- doc: '(-OVM:Boolean)  If true, create a a MD5 digest any VCF file created.  Default
    value: false. Possible values: {true, false} '
  id: createOutputVariantMd5
  inputBinding:
    prefix: --create-output-variant-md5
  label: createOutputVariantMd5
  type:
  - string
  - 'null'
- doc: "(-DBIC:Boolean)  If true, don't cache bam indexes, this will reduce memory\
    \ requirements but may harm performance if many intervals are specified.  Caching\
    \ is automatically disabled if there are no intervals specified.  Default value:\
    \ false. Possible values: {true, false} "
  id: disableBamIndexCaching
  inputBinding:
    prefix: --disable-bam-index-caching
  label: disableBamIndexCaching
  type:
  - string
  - 'null'
- doc: '(-DF:String)  Read filters to be disabled before analysis  This argument may
    be specified 0 or more times. Default value: null. Possible Values: {WellformedReadFilter}'
  id: disableReadFilter
  inputBinding:
    prefix: --disable-read-filter
  label: disableReadFilter
  type:
  - string
  - 'null'
- doc: '(--disable-sequence-dictionary-validation)  If specified, do not check the
    sequence dictionaries from our inputs for compatibility. Use at your own risk!  Default
    value: false. Possible values: {true, false} '
  id: disableSequenceDictionaryValidation
  inputBinding:
    prefix: -disable-sequence-dictionary-validation
  label: disableSequenceDictionaryValidation
  type:
  - boolean
  - 'null'
- doc: '(-XL:StringOne) This argument may be specified 0 or more times. Default value:
    null. '
  id: excludeIntervals
  inputBinding:
    prefix: --exclude-intervals
  label: excludeIntervals
  type:
  - string
  - 'null'
- doc: 'A configuration file to use with the GATK. Default value: null.'
  id: gatkConfigFile
  inputBinding:
    prefix: --gatk-config-file
  label: gatkConfigFile
  type:
  - File
  - 'null'
- doc: '(--gcs-max-retries)  If the GCS bucket channel errors out, how many times
    it will attempt to re-initiate the connection  Default value: 20. '
  id: gcsRetries
  inputBinding:
    prefix: -gcs-retries
  label: gcsRetries
  type:
  - int
  - 'null'
- doc: ' Project to bill when accessing requester pays  buckets. If unset, these buckets
    cannot be accessed.  Default value: . '
  id: gcsProjectForRequesterPays
  inputBinding:
    prefix: --gcs-project-for-requester-pays
  label: gcsProjectForRequesterPays
  type:
  - string
  - 'null'
- doc: '(-ixp:Integer)  Amount of padding (in bp) to add to each interval you are
    excluding.  Default value: 0. '
  id: intervalExclusionPadding
  inputBinding:
    prefix: --interval-exclusion-padding
  label: intervalExclusionPadding
  type:
  - int
  - 'null'
- doc: '(--interval-merging-rule)  Interval merging rule for abutting intervals  Default
    value: ALL. Possible values: {ALL, OVERLAPPING_ONLY} '
  id: imr
  inputBinding:
    prefix: -imr:IntervalMergingRule
  label: imr
  type:
  - string
  - 'null'
- doc: '(--interval-padding) Default value: 0.'
  id: ip
  inputBinding:
    prefix: -ip
  label: ip
  type:
  - int
  - 'null'
- doc: '(--interval-set-rule)  Set merging approach to use for combining interval
    inputs  Default value: UNION. Possible values: {UNION, INTERSECTION} '
  id: isr
  inputBinding:
    prefix: -isr:IntervalSetRule
  label: isr
  type:
  - string
  - 'null'
- doc: '(-LE) Lenient processing of VCF files Default value: false. Possible values:
    {true, false}'
  id: le
  inputBinding:
    prefix: --lenient
  label: le
  type:
  - boolean
  - 'null'
- doc: 'Whether to suppress job-summary info on System.err. Default value: false.
    Possible values: {true, false} '
  id: quiet
  inputBinding:
    prefix: --QUIET
  label: quiet
  type:
  - boolean
  - 'null'
- doc: '(-RF:String) Read filters to be applied before analysis This argument may
    be specified 0 or more times. Default value: null. Possible Values: {AlignmentAgreesWithHeaderReadFilter,
    AllowAllReadsReadFilter, AmbiguousBaseReadFilter, CigarContainsNoNOperator, FirstOfPairReadFilter,
    FragmentLengthReadFilter, GoodCigarReadFilter, HasReadGroupReadFilter, IntervalOverlapReadFilter,
    LibraryReadFilter, MappedReadFilter, MappingQualityAvailableReadFilter, MappingQualityNotZeroReadFilter,
    MappingQualityReadFilter, MatchingBasesAndQualsReadFilter, MateDifferentStrandReadFilter,
    MateOnSameContigOrNoMappedMateReadFilter, MateUnmappedAndUnmappedReadFilter, MetricsReadFilter,
    NonChimericOriginalAlignmentReadFilter, NonZeroFragmentLengthReadFilter, NonZeroReferenceLengthAlignmentReadFilter,
    NotDuplicateReadFilter, NotOpticalDuplicateReadFilter, NotSecondaryAlignmentReadFilter,
    NotSupplementaryAlignmentReadFilter, OverclippedReadFilter, PairedReadFilter,
    PassesVendorQualityCheckReadFilter, PlatformReadFilter, PlatformUnitReadFilter,
    PrimaryLineReadFilter, ProperlyPairedReadFilter, ReadGroupBlackListReadFilter,
    ReadGroupReadFilter, ReadLengthEqualsCigarLengthReadFilter, ReadLengthReadFilter,
    ReadNameReadFilter, ReadStrandFilter, SampleReadFilter, SecondOfPairReadFilter,
    SeqIsStoredReadFilter, SoftClippedReadFilter, ValidAlignmentEndReadFilter, ValidAlignmentStartReadFilter,
    WellformedReadFilter}'
  id: readFilter
  inputBinding:
    prefix: --read-filter
  label: readFilter
  type:
  - string
  - 'null'
- doc: '(--read-index)  Indices to use for the read inputs. If specified, an index
    must be provided for every read input and in the same order as the read inputs.
    If this argument is not specified, the path to the index for each input will be
    inferred automatically.  This argument may be specified 0 or more times. Default
    value: null. '
  id: readIndex
  inputBinding:
    prefix: -read-index
  label: readIndex
  type:
  - string
  - 'null'
- doc: '(-VS:ValidationStringency)  Validation stringency for all SAM/BAM/CRAM/SRA
    files read by this program.  The default stringency value SILENT can improve performance
    when processing a BAM file in which variable-length data (read, qualities, tags)
    do not otherwise need to be decoded.  Default value: SITool returned: 0 LENT.
    Possible values: {STRICT, LENIENT, SILENT} '
  id: readValidationStringency
  inputBinding:
    prefix: --read-validation-stringency
  label: readValidationStringency
  type:
  - string
  - 'null'
- doc: '(-R:String) Reference sequence Default value: null.'
  id: reference
  inputBinding:
    prefix: --reference
  label: reference
  secondaryFiles:
  - .fai
  - .amb
  - .ann
  - .bwt
  - .pac
  - .sa
  - ^.dict
  type:
  - File
  - 'null'
- doc: '(--seconds-between-progress-updates)  Output traversal statistics every time
    this many seconds elapse  Default value: 10.0. '
  id: secondsBetweenProgressUpdates
  inputBinding:
    prefix: -seconds-between-progress-updates
  label: secondsBetweenProgressUpdates
  type:
  - double
  - 'null'
- doc: '(--sequence-dictionary)  Use the given sequence dictionary as the master/canonical
    sequence dictionary.  Must be a .dict file.  Default value: null. '
  id: sequenceDictionary
  inputBinding:
    prefix: -sequence-dictionary
  label: sequenceDictionary
  type:
  - string
  - 'null'
- doc: " If true, don't emit genotype fields when writing vcf file output.  Default\
    \ value: false. Possible values: {true, false} "
  id: sitesOnlyVcfOutput
  inputBinding:
    prefix: --sites-only-vcf-output:Boolean
  label: sitesOnlyVcfOutput
  type:
  - boolean
  - 'null'
- doc: '(-LB)  Split file by library.  Default value: false. Possible values: {true,
    false} '
  id: splitLibraryName
  inputBinding:
    prefix: --split-library-name
  label: splitLibraryName
  type:
  - string
  - 'null'
- doc: '(-RG:BooleanSplit) Default value: false. Possible values: {true, false}'
  id: rg
  inputBinding:
    prefix: --split-read-group
  label: rg
  type:
  - string
  - 'null'
- doc: '(-SM:Boolean) Split file by sample. Default value: false. Possible values:
    {true, false}'
  id: splitSample
  inputBinding:
    prefix: --split-sample
  label: splitSample
  type:
  - string
  - 'null'
- doc: 'Temp directory to use. Default value: null.'
  id: tmpDir
  inputBinding:
    prefix: --tmp-dir:GATKPathSpecifier
  label: tmpDir
  type:
  - string
  - 'null'
- doc: '(--use-jdk-deflater)  Whether to use the JdkDeflater (as opposed to IntelDeflater)  Default
    value: false. Possible values: {true, false} '
  id: jdkDeflater
  inputBinding:
    prefix: -jdk-deflater
  label: jdkDeflater
  type:
  - boolean
  - 'null'
- doc: '(--use-jdk-inflater)  Whether to use the JdkInflater (as opposed to IntelInflater)  Default
    value: false. Possible values: {true, false} '
  id: jdkInflater
  inputBinding:
    prefix: -jdk-inflater
  label: jdkInflater
  type:
  - boolean
  - 'null'
- doc: '(--verbosity)  Control verbosity of logging.  Default value: INFO. Possible
    values: {ERROR, WARNING, INFO, DEBUG} '
  id: verbosity
  inputBinding:
    prefix: -verbosity:LogLevel
  label: verbosity
  type:
  - string
  - 'null'
- doc: '(--disable-tool-default-read-filters)  Disable all tool default read filters
    (WARNING: many tools will not function correctly without their default read filters
    on)  Default value: false. Possible values: {true, false} '
  id: disableToolDefaultReadFilters
  inputBinding:
    prefix: -disable-tool-default-read-filters
  label: disableToolDefaultReadFilters
  type:
  - boolean
  - 'null'
- doc: 'Threshold number of ambiguous bases. If null, uses threshold fraction; otherwise,
    overrides threshold fraction.  Default value: null.  Cannot be used in conjuction
    with argument(s) maxAmbiguousBaseFraction'
  id: ambigFilterBases
  inputBinding:
    prefix: --ambig-filter-bases
  label: ambigFilterBases
  type:
  - int
  - 'null'
- doc: 'Threshold fraction of ambiguous bases Default value: 0.05. Cannot be used
    in conjuction with argument(s) maxAmbiguousBases'
  id: ambigFilterFrac
  inputBinding:
    prefix: --ambig-filter-frac
  label: ambigFilterFrac
  type:
  - double
  - 'null'
- doc: 'Default value: 1000000.'
  id: maxFragmentLength
  inputBinding:
    prefix: --max-fragment-length
  label: maxFragmentLength
  type:
  - int
  - 'null'
- doc: 'Default value: 0.'
  id: minFragmentLength
  inputBinding:
    prefix: --min-fragment-length
  label: minFragmentLength
  type:
  - int
  - 'null'
- doc: 'Valid only if "IntervalOverlapReadFilter" is specified: One or more genomic
    intervals to keep This argument must be specified at least once. Required. '
  id: keepIntervals
  inputBinding:
    prefix: --keep-intervals
  label: keepIntervals
  type:
  - string
  - 'null'
- doc: '(--library) Valid only if "LibraryReadFilter" is specified: Name of the library
    to keep This argument must be specified at least once. Required.'
  id: library
  inputBinding:
    prefix: -library
  label: library
  type:
  - string
  - 'null'
- doc: ' Maximum mapping quality to keep (inclusive)  Default value: null. '
  id: maximumMappingQuality
  inputBinding:
    prefix: --maximum-mapping-quality
  label: maximumMappingQuality
  type:
  - int
  - 'null'
- doc: ' Minimum mapping quality to keep (inclusive)  Default value: 10. '
  id: minimumMappingQuality
  inputBinding:
    prefix: --minimum-mapping-quality
  label: minimumMappingQuality
  type:
  - int
  - 'null'
- doc: ' Allow a read to be filtered out based on having only 1 soft-clipped block.
    By default, both ends must have a soft-clipped block, setting this flag requires
    only 1 soft-clipped block  Default value: false. Possible values: {true, false} '
  id: dontRequireSoftClipsBothEnds
  inputBinding:
    prefix: --dont-require-soft-clips-both-ends
  label: dontRequireSoftClipsBothEnds
  type:
  - boolean
  - 'null'
- doc: 'Minimum number of aligned bases Default value: 30.'
  id: filterTooShort
  inputBinding:
    prefix: --filter-too-short
  label: filterTooShort
  type:
  - int
  - 'null'
- doc: This argument must be specified at least once. Required.
  id: platformFilterName
  inputBinding:
    prefix: --platform-filter-name:String
  label: platformFilterName
  type:
  - string
  - 'null'
- doc: Platform unit (PU) to filter out This argument must be specified at least once.
    Required.
  id: blackListedLanes
  inputBinding:
    prefix: --black-listed-lanes:String
  label: blackListedLanes
  type:
  - string
  - 'null'
- doc: 'This argument must be specified at least once. Required. '
  id: readGroupBlackList
  inputBinding:
    prefix: --read-group-black-list:StringThe
  label: readGroupBlackList
  type:
  - string
  - 'null'
- doc: The name of the read group to keep Required.
  id: keepReadGroup
  inputBinding:
    prefix: --keep-read-group:String
  label: keepReadGroup
  type:
  - string
  - 'null'
- doc: Keep only reads with length at most equal to the specified value Required.
  id: maxReadLength
  inputBinding:
    prefix: --max-read-length
  label: maxReadLength
  type:
  - int
  - 'null'
- doc: 'Keep only reads with length at least equal to the specified value Default
    value: 1.'
  id: minReadLength
  inputBinding:
    prefix: --min-read-length
  label: minReadLength
  type:
  - int
  - 'null'
- doc: Keep only reads with this read name Required.
  id: readName
  inputBinding:
    prefix: --read-name:String
  label: readName
  type:
  - string
  - 'null'
- doc: ' Keep only reads on the reverse strand  Required. Possible values: {true,
    false} '
  id: keepReverseStrandOnly
  inputBinding:
    prefix: --keep-reverse-strand-only
  label: keepReverseStrandOnly
  type:
  - boolean
  - 'null'
- doc: '(--sample) The name of the sample(s) to keep, filtering out all others This
    argument must be specified at least once. Required. '
  id: sample
  inputBinding:
    prefix: -sample:String
  label: sample
  type:
  - string
  - 'null'
- doc: ' Inverts the results from this filter, causing all variants that would pass
    to fail and visa-versa.  Default value: false. Possible values: {true, false} '
  id: invertSoftClipRatioFilter
  inputBinding:
    prefix: --invert-soft-clip-ratio-filter
  label: invertSoftClipRatioFilter
  type:
  - boolean
  - 'null'
- doc: ' Threshold ratio of soft clipped bases (leading / trailing the cigar string)
    to total bases in read for read to be filtered.  Default value: null.  Cannot
    be used in conjuction with argument(s) minimumSoftClippedRatio'
  id: softClippedLeadingTrailingRatio
  inputBinding:
    prefix: --soft-clipped-leading-trailing-ratio
  label: softClippedLeadingTrailingRatio
  type:
  - double
  - 'null'
- doc: ' Threshold ratio of soft clipped bases (anywhere in the cigar string) to total
    bases in read for read to be filtered.  Default value: null.  Cannot be used in
    conjuction with argument(s) minimumLeadingTrailingSoftClippedRatio'
  id: softClippedRatioThreshold
  inputBinding:
    prefix: --soft-clipped-ratio-threshold
  label: softClippedRatioThreshold
  type:
  - double
  - 'null'
label: Gatk4SplitReads
outputs:
- doc: Bam
  id: out
  label: out
  outputBinding:
    glob: $(inputs.bam.basename)
  secondaryFiles: "${\n\n        function resolveSecondary(base, secPattern) {\n \
    \         if (secPattern[0] == \"^\") {\n            var spl = base.split(\".\"\
    );\n            var endIndex = spl.length > 1 ? spl.length - 1 : 1;\n        \
    \    return resolveSecondary(spl.slice(undefined, endIndex).join(\".\"), secPattern.slice(1));\n\
    \          }\n          return base + secPattern\n        }\n        return [\n\
    \                {\n                    path: resolveSecondary(self.path, \"^.bai\"\
    ),\n                    basename: resolveSecondary(self.basename, \".bai\")\n\
    \                }\n        ];\n\n}"
  type: File
requirements:
  DockerRequirement:
    dockerPull: broadinstitute/gatk:4.1.3.0
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
