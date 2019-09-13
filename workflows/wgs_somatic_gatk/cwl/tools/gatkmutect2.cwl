baseCommand:
- gatk
- Mutect2
class: CommandLineTool
cwlVersion: v1.0
doc: "USAGE: Mutect2 [arguments]\nCall somatic SNVs and indels via local assembly\
  \ of haplotypes\nVersion:4.1.2.0\n"
id: gatkmutect2
inputs:
- doc: '(--input) BAM/SAM/CRAM file containing reads This argument must be specified
    at least once. Required. '
  id: tumorBams
  label: tumorBams
  type:
    inputBinding:
      prefix: -I
    items: File
    type: array
- doc: '(--input) Extra BAM/SAM/CRAM file containing reads This argument must be specified
    at least once. Required. '
  id: normalBams
  label: normalBams
  type:
    inputBinding:
      prefix: -I
    items: File
    type: array
- doc: (--normal-sample, if) May be URL-encoded as output by GetSampleName with
  id: normalSample
  inputBinding:
    prefix: --normal-sample
  label: normalSample
  type: string
- default: generated-b85f4aa2-d5b7-11e9-a06a-f218985ebfa7.vcf.gz
  id: outputFilename
  inputBinding:
    position: 20
    prefix: -O
  label: outputFilename
  type: string
- doc: (-R) Reference sequence file Required.
  id: reference
  inputBinding:
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
  type: File
- doc: 'Default value: null.'
  id: activityProfileOut
  inputBinding:
    prefix: --activity-profile-out
  label: activityProfileOut
  type:
  - string
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
- doc: '(-default-af)  Population allele fraction assigned to alleles not found in
    germline resource.  Please see docs/mutect/mutect2.pdf fora derivation of the
    default value.  Default value: -1.0. '
  id: afOfAllelesNotInResource
  inputBinding:
    prefix: --af-of-alleles-not-in-resource
  label: afOfAllelesNotInResource
  type:
  - string
  - 'null'
- doc: 'The set of alleles for which to force genotyping regardless of evidence Default
    value: null. '
  id: alleles
  inputBinding:
    prefix: --alleles
  label: alleles
  type:
  - string
  - 'null'
- doc: '(-A) One or more specific annotations to add to variant calls This argument
    may be specified 0 or more times. Default value: null. Possible Values: {AlleleFraction,
    AS_BaseQualityRankSumTest, AS_FisherStrand, AS_InbreedingCoeff, AS_MappingQualityRankSumTest,
    AS_QualByDepth, AS_ReadPosRankSumTest, AS_RMSMappingQuality, AS_StrandOddsRatio,
    BaseQuality, BaseQualityRankSumTest, ChromosomeCounts, ClippingRankSumTest, CountNs,
    Coverage, DepthPerAlleleBySample, DepthPerSampleHC, ExcessHet, FisherStrand, FragmentLength,
    GenotypeSummaries, InbreedingCoeff, LikelihoodRankSumTest, MappingQuality, MappingQualityRankSumTest,
    MappingQualityZero, OrientationBiasReadCounts, OriginalAlignment, PossibleDeNovo,
    QualByDepth, ReadPosition, ReadPosRankSumTest, ReferenceBases, RMSMappingQuality,
    SampleList, StrandBiasBySample, StrandOddsRatio, TandemRepeat, UniqueAltReadCount}'
  id: annotation
  inputBinding:
    prefix: --annotation
  label: annotation
  type:
  - string
  - 'null'
- doc: '(-G) One or more groups of annotations to apply to variant calls This argument
    may be specified 0 or more times. Default value: null. Possible Values: {AS_StandardAnnotation,
    ReducibleAnnotation, StandardAnnotation, StandardHCAnnotation, StandardMutectAnnotation}'
  id: annotationGroup
  inputBinding:
    prefix: --annotation-group
  label: annotationGroup
  type:
  - string
  - 'null'
- doc: '(-AX)  One or more specific annotations to exclude from variant calls  This
    argument may be specified 0 or more times. Default value: null. Possible Values:
    {BaseQuality, Coverage, DepthPerAlleleBySample, DepthPerSampleHC, FragmentLength,
    MappingQuality, OrientationBiasReadCounts, ReadPosition, StrandBiasBySample, TandemRepeat}'
  id: annotationsToExclude
  inputBinding:
    prefix: --annotations-to-exclude
  label: annotationsToExclude
  type:
  - string
  - 'null'
- doc: 'read one or more arguments files and add them to the command line This argument
    may be specified 0 or more times. Default value: null. '
  id: arguments_file
  inputBinding:
    prefix: --arguments_file
  label: arguments_file
  type:
  - File
  - 'null'
- doc: 'Output the assembly region to this IGV formatted file Default value: null.'
  id: assemblyRegionOut
  inputBinding:
    prefix: --assembly-region-out
  label: assemblyRegionOut
  type:
  - string
  - 'null'
- doc: ' Base qualities below this threshold will be reduced to the minimum (6)  Default
    value: 18.'
  id: baseQualityScoreThreshold
  inputBinding:
    prefix: --base-quality-score-threshold
  label: baseQualityScoreThreshold
  type:
  - int
  - 'null'
- doc: 'Minimum depth to be considered callable for Mutect stats. Does not affect
    genotyping. Default value: 10. '
  id: callableDepth
  inputBinding:
    prefix: --callable-depth
  label: callableDepth
  type:
  - int
  - 'null'
- doc: '(-CIPB)  Size of the cloud-only prefetch buffer (in MB; 0 to disable). Defaults
    to cloudPrefetchBuffer if unset.  Default value: -1. '
  id: cloudIndexPrefetchBuffer
  inputBinding:
    prefix: --cloud-index-prefetch-buffer
  label: cloudIndexPrefetchBuffer
  type:
  - int
  - 'null'
- doc: '(-CPB)  Size of the cloud-only prefetch buffer (in MB; 0 to disable).  Default
    value: 40. '
  id: cloudPrefetchBuffer
  inputBinding:
    prefix: --cloud-prefetch-buffer
  label: cloudPrefetchBuffer
  type:
  - int
  - 'null'
- doc: '(-OBI)  If true, create a BAM/CRAM index when writing a coordinate-sorted
    BAM/CRAM file.  Default value: true. Possible values: {true, false} '
  id: createOutputBamIndex
  inputBinding:
    prefix: --create-output-bam-index
  label: createOutputBamIndex
  type:
  - boolean
  - 'null'
- doc: '(-OBM)  If true, create a MD5 digest for any BAM/SAM/CRAM file created  Default
    value: false. Possible values: {true, false} '
  id: createOutputBamMd5
  inputBinding:
    prefix: --create-output-bam-md5
  label: createOutputBamMd5
  type:
  - boolean
  - 'null'
- doc: '(-OVI)  If true, create a VCF index when writing a coordinate-sorted VCF file.  Default
    value: true. Possible values: {true, false} '
  id: createOutputVariantIndex
  inputBinding:
    prefix: --create-output-variant-index
  label: createOutputVariantIndex
  type:
  - boolean
  - 'null'
- doc: '(-OVM)  If true, create a a MD5 digest any VCF file created.  Default value:
    false. Possible values: {true, false} '
  id: createOutputVariantMd5
  inputBinding:
    prefix: --create-output-variant-md5
  label: createOutputVariantMd5
  type:
  - boolean
  - 'null'
- doc: "(-DBIC)  If true, don't cache bam indexes, this will reduce memory requirements\
    \ but may harm performance if many intervals are specified.  Caching is automatically\
    \ disabled if there are no intervals specified.  Default value: false. Possible\
    \ values: {true, false} "
  id: disableBamIndexCaching
  inputBinding:
    prefix: --disable-bam-index-caching
  label: disableBamIndexCaching
  type:
  - boolean
  - 'null'
- doc: '(-DF)  Read filters to be disabled before analysis  This argument may be specified
    0 or more times. Default value: null. Possible Values: {GoodCigarReadFilter, MappedReadFilter,
    MappingQualityAvailableReadFilter, MappingQualityNotZeroReadFilter, MappingQualityReadFilter,
    NonChimericOriginalAlignmentReadFilter, NonZeroReferenceLengthAlignmentReadFilter,
    NotDuplicateReadFilter, NotSecondaryAlignmentReadFilter, PassesVendorQualityCheckReadFilter,
    ReadLengthReadFilter, WellformedReadFilter}'
  id: disableReadFilter
  inputBinding:
    prefix: --disable-read-filter
  label: disableReadFilter
  type:
  - boolean
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
- doc: '(-stride)  Downsample a pool of reads starting within a range of one or more
    bases.  Default value: 1. '
  id: downsamplingStride
  inputBinding:
    prefix: --downsampling-stride
  label: downsamplingStride
  type:
  - int
  - 'null'
- doc: '(-XLOne) This argument may be specified 0 or more times. Default value: null. '
  id: excludeIntervals
  inputBinding:
    prefix: --exclude-intervals
  label: excludeIntervals
  type:
  - boolean
  - 'null'
- doc: 'sites with depth higher than this value will be grouped Default value: 200.'
  id: f1r2MaxDepth
  inputBinding:
    prefix: --f1r2-max-depth
  label: f1r2MaxDepth
  type:
  - int
  - 'null'
- doc: 'skip sites with median mapping quality below this value Default value: 50.'
  id: f1r2MedianMq
  inputBinding:
    prefix: --f1r2-median-mq
  label: f1r2MedianMq
  type:
  - int
  - 'null'
- doc: 'exclude bases below this quality from pileup Default value: 20.'
  id: f1r2MinBq
  inputBinding:
    prefix: --f1r2-min-bq
  label: f1r2MinBq
  type:
  - int
  - 'null'
- default: generated-b85f4ef8-d5b7-11e9-a06a-f218985ebfa7.tar.gz
  doc: 'If specified, collect F1R2 counts and output files into this tar.gz file Default
    value: null. '
  id: f1r2TarGz_outputFilename
  inputBinding:
    prefix: --f1r2-tar-gz
  label: f1r2TarGz_outputFilename
  type: string
- doc: '(--founder-id)  Samples representing the population founders This argument
    may be specified 0 or more times. Default value: null. '
  id: founderId
  inputBinding:
    prefix: -founder-id
  label: founderId
  type:
  - string
  - 'null'
- doc: 'A configuration file to use with the GATK. Default value: null.'
  id: gatkConfigFile
  inputBinding:
    prefix: --gatk-config-file
  label: gatkConfigFile
  type:
  - string
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
- doc: ' Project to bill when accessing requester pays buckets. If unset, these buckets
    cannot be accessed.  Default value: . '
  id: gcsProjectForRequesterPays
  inputBinding:
    prefix: --gcs-project-for-requester-pays
  label: gcsProjectForRequesterPays
  type:
  - string
  - 'null'
- doc: ' (EXPERIMENTAL) Call all apparent germline site even though they will ultimately
    be filtered.  Default value: false. Possible values: {true, false} '
  id: genotypeGermlineSites
  inputBinding:
    prefix: --genotype-germline-sites
  label: genotypeGermlineSites
  type:
  - boolean
  - 'null'
- doc: 'Call sites in the PoN even though they will ultimately be filtered. Default
    value: false. Possible values: {true, false} '
  id: genotypePonSites
  inputBinding:
    prefix: --genotype-pon-sites
  label: genotypePonSites
  type:
  - boolean
  - 'null'
- doc: ' Population vcf of germline sequencing containing allele fractions.  Default
    value: null. '
  id: germlineResource
  inputBinding:
    prefix: --germline-resource
  label: germlineResource
  secondaryFiles:
  - .tbi
  type:
  - File
  - 'null'
- doc: '(--graph-output) Write debug assembly graph information to this file Default
    value: null.'
  id: graph
  inputBinding:
    prefix: -graph
  label: graph
  type:
  - string
  - 'null'
- doc: '(--help) display the help message Default value: false. Possible values: {true,
    false}'
  id: help
  inputBinding:
    prefix: -h
  label: help
  type:
  - boolean
  - 'null'
- doc: ' inverted tandem repeats.  Default value: false. Possible values: {true, false} '
  id: ignoreItrArtifacts
  inputBinding:
    prefix: --ignore-itr-artifactsTurn
  label: ignoreItrArtifacts
  type:
  - string
  - 'null'
- doc: '(-init-lod)  Log 10 odds threshold to consider pileup active.  Default value:
    2.0. '
  id: initialTumorLod
  inputBinding:
    prefix: --initial-tumor-lod
  label: initialTumorLod
  type:
  - string
  - 'null'
- doc: '(-ixp)  Amount of padding (in bp) to add to each interval you are excluding.  Default
    value: 0. '
  id: intervalExclusionPadding
  inputBinding:
    prefix: --interval-exclusion-padding
  label: intervalExclusionPadding
  type:
  - string
  - 'null'
- doc: '(--interval-merging-rule)  Interval merging rule for abutting intervals  Default
    value: ALL. Possible values: {ALL, OVERLAPPING_ONLY} '
  id: imr
  inputBinding:
    prefix: --interval-merging-rule
  label: imr
  type:
  - string
  - 'null'
- doc: '(--interval-padding) Default value: 0.'
  id: ip
  inputBinding:
    prefix: -ipAmount
  label: ip
  type:
  - string
  - 'null'
- doc: '(--interval-set-rule)  Set merging approach to use for combining interval
    inputs  Default value: UNION. Possible values: {UNION, INTERSECTION} '
  id: isr
  inputBinding:
    prefix: --interval-set-rule
  label: isr
  type:
  - string
  - 'null'
- doc: '(-L) One or more genomic intervals over which to operate This argument may
    be specified 0 or more times. Default value: null. '
  id: intervals
  inputBinding:
    prefix: --intervals
  label: intervals
  type:
  - string
  - 'null'
- doc: '(--lenient) Lenient processing of VCF files Default value: false. Possible
    values: {true, false}'
  id: le
  inputBinding:
    prefix: -LE
  label: le
  type:
  - boolean
  - 'null'
- doc: '(-max-af)  Maximum population allele frequency in tumor-only mode.  Default
    value: 0.01. '
  id: maxPopulationAf
  inputBinding:
    prefix: --max-population-af
  label: maxPopulationAf
  type:
  - string
  - 'null'
- doc: ' Maximum number of reads to retain per alignment start position. Reads above
    this threshold will be downsampled. Set to 0 to disable.  Default value: 50. '
  id: maxReadsPerAlignmentStart
  inputBinding:
    prefix: --max-reads-per-alignment-start
  label: maxReadsPerAlignmentStart
  type:
  - int
  - 'null'
- doc: '(-mbq:Byte)  Minimum base quality required to consider a base for calling  Default
    value: 10. '
  id: minBaseQualityScore
  inputBinding:
    prefix: --min-base-quality-score
  label: minBaseQualityScore
  type:
  - string
  - 'null'
- doc: 'Mitochondria mode sets emission and initial LODs to 0. Default value: false.
    Possible values: {true, false} '
  id: mitochondriaMode
  inputBinding:
    prefix: --mitochondria-mode
  label: mitochondriaMode
  type:
  - boolean
  - 'null'
- doc: ' How many threads should a native pairHMM implementation use  Default value:
    4. '
  id: nativePairHmmThreads
  inputBinding:
    prefix: --native-pair-hmm-threads
    valueFrom: $(inputs.runtime_cpu)
  label: nativePairHmmThreads
  type:
  - int
  - 'null'
- doc: ' use double precision in the native pairHmm. This is slower but matches the
    java implementation better  Default value: false. Possible values: {true, false} '
  id: nativePairHmmUseDoublePrecision
  inputBinding:
    prefix: --native-pair-hmm-use-double-precision
  label: nativePairHmmUseDoublePrecision
  type:
  - boolean
  - 'null'
- doc: 'Log 10 odds threshold for calling normal variant non-germline. Default value:
    2.2.'
  id: normalLod
  inputBinding:
    prefix: --normal-lod
  label: normalLod
  type:
  - double
  - 'null'
- doc: 'This argument may be specified 0 or more times. Default value: null.'
  id: encode
  inputBinding:
    prefix: -encode
  label: encode
  type:
  - string
  - 'null'
- doc: '(--panel-of-normals)  VCF file of sites observed in normal.  Default value:
    null. '
  id: panelOfNormals
  inputBinding:
    prefix: --panel-of-normals
  label: panelOfNormals
  secondaryFiles:
  - .tbi
  type:
  - File
  - 'null'
- doc: 'Phred-scaled PCR SNV qual for overlapping fragments Default value: 40.'
  id: pcrIndelQual
  inputBinding:
    prefix: --pcr-indel-qual
  label: pcrIndelQual
  type:
  - int
  - 'null'
- doc: 'Phred-scaled PCR SNV qual for overlapping fragments Default value: 40.'
  id: pcrSnvQual
  inputBinding:
    prefix: --pcr-snv-qual
  label: pcrSnvQual
  type:
  - int
  - 'null'
- doc: '(-ped) Pedigree file for determining the population founders. Default value:
    null.'
  id: pedigree
  inputBinding:
    prefix: --pedigree
  label: pedigree
  type:
  - string
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
- doc: '(-RF) Read filters to be applied before analysis This argument may be specified
    0 or more times. Default value: null. Possible Values: {AlignmentAgreesWithHeaderReadFilter,
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
    SeqIsStoredReadFilter, ValidAlignmentEndReadFilter, ValidAlignmentStartReadFilter,
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
    do not otherwise need to be decoded.  Default value: SILENT. Possible values:
    {STRICT, LENIENT, SILENT} '
  id: readValidationStringency
  inputBinding:
    prefix: --read-validation-stringency
  label: readValidationStringency
  type:
  - string
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
    prefix: --sites-only-vcf-output
  label: sitesOnlyVcfOutput
  type:
  - boolean
  - 'null'
- doc: 'Temp directory to use. Default value: null.'
  id: tmpDir
  inputBinding:
    prefix: --tmp-dir
  label: tmpDir
  type:
  - string
  - 'null'
- doc: '(-emit-lod)  Log 10 odds threshold to emit variant to VCF.  Default value:
    3.0. '
  id: tumorLodToEmit
  inputBinding:
    prefix: --tumor-lod-to-emit
  label: tumorLodToEmit
  type:
  - string
  - 'null'
- doc: '(--tumor-sample) BAM sample name of tumor. May be URL-encoded as output by
    GetSampleName with -encode argument.  Default value: null. '
  id: tumor
  inputBinding:
    prefix: -tumor
  label: tumor
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
    prefix: -verbosity
  label: verbosity
  type:
  - string
  - 'null'
- doc: 'display the version number for this tool Default value: false. Possible values:
    {true, false} '
  id: version
  inputBinding:
    prefix: --version
  label: version
  type:
  - boolean
  - 'null'
- doc: ' Minimum probability for a locus to be considered active.  Default value:
    0.002. '
  id: activeProbabilityThreshold
  inputBinding:
    prefix: --active-probability-threshold
  label: activeProbabilityThreshold
  type:
  - double
  - 'null'
- doc: ' Initial base error rate estimate for adaptive pruning  Default value: 0.001. '
  id: adaptivePruningInitialErrorRate
  inputBinding:
    prefix: --adaptive-pruning-initial-error-rate
  label: adaptivePruningInitialErrorRate
  type:
  - double
  - 'null'
- doc: ' Allow graphs that have non-unique kmers in the reference  Default value:
    false. Possible values: {true, false} '
  id: allowNonUniqueKmersInRef
  inputBinding:
    prefix: --allow-non-unique-kmers-in-ref
  label: allowNonUniqueKmersInRef
  type:
  - boolean
  - 'null'
- doc: ' Number of additional bases of context to include around each assembly region  Default
    value: 100. '
  id: assemblyRegionPadding
  inputBinding:
    prefix: --assembly-region-padding
  label: assemblyRegionPadding
  type:
  - int
  - 'null'
- doc: '(--bam-output) File to which assembled haplotypes should be written Default
    value: null.'
  id: bamout
  inputBinding:
    prefix: -bamout
  label: bamout
  type:
  - string
  - 'null'
- doc: 'Which haplotypes should be written to the BAM Default value: CALLED_HAPLOTYPES.
    Possible values: {ALL_POSSIBLE_HAPLOTYPES, CALLED_HAPLOTYPES} '
  id: bamWriterType
  inputBinding:
    prefix: --bam-writer-type
  label: bamWriterType
  type:
  - string
  - 'null'
- doc: '(-debug)  Print out verbose debug information about each assembly region  Default
    value: false. Possible values: {true, false} '
  id: debugAssembly
  inputBinding:
    prefix: --debug-assembly
  label: debugAssembly
  type:
  - string
  - 'null'
- doc: ' Disable the adaptive algorithm for pruning paths in the graph  Default value:
    false. Possible values: {true, false} '
  id: disableAdaptivePruning
  inputBinding:
    prefix: --disable-adaptive-pruning
  label: disableAdaptivePruning
  type:
  - boolean
  - 'null'
- doc: '(--disable-tool-default-annotations)  Disable all tool default annotations  Default
    value: false. Possible values: {true, false}'
  id: disableToolDefaultAnnotations
  inputBinding:
    prefix: -disable-tool-default-annotations
  label: disableToolDefaultAnnotations
  type:
  - boolean
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
- doc: ' Disable iterating over kmer sizes when graph cycles are detected  Default
    value: false. Possible values: {true, false} '
  id: dontIncreaseKmerSizesForCycles
  inputBinding:
    prefix: --dont-increase-kmer-sizes-for-cycles
  label: dontIncreaseKmerSizesForCycles
  type:
  - boolean
  - 'null'
- doc: ' If specified, we will not trim down the active region from the full region
    (active + extension) to just the active interval for genotyping  Default value:
    false. Possible values: {true, false} '
  id: dontTrimActiveRegions
  inputBinding:
    prefix: --dont-trim-active-regions
  label: dontTrimActiveRegions
  type:
  - boolean
  - 'null'
- doc: ' Do not analyze soft clipped bases in the reads  Default value: false. Possible
    values: {true, false} '
  id: dontUseSoftClippedBases
  inputBinding:
    prefix: --dont-use-soft-clipped-bases
  label: dontUseSoftClippedBases
  type:
  - boolean
  - 'null'
- doc: '(--emit-ref-confidence)  (BETA feature) Mode for emitting reference confidence
    scores  Default value: NONE. Possible values: {NONE, BP_RESOLUTION, GVCF} '
  id: erc
  inputBinding:
    prefix: -ERC
  label: erc
  type:
  - string
  - 'null'
- doc: ' Use all possible annotations (not for the faint of heart)  Default value:
    false. Possible values: {true, false} '
  id: enableAllAnnotations
  inputBinding:
    prefix: --enable-all-annotations
  label: enableAllAnnotations
  type:
  - boolean
  - 'null'
- doc: 'If provided, all regions will be marked as active Default value: false. Possible
    values: {true, false} '
  id: forceActive
  inputBinding:
    prefix: --force-active
  label: forceActive
  type:
  - boolean
  - 'null'
- doc: ' Whether to force genotype even filtered alleles  Default value: false. Possible
    values: {true, false} '
  id: genotypeFilteredAlleles
  inputBinding:
    prefix: --genotype-filtered-alleles
  label: genotypeFilteredAlleles
  type:
  - boolean
  - 'null'
- doc: '(-LODB) Exclusive upper bounds for reference confidence LOD bands (must be
    specified in increasing order)  This argument may be specified 0 or more times.
    Default value: [-2.5, -2.0, -1.5,'
  id: gvcfLodBand
  inputBinding:
    prefix: --gvcf-lod-band
  label: gvcfLodBand
  type:
  - string
  - 'null'
- doc: 'Kmer size to use in the read threading assembler This argument may be specified
    0 or more times. Default value: [10, 25]. '
  id: kmerSize
  inputBinding:
    prefix: --kmer-size
  label: kmerSize
  type:
  - int
  - 'null'
- doc: ' Maximum size of an assembly region  Default value: 300. '
  id: maxAssemblyRegionSize
  inputBinding:
    prefix: --max-assembly-region-size
  label: maxAssemblyRegionSize
  type:
  - int
  - 'null'
- doc: '(--max-mnp-distance)  Two or more phased substitutions separated by this distance
    or less are merged into MNPs.  Default value: 1. '
  id: mnpDist
  inputBinding:
    prefix: -mnp-dist
  label: mnpDist
  type:
  - int
  - 'null'
- doc: ' Maximum number of haplotypes to consider for your population  Default value:
    128. '
  id: maxNumHaplotypesInPopulation
  inputBinding:
    prefix: --max-num-haplotypes-in-population
  label: maxNumHaplotypesInPopulation
  type:
  - int
  - 'null'
- doc: ' Upper limit on how many bases away probability mass can be moved around when
    calculating the boundaries between active and inactive assembly regions  Default
    value: 50. '
  id: maxProbPropagationDistance
  inputBinding:
    prefix: --max-prob-propagation-distance
  label: maxProbPropagationDistance
  type:
  - int
  - 'null'
- doc: ' Maximum number of suspicious reads (mediocre mapping quality or too many
    substitutions) allowed in a downsampling stride.  Set to 0 to disable.  Default
    value: 0. '
  id: maxSuspiciousReadsPerAlignmentStart
  inputBinding:
    prefix: --max-suspicious-reads-per-alignment-start
  label: maxSuspiciousReadsPerAlignmentStart
  type:
  - int
  - 'null'
- doc: ' Maximum number of variants in graph the adaptive pruner will allow  Default
    value: 100. '
  id: maxUnprunedVariants
  inputBinding:
    prefix: --max-unpruned-variants
  label: maxUnprunedVariants
  type:
  - int
  - 'null'
- doc: ' Minimum size of an assembly region  Default value: 50. '
  id: minAssemblyRegionSize
  inputBinding:
    prefix: --min-assembly-region-size
  label: minAssemblyRegionSize
  type:
  - int
  - 'null'
- doc: ' Minimum length of a dangling branch to attempt recovery  Default value: 4. '
  id: minDanglingBranchLength
  inputBinding:
    prefix: --min-dangling-branch-length
  label: minDanglingBranchLength
  type:
  - int
  - 'null'
- doc: 'Minimum support to not prune paths in the graph Default value: 2.'
  id: minPruning
  inputBinding:
    prefix: --min-pruning
  label: minPruning
  type:
  - int
  - 'null'
- doc: '(-min-AF)  Lower bound of variant allele fractions to consider when calculating
    variant LOD  Default value: 0.0. '
  id: minimumAlleleFraction
  inputBinding:
    prefix: --minimum-allele-fraction
  label: minimumAlleleFraction
  type:
  - float
  - 'null'
- doc: 'Default value: 1.'
  id: numPruningSamples
  inputBinding:
    prefix: --num-pruning-samples
  label: numPruningSamples
  type:
  - int
  - 'null'
- doc: ' Flat gap continuation penalty for use in the Pair HMM  Default value: 10. '
  id: pairHmmGapContinuationPenalty
  inputBinding:
    prefix: --pair-hmm-gap-continuation-penalty
  label: pairHmmGapContinuationPenalty
  type:
  - int
  - 'null'
- doc: '(--pair-hmm-implementation)  The PairHMM implementation to use for genotype
    likelihood calculations  Default value: FASTEST_AVAILABLE. Possible values: {EXACT,
    ORIGINAL, LOGLESS_CACHING, AVX_LOGLESS_CACHING, AVX_LOGLESS_CACHING_OMP, EXPERIMENTAL_FPGA_LOGLESS_CACHING,
    FASTEST_AVAILABLE} '
  id: pairhmm
  inputBinding:
    prefix: -pairHMM
  label: pairhmm
  type:
  - string
  - 'null'
- doc: ' The PCR indel model to use  Default value: CONSERVATIVE. Possible values:
    {NONE, HOSTILE, AGGRESSIVE, CONSERVATIVE} '
  id: pcrIndelModel
  inputBinding:
    prefix: --pcr-indel-model
  label: pcrIndelModel
  type:
  - string
  - 'null'
- doc: ' The global assumed mismapping rate for reads  Default value: 45. '
  id: phredScaledGlobalReadMismappingRate
  inputBinding:
    prefix: --phred-scaled-global-read-mismapping-rate
  label: phredScaledGlobalReadMismappingRate
  type:
  - int
  - 'null'
- doc: 'Default value: 2.302585092994046. '
  id: pruningLodThreshold
  inputBinding:
    prefix: --pruning-lod-thresholdLn
  label: pruningLodThreshold
  type:
  - float
  - 'null'
- doc: ' Recover all dangling branches  Default value: false. Possible values: {true,
    false} '
  id: recoverAllDanglingBranches
  inputBinding:
    prefix: --recover-all-dangling-branches
  label: recoverAllDanglingBranches
  type:
  - boolean
  - 'null'
- doc: '(--showHidden)  display hidden arguments  Default value: false. Possible values:
    {true, false} '
  id: showhidden
  inputBinding:
    prefix: -showHidden
  label: showhidden
  type:
  - boolean
  - 'null'
- doc: ' Which Smith-Waterman implementation to use, generally FASTEST_AVAILABLE is
    the right choice  Default value: JAVA. Possible values: {FASTEST_AVAILABLE, AVX_ENABLED,
    JAVA} '
  id: smithWaterman
  inputBinding:
    prefix: --smith-waterman
  label: smithWaterman
  type:
  - string
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
- doc: 'One or more genomic intervals to keep This argument must be specified at least
    once. Required. '
  id: keepIntervals
  inputBinding:
    prefix: --keep-intervals
  label: keepIntervals
  type:
  - string
  - 'null'
- doc: (--library) Name of the library to keep This argument must be specified at
    least once. Required.
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
- doc: ' Minimum mapping quality to keep (inclusive)  Default value: 20. '
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
    prefix: --platform-filter-name
  label: platformFilterName
  type:
  - string
  - 'null'
- doc: Platform unit (PU) to filter out This argument must be specified at least once.
    Required.
  id: blackListedLanes
  inputBinding:
    prefix: --black-listed-lanes
  label: blackListedLanes
  type:
  - string
  - 'null'
- doc: 'This argument must be specified at least once. Required. '
  id: readGroupBlackList
  inputBinding:
    prefix: --read-group-black-listThe
  label: readGroupBlackList
  type:
  - string
  - 'null'
- doc: The name of the read group to keep Required.
  id: keepReadGroup
  inputBinding:
    prefix: --keep-read-group
  label: keepReadGroup
  type:
  - string
  - 'null'
- doc: 'Keep only reads with length at most equal to the specified value Default value:
    2147483647. '
  id: maxReadLength
  inputBinding:
    prefix: --max-read-length
  label: maxReadLength
  type:
  - int
  - 'null'
- doc: 'Keep only reads with length at least equal to the specified value Default
    value: 30.'
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
    prefix: --read-name
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
    prefix: -sample
  label: sample
  type:
  - string
  - 'null'
label: gatkmutect2
outputs:
- doc: To determine type
  id: out
  label: out
  outputBinding:
    glob: $(inputs.outputFilename)
  secondaryFiles:
  - .tbi
  type: File
- doc: To determine type
  id: stats
  label: stats
  outputBinding:
    glob: $("{outputFilename}.stats".replace(/\{outputFilename\}/g, inputs.outputFilename))
  type: File
- doc: To determine type
  id: f1f2r_out
  label: f1f2r_out
  outputBinding:
    glob: $(inputs.f1r2TarGz_outputFilename)
  type: File
requirements:
  DockerRequirement:
    dockerPull: broadinstitute/gatk:4.1.3.0
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
