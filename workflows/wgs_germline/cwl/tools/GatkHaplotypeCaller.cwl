baseCommand:
- gatk
- HaplotypeCaller
class: CommandLineTool
cwlVersion: v1.0
id: GatkHaplotypeCaller
inputs:
- doc: 'Output the raw activity profile results in IGV format (default: null)'
  id: activityProfileOut
  inputBinding:
    prefix: --activity-profile-out
  label: activityProfileOut
  type:
  - string
  - 'null'
- doc: '(default: null) The set of alleles at which to genotype when --genotyping_mode
    is GENOTYPE_GIVEN_ALLELES'
  id: alleles
  inputBinding:
    prefix: --alleles
  label: alleles
  type:
  - File
  - 'null'
- doc: If provided, we will annotate records with the number of alternate alleles
    that were discovered (but not necessarily genotyped) at a given site
  id: annotateWithNumDiscoveredAlleles
  inputBinding:
    prefix: --annotate-with-num-discovered-alleles
  label: annotateWithNumDiscoveredAlleles
  type:
  - boolean
  - 'null'
- doc: '-A: One or more specific annotations to add to variant calls'
  id: annotation
  inputBinding:
    prefix: --annotation
  label: annotation
  type:
  - items: string
    type: array
  - 'null'
- doc: "-G\tOne or more groups of annotations to apply to variant calls"
  id: annotationGroup
  inputBinding:
    prefix: --annotation-group
  label: annotationGroup
  type:
  - items: string
    type: array
  - 'null'
- doc: "-AX\tOne or more specific annotations to exclude from variant calls"
  id: annotationsToExclude
  inputBinding:
    prefix: --annotations-to-exclude
  label: annotationsToExclude
  type:
  - items: string
    type: array
  - 'null'
- doc: read one or more arguments files and add them to the command line
  id: arguments_file
  inputBinding:
    prefix: --arguments_file
  label: arguments_file
  type:
  - items: File
    type: array
  - 'null'
- doc: '(default: null) Output the assembly region to this IGV formatted file. Which
    annotations to exclude from output in the variant calls. Note that this argument
    has higher priority than the -A or -G arguments, so these annotations will be
    excluded even if they are explicitly included with the other options.'
  id: assemblyRegionOut
  inputBinding:
    prefix: --assembly-region-out
  label: assemblyRegionOut
  type:
  - string
  - 'null'
- doc: '(default: 18) Base qualities below this threshold will be reduced to the minimum
    (6)'
  id: baseQualityScoreThreshold
  inputBinding:
    prefix: --base-quality-score-threshold
  label: baseQualityScoreThreshold
  type:
  - int
  - 'null'
- doc: '-CIPB (default: -1) Size of the cloud-only prefetch buffer (in MB; 0 to disable).
    Defaults to cloudPrefetchBuffer if unset.'
  id: cloudIndexPrefetchBuffer
  inputBinding:
    prefix: --cloud-index-prefetch-buffer
  label: cloudIndexPrefetchBuffer
  type:
  - int
  - 'null'
- doc: '-CPB (default: 40) Size of the cloud-only prefetch buffer (in MB; 0 to disable).'
  id: cloudPrefetchBuffer
  inputBinding:
    prefix: --cloud-prefetch-buffer
  label: cloudPrefetchBuffer
  type:
  - int
  - 'null'
- doc: '-contamination (default: 0.0) Fraction of contamination in sequencing data
    (for all samples) to aggressively remove'
  id: contaminationFractionToFilter
  inputBinding:
    prefix: --contamination-fraction-to-filter
  label: contaminationFractionToFilter
  type:
  - double
  - 'null'
- doc: Undocumented option
  id: correctOverlappingQuality
  inputBinding:
    prefix: --correct-overlapping-quality
  label: correctOverlappingQuality
  type:
  - boolean
  - 'null'
- doc: -DBIC. If true, don't cache bam indexes, this will reduce memory requirements
    but may harm performance if many intervals are specified. Caching is automatically
    disabled if there are no intervals specified.
  id: disableBamIndexCaching
  inputBinding:
    prefix: --disable-bam-index-caching
  label: disableBamIndexCaching
  type:
  - boolean
  - 'null'
- doc: Samples representing the population "founders"
  id: founderId
  inputBinding:
    prefix: --founder-id
  label: founderId
  type:
  - items: string
    type: array
  - 'null'
- doc: '(default: DISCOVERY) Specifies how to determine the alternate alleles to use
    for genotyping. The --genotyping-mode argument is an enumerated type (GenotypingOutputMode),
    which can have one of the following values: DISCOVERY (The genotyper will choose
    the most likely alternate allele) or GENOTYPE_GIVEN_ALLELES (Only the alleles
    passed by the user should be considered).'
  id: genotypingMode
  inputBinding:
    prefix: --genotyping-mode
  label: genotypingMode
  type:
  - string
  - 'null'
- doc: "(default: 0.001) Heterozygosity value used to compute prior likelihoods for\
    \ any locus. The expected heterozygosity value used to compute prior probability\
    \ that a locus is non-reference. The default priors are for provided for humans:\
    \ het = 1e-3 which means that the probability of N samples being hom-ref at a\
    \ site is: 1 - sum_i_2N (het / i) Note that heterozygosity as used here is the\
    \ population genetics concept: http://en.wikipedia.org/wiki/Zygosity#Heterozygosity_in_population_genetics\
    \ . That is, a hets value of 0.01 implies that two randomly chosen chromosomes\
    \ from the population of organisms would differ from each other (one being A and\
    \ the other B) at a rate of 1 in 100 bp. Note that this quantity has nothing to\
    \ do with the likelihood of any given sample having a heterozygous genotype, which\
    \ in the GATK is purely determined by the probability of the observed data P(D\
    \ | AB) under the model that there may be a AB het genotype. The posterior probability\
    \ of this AB genotype would use the het prior, but the GATK only uses this posterior\
    \ probability in determining the prob. that a site is polymorphic. So changing\
    \ the het parameters only increases the chance that a site will be called non-reference\
    \ across all samples, but doesn't actually change the output genotype likelihoods\
    \ at all, as these aren't posterior probabilities at all. The quantity that changes\
    \ whether the GATK considers the possibility of a het genotype at all is the ploidy,\
    \ which determines how many chromosomes each individual in the species carries."
  id: heterozygosity
  inputBinding:
    prefix: --heterozygosity
  label: heterozygosity
  type:
  - double
  - 'null'
- doc: (default 0.01) Standard deviation of heterozygosity for SNP and indel calling.
  id: heterozygosityStdev
  inputBinding:
    prefix: --heterozygosity-stdev
  label: heterozygosityStdev
  type:
  - double
  - 'null'
- doc: '(default: 1.25E-4) Heterozygosity for indel calling. This argument informs
    the prior probability of having an indel at a site. (See heterozygosity)'
  id: indelHeterozygosity
  inputBinding:
    prefix: --indel-heterozygosity
  label: indelHeterozygosity
  type:
  - double
  - 'null'
- doc: '-imr (default: ALL) Interval merging rule for abutting intervals. By default,
    the program merges abutting intervals (i.e. intervals that are directly side-by-side
    but do not actually overlap) into a single continuous interval. However you can
    change this behavior if you want them to be treated as separate intervals instead.
    The --interval-merging-rule argument is an enumerated type (IntervalMergingRule),
    which can have one of the following values:[ALL, OVERLAPPING]'
  id: intervalMergingRule
  inputBinding:
    prefix: --interval-merging-rule
  label: intervalMergingRule
  type:
  - string
  - 'null'
- doc: '(default: 50) Maximum number of reads to retain per alignment start position.
    Reads above this threshold will be downsampled. Set to 0 to disable.'
  id: maxReadsPerAlignmentStart
  inputBinding:
    prefix: --max-reads-per-alignment-start
  label: maxReadsPerAlignmentStart
  type:
  - int
  - 'null'
- doc: '-mbq (default: 10) Minimum base quality required to consider a base for calling'
  id: minBaseQualityScore
  inputBinding:
    prefix: --min-base-quality-score
  label: minBaseQualityScore
  type:
  - int
  - 'null'
- doc: '(default: 4) How many threads should a native pairHMM implementation use'
  id: nativePairHmmThreads
  inputBinding:
    prefix: --native-pair-hmm-threads
  label: nativePairHmmThreads
  type:
  - int
  - 'null'
- doc: use double precision in the native pairHmm. This is slower but matches the
    java implementation better
  id: nativePairHmmUseDoublePrecision
  inputBinding:
    prefix: --native-pair-hmm-use-double-precision
  label: nativePairHmmUseDoublePrecision
  type:
  - boolean
  - 'null'
- doc: '(default: 0) Number of hom-ref genotypes to infer at sites not present in
    a panel. When a variant is not seen in any panel, this argument controls whether
    to infer (and with what effective strength) that only reference alleles were observed
    at that site. E.g. "If not seen in 1000Genomes, treat it as AC=0, AN=2000".'
  id: numReferenceSamplesIfNoCall
  inputBinding:
    prefix: --num-reference-samples-if-no-call
  label: numReferenceSamplesIfNoCall
  type:
  - int
  - 'null'
- doc: '(default: EMIT_VARIANTS_ONLY) Specifies which type of calls we should output.
    The --output-mode argument is an enumerated type (OutputMode), which can have
    one of the following values: [EMIT_VARIANTS_ONLY (produces calls only at variant
    sites), EMIT_ALL_CONFIDENT_SITES (produces calls at variant sites and confident
    reference sites), EMIT_ALL_SITES (produces calls at any callable site regardless
    of confidence; this argument is intended only for point mutations (SNPs) in DISCOVERY
    mode or generally when running in GENOTYPE_GIVEN_ALLELES mode; it will by no means
    produce a comprehensive set of indels in DISCOVERY mode)]'
  id: outputMode
  inputBinding:
    prefix: --output-mode
  label: outputMode
  type:
  - string
  - 'null'
- doc: '-ped (default: null) Pedigree file for determining the population "founders"'
  id: pedigree
  inputBinding:
    prefix: --pedigree
  label: pedigree
  type:
  - File
  - 'null'
- doc: '-population (default: null) Callset to use in calculating genotype priors'
  id: populationCallset
  inputBinding:
    prefix: --population-callset
  label: populationCallset
  type:
  - File
  - 'null'
- doc: '-ALIAS (default: null) Name of single sample to use from a multi-sample bam.
    You can use this argument to specify that HC should process a single sample out
    of a multisample BAM file. This is especially useful if your samples are all in
    the same file but you need to run them individually through HC in -ERC GVC mode
    (which is the recommended usage). Note that the name is case-sensitive.'
  id: sampleName
  inputBinding:
    prefix: --sample-name
  label: sampleName
  type:
  - string
  - 'null'
- doc: '-ploidy (default: 2) Ploidy (number of chromosomes) per sample. For pooled
    data, set to (Number of samples in each pool * Sample Ploidy). Sample ploidy -
    equivalent to number of chromosomes per pool. In pooled experiments this should
    be = # of samples in pool * individual sample ploidy'
  id: samplePloidy
  inputBinding:
    prefix: --sample-ploidy
  label: samplePloidy
  type:
  - int
  - 'null'
- doc: "(default: false) If true, don't emit genotype fields when writing vcf file\
    \ output."
  id: sitesOnlyVcfOutput
  inputBinding:
    prefix: --sites-only-vcf-output
  label: sitesOnlyVcfOutput
  type:
  - boolean
  - 'null'
- doc: '-stand-call-conf (default: 10.0) The minimum phred-scaled confidence threshold
    at which variants should be called'
  id: standardMinConfidenceThresholdForCalling
  inputBinding:
    prefix: --standard-min-confidence-threshold-for-calling
  label: standardMinConfidenceThresholdForCalling
  type:
  - double
  - 'null'
- doc: -new-qual If provided, we will use the new AF model instead of the so-called
    exact model
  id: useNewQualCalculator
  inputBinding:
    prefix: --use-new-qual-calculator
  label: useNewQualCalculator
  type:
  - boolean
  - 'null'
- doc: BAM/SAM/CRAM file containing reads
  id: inputRead
  inputBinding:
    prefix: --input
  label: inputRead
  secondaryFiles:
  - ^.bai
  type: File
- doc: Reference sequence file
  id: reference
  inputBinding:
    position: 5
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
- default: generated-6515fa74-cf83-11e9-b4cb-acde48001122.vcf
  doc: File to which variants should be written
  id: outputFilename
  inputBinding:
    position: 8
    prefix: --output
  label: outputFilename
  type: string
- doc: '(Also: -D) A dbSNP VCF file.'
  id: dbsnp
  inputBinding:
    position: 7
    prefix: --dbsnp
  label: dbsnp
  secondaryFiles:
  - .tbi
  type: File
- doc: -L (BASE) One or more genomic intervals over which to operate
  id: intervals
  inputBinding:
    prefix: --intervals
  label: intervals
  type:
  - File
  - 'null'
label: GatkHaplotypeCaller
outputs:
- doc: A raw, unfiltered, highly sensitive callset in VCF format. File to which variants
    should be written
  id: out
  label: out
  outputBinding:
    glob: $(inputs.outputFilename)
  secondaryFiles:
  - .idx
  type: File
requirements:
  DockerRequirement:
    dockerPull: broadinstitute/gatk:4.0.12.0
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
