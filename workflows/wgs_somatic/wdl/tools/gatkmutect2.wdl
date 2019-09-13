version development

task gatkmutect2 {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Array[File] tumorBams
    Array[File] tumorBams_bai
    Array[File] normalBams
    Array[File] normalBams_bai
    String normalSample
    String outputFilename = "generated-55bed902-d5cc-11e9-bc6b-f218985ebfa7.vcf.gz"
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    String? activityProfileOut
    Boolean? addOutputSamProgramRecord
    Boolean? addOutputVcfCommandLine
    String? afOfAllelesNotInResource
    String? alleles
    String? annotation
    String? annotationGroup
    String? annotationsToExclude
    File? arguments_file
    String? assemblyRegionOut
    Int? baseQualityScoreThreshold
    Int? callableDepth
    Int? cloudIndexPrefetchBuffer
    Int? cloudPrefetchBuffer
    Boolean? createOutputBamIndex
    Boolean? createOutputBamMd5
    Boolean? createOutputVariantIndex
    Boolean? createOutputVariantMd5
    Boolean? disableBamIndexCaching
    Boolean? disableReadFilter
    Boolean? disableSequenceDictionaryValidation
    Int? downsamplingStride
    Boolean? excludeIntervals
    Int? f1r2MaxDepth
    Int? f1r2MedianMq
    Int? f1r2MinBq
    String f1r2TarGz_outputFilename = "generated-55beddda-d5cc-11e9-bc6b-f218985ebfa7.tar.gz"
    String? founderId
    String? gatkConfigFile
    Int? gcsRetries
    String? gcsProjectForRequesterPays
    Boolean? genotypeGermlineSites
    Boolean? genotypePonSites
    File? germlineResource
    File? germlineResource_tbi
    String? graph
    Boolean? help
    String? ignoreItrArtifacts
    String? initialTumorLod
    String? intervalExclusionPadding
    String? imr
    String? ip
    String? isr
    String? intervals
    Boolean? le
    String? maxPopulationAf
    Int? maxReadsPerAlignmentStart
    String? minBaseQualityScore
    Boolean? mitochondriaMode
    Int? nativePairHmmThreads
    Boolean? nativePairHmmUseDoublePrecision
    Float? normalLod
    String? encode
    File? panelOfNormals
    File? panelOfNormals_tbi
    Int? pcrIndelQual
    Int? pcrSnvQual
    String? pedigree
    Boolean? quiet
    String? readFilter
    String? readIndex
    String? readValidationStringency
    Float? secondsBetweenProgressUpdates
    String? sequenceDictionary
    Boolean? sitesOnlyVcfOutput
    String? tmpDir
    String? tumorLodToEmit
    String? tumor
    Boolean? jdkDeflater
    Boolean? jdkInflater
    String? verbosity
    Boolean? version
    Float? activeProbabilityThreshold
    Float? adaptivePruningInitialErrorRate
    Boolean? allowNonUniqueKmersInRef
    Int? assemblyRegionPadding
    String? bamout
    String? bamWriterType
    String? debugAssembly
    Boolean? disableAdaptivePruning
    Boolean? disableToolDefaultAnnotations
    Boolean? disableToolDefaultReadFilters
    Boolean? dontIncreaseKmerSizesForCycles
    Boolean? dontTrimActiveRegions
    Boolean? dontUseSoftClippedBases
    String? erc
    Boolean? enableAllAnnotations
    Boolean? forceActive
    Boolean? genotypeFilteredAlleles
    String? gvcfLodBand
    Int? kmerSize
    Int? maxAssemblyRegionSize
    Int? mnpDist
    Int? maxNumHaplotypesInPopulation
    Int? maxProbPropagationDistance
    Int? maxSuspiciousReadsPerAlignmentStart
    Int? maxUnprunedVariants
    Int? minAssemblyRegionSize
    Int? minDanglingBranchLength
    Int? minPruning
    Float? minimumAlleleFraction
    Int? numPruningSamples
    Int? pairHmmGapContinuationPenalty
    String? pairhmm
    String? pcrIndelModel
    Int? phredScaledGlobalReadMismappingRate
    Float? pruningLodThreshold
    Boolean? recoverAllDanglingBranches
    Boolean? showhidden
    String? smithWaterman
    Int? ambigFilterBases
    Float? ambigFilterFrac
    Int? maxFragmentLength
    Int? minFragmentLength
    String? keepIntervals
    String? library
    Int? maximumMappingQuality
    Int? minimumMappingQuality
    Boolean? dontRequireSoftClipsBothEnds
    Int? filterTooShort
    String? platformFilterName
    String? blackListedLanes
    String? readGroupBlackList
    String? keepReadGroup
    Int? maxReadLength
    Int? minReadLength
    String? readName
    Boolean? keepReverseStrandOnly
    String? sample
  }
  command {
    gatk Mutect2 \
      ${sep=" " prefix("-I ", tumorBams)} \
      ${sep=" " prefix("-I ", normalBams)} \
      --normal-sample ${normalSample} \
      --reference ${reference} \
      ${"--activity-profile-out " + activityProfileOut} \
      ${true="-add-output-sam-program-record" false="" addOutputSamProgramRecord} \
      ${true="-add-output-vcf-command-line" false="" addOutputVcfCommandLine} \
      ${"--af-of-alleles-not-in-resource " + afOfAllelesNotInResource} \
      ${"--alleles " + alleles} \
      ${"--annotation " + annotation} \
      ${"--annotation-group " + annotationGroup} \
      ${"--annotations-to-exclude " + annotationsToExclude} \
      ${"--arguments_file " + arguments_file} \
      ${"--assembly-region-out " + assemblyRegionOut} \
      ${"--base-quality-score-threshold " + baseQualityScoreThreshold} \
      ${"--callable-depth " + callableDepth} \
      ${"--cloud-index-prefetch-buffer " + cloudIndexPrefetchBuffer} \
      ${"--cloud-prefetch-buffer " + cloudPrefetchBuffer} \
      ${true="--create-output-bam-index" false="" createOutputBamIndex} \
      ${true="--create-output-bam-md5" false="" createOutputBamMd5} \
      ${true="--create-output-variant-index" false="" createOutputVariantIndex} \
      ${true="--create-output-variant-md5" false="" createOutputVariantMd5} \
      ${true="--disable-bam-index-caching" false="" disableBamIndexCaching} \
      ${true="--disable-read-filter" false="" disableReadFilter} \
      ${true="-disable-sequence-dictionary-validation" false="" disableSequenceDictionaryValidation} \
      ${"--downsampling-stride " + downsamplingStride} \
      ${true="--exclude-intervals" false="" excludeIntervals} \
      ${"--f1r2-max-depth " + f1r2MaxDepth} \
      ${"--f1r2-median-mq " + f1r2MedianMq} \
      ${"--f1r2-min-bq " + f1r2MinBq} \
      ${"--f1r2-tar-gz " + if defined(f1r2TarGz_outputFilename) then f1r2TarGz_outputFilename else "generated-55bf2998-d5cc-11e9-bc6b-f218985ebfa7.tar.gz"} \
      ${"-founder-id " + founderId} \
      ${"--gatk-config-file " + gatkConfigFile} \
      ${"-gcs-retries " + gcsRetries} \
      ${"--gcs-project-for-requester-pays " + gcsProjectForRequesterPays} \
      ${true="--genotype-germline-sites" false="" genotypeGermlineSites} \
      ${true="--genotype-pon-sites" false="" genotypePonSites} \
      ${"--germline-resource " + germlineResource} \
      ${"-graph " + graph} \
      ${true="-h" false="" help} \
      ${"--ignore-itr-artifactsTurn " + ignoreItrArtifacts} \
      ${"--initial-tumor-lod " + initialTumorLod} \
      ${"--interval-exclusion-padding " + intervalExclusionPadding} \
      ${"--interval-merging-rule " + imr} \
      ${"-ipAmount " + ip} \
      ${"--interval-set-rule " + isr} \
      ${"--intervals " + intervals} \
      ${true="-LE" false="" le} \
      ${"--max-population-af " + maxPopulationAf} \
      ${"--max-reads-per-alignment-start " + maxReadsPerAlignmentStart} \
      ${"--min-base-quality-score " + minBaseQualityScore} \
      ${true="--mitochondria-mode" false="" mitochondriaMode} \
      ${"--native-pair-hmm-threads " + if defined(nativePairHmmThreads) then nativePairHmmThreads else if defined(runtime_cpu) then runtime_cpu else 1} \
      ${true="--native-pair-hmm-use-double-precision" false="" nativePairHmmUseDoublePrecision} \
      ${"--normal-lod " + normalLod} \
      ${"-encode " + encode} \
      ${"--panel-of-normals " + panelOfNormals} \
      ${"--pcr-indel-qual " + pcrIndelQual} \
      ${"--pcr-snv-qual " + pcrSnvQual} \
      ${"--pedigree " + pedigree} \
      ${true="--QUIET" false="" quiet} \
      ${"--read-filter " + readFilter} \
      ${"-read-index " + readIndex} \
      ${"--read-validation-stringency " + readValidationStringency} \
      ${"-seconds-between-progress-updates " + secondsBetweenProgressUpdates} \
      ${"-sequence-dictionary " + sequenceDictionary} \
      ${true="--sites-only-vcf-output" false="" sitesOnlyVcfOutput} \
      ${"--tmp-dir " + tmpDir} \
      ${"--tumor-lod-to-emit " + tumorLodToEmit} \
      ${"-tumor " + tumor} \
      ${true="-jdk-deflater" false="" jdkDeflater} \
      ${true="-jdk-inflater" false="" jdkInflater} \
      ${"-verbosity " + verbosity} \
      ${true="--version" false="" version} \
      ${"--active-probability-threshold " + activeProbabilityThreshold} \
      ${"--adaptive-pruning-initial-error-rate " + adaptivePruningInitialErrorRate} \
      ${true="--allow-non-unique-kmers-in-ref" false="" allowNonUniqueKmersInRef} \
      ${"--assembly-region-padding " + assemblyRegionPadding} \
      ${"-bamout " + bamout} \
      ${"--bam-writer-type " + bamWriterType} \
      ${"--debug-assembly " + debugAssembly} \
      ${true="--disable-adaptive-pruning" false="" disableAdaptivePruning} \
      ${true="-disable-tool-default-annotations" false="" disableToolDefaultAnnotations} \
      ${true="-disable-tool-default-read-filters" false="" disableToolDefaultReadFilters} \
      ${true="--dont-increase-kmer-sizes-for-cycles" false="" dontIncreaseKmerSizesForCycles} \
      ${true="--dont-trim-active-regions" false="" dontTrimActiveRegions} \
      ${true="--dont-use-soft-clipped-bases" false="" dontUseSoftClippedBases} \
      ${"-ERC " + erc} \
      ${true="--enable-all-annotations" false="" enableAllAnnotations} \
      ${true="--force-active" false="" forceActive} \
      ${true="--genotype-filtered-alleles" false="" genotypeFilteredAlleles} \
      ${"--gvcf-lod-band " + gvcfLodBand} \
      ${"--kmer-size " + kmerSize} \
      ${"--max-assembly-region-size " + maxAssemblyRegionSize} \
      ${"-mnp-dist " + mnpDist} \
      ${"--max-num-haplotypes-in-population " + maxNumHaplotypesInPopulation} \
      ${"--max-prob-propagation-distance " + maxProbPropagationDistance} \
      ${"--max-suspicious-reads-per-alignment-start " + maxSuspiciousReadsPerAlignmentStart} \
      ${"--max-unpruned-variants " + maxUnprunedVariants} \
      ${"--min-assembly-region-size " + minAssemblyRegionSize} \
      ${"--min-dangling-branch-length " + minDanglingBranchLength} \
      ${"--min-pruning " + minPruning} \
      ${"--minimum-allele-fraction " + minimumAlleleFraction} \
      ${"--num-pruning-samples " + numPruningSamples} \
      ${"--pair-hmm-gap-continuation-penalty " + pairHmmGapContinuationPenalty} \
      ${"-pairHMM " + pairhmm} \
      ${"--pcr-indel-model " + pcrIndelModel} \
      ${"--phred-scaled-global-read-mismapping-rate " + phredScaledGlobalReadMismappingRate} \
      ${"--pruning-lod-thresholdLn " + pruningLodThreshold} \
      ${true="--recover-all-dangling-branches" false="" recoverAllDanglingBranches} \
      ${true="-showHidden" false="" showhidden} \
      ${"--smith-waterman " + smithWaterman} \
      ${"--ambig-filter-bases " + ambigFilterBases} \
      ${"--ambig-filter-frac " + ambigFilterFrac} \
      ${"--max-fragment-length " + maxFragmentLength} \
      ${"--min-fragment-length " + minFragmentLength} \
      ${"--keep-intervals " + keepIntervals} \
      ${"-library " + library} \
      ${"--maximum-mapping-quality " + maximumMappingQuality} \
      ${"--minimum-mapping-quality " + minimumMappingQuality} \
      ${true="--dont-require-soft-clips-both-ends" false="" dontRequireSoftClipsBothEnds} \
      ${"--filter-too-short " + filterTooShort} \
      ${"--platform-filter-name " + platformFilterName} \
      ${"--black-listed-lanes " + blackListedLanes} \
      ${"--read-group-black-listThe " + readGroupBlackList} \
      ${"--keep-read-group " + keepReadGroup} \
      ${"--max-read-length " + maxReadLength} \
      ${"--min-read-length " + minReadLength} \
      ${"--read-name " + readName} \
      ${true="--keep-reverse-strand-only" false="" keepReverseStrandOnly} \
      ${"-sample " + sample} \
      ${"-O " + if defined(outputFilename) then outputFilename else "generated-55bf2484-d5cc-11e9-bc6b-f218985ebfa7.vcf.gz"}
  }
  runtime {
    docker: "broadinstitute/gatk:4.1.3.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-55bed902-d5cc-11e9-bc6b-f218985ebfa7.vcf.gz"
    File out_tbi = if defined(outputFilename) then outputFilename else "generated-55bed902-d5cc-11e9-bc6b-f218985ebfa7.vcf.gz" + ".tbi"
    File stats = "${if defined(outputFilename) then outputFilename else "generated-55bed902-d5cc-11e9-bc6b-f218985ebfa7.vcf.gz"}.stats"
    File f1f2r_out = if defined(f1r2TarGz_outputFilename) then f1r2TarGz_outputFilename else "generated-55beddda-d5cc-11e9-bc6b-f218985ebfa7.tar.gz"
  }
}