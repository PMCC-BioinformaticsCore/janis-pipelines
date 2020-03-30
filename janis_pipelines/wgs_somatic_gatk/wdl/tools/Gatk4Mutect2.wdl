version development

task Gatk4Mutect2 {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Array[File] tumorBams
    Array[File] tumorBams_bai
    Array[File] normalBams
    Array[File] normalBams_bai
    String normalSample
    String? outputFilename = "generated.vcf.gz"
    File reference
    File reference_fai
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
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
    String? f1r2TarGz_outputFilename = "generated.tar.gz"
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
    File? intervals
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
  command <<<
    gatk Mutect2 \
      ~{sep=" " prefix("-I ", tumorBams)} \
      ~{sep=" " prefix("-I ", normalBams)} \
      --normal-sample ~{normalSample} \
      --reference ~{reference} \
      ~{if defined(activityProfileOut) then ("--activity-profile-out " +  '"' + activityProfileOut + '"') else ""} \
      ~{true="-add-output-sam-program-record" false="" addOutputSamProgramRecord} \
      ~{true="-add-output-vcf-command-line" false="" addOutputVcfCommandLine} \
      ~{if defined(afOfAllelesNotInResource) then ("--af-of-alleles-not-in-resource " +  '"' + afOfAllelesNotInResource + '"') else ""} \
      ~{if defined(alleles) then ("--alleles " +  '"' + alleles + '"') else ""} \
      ~{if defined(annotation) then ("--annotation " +  '"' + annotation + '"') else ""} \
      ~{if defined(annotationGroup) then ("--annotation-group " +  '"' + annotationGroup + '"') else ""} \
      ~{if defined(annotationsToExclude) then ("--annotations-to-exclude " +  '"' + annotationsToExclude + '"') else ""} \
      ~{if defined(arguments_file) then ("--arguments_file " +  '"' + arguments_file + '"') else ""} \
      ~{if defined(assemblyRegionOut) then ("--assembly-region-out " +  '"' + assemblyRegionOut + '"') else ""} \
      ~{if defined(baseQualityScoreThreshold) then ("--base-quality-score-threshold " +  '"' + baseQualityScoreThreshold + '"') else ""} \
      ~{if defined(callableDepth) then ("--callable-depth " +  '"' + callableDepth + '"') else ""} \
      ~{if defined(cloudIndexPrefetchBuffer) then ("--cloud-index-prefetch-buffer " +  '"' + cloudIndexPrefetchBuffer + '"') else ""} \
      ~{if defined(cloudPrefetchBuffer) then ("--cloud-prefetch-buffer " +  '"' + cloudPrefetchBuffer + '"') else ""} \
      ~{true="--create-output-bam-index" false="" createOutputBamIndex} \
      ~{true="--create-output-bam-md5" false="" createOutputBamMd5} \
      ~{true="--create-output-variant-index" false="" createOutputVariantIndex} \
      ~{true="--create-output-variant-md5" false="" createOutputVariantMd5} \
      ~{true="--disable-bam-index-caching" false="" disableBamIndexCaching} \
      ~{true="--disable-read-filter" false="" disableReadFilter} \
      ~{true="-disable-sequence-dictionary-validation" false="" disableSequenceDictionaryValidation} \
      ~{if defined(downsamplingStride) then ("--downsampling-stride " +  '"' + downsamplingStride + '"') else ""} \
      ~{true="--exclude-intervals" false="" excludeIntervals} \
      ~{if defined(f1r2MaxDepth) then ("--f1r2-max-depth " +  '"' + f1r2MaxDepth + '"') else ""} \
      ~{if defined(f1r2MedianMq) then ("--f1r2-median-mq " +  '"' + f1r2MedianMq + '"') else ""} \
      ~{if defined(f1r2MinBq) then ("--f1r2-min-bq " +  '"' + f1r2MinBq + '"') else ""} \
      ~{if defined(select_first([f1r2TarGz_outputFilename, "generated.tar.gz"])) then ("--f1r2-tar-gz " +  '"' + select_first([f1r2TarGz_outputFilename, "generated.tar.gz"]) + '"') else ""} \
      ~{if defined(founderId) then ("-founder-id " +  '"' + founderId + '"') else ""} \
      ~{if defined(gatkConfigFile) then ("--gatk-config-file " +  '"' + gatkConfigFile + '"') else ""} \
      ~{if defined(gcsRetries) then ("-gcs-retries " +  '"' + gcsRetries + '"') else ""} \
      ~{if defined(gcsProjectForRequesterPays) then ("--gcs-project-for-requester-pays " +  '"' + gcsProjectForRequesterPays + '"') else ""} \
      ~{true="--genotype-germline-sites" false="" genotypeGermlineSites} \
      ~{true="--genotype-pon-sites" false="" genotypePonSites} \
      ~{if defined(germlineResource) then ("--germline-resource " +  '"' + germlineResource + '"') else ""} \
      ~{if defined(graph) then ("-graph " +  '"' + graph + '"') else ""} \
      ~{true="-h" false="" help} \
      ~{if defined(ignoreItrArtifacts) then ("--ignore-itr-artifactsTurn " +  '"' + ignoreItrArtifacts + '"') else ""} \
      ~{if defined(initialTumorLod) then ("--initial-tumor-lod " +  '"' + initialTumorLod + '"') else ""} \
      ~{if defined(intervalExclusionPadding) then ("--interval-exclusion-padding " +  '"' + intervalExclusionPadding + '"') else ""} \
      ~{if defined(imr) then ("--interval-merging-rule " +  '"' + imr + '"') else ""} \
      ~{if defined(ip) then ("-ipAmount " +  '"' + ip + '"') else ""} \
      ~{if defined(isr) then ("--interval-set-rule " +  '"' + isr + '"') else ""} \
      ~{if defined(intervals) then ("--intervals " +  '"' + intervals + '"') else ""} \
      ~{true="-LE" false="" le} \
      ~{if defined(maxPopulationAf) then ("--max-population-af " +  '"' + maxPopulationAf + '"') else ""} \
      ~{if defined(maxReadsPerAlignmentStart) then ("--max-reads-per-alignment-start " +  '"' + maxReadsPerAlignmentStart + '"') else ""} \
      ~{if defined(minBaseQualityScore) then ("--min-base-quality-score " +  '"' + minBaseQualityScore + '"') else ""} \
      ~{true="--mitochondria-mode" false="" mitochondriaMode} \
      ~{if defined(select_first([nativePairHmmThreads, select_first([runtime_cpu, 1])])) then ("--native-pair-hmm-threads " +  '"' + select_first([nativePairHmmThreads, select_first([runtime_cpu, 1])]) + '"') else ""} \
      ~{true="--native-pair-hmm-use-double-precision" false="" nativePairHmmUseDoublePrecision} \
      ~{if defined(normalLod) then ("--normal-lod " +  '"' + normalLod + '"') else ""} \
      ~{if defined(encode) then ("-encode " +  '"' + encode + '"') else ""} \
      ~{if defined(panelOfNormals) then ("--panel-of-normals " +  '"' + panelOfNormals + '"') else ""} \
      ~{if defined(pcrIndelQual) then ("--pcr-indel-qual " +  '"' + pcrIndelQual + '"') else ""} \
      ~{if defined(pcrSnvQual) then ("--pcr-snv-qual " +  '"' + pcrSnvQual + '"') else ""} \
      ~{if defined(pedigree) then ("--pedigree " +  '"' + pedigree + '"') else ""} \
      ~{true="--QUIET" false="" quiet} \
      ~{if defined(readFilter) then ("--read-filter " +  '"' + readFilter + '"') else ""} \
      ~{if defined(readIndex) then ("-read-index " +  '"' + readIndex + '"') else ""} \
      ~{if defined(readValidationStringency) then ("--read-validation-stringency " +  '"' + readValidationStringency + '"') else ""} \
      ~{if defined(secondsBetweenProgressUpdates) then ("-seconds-between-progress-updates " +  '"' + secondsBetweenProgressUpdates + '"') else ""} \
      ~{if defined(sequenceDictionary) then ("-sequence-dictionary " +  '"' + sequenceDictionary + '"') else ""} \
      ~{true="--sites-only-vcf-output" false="" sitesOnlyVcfOutput} \
      ~{if defined(tmpDir) then ("--tmp-dir " +  '"' + tmpDir + '"') else ""} \
      ~{if defined(tumorLodToEmit) then ("--tumor-lod-to-emit " +  '"' + tumorLodToEmit + '"') else ""} \
      ~{if defined(tumor) then ("-tumor " +  '"' + tumor + '"') else ""} \
      ~{true="-jdk-deflater" false="" jdkDeflater} \
      ~{true="-jdk-inflater" false="" jdkInflater} \
      ~{if defined(verbosity) then ("-verbosity " +  '"' + verbosity + '"') else ""} \
      ~{true="--version" false="" version} \
      ~{if defined(activeProbabilityThreshold) then ("--active-probability-threshold " +  '"' + activeProbabilityThreshold + '"') else ""} \
      ~{if defined(adaptivePruningInitialErrorRate) then ("--adaptive-pruning-initial-error-rate " +  '"' + adaptivePruningInitialErrorRate + '"') else ""} \
      ~{true="--allow-non-unique-kmers-in-ref" false="" allowNonUniqueKmersInRef} \
      ~{if defined(assemblyRegionPadding) then ("--assembly-region-padding " +  '"' + assemblyRegionPadding + '"') else ""} \
      ~{if defined(bamout) then ("-bamout " +  '"' + bamout + '"') else ""} \
      ~{if defined(bamWriterType) then ("--bam-writer-type " +  '"' + bamWriterType + '"') else ""} \
      ~{if defined(debugAssembly) then ("--debug-assembly " +  '"' + debugAssembly + '"') else ""} \
      ~{true="--disable-adaptive-pruning" false="" disableAdaptivePruning} \
      ~{true="-disable-tool-default-annotations" false="" disableToolDefaultAnnotations} \
      ~{true="-disable-tool-default-read-filters" false="" disableToolDefaultReadFilters} \
      ~{true="--dont-increase-kmer-sizes-for-cycles" false="" dontIncreaseKmerSizesForCycles} \
      ~{true="--dont-trim-active-regions" false="" dontTrimActiveRegions} \
      ~{true="--dont-use-soft-clipped-bases" false="" dontUseSoftClippedBases} \
      ~{if defined(erc) then ("-ERC " +  '"' + erc + '"') else ""} \
      ~{true="--enable-all-annotations" false="" enableAllAnnotations} \
      ~{true="--force-active" false="" forceActive} \
      ~{true="--genotype-filtered-alleles" false="" genotypeFilteredAlleles} \
      ~{if defined(gvcfLodBand) then ("--gvcf-lod-band " +  '"' + gvcfLodBand + '"') else ""} \
      ~{if defined(kmerSize) then ("--kmer-size " +  '"' + kmerSize + '"') else ""} \
      ~{if defined(maxAssemblyRegionSize) then ("--max-assembly-region-size " +  '"' + maxAssemblyRegionSize + '"') else ""} \
      ~{if defined(mnpDist) then ("-mnp-dist " +  '"' + mnpDist + '"') else ""} \
      ~{if defined(maxNumHaplotypesInPopulation) then ("--max-num-haplotypes-in-population " +  '"' + maxNumHaplotypesInPopulation + '"') else ""} \
      ~{if defined(maxProbPropagationDistance) then ("--max-prob-propagation-distance " +  '"' + maxProbPropagationDistance + '"') else ""} \
      ~{if defined(maxSuspiciousReadsPerAlignmentStart) then ("--max-suspicious-reads-per-alignment-start " +  '"' + maxSuspiciousReadsPerAlignmentStart + '"') else ""} \
      ~{if defined(maxUnprunedVariants) then ("--max-unpruned-variants " +  '"' + maxUnprunedVariants + '"') else ""} \
      ~{if defined(minAssemblyRegionSize) then ("--min-assembly-region-size " +  '"' + minAssemblyRegionSize + '"') else ""} \
      ~{if defined(minDanglingBranchLength) then ("--min-dangling-branch-length " +  '"' + minDanglingBranchLength + '"') else ""} \
      ~{if defined(minPruning) then ("--min-pruning " +  '"' + minPruning + '"') else ""} \
      ~{if defined(minimumAlleleFraction) then ("--minimum-allele-fraction " +  '"' + minimumAlleleFraction + '"') else ""} \
      ~{if defined(numPruningSamples) then ("--num-pruning-samples " +  '"' + numPruningSamples + '"') else ""} \
      ~{if defined(pairHmmGapContinuationPenalty) then ("--pair-hmm-gap-continuation-penalty " +  '"' + pairHmmGapContinuationPenalty + '"') else ""} \
      ~{if defined(pairhmm) then ("-pairHMM " +  '"' + pairhmm + '"') else ""} \
      ~{if defined(pcrIndelModel) then ("--pcr-indel-model " +  '"' + pcrIndelModel + '"') else ""} \
      ~{if defined(phredScaledGlobalReadMismappingRate) then ("--phred-scaled-global-read-mismapping-rate " +  '"' + phredScaledGlobalReadMismappingRate + '"') else ""} \
      ~{if defined(pruningLodThreshold) then ("--pruning-lod-thresholdLn " +  '"' + pruningLodThreshold + '"') else ""} \
      ~{true="--recover-all-dangling-branches" false="" recoverAllDanglingBranches} \
      ~{true="-showHidden" false="" showhidden} \
      ~{if defined(smithWaterman) then ("--smith-waterman " +  '"' + smithWaterman + '"') else ""} \
      ~{if defined(ambigFilterBases) then ("--ambig-filter-bases " +  '"' + ambigFilterBases + '"') else ""} \
      ~{if defined(ambigFilterFrac) then ("--ambig-filter-frac " +  '"' + ambigFilterFrac + '"') else ""} \
      ~{if defined(maxFragmentLength) then ("--max-fragment-length " +  '"' + maxFragmentLength + '"') else ""} \
      ~{if defined(minFragmentLength) then ("--min-fragment-length " +  '"' + minFragmentLength + '"') else ""} \
      ~{if defined(keepIntervals) then ("--keep-intervals " +  '"' + keepIntervals + '"') else ""} \
      ~{if defined(library) then ("-library " +  '"' + library + '"') else ""} \
      ~{if defined(maximumMappingQuality) then ("--maximum-mapping-quality " +  '"' + maximumMappingQuality + '"') else ""} \
      ~{if defined(minimumMappingQuality) then ("--minimum-mapping-quality " +  '"' + minimumMappingQuality + '"') else ""} \
      ~{true="--dont-require-soft-clips-both-ends" false="" dontRequireSoftClipsBothEnds} \
      ~{if defined(filterTooShort) then ("--filter-too-short " +  '"' + filterTooShort + '"') else ""} \
      ~{if defined(platformFilterName) then ("--platform-filter-name " +  '"' + platformFilterName + '"') else ""} \
      ~{if defined(blackListedLanes) then ("--black-listed-lanes " +  '"' + blackListedLanes + '"') else ""} \
      ~{if defined(readGroupBlackList) then ("--read-group-black-listThe " +  '"' + readGroupBlackList + '"') else ""} \
      ~{if defined(keepReadGroup) then ("--keep-read-group " +  '"' + keepReadGroup + '"') else ""} \
      ~{if defined(maxReadLength) then ("--max-read-length " +  '"' + maxReadLength + '"') else ""} \
      ~{if defined(minReadLength) then ("--min-read-length " +  '"' + minReadLength + '"') else ""} \
      ~{if defined(readName) then ("--read-name " +  '"' + readName + '"') else ""} \
      ~{true="--keep-reverse-strand-only" false="" keepReverseStrandOnly} \
      ~{if defined(sample) then ("-sample " +  '"' + sample + '"') else ""} \
      ~{if defined(select_first([outputFilename, "generated.vcf.gz"])) then ("-O " +  '"' + select_first([outputFilename, "generated.vcf.gz"]) + '"') else ""}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    docker: "broadinstitute/gatk:4.1.3.0"
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated.vcf.gz"])
    File out_tbi = (select_first([outputFilename, "generated.vcf.gz"])) + ".tbi"
    File stats = "~{select_first([outputFilename, "generated.vcf.gz"])}.stats"
    File f1f2r_out = select_first([f1r2TarGz_outputFilename, "generated.tar.gz"])
  }
}