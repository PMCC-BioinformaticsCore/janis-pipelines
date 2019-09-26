version development

task gatk4splitreads {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    String? outputFilename
    File bam
    File bam_bai
    File? intervals
    Boolean? addOutputSamProgramRecord
    Boolean? addOutputVcfCommandLine
    File? arguments_file
    String? cloudIndexPrefetchBuffer
    String? cloudPrefetchBuffer
    String? createOutputBamIndex
    String? createOutputBamMd5
    String? createOutputVariantIndex
    String? createOutputVariantMd5
    String? disableBamIndexCaching
    String? disableReadFilter
    Boolean? disableSequenceDictionaryValidation
    String? excludeIntervals
    File? gatkConfigFile
    Int? gcsRetries
    String? gcsProjectForRequesterPays
    Int? intervalExclusionPadding
    String? imr
    Int? ip
    String? isr
    Boolean? le
    Boolean? quiet
    String? readFilter
    String? readIndex
    String? readValidationStringency
    File? reference
    File? reference_amb
    File? reference_ann
    File? reference_bwt
    File? reference_pac
    File? reference_sa
    File? reference_fai
    File? reference_dict
    Float? secondsBetweenProgressUpdates
    String? sequenceDictionary
    Boolean? sitesOnlyVcfOutput
    String? splitLibraryName
    String? rg
    String? splitSample
    String? tmpDir
    Boolean? jdkDeflater
    Boolean? jdkInflater
    String? verbosity
    Boolean? disableToolDefaultReadFilters
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
    Boolean? invertSoftClipRatioFilter
    Float? softClippedLeadingTrailingRatio
    Float? softClippedRatioThreshold
  }
  command {
    if [ $(dirname "${bam_bai}") != $(dirname "bam") ]; then mv ${bam_bai} $(dirname ${bam}); fi
    if [ $(dirname "${reference_amb}") != $(dirname "reference") ]; then mv ${reference_amb} $(dirname ${reference}); fi
    if [ $(dirname "${reference_ann}") != $(dirname "reference") ]; then mv ${reference_ann} $(dirname ${reference}); fi
    if [ $(dirname "${reference_bwt}") != $(dirname "reference") ]; then mv ${reference_bwt} $(dirname ${reference}); fi
    if [ $(dirname "${reference_pac}") != $(dirname "reference") ]; then mv ${reference_pac} $(dirname ${reference}); fi
    if [ $(dirname "${reference_sa}") != $(dirname "reference") ]; then mv ${reference_sa} $(dirname ${reference}); fi
    if [ $(dirname "${reference_fai}") != $(dirname "reference") ]; then mv ${reference_fai} $(dirname ${reference}); fi
    if [ $(dirname "${reference_dict}") != $(dirname "reference") ]; then mv ${reference_dict} $(dirname ${reference}); fi
    gatk SplitReads \
      --output ${if defined(outputFilename) then outputFilename else "."} \
      ${"--intervals " + intervals} \
      ${true="-add-output-sam-program-record" false="" addOutputSamProgramRecord} \
      ${true="-add-output-vcf-command-line" false="" addOutputVcfCommandLine} \
      ${"--arguments_file:File " + arguments_file} \
      ${"--cloud-index-prefetch-buffer " + cloudIndexPrefetchBuffer} \
      ${"--cloud-prefetch-buffer " + cloudPrefetchBuffer} \
      ${"--create-output-bam-index " + createOutputBamIndex} \
      ${"--create-output-bam-md5 " + createOutputBamMd5} \
      ${"--create-output-variant-index " + createOutputVariantIndex} \
      ${"--create-output-variant-md5 " + createOutputVariantMd5} \
      ${"--disable-bam-index-caching " + disableBamIndexCaching} \
      ${"--disable-read-filter " + disableReadFilter} \
      ${true="-disable-sequence-dictionary-validation" false="" disableSequenceDictionaryValidation} \
      ${"--exclude-intervals " + excludeIntervals} \
      ${"--gatk-config-file " + gatkConfigFile} \
      ${"-gcs-retries " + gcsRetries} \
      ${"--gcs-project-for-requester-pays " + gcsProjectForRequesterPays} \
      ${"--interval-exclusion-padding " + intervalExclusionPadding} \
      ${"-imr:IntervalMergingRule " + imr} \
      ${"-ip " + ip} \
      ${"-isr:IntervalSetRule " + isr} \
      ${true="--lenient" false="" le} \
      ${true="--QUIET" false="" quiet} \
      ${"--read-filter " + readFilter} \
      ${"-read-index " + readIndex} \
      ${"--read-validation-stringency " + readValidationStringency} \
      ${"--reference " + reference} \
      ${"-seconds-between-progress-updates " + secondsBetweenProgressUpdates} \
      ${"-sequence-dictionary " + sequenceDictionary} \
      ${true="--sites-only-vcf-output:Boolean" false="" sitesOnlyVcfOutput} \
      ${"--split-library-name " + splitLibraryName} \
      ${"--split-read-group " + rg} \
      ${"--split-sample " + splitSample} \
      ${"--tmp-dir:GATKPathSpecifier " + tmpDir} \
      ${true="-jdk-deflater" false="" jdkDeflater} \
      ${true="-jdk-inflater" false="" jdkInflater} \
      ${"-verbosity:LogLevel " + verbosity} \
      ${true="-disable-tool-default-read-filters" false="" disableToolDefaultReadFilters} \
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
      ${"--platform-filter-name:String " + platformFilterName} \
      ${"--black-listed-lanes:String " + blackListedLanes} \
      ${"--read-group-black-list:StringThe " + readGroupBlackList} \
      ${"--keep-read-group:String " + keepReadGroup} \
      ${"--max-read-length " + maxReadLength} \
      ${"--min-read-length " + minReadLength} \
      ${"--read-name:String " + readName} \
      ${true="--keep-reverse-strand-only" false="" keepReverseStrandOnly} \
      ${"-sample:String " + sample} \
      ${true="--invert-soft-clip-ratio-filter" false="" invertSoftClipRatioFilter} \
      ${"--soft-clipped-leading-trailing-ratio " + softClippedLeadingTrailingRatio} \
      ${"--soft-clipped-ratio-threshold " + softClippedRatioThreshold} \
      --input ${bam}
  }
  runtime {
    docker: "broadinstitute/gatk:4.1.3.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = basename(bam)
    File out_bai = basename(basename(bam), ".bam") + ".bai"
  }
}