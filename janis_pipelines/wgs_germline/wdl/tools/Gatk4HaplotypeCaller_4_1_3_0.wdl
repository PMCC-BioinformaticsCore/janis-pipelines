version development

task Gatk4HaplotypeCaller {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Int? runtime_seconds
    Int? runtime_disks
    Array[String]? javaOptions
    Int? compression_level
    String? pairHmmImplementation
    String? activityProfileOut
    File? alleles
    Boolean? annotateWithNumDiscoveredAlleles
    Array[String]? annotation
    Array[String]? annotationGroup
    Array[String]? annotationsToExclude
    Array[File]? arguments_file
    String? assemblyRegionOut
    Int? baseQualityScoreThreshold
    Int? cloudIndexPrefetchBuffer
    Int? cloudPrefetchBuffer
    Float? contaminationFractionToFilter
    Boolean? correctOverlappingQuality
    Boolean? disableBamIndexCaching
    Array[String]? founderId
    String? genotypingMode
    Float? heterozygosity
    Float? heterozygosityStdev
    Float? indelHeterozygosity
    String? intervalMergingRule
    Int? maxReadsPerAlignmentStart
    Int? minBaseQualityScore
    Int? nativePairHmmThreads
    Boolean? nativePairHmmUseDoublePrecision
    Int? numReferenceSamplesIfNoCall
    String? outputMode
    File? pedigree
    File? populationCallset
    String? sampleName
    Int? samplePloidy
    Boolean? sitesOnlyVcfOutput
    Float? standardMinConfidenceThresholdForCalling
    Boolean? useNewQualCalculator
    Array[Int]? gvcfGqBands
    String? emitRefConfidence
    File inputRead
    File inputRead_bai
    File reference
    File reference_fai
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_dict
    String? outputFilename
    File? dbsnp
    File? dbsnp_tbi
    File? intervals
    String? outputBamName
  }
  command <<<
    cp -f ~{inputRead_bai} $(echo '~{inputRead}' | sed 's/\.[^.]*$//').bai
    gatk HaplotypeCaller \
      --java-options '-Xmx~{((select_first([runtime_memory, 8, 4]) * 3) / 4)}G ~{if (defined(compression_level)) then ("-Dsamjdk.compress_level=" + compression_level) else ""} ~{sep(" ", select_first([javaOptions, []]))}' \
      ~{if defined(pairHmmImplementation) then ("--pair-hmm-implementation '" + pairHmmImplementation + "'") else ""} \
      ~{if defined(activityProfileOut) then ("--activity-profile-out '" + activityProfileOut + "'") else ""} \
      ~{if defined(alleles) then ("--alleles '" + alleles + "'") else ""} \
      ~{if defined(annotateWithNumDiscoveredAlleles) then "--annotate-with-num-discovered-alleles" else ""} \
      ~{if (defined(annotation) && length(select_first([annotation])) > 0) then "--annotation '" + sep("' '", select_first([annotation])) + "'" else ""} \
      ~{if (defined(annotationGroup) && length(select_first([annotationGroup])) > 0) then "--annotation-group '" + sep("' '", select_first([annotationGroup])) + "'" else ""} \
      ~{if (defined(annotationsToExclude) && length(select_first([annotationsToExclude])) > 0) then "--annotations-to-exclude '" + sep("' '", select_first([annotationsToExclude])) + "'" else ""} \
      ~{if (defined(arguments_file) && length(select_first([arguments_file])) > 0) then "--arguments_file '" + sep("' '", select_first([arguments_file])) + "'" else ""} \
      ~{if defined(assemblyRegionOut) then ("--assembly-region-out '" + assemblyRegionOut + "'") else ""} \
      ~{if defined(baseQualityScoreThreshold) then ("--base-quality-score-threshold " + baseQualityScoreThreshold) else ''} \
      ~{if defined(cloudIndexPrefetchBuffer) then ("--cloud-index-prefetch-buffer " + cloudIndexPrefetchBuffer) else ''} \
      ~{if defined(cloudPrefetchBuffer) then ("--cloud-prefetch-buffer " + cloudPrefetchBuffer) else ''} \
      ~{if defined(contaminationFractionToFilter) then ("--contamination-fraction-to-filter " + contaminationFractionToFilter) else ''} \
      ~{if defined(correctOverlappingQuality) then "--correct-overlapping-quality" else ""} \
      ~{if defined(disableBamIndexCaching) then "--disable-bam-index-caching" else ""} \
      ~{if (defined(founderId) && length(select_first([founderId])) > 0) then "--founder-id '" + sep("' '", select_first([founderId])) + "'" else ""} \
      ~{if defined(genotypingMode) then ("--genotyping-mode '" + genotypingMode + "'") else ""} \
      ~{if defined(heterozygosity) then ("--heterozygosity " + heterozygosity) else ''} \
      ~{if defined(heterozygosityStdev) then ("--heterozygosity-stdev " + heterozygosityStdev) else ''} \
      ~{if defined(indelHeterozygosity) then ("--indel-heterozygosity " + indelHeterozygosity) else ''} \
      ~{if defined(intervalMergingRule) then ("--interval-merging-rule '" + intervalMergingRule + "'") else ""} \
      ~{if defined(maxReadsPerAlignmentStart) then ("--max-reads-per-alignment-start " + maxReadsPerAlignmentStart) else ''} \
      ~{if defined(minBaseQualityScore) then ("--min-base-quality-score " + minBaseQualityScore) else ''} \
      ~{if defined(nativePairHmmThreads) then ("--native-pair-hmm-threads " + nativePairHmmThreads) else ''} \
      ~{if defined(nativePairHmmUseDoublePrecision) then "--native-pair-hmm-use-double-precision" else ""} \
      ~{if defined(numReferenceSamplesIfNoCall) then ("--num-reference-samples-if-no-call " + numReferenceSamplesIfNoCall) else ''} \
      ~{if defined(outputMode) then ("--output-mode '" + outputMode + "'") else ""} \
      ~{if defined(pedigree) then ("--pedigree '" + pedigree + "'") else ""} \
      ~{if defined(populationCallset) then ("--population-callset '" + populationCallset + "'") else ""} \
      ~{if defined(sampleName) then ("--sample-name '" + sampleName + "'") else ""} \
      ~{if defined(samplePloidy) then ("--sample-ploidy " + samplePloidy) else ''} \
      ~{if defined(sitesOnlyVcfOutput) then "--sites-only-vcf-output" else ""} \
      ~{if defined(standardMinConfidenceThresholdForCalling) then ("--standard-min-confidence-threshold-for-calling " + standardMinConfidenceThresholdForCalling) else ''} \
      ~{if defined(useNewQualCalculator) then "--use-new-qual-calculator" else ""} \
      ~{if (defined(gvcfGqBands) && length(select_first([gvcfGqBands])) > 0) then sep(" ", prefix("-GQB ", select_first([gvcfGqBands]))) else ""} \
      ~{if defined(emitRefConfidence) then ("--emit-ref-confidence '" + emitRefConfidence + "'") else ""} \
      --input '~{inputRead}' \
      ~{if defined(intervals) then ("--intervals '" + intervals + "'") else ""} \
      --reference '~{reference}' \
      ~{if defined(dbsnp) then ("--dbsnp '" + dbsnp + "'") else ""} \
      --output '~{select_first([outputFilename, "~{basename(inputRead, ".bam")}.vcf.gz"])}' \
      -bamout '~{select_first([outputBamName, "~{basename(inputRead, ".bam")}.bam"])}'
    if [ -f $(echo '~{select_first([outputBamName, "~{basename(inputRead, ".bam")}.bam"])}' | sed 's/\.[^.]*$//').bai ]; then ln -f $(echo '~{select_first([outputBamName, "~{basename(inputRead, ".bam")}.bam"])}' | sed 's/\.[^.]*$//').bai $(echo '~{select_first([outputBamName, "~{basename(inputRead, ".bam")}.bam"])}' ).bai; fi
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1, 1])
    disks: "local-disk ~{select_first([runtime_disks, 20])} SSD"
    docker: "broadinstitute/gatk:4.1.3.0"
    duration: select_first([runtime_seconds, 86400])
    memory: "~{select_first([runtime_memory, 8, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "~{basename(inputRead, ".bam")}.vcf.gz"])
    File out_tbi = select_first([outputFilename, "~{basename(inputRead, ".bam")}.vcf.gz"]) + ".tbi"
    File bam = select_first([outputBamName, "~{basename(inputRead, ".bam")}.bam"])
    File bam_bai = select_first([outputBamName, "~{basename(inputRead, ".bam")}.bam"]) + ".bai"
  }
}