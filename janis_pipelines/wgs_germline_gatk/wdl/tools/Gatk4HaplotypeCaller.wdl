version development

task Gatk4HaplotypeCaller {
  input {
    Int? runtime_cpu
    Int? runtime_memory
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
    File inputRead
    File inputRead_bai
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    String? outputFilename = "generated.vcf.gz"
    File dbsnp
    File dbsnp_tbi
    File? intervals
  }
  command <<<
    ln -f ~{inputRead_bai} `echo '~{inputRead}' | sed 's/\.[^.]*$//'`.bai
    gatk HaplotypeCaller \
      ~{if defined(activityProfileOut) then ("--activity-profile-out " +  '"' + activityProfileOut + '"') else ""} \
      ~{if defined(alleles) then ("--alleles " +  '"' + alleles + '"') else ""} \
      ~{true="--annotate-with-num-discovered-alleles" false="" annotateWithNumDiscoveredAlleles} \
      ~{true="--annotation " false="" defined(annotation)}~{sep=" " annotation} \
      ~{true="--annotation-group " false="" defined(annotationGroup)}~{sep=" " annotationGroup} \
      ~{true="--annotations-to-exclude " false="" defined(annotationsToExclude)}~{sep=" " annotationsToExclude} \
      ~{true="--arguments_file " false="" defined(arguments_file)}~{sep=" " arguments_file} \
      ~{if defined(assemblyRegionOut) then ("--assembly-region-out " +  '"' + assemblyRegionOut + '"') else ""} \
      ~{if defined(baseQualityScoreThreshold) then ("--base-quality-score-threshold " +  '"' + baseQualityScoreThreshold + '"') else ""} \
      ~{if defined(cloudIndexPrefetchBuffer) then ("--cloud-index-prefetch-buffer " +  '"' + cloudIndexPrefetchBuffer + '"') else ""} \
      ~{if defined(cloudPrefetchBuffer) then ("--cloud-prefetch-buffer " +  '"' + cloudPrefetchBuffer + '"') else ""} \
      ~{if defined(contaminationFractionToFilter) then ("--contamination-fraction-to-filter " +  '"' + contaminationFractionToFilter + '"') else ""} \
      ~{true="--correct-overlapping-quality" false="" correctOverlappingQuality} \
      ~{true="--disable-bam-index-caching" false="" disableBamIndexCaching} \
      ~{true="--founder-id " false="" defined(founderId)}~{sep=" " founderId} \
      ~{if defined(genotypingMode) then ("--genotyping-mode " +  '"' + genotypingMode + '"') else ""} \
      ~{if defined(heterozygosity) then ("--heterozygosity " +  '"' + heterozygosity + '"') else ""} \
      ~{if defined(heterozygosityStdev) then ("--heterozygosity-stdev " +  '"' + heterozygosityStdev + '"') else ""} \
      ~{if defined(indelHeterozygosity) then ("--indel-heterozygosity " +  '"' + indelHeterozygosity + '"') else ""} \
      ~{if defined(intervalMergingRule) then ("--interval-merging-rule " +  '"' + intervalMergingRule + '"') else ""} \
      ~{if defined(maxReadsPerAlignmentStart) then ("--max-reads-per-alignment-start " +  '"' + maxReadsPerAlignmentStart + '"') else ""} \
      ~{if defined(minBaseQualityScore) then ("--min-base-quality-score " +  '"' + minBaseQualityScore + '"') else ""} \
      ~{if defined(nativePairHmmThreads) then ("--native-pair-hmm-threads " +  '"' + nativePairHmmThreads + '"') else ""} \
      ~{true="--native-pair-hmm-use-double-precision" false="" nativePairHmmUseDoublePrecision} \
      ~{if defined(numReferenceSamplesIfNoCall) then ("--num-reference-samples-if-no-call " +  '"' + numReferenceSamplesIfNoCall + '"') else ""} \
      ~{if defined(outputMode) then ("--output-mode " +  '"' + outputMode + '"') else ""} \
      ~{if defined(pedigree) then ("--pedigree " +  '"' + pedigree + '"') else ""} \
      ~{if defined(populationCallset) then ("--population-callset " +  '"' + populationCallset + '"') else ""} \
      ~{if defined(sampleName) then ("--sample-name " +  '"' + sampleName + '"') else ""} \
      ~{if defined(samplePloidy) then ("--sample-ploidy " +  '"' + samplePloidy + '"') else ""} \
      ~{true="--sites-only-vcf-output" false="" sitesOnlyVcfOutput} \
      ~{if defined(standardMinConfidenceThresholdForCalling) then ("--standard-min-confidence-threshold-for-calling " +  '"' + standardMinConfidenceThresholdForCalling + '"') else ""} \
      ~{true="--use-new-qual-calculator" false="" useNewQualCalculator} \
      --input ~{inputRead} \
      ~{if defined(intervals) then ("--intervals " +  '"' + intervals + '"') else ""} \
      --reference ~{reference} \
      --dbsnp ~{dbsnp} \
      ~{if defined(select_first([outputFilename, "generated.vcf.gz"])) then ("--output " +  '"' + select_first([outputFilename, "generated.vcf.gz"]) + '"') else ""}
  >>>
  runtime {
    docker: "broadinstitute/gatk:4.1.3.0"
    cpu: select_first([runtime_cpu, 1])
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated.vcf.gz"])
  }
}