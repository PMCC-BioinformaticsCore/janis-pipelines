version development

task GatkHaplotypeCaller {
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
    String outputFilename = "generated-6815bd5e-cf83-11e9-b4cb-acde48001122.vcf"
    File dbsnp
    File dbsnp_tbi
    File? intervals
  }
  command {
    gatk HaplotypeCaller \
      ${"--activity-profile-out " + activityProfileOut} \
      ${"--alleles " + alleles} \
      ${true="--annotate-with-num-discovered-alleles" false="" annotateWithNumDiscoveredAlleles} \
      ${if defined(annotation) then "--annotation " else ""}${sep=" --annotation " annotation} \
      ${if defined(annotationGroup) then "--annotation-group " else ""}${sep=" --annotation-group " annotationGroup} \
      ${if defined(annotationsToExclude) then "--annotations-to-exclude " else ""}${sep=" --annotations-to-exclude " annotationsToExclude} \
      ${if defined(arguments_file) then "--arguments_file " else ""}${sep=" --arguments_file " arguments_file} \
      ${"--assembly-region-out " + assemblyRegionOut} \
      ${"--base-quality-score-threshold " + baseQualityScoreThreshold} \
      ${"--cloud-index-prefetch-buffer " + cloudIndexPrefetchBuffer} \
      ${"--cloud-prefetch-buffer " + cloudPrefetchBuffer} \
      ${"--contamination-fraction-to-filter " + contaminationFractionToFilter} \
      ${true="--correct-overlapping-quality" false="" correctOverlappingQuality} \
      ${true="--disable-bam-index-caching" false="" disableBamIndexCaching} \
      ${if defined(founderId) then "--founder-id " else ""}${sep=" --founder-id " founderId} \
      ${"--genotyping-mode " + genotypingMode} \
      ${"--heterozygosity " + heterozygosity} \
      ${"--heterozygosity-stdev " + heterozygosityStdev} \
      ${"--indel-heterozygosity " + indelHeterozygosity} \
      ${"--interval-merging-rule " + intervalMergingRule} \
      ${"--max-reads-per-alignment-start " + maxReadsPerAlignmentStart} \
      ${"--min-base-quality-score " + minBaseQualityScore} \
      ${"--native-pair-hmm-threads " + nativePairHmmThreads} \
      ${true="--native-pair-hmm-use-double-precision" false="" nativePairHmmUseDoublePrecision} \
      ${"--num-reference-samples-if-no-call " + numReferenceSamplesIfNoCall} \
      ${"--output-mode " + outputMode} \
      ${"--pedigree " + pedigree} \
      ${"--population-callset " + populationCallset} \
      ${"--sample-name " + sampleName} \
      ${"--sample-ploidy " + samplePloidy} \
      ${true="--sites-only-vcf-output" false="" sitesOnlyVcfOutput} \
      ${"--standard-min-confidence-threshold-for-calling " + standardMinConfidenceThresholdForCalling} \
      ${true="--use-new-qual-calculator" false="" useNewQualCalculator} \
      --input ${inputRead} \
      ${"--intervals " + intervals} \
      --reference ${reference} \
      --dbsnp ${dbsnp} \
      ${"--output " + if defined(outputFilename) then outputFilename else "generated-6815ce48-cf83-11e9-b4cb-acde48001122.vcf"}
  }
  runtime {
    docker: "broadinstitute/gatk:4.0.12.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-6815bd5e-cf83-11e9-b4cb-acde48001122.vcf"
    File out_idx = if defined(outputFilename) then outputFilename else "generated-6815bd5e-cf83-11e9-b4cb-acde48001122.vcf" + ".idx"
  }
}