version development

task Gatk4DepthOfCoverage {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Int? runtime_seconds
    Int? runtime_disks
    Array[String]? javaOptions
    Int? compression_level
    File bam
    File bam_bai
    File reference
    File reference_fai
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_dict
    String outputPrefix
    Array[File] intervals
    String? countType
    Array[Int]? summaryCoverageThreshold
    Boolean? omitDepthOutputAtEachBase
    Boolean? omitGenesNotEntirelyCoveredByTraversal
    Boolean? omitIntervalStatistics
    Boolean? omitLocusTable
    Boolean? omitPerSampleStatistics
  }
  command <<<
    cp -f ~{bam_bai} $(echo '~{bam}' | sed 's/\.[^.]*$//').bai
    gatk DepthOfCoverage \
      --java-options '-Xmx~{((select_first([runtime_memory, 8, 4]) * 3) / 4)}G ~{if (defined(compression_level)) then ("-Dsamjdk.compress_level=" + compression_level) else ""} ~{sep(" ", select_first([javaOptions, []]))}' \
      -I '~{bam}' \
      -R '~{reference}' \
      -O '~{outputPrefix}' \
      ~{"--intervals '" + sep("' --intervals  '", intervals) + "'"} \
      ~{if defined(countType) then ("--count-type '" + countType + "'") else ""} \
      ~{if (defined(summaryCoverageThreshold) && length(select_first([summaryCoverageThreshold])) > 0) then sep(" ", prefix("--summary-coverage-threshold ", select_first([summaryCoverageThreshold]))) else ""} \
      ~{if defined(omitDepthOutputAtEachBase) then "--omit-depth-output-at-each-base" else ""} \
      ~{if defined(omitGenesNotEntirelyCoveredByTraversal) then "--omit-genes-not-entirely-covered-by-traversal" else ""} \
      ~{if defined(omitIntervalStatistics) then "--omit-interval-statistics" else ""} \
      ~{if defined(omitLocusTable) then "--omit-locus-table" else ""} \
      ~{if defined(omitPerSampleStatistics) then "--omit-per-sample-statistics" else ""}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1, 1])
    disks: "local-disk ~{select_first([runtime_disks, 20])} SSD"
    docker: "broadinstitute/gatk:4.1.6.0"
    duration: select_first([runtime_seconds, 86400])
    memory: "~{select_first([runtime_memory, 8, 4])}G"
    preemptible: 2
  }
  output {
    File? out_sample = outputPrefix
    File out_sampleCumulativeCoverageCounts = (outputPrefix + ".sample_cumulative_coverage_counts")
    File out_sampleCumulativeCoverageProportions = (outputPrefix + ".sample_cumulative_coverage_proportions")
    File out_sampleIntervalStatistics = (outputPrefix + ".sample_interval_statistics")
    File out_sampleIntervalSummary = (outputPrefix + ".sample_interval_summary")
    File out_sampleStatistics = (outputPrefix + ".sample_statistics")
    File out_sampleSummary = (outputPrefix + ".sample_summary")
  }
}