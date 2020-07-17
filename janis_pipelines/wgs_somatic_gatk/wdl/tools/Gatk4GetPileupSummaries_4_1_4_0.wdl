version development

task Gatk4GetPileupSummaries {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Int? runtime_seconds
    Int? runtime_disks
    Array[String]? javaOptions
    Int? compression_level
    Array[File] bam
    Array[File] bam_bai
    File sites
    File sites_tbi
    File? intervals
    String? pileupTableOut
  }
  command <<<
    gatk GetPileupSummaries \
      --java-options '-Xmx~{((select_first([runtime_memory, 64, 4]) * 3) / 4)}G ~{if (defined(compression_level)) then ("-Dsamjdk.compress_level=" + compression_level) else ""} ~{sep(" ", select_first([javaOptions, []]))}' \
      ~{"-I '" + sep("' -I  '", bam) + "'"} \
      -V '~{sites}' \
      ~{if defined(intervals) then ("--intervals '" + intervals + "'") else ""} \
      -O '~{select_first([pileupTableOut, "generated.txt"])}'
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1, 1])
    disks: "local-disk ~{select_first([runtime_disks, 20])} SSD"
    docker: "broadinstitute/gatk:4.1.4.0"
    duration: select_first([runtime_seconds, 86400])
    memory: "~{select_first([runtime_memory, 64, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([pileupTableOut, "generated.txt"])
  }
}