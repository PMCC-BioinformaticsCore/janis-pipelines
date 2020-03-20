version development

task Gatk4BaseRecalibrator {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    String? tmpDir
    File bam
    File bam_bai
    Array[File] knownSites
    Array[File] knownSites_tbi
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    String? outputFilename = "generated.table"
    File? intervals
  }
  command <<<
    ln -f ~{bam_bai} `echo '~{bam}' | sed 's/\.[^.]*$//'`.bai
    gatk BaseRecalibrator \
      ~{if defined(select_first([tmpDir, "/tmp/"])) then ("--tmp-dir " +  '"' + select_first([tmpDir, "/tmp/"]) + '"') else ""} \
      ~{if defined(intervals) then ("--intervals " +  '"' + intervals + '"') else ""} \
      -R ~{reference} \
      -I ~{bam} \
      ~{if defined(select_first([outputFilename, "generated.table"])) then ("-O " +  '"' + select_first([outputFilename, "generated.table"]) + '"') else ""} \
      ~{sep=" " prefix("--known-sites ", knownSites)}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    docker: "broadinstitute/gatk:4.1.3.0"
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated.table"])
  }
}