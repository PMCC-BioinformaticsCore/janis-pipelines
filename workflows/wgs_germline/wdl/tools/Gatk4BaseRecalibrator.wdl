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
    String outputFilename = "generated-363ce066-c3b0-11e9-81d9-f218985ebfa7.table"
    File? intervals
  }
  command {
    gatk BaseRecalibrator \
      ${"--tmp-dir " + if defined(tmpDir) then tmpDir else "/tmp/"} \
      ${"--intervals " + intervals} \
      -R ${reference} \
      -I ${bam} \
      ${"-O " + if defined(outputFilename) then outputFilename else "generated-363ce7fa-c3b0-11e9-81d9-f218985ebfa7.table"} \
      ${sep=" " prefix("--known-sites ", knownSites)}
  }
  runtime {
    docker: "broadinstitute/gatk:4.0.12.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-363ce066-c3b0-11e9-81d9-f218985ebfa7.table"
  }
}