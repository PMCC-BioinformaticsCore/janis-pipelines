version development

task GATK4ApplyBQSR {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File bam
    File bam_bai
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    String outputFilename = "generated-56581d94-cf9e-11e9-97c1-acde48001122.bam"
    File? recalFile
    File? intervals
    String? tmpDir
  }
  command {
    gatk ApplyBQSR \
      -R ${reference} \
      ${"-O " + if defined(outputFilename) then outputFilename else "generated-56582424-cf9e-11e9-97c1-acde48001122.bam"} \
      ${"--bqsr-recal-file " + recalFile} \
      ${"--intervals " + intervals} \
      -I ${bam} \
      ${"--tmp-dir " + if defined(tmpDir) then tmpDir else "/tmp/"}
  }
  runtime {
    docker: "broadinstitute/gatk:4.0.12.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-56581d94-cf9e-11e9-97c1-acde48001122.bam"
    File out_bai = sub(if defined(outputFilename) then outputFilename else "generated-56581d94-cf9e-11e9-97c1-acde48001122.bam", "\\.bam$", ".bai")
  }
}