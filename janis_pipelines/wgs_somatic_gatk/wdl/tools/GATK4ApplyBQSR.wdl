version development

task Gatk4ApplyBQSR {
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
    String outputFilename = "generated.bam"
    File? recalFile
    File? intervals
    String? tmpDir
  }
  command <<<
    ln -f ~{bam_bai} `echo '~{bam}' | sed 's/\.[^.]*$//'`.bai
    gatk ApplyBQSR \
      -R ~{reference} \
      ~{"-O " + if defined(outputFilename) then outputFilename else "generated.bam"} \
      ~{"--bqsr-recal-file " + recalFile} \
      ~{"--intervals " + intervals} \
      -I ~{bam} \
      ~{"--tmp-dir " + if defined(tmpDir) then tmpDir else "/tmp/"}
    ln -f `echo '~{if defined(outputFilename) then outputFilename else "generated.bam"}' | sed 's/\.[^.]*$//'`.bai `echo '~{if defined(outputFilename) then outputFilename else "generated.bam"}' `.bai
  >>>
  runtime {
    docker: "broadinstitute/gatk:4.1.3.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "~{runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated.bam"
    File out_bai = (if defined(outputFilename) then outputFilename else "generated.bam") + ".bai"
  }
}