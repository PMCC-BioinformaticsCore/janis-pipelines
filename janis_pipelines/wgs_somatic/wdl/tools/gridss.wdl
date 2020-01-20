version development

task gridss {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Array[File] bams
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    String outputFilename = "generated.vcf"
    String assemblyFilename = "generated.bam"
    Int? threads
    File? blacklist
  }
  command <<<
    gridss.sh \
      ~{"--threads " + if defined(threads) then threads else if defined(runtime_cpu) then runtime_cpu else 1} \
      --reference ~{reference} \
      ~{"--output " + if defined(outputFilename) then outputFilename else "generated.vcf"} \
      ~{"--assembly " + if defined(assemblyFilename) then assemblyFilename else "generated.bam"} \
      ~{"--blacklist " + blacklist} \
      ~{sep=" " bams}
  >>>
  runtime {
    docker: "michaelfranklin/gridss:2.5.1-dev2"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "~{runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated.vcf"
    File assembly = if defined(assemblyFilename) then assemblyFilename else "generated.bam"
  }
}