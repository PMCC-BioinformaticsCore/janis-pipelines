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
    String? outputFilename = "generated.vcf"
    String? assemblyFilename = "generated.bam"
    Int? threads
    File? blacklist
  }
  command <<<
    gridss.sh \
      ~{if defined(select_first([threads, select_first([runtime_cpu, 1])])) then ("--threads " +  '"' + select_first([threads, select_first([runtime_cpu, 1])]) + '"') else ""} \
      --reference ~{reference} \
      ~{if defined(select_first([outputFilename, "generated.vcf"])) then ("--output " +  '"' + select_first([outputFilename, "generated.vcf"]) + '"') else ""} \
      ~{if defined(select_first([assemblyFilename, "generated.bam"])) then ("--assembly " +  '"' + select_first([assemblyFilename, "generated.bam"]) + '"') else ""} \
      ~{if defined(blacklist) then ("--blacklist " +  '"' + blacklist + '"') else ""} \
      ~{sep=" " bams}
  >>>
  runtime {
    docker: "michaelfranklin/gridss:2.5.1-dev2"
    cpu: select_first([runtime_cpu, 1])
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated.vcf"])
    File assembly = select_first([assemblyFilename, "generated.bam"])
  }
}