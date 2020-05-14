version development

task gridss {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Array[File] bams
    File reference
    File reference_fai
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_dict
    String? outputFilename
    String? assemblyFilename
    Int? threads
    File? blacklist
    String? tmpdir
  }
  command <<<
    /opt/gridss/gridss.sh \
      ~{if defined(select_first([threads, select_first([runtime_cpu, 1])])) then ("--threads " +  '"' + select_first([threads, select_first([runtime_cpu, 1])]) + '"') else ""} \
      ~{if defined(select_first([tmpdir, "./TMP"])) then ("--workingdir " +  '"' + select_first([tmpdir, "./TMP"]) + '"') else ""} \
      --reference ~{reference} \
      ~{if defined(select_first([outputFilename, "generated.svs.vcf"])) then ("--output " +  '"' + select_first([outputFilename, "generated.svs.vcf"]) + '"') else ""} \
      ~{if defined(select_first([assemblyFilename, "generated.assembled.bam"])) then ("--assembly " +  '"' + select_first([assemblyFilename, "generated.assembled.bam"]) + '"') else ""} \
      ~{if defined(blacklist) then ("--blacklist " +  '"' + blacklist + '"') else ""} \
      ~{sep=" " bams}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    docker: "gridss/gridss:2.6.2"
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated.svs.vcf"])
    File assembly = select_first([assemblyFilename, "generated.assembled.bam"])
  }
}