version development

task trimIUPAC {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File vcf
    String? outputFilename = "generated-.trimmed.vcf"
  }
  command <<<
    trimIUPAC.py \
      ~{vcf} \
      ~{select_first([outputFilename, "generated-.trimmed.vcf"])}
  >>>
  runtime {
    docker: "michaelfranklin/pmacutil:0.0.5"
    cpu: select_first([runtime_cpu, 1])
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated-.trimmed.vcf"])
  }
}