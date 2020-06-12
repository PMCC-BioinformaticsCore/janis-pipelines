version development

task trimIUPAC {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File vcf
    String? outputFilename
  }
  command <<<
    trimIUPAC.py \
      ~{vcf} \
      ~{select_first([outputFilename, "generated.trimmed.vcf"])}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    docker: "michaelfranklin/pmacutil:0.0.5"
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated.trimmed.vcf"])
  }
}