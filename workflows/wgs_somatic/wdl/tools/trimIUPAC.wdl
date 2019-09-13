version development

task trimIUPAC {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File vcf
    String outputFilename = "generated-32e08446-d5c0-11e9-8cfd-f218985ebfa7.trimmed.vcf"
  }
  command {
    trimIUPAC.py \
      ${vcf} \
      ${if defined(outputFilename) then outputFilename else "generated-32e089c8-d5c0-11e9-8cfd-f218985ebfa7.trimmed.vcf"}
  }
  runtime {
    docker: "michaelfranklin/pmacutil:0.0.4"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-32e08446-d5c0-11e9-8cfd-f218985ebfa7.trimmed.vcf"
  }
}