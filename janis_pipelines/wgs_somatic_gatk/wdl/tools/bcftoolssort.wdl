version development

task bcftoolssort {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File vcf
    String outputFilename = "generated-8a49d662-0fca-11ea-a7d3-acde48001122.sorted.vcf.gz"
    String? outputType
    String? tempDir
  }
  command {
    bcftools sort \
      ${"--output-file " + if defined(outputFilename) then outputFilename else "generated-8a49db44-0fca-11ea-a7d3-acde48001122.sorted.vcf.gz"} \
      ${"--output-type " + if defined(outputType) then outputType else "z"} \
      ${"--temp-dir " + tempDir} \
      ${vcf}
  }
  runtime {
    docker: "michaelfranklin/bcftools:1.9"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-8a49d662-0fca-11ea-a7d3-acde48001122.sorted.vcf.gz"
  }
}