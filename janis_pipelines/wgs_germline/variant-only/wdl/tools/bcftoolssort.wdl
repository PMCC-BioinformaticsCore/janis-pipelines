version development

task bcftoolssort {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File vcf
    String? outputFilename = "generated-.sorted.vcf.gz"
    String? outputType
    String? tempDir
  }
  command <<<
    bcftools sort \
      ~{if defined(select_first([outputFilename, "generated-.sorted.vcf.gz"])) then ("--output-file " +  '"' + select_first([outputFilename, "generated-.sorted.vcf.gz"]) + '"') else ""} \
      ~{if defined(select_first([outputType, "z"])) then ("--output-type " +  '"' + select_first([outputType, "z"]) + '"') else ""} \
      ~{if defined(tempDir) then ("--temp-dir " +  '"' + tempDir + '"') else ""} \
      ~{vcf}
  >>>
  runtime {
    docker: "michaelfranklin/bcftools:1.9"
    cpu: select_first([runtime_cpu, 1])
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated-.sorted.vcf.gz"])
  }
}