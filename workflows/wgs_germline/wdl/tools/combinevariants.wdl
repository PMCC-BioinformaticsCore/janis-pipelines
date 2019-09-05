version development

task combinevariants {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    String outputFilename = "generated-565a8674-cf9e-11e9-97c1-acde48001122.combined.vcf"
    String regions = "generated-565a870a-cf9e-11e9-97c1-acde48001122.tsv"
    Array[File] vcfs
    String type
    Array[String]? columns
    String? normal
    String? tumor
    Int? priority
  }
  command {
    combine_vcf.py \
      ${"-o " + if defined(outputFilename) then outputFilename else "generated-565a8eb2-cf9e-11e9-97c1-acde48001122.combined.vcf"} \
      ${"--regions " + if defined(regions) then regions else "generated-565a8f5c-cf9e-11e9-97c1-acde48001122.tsv"} \
      ${sep=" " prefix("-i ", vcfs)} \
      --type ${type} \
      ${if defined(columns) then "--columns " else ""}${sep=" --columns " columns} \
      ${"--normal " + normal} \
      ${"--tumor " + tumor} \
      ${"--priority " + priority}
  }
  runtime {
    docker: "michaelfranklin/pmacutil:0.0.4"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File vcf = if defined(outputFilename) then outputFilename else "generated-565a8674-cf9e-11e9-97c1-acde48001122.combined.vcf"
    File tsv = if defined(regions) then regions else "generated-565a870a-cf9e-11e9-97c1-acde48001122.tsv"
  }
}