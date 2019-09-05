version development

task combinevariants {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    String outputFilename = "generated-8f3cf548-cf9f-11e9-b76d-acde48001122.combined.vcf"
    String regions = "generated-8f3cf5c0-cf9f-11e9-b76d-acde48001122.tsv"
    Array[File] vcfs
    String type
    Array[String]? columns
    String? normal
    String? tumor
    Int? priority
  }
  command {
    combine_vcf.py \
      ${"-o " + if defined(outputFilename) then outputFilename else "generated-8f3cfd5e-cf9f-11e9-b76d-acde48001122.combined.vcf"} \
      ${"--regions " + if defined(regions) then regions else "generated-8f3cfe1c-cf9f-11e9-b76d-acde48001122.tsv"} \
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
    File vcf = if defined(outputFilename) then outputFilename else "generated-8f3cf548-cf9f-11e9-b76d-acde48001122.combined.vcf"
    File tsv = if defined(regions) then regions else "generated-8f3cf5c0-cf9f-11e9-b76d-acde48001122.tsv"
  }
}