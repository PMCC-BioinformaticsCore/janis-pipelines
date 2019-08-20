version development

task combinevariants {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    String outputFilename = "generated-0668b4a6-c2dd-11e9-933b-f218985ebfa7.combined.vcf"
    String regions = "generated-0668b514-c2dd-11e9-933b-f218985ebfa7.tsv"
    Array[File] vcfs
    String type
    Array[String]? columns
    String? normal
    String? tumor
    Int? priority
  }
  command {
    combine_vcf.py \
      ${"-o " + if defined(outputFilename) then outputFilename else "generated-0668bc26-c2dd-11e9-933b-f218985ebfa7.combined.vcf"} \
      ${"--regions " + if defined(regions) then regions else "generated-0668bcb2-c2dd-11e9-933b-f218985ebfa7.tsv"} \
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
    File vcf = if defined(outputFilename) then outputFilename else "generated-0668b4a6-c2dd-11e9-933b-f218985ebfa7.combined.vcf"
    File tsv = if defined(regions) then regions else "generated-0668b514-c2dd-11e9-933b-f218985ebfa7.tsv"
  }
}