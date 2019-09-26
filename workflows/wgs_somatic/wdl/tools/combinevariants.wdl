version development

task combinevariants {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    String outputFilename = "generated-f5b13102-e018-11e9-af76-a0cec8186c53.combined.vcf"
    String regions = "generated-f5b13184-e018-11e9-af76-a0cec8186c53.tsv"
    Array[File] vcfs
    String type
    Array[String]? columns
    String? normal
    String? tumor
    Int? priority
  }
  command {
    combine_vcf.py \
      ${"-o " + if defined(outputFilename) then outputFilename else "generated-f5b138e6-e018-11e9-af76-a0cec8186c53.combined.vcf"} \
      ${"--regions " + if defined(regions) then regions else "generated-f5b13986-e018-11e9-af76-a0cec8186c53.tsv"} \
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
    File vcf = if defined(outputFilename) then outputFilename else "generated-f5b13102-e018-11e9-af76-a0cec8186c53.combined.vcf"
    File tsv = if defined(regions) then regions else "generated-f5b13184-e018-11e9-af76-a0cec8186c53.tsv"
  }
}