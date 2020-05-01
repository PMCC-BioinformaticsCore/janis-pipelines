version development

task combinevariants {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    String? outputFilename
    String? regions
    Array[File] vcfs
    String type
    Array[String]? columns
    String? normal
    String? tumor
    Int? priority
  }
  command <<<
    combine_vcf.py \
      ~{if defined(select_first([outputFilename, "generated.combined.vcf"])) then ("-o " +  '"' + select_first([outputFilename, "generated.combined.vcf"]) + '"') else ""} \
      ~{if defined(select_first([regions, "generated.tsv"])) then ("--regions " +  '"' + select_first([regions, "generated.tsv"]) + '"') else ""} \
      ~{sep=" " prefix("-i ", vcfs)} \
      --type ~{type} \
      ~{if defined(columns) && length(select_first([columns, []])) > 0 then "--columns " else ""}~{sep=" --columns " columns} \
      ~{if defined(normal) then ("--normal " +  '"' + normal + '"') else ""} \
      ~{if defined(tumor) then ("--tumor " +  '"' + tumor + '"') else ""} \
      ~{if defined(priority) then ("--priority " +  '"' + priority + '"') else ""}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    docker: "michaelfranklin/pmacutil:0.0.4"
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File vcf = select_first([outputFilename, "generated.combined.vcf"])
    File tsv = select_first([regions, "generated.tsv"])
  }
}