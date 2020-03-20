version development

task SplitMultiAllele {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File vcf
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    String? outputFilename = "generated-.norm.vcf"
  }
  command <<<
     \
      zcat \
      | \
      sed 's/ID=AD,Number=./ID=AD,Number=R/' < \
      ~{vcf} \
      | \
      vt decompose -s - -o - \
      | \
      vt normalize -n -q - -o - \
      -r ~{reference} \
      | \
      ~{if defined(select_first([outputFilename, "generated-.norm.vcf"])) then ("> " +  '"' + select_first([outputFilename, "generated-.norm.vcf"]) + '"') else ""} \
      sed 's/ID=AD,Number=./ID=AD,Number=1/'
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    docker: "heuermh/vt"
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated-.norm.vcf"])
  }
}