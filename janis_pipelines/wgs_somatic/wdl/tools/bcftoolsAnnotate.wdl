version development

task bcftoolsAnnotate {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File file
    String? outputFilename = "generated.vcf.gz"
    File? annotations
    String? collapse
    Array[String]? columns
    String? exclude
    File? headerLines
    String? setId
    String? include
    Boolean? keepSites
    String? markSites
    String? outputType
    String? regions
    File? regionsFile
    File? renameChrs
    Array[File]? samples
    File? samplesFile
    Int? threads
    Array[String]? remove
  }
  command <<<
    bcftools annotate \
      ~{if defined(select_first([outputFilename, "generated.vcf.gz"])) then ("--output " +  '"' + select_first([outputFilename, "generated.vcf.gz"]) + '"') else ""} \
      ~{if defined(annotations) then ("--annotations " +  '"' + annotations + '"') else ""} \
      ~{if defined(collapse) then ("--collapse " +  '"' + collapse + '"') else ""} \
      ~{true="--columns " false="" defined(columns)}~{sep=" " columns} \
      ~{if defined(exclude) then ("--exclude " +  '"' + exclude + '"') else ""} \
      ~{if defined(headerLines) then ("--header-lines " +  '"' + headerLines + '"') else ""} \
      ~{if defined(setId) then ("--set-id " +  '"' + setId + '"') else ""} \
      ~{if defined(include) then ("--include " +  '"' + include + '"') else ""} \
      ~{true="--keep-sites" false="" keepSites} \
      ~{if defined(markSites) then ("--mark-sites " +  '"' + markSites + '"') else ""} \
      ~{if defined(outputType) then ("--output-type " +  '"' + outputType + '"') else ""} \
      ~{if defined(regions) then ("--regions " +  '"' + regions + '"') else ""} \
      ~{if defined(regionsFile) then ("--regions-file " +  '"' + regionsFile + '"') else ""} \
      ~{if defined(renameChrs) then ("--rename-chrs " +  '"' + renameChrs + '"') else ""} \
      ~{true="--samples " false="" defined(samples)}~{sep=" " samples} \
      ~{if defined(samplesFile) then ("--samples-file " +  '"' + samplesFile + '"') else ""} \
      ~{if defined(threads) then ("--threads " +  '"' + threads + '"') else ""} \
      ~{true="--remove " false="" defined(remove)}~{sep=" " remove} \
      ~{file}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    docker: "biocontainers/bcftools:v1.5_cv2"
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated.vcf.gz"])
  }
}