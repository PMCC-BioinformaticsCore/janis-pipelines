version development

task bcftoolsAnnotate {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File file
    String outputFilename = "generated-f8d407e2-cf83-11e9-8e32-acde48001122.vcf"
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
  command {
    bcftools annotate \
      ${"--output " + if defined(outputFilename) then outputFilename else "generated-f8d411ba-cf83-11e9-8e32-acde48001122.vcf"} \
      ${"--annotations " + annotations} \
      ${"--collapse " + collapse} \
      ${if defined(columns) then "--columns " else ""}${sep=" --columns " columns} \
      ${"--exclude " + exclude} \
      ${"--header-lines " + headerLines} \
      ${"--set-id " + setId} \
      ${"--include " + include} \
      ${true="--keep-sites" false="" keepSites} \
      ${"--mark-sites " + markSites} \
      ${"--output-type " + outputType} \
      ${"--regions " + regions} \
      ${"--regions-file " + regionsFile} \
      ${"--rename-chrs " + renameChrs} \
      ${if defined(samples) then "--samples " else ""}${sep=" --samples " samples} \
      ${"--samples-file " + samplesFile} \
      ${"--threads " + threads} \
      ${if defined(remove) then "--remove " else ""}${sep=" --remove " remove} \
      ${file}
  }
  runtime {
    docker: "biocontainers/bcftools:v1.5_cv2"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-f8d407e2-cf83-11e9-8e32-acde48001122.vcf"
  }
}