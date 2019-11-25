version development

task bcftoolsAnnotate {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File file
    String outputFilename = "generated-5769034e-0fca-11ea-99c5-acde48001122.vcf.gz"
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
      ${"--output " + if defined(outputFilename) then outputFilename else "generated-57690c90-0fca-11ea-99c5-acde48001122.vcf.gz"} \
      ${"--annotations " + annotations} \
      ${"--collapse " + collapse} \
      ${true="--columns " false="" defined(columns)}${sep=" " columns} \
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
      ${true="--samples " false="" defined(samples)}${sep=" " samples} \
      ${"--samples-file " + samplesFile} \
      ${"--threads " + threads} \
      ${true="--remove " false="" defined(remove)}${sep=" " remove} \
      ${file}
  }
  runtime {
    docker: "biocontainers/bcftools:v1.5_cv2"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-5769034e-0fca-11ea-99c5-acde48001122.vcf.gz"
  }
}