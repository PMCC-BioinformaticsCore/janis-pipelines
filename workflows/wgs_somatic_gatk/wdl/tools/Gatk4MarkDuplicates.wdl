version development

task Gatk4MarkDuplicates {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File bam
    File bam_bai
    String outputFilename = "generated-9c2ef326-c2e5-11e9-91cd-f218985ebfa7.bam"
    String metricsFilename = "generated-9c2ef38a-c2e5-11e9-91cd-f218985ebfa7.metrics.txt"
    Array[File]? argumentsFile
    String? assumeSortOrder
    String? barcodeTag
    Array[String]? comment
    Int? compressionLevel
    Boolean? createIndex
    Boolean? createMd5File
    Int? maxRecordsInRam
    Boolean? quiet
    String? tmpDir
    Boolean? useJdkDeflater
    Boolean? useJdkInflater
    String? validationStringency
    String? verbosity
  }
  command {
    gatk MarkDuplicates \
      ${"-ASO " + assumeSortOrder} \
      ${"--BARCODE_TAG " + barcodeTag} \
      ${if defined(comment) then "-CO " else ""}${sep=" -CO " comment} \
      -I ${bam} \
      ${"-O " + if defined(outputFilename) then outputFilename else "generated-9c2efcea-c2e5-11e9-91cd-f218985ebfa7.bam"} \
      ${"-M " + if defined(metricsFilename) then metricsFilename else "generated-9c2efd62-c2e5-11e9-91cd-f218985ebfa7.metrics.txt"} \
      ${if defined(argumentsFile) then "--arguments_file " else ""}${sep=" --arguments_file " argumentsFile} \
      ${"--COMPRESSION_LEVEL " + compressionLevel} \
      ${true="--CREATE_INDEX" false="" createIndex} \
      ${true="--CREATE_MD5_FILE" false="" createMd5File} \
      ${"--MAX_RECORDS_IN_RAM " + maxRecordsInRam} \
      ${true="--QUIET" false="" quiet} \
      ${"--TMP_DIR " + if defined(tmpDir) then tmpDir else "tmp/"} \
      ${true="--use_jdk_deflater" false="" useJdkDeflater} \
      ${true="--use_jdk_inflater" false="" useJdkInflater} \
      ${"--VALIDATION_STRINGENCY " + validationStringency} \
      ${"--verbosity " + verbosity}
  }
  runtime {
    docker: "broadinstitute/gatk:4.0.12.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-9c2ef326-c2e5-11e9-91cd-f218985ebfa7.bam"
    File out_bai = sub(if defined(outputFilename) then outputFilename else "generated-9c2ef326-c2e5-11e9-91cd-f218985ebfa7.bam", "\\.bam$", ".bai")
    File metrics = if defined(metricsFilename) then metricsFilename else "generated-9c2ef38a-c2e5-11e9-91cd-f218985ebfa7.metrics.txt"
  }
}