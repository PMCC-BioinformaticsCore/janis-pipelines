version development

task Gatk4MarkDuplicates {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File bam
    File bam_bai
    String outputFilename = "generated-f8d16bfe-cf83-11e9-8e32-acde48001122.bam"
    String metricsFilename = "generated-f8d16c80-cf83-11e9-8e32-acde48001122.metrics.txt"
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
      ${"-O " + if defined(outputFilename) then outputFilename else "generated-f8d17770-cf83-11e9-8e32-acde48001122.bam"} \
      ${"-M " + if defined(metricsFilename) then metricsFilename else "generated-f8d17810-cf83-11e9-8e32-acde48001122.metrics.txt"} \
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
    File out = if defined(outputFilename) then outputFilename else "generated-f8d16bfe-cf83-11e9-8e32-acde48001122.bam"
    File out_bai = sub(if defined(outputFilename) then outputFilename else "generated-f8d16bfe-cf83-11e9-8e32-acde48001122.bam", "\\.bam$", ".bai")
    File metrics = if defined(metricsFilename) then metricsFilename else "generated-f8d16c80-cf83-11e9-8e32-acde48001122.metrics.txt"
  }
}