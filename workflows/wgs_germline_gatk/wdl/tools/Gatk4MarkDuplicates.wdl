version development

task Gatk4MarkDuplicates {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File bam
    File bam_bai
    String outputFilename = "generated-e6b224ea-e018-11e9-b4b3-a0cec8186c53.bam"
    String metricsFilename = "generated-e6b2254e-e018-11e9-b4b3-a0cec8186c53.metrics.txt"
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
    if [ $(dirname "${bam_bai}") != $(dirname "bam") ]; then mv ${bam_bai} $(dirname ${bam}); fi
    gatk MarkDuplicates \
      ${"-ASO " + assumeSortOrder} \
      ${"--BARCODE_TAG " + barcodeTag} \
      ${true="-CO " false="" defined(comment)}${sep=" " comment} \
      -I ${bam} \
      ${"-O " + if defined(outputFilename) then outputFilename else "generated-e6b22d82-e018-11e9-b4b3-a0cec8186c53.bam"} \
      ${"-M " + if defined(metricsFilename) then metricsFilename else "generated-e6b22e22-e018-11e9-b4b3-a0cec8186c53.metrics.txt"} \
      ${true="--arguments_file " false="" defined(argumentsFile)}${sep=" " argumentsFile} \
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
    docker: "broadinstitute/gatk:4.1.3.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-e6b224ea-e018-11e9-b4b3-a0cec8186c53.bam"
    File out_bai = sub(if defined(outputFilename) then outputFilename else "generated-e6b224ea-e018-11e9-b4b3-a0cec8186c53.bam", "\\.bam$", ".bai")
    File metrics = if defined(metricsFilename) then metricsFilename else "generated-e6b2254e-e018-11e9-b4b3-a0cec8186c53.metrics.txt"
  }
}