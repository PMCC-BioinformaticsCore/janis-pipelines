version development

task Gatk4MarkDuplicates {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File bam
    File bam_bai
    String? outputFilename
    String? metricsFilename
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
  command <<<
    ln -f ~{bam_bai} `echo '~{bam}' | sed 's/\.[^.]*$//'`.bai
    gatk MarkDuplicates \
      ~{if defined(assumeSortOrder) then ("-ASO " +  '"' + assumeSortOrder + '"') else ""} \
      ~{if defined(barcodeTag) then ("--BARCODE_TAG " +  '"' + barcodeTag + '"') else ""} \
      ~{true="-CO " false="" defined(comment)}~{sep=" " comment} \
      -I ~{bam} \
      ~{if defined(select_first([outputFilename, "~{basename(bam, ".bam")}.markduped.bam"])) then ("-O " +  '"' + select_first([outputFilename, "~{basename(bam, ".bam")}.markduped.bam"]) + '"') else ""} \
      ~{if defined(select_first([metricsFilename, "generated.metrics.txt"])) then ("-M " +  '"' + select_first([metricsFilename, "generated.metrics.txt"]) + '"') else ""} \
      ~{true="--arguments_file " false="" defined(argumentsFile)}~{sep=" " argumentsFile} \
      ~{if defined(compressionLevel) then ("--COMPRESSION_LEVEL " +  '"' + compressionLevel + '"') else ""} \
      ~{true="--CREATE_INDEX" false="" createIndex} \
      ~{true="--CREATE_MD5_FILE" false="" createMd5File} \
      ~{if defined(maxRecordsInRam) then ("--MAX_RECORDS_IN_RAM " +  '"' + maxRecordsInRam + '"') else ""} \
      ~{true="--QUIET" false="" quiet} \
      ~{if defined(select_first([tmpDir, "tmp/"])) then ("--TMP_DIR " +  '"' + select_first([tmpDir, "tmp/"]) + '"') else ""} \
      ~{true="--use_jdk_deflater" false="" useJdkDeflater} \
      ~{true="--use_jdk_inflater" false="" useJdkInflater} \
      ~{if defined(validationStringency) then ("--VALIDATION_STRINGENCY " +  '"' + validationStringency + '"') else ""} \
      ~{if defined(verbosity) then ("--verbosity " +  '"' + verbosity + '"') else ""}
    ln -f `echo '~{select_first([outputFilename, "~{basename(bam, ".bam")}.markduped.bam"])}' | sed 's/\.[^.]*$//'`.bai `echo '~{select_first([outputFilename, "~{basename(bam, ".bam")}.markduped.bam"])}' `.bai
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    docker: "broadinstitute/gatk:4.1.3.0"
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "~{basename(bam, ".bam")}.markduped.bam"])
    File out_bai = (select_first([outputFilename, "~{basename(bam, ".bam")}.markduped.bam"])) + ".bai"
    File metrics = select_first([metricsFilename, "generated.metrics.txt"])
  }
}