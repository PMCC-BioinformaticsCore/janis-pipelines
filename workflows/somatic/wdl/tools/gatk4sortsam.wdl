version development

task gatk4sortsam {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File bam
    String outputFilename = "generated-b6b1b9d4-b1b2-11e9-8bf3-acde48001122.bam"
    String sortOrder
    Array[File]? argumentsFile
    Int? compressionLevel
    Boolean? createIndex
    Boolean? createMd5File
    Int? maxRecordsInRam
    Boolean? quiet
    File? reference
    File? reference_amb
    File? reference_ann
    File? reference_bwt
    File? reference_pac
    File? reference_sa
    File? reference_fai
    File? reference_dict
    String? tmpDir
    Boolean? useJdkDeflater
    Boolean? useJdkInflater
    String? validationStringency
    String? verbosity
  }
  command {
    gatk SortSam \
      -I ${bam} \
      ${"-O " + if defined(outputFilename) then outputFilename else "generated-b6b1c29e-b1b2-11e9-8bf3-acde48001122.bam"} \
      -SO ${sortOrder} \
      ${if defined(argumentsFile) then "--arguments_file " else ""}${sep=" --arguments_file " argumentsFile} \
      ${"--COMPRESSION_LEVEL " + compressionLevel} \
      ${true="--CREATE_INDEX" false="" createIndex} \
      ${true="--CREATE_MD5_FILE" false="" createMd5File} \
      ${"--MAX_RECORDS_IN_RAM " + maxRecordsInRam} \
      ${true="--QUIET" false="" quiet} \
      ${"--reference " + reference} \
      ${"--TMP_DIR " + if defined(tmpDir) then tmpDir else "/tmp/"} \
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
    File out = if defined(outputFilename) then outputFilename else "generated-b6b1b9d4-b1b2-11e9-8bf3-acde48001122.bam"
    File out_bai = sub(if defined(outputFilename) then outputFilename else "generated-b6b1b9d4-b1b2-11e9-8bf3-acde48001122.bam", "\\.bam$", ".bai")
  }
}