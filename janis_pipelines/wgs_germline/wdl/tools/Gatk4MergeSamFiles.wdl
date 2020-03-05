version development

task Gatk4MergeSamFiles {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Array[File] bams
    Array[File] bams_bai
    String? outputFilename = "generated.bam"
    Array[File]? argumentsFile
    Boolean? assumeSorted
    Array[String]? comment
    Boolean? mergeSequenceDictionaries
    String? sortOrder
    Boolean? useThreading
    Int? compressionLevel
    Boolean? createIndex
    Boolean? createMd5File
    Int? maxRecordsInRam
    Boolean? quiet
    File? reference
    File? reference_fai
    File? reference_amb
    File? reference_ann
    File? reference_bwt
    File? reference_pac
    File? reference_sa
    File? reference_dict
    String? tmpDir
    Boolean? useJdkDeflater
    Boolean? useJdkInflater
    String? validationStringency
    String? verbosity
  }
  command <<<
    gatk MergeSamFiles \
      ~{true="-AS" false="" assumeSorted} \
      ~{true="-CO " false="" defined(comment)}~{sep=" " comment} \
      ~{true="-MSD" false="" mergeSequenceDictionaries} \
      ~{true="--USE_THREADING" false="" useThreading} \
      ~{sep=" " prefix("-I ", bams)} \
      ~{if defined(select_first([outputFilename, "generated.bam"])) then ("-O " +  '"' + select_first([outputFilename, "generated.bam"]) + '"') else ""} \
      ~{true="--arguments_file " false="" defined(argumentsFile)}~{sep=" " argumentsFile} \
      ~{if defined(sortOrder) then ("-SO " +  '"' + sortOrder + '"') else ""} \
      ~{if defined(compressionLevel) then ("--COMPRESSION_LEVEL " +  '"' + compressionLevel + '"') else ""} \
      ~{true="--CREATE_INDEX" false="" createIndex} \
      ~{true="--CREATE_MD5_FILE" false="" createMd5File} \
      ~{if defined(maxRecordsInRam) then ("--MAX_RECORDS_IN_RAM " +  '"' + maxRecordsInRam + '"') else ""} \
      ~{true="--QUIET" false="" quiet} \
      ~{if defined(reference) then ("--reference " +  '"' + reference + '"') else ""} \
      ~{if defined(select_first([tmpDir, "/tmp/"])) then ("--TMP_DIR " +  '"' + select_first([tmpDir, "/tmp/"]) + '"') else ""} \
      ~{true="--use_jdk_deflater" false="" useJdkDeflater} \
      ~{true="--use_jdk_inflater" false="" useJdkInflater} \
      ~{if defined(validationStringency) then ("--VALIDATION_STRINGENCY " +  '"' + validationStringency + '"') else ""} \
      ~{if defined(verbosity) then ("--verbosity " +  '"' + verbosity + '"') else ""}
    ln -f `echo '~{select_first([outputFilename, "generated.bam"])}' | sed 's/\.[^.]*$//'`.bai `echo '~{select_first([outputFilename, "generated.bam"])}' `.bai
  >>>
  runtime {
    docker: "broadinstitute/gatk:4.1.3.0"
    cpu: select_first([runtime_cpu, 1])
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated.bam"])
    File out_bai = (select_first([outputFilename, "generated.bam"])) + ".bai"
  }
}