version development

task Gatk4MergeSamFiles {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Array[File] bams
    Array[File] bams_bai
    String outputFilename = "generated-55be0cac-d5cc-11e9-bc6b-f218985ebfa7.bam"
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
    gatk MergeSamFiles \
      ${true="-AS" false="" assumeSorted} \
      ${true="-CO " false="" defined(comment)}${sep=" " comment} \
      ${true="-MSD" false="" mergeSequenceDictionaries} \
      ${true="--USE_THREADING" false="" useThreading} \
      -I ${sep=" " bams} \
      ${"-O " + if defined(outputFilename) then outputFilename else "generated-55be17b0-d5cc-11e9-bc6b-f218985ebfa7.bam"} \
      ${true="--arguments_file " false="" defined(argumentsFile)}${sep=" " argumentsFile} \
      ${"-SO " + sortOrder} \
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
    docker: "broadinstitute/gatk:4.1.3.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-55be0cac-d5cc-11e9-bc6b-f218985ebfa7.bam"
    File out_bai = sub(if defined(outputFilename) then outputFilename else "generated-55be0cac-d5cc-11e9-bc6b-f218985ebfa7.bam", "\\.bam$", ".bai")
  }
}