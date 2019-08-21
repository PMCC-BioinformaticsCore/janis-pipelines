version development

task Gatk4GatherVcfs {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Array[File] vcfs
    String outputFilename = "generated-437f9264-c3b0-11e9-af7e-f218985ebfa7.gathered.vcf"
    Array[File]? argumentsFile
    Int? compressionLevel
    Boolean? createIndex
    Boolean? createMd5File
    File? ga4ghClientSecrets
    Int? maxRecordsInRam
    Boolean? quiet
    File? referenceSequence
    String? tmpDir
    Boolean? useJdkDeflater
    Boolean? useJdkInflater
    String? validationStringency
    Boolean? verbosity
  }
  command {
    gatk GatherVcfs \
      ${sep=" " prefix("--INPUT ", vcfs)} \
      ${"--OUTPUT " + if defined(outputFilename) then outputFilename else "generated-437f9c1e-c3b0-11e9-af7e-f218985ebfa7.gathered.vcf"} \
      ${if defined(argumentsFile) then "--arguments_file " else ""}${sep=" --arguments_file " argumentsFile} \
      ${"--COMPRESSION_LEVEL " + compressionLevel} \
      ${true="--CREATE_INDEX" false="" createIndex} \
      ${true="--CREATE_MD5_FILE" false="" createMd5File} \
      ${"--GA4GH_CLIENT_SECRETS " + ga4ghClientSecrets} \
      ${"--MAX_RECORDS_IN_RAM " + maxRecordsInRam} \
      ${true="--QUIET" false="" quiet} \
      ${"--REFERENCE_SEQUENCE " + referenceSequence} \
      ${"--TMP_DIR " + if defined(tmpDir) then tmpDir else "/tmp"} \
      ${true="--USE_JDK_DEFLATER" false="" useJdkDeflater} \
      ${true="--USE_JDK_INFLATER" false="" useJdkInflater} \
      ${"--VALIDATION_STRINGENCY " + validationStringency} \
      ${true="--VERBOSITY" false="" verbosity}
  }
  runtime {
    docker: "broadinstitute/gatk:4.0.12.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-437f9264-c3b0-11e9-af7e-f218985ebfa7.gathered.vcf"
  }
}