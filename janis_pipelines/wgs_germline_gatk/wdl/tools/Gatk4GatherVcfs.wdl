version development

task Gatk4GatherVcfs {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Array[File] vcfs
    String? outputFilename = "generated-.gathered.vcf"
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
  command <<<
    gatk GatherVcfs \
      ~{sep=" " prefix("--INPUT ", vcfs)} \
      ~{if defined(select_first([outputFilename, "generated-.gathered.vcf"])) then ("--OUTPUT " +  '"' + select_first([outputFilename, "generated-.gathered.vcf"]) + '"') else ""} \
      ~{true="--arguments_file " false="" defined(argumentsFile)}~{sep=" " argumentsFile} \
      ~{if defined(compressionLevel) then ("--COMPRESSION_LEVEL " +  '"' + compressionLevel + '"') else ""} \
      ~{true="--CREATE_INDEX" false="" createIndex} \
      ~{true="--CREATE_MD5_FILE" false="" createMd5File} \
      ~{if defined(ga4ghClientSecrets) then ("--GA4GH_CLIENT_SECRETS " +  '"' + ga4ghClientSecrets + '"') else ""} \
      ~{if defined(maxRecordsInRam) then ("--MAX_RECORDS_IN_RAM " +  '"' + maxRecordsInRam + '"') else ""} \
      ~{true="--QUIET" false="" quiet} \
      ~{if defined(referenceSequence) then ("--REFERENCE_SEQUENCE " +  '"' + referenceSequence + '"') else ""} \
      ~{if defined(select_first([tmpDir, "/tmp"])) then ("--TMP_DIR " +  '"' + select_first([tmpDir, "/tmp"]) + '"') else ""} \
      ~{true="--USE_JDK_DEFLATER" false="" useJdkDeflater} \
      ~{true="--USE_JDK_INFLATER" false="" useJdkInflater} \
      ~{if defined(validationStringency) then ("--VALIDATION_STRINGENCY " +  '"' + validationStringency + '"') else ""} \
      ~{true="--VERBOSITY" false="" verbosity}
  >>>
  runtime {
    docker: "broadinstitute/gatk:4.0.12.0"
    cpu: select_first([runtime_cpu, 1])
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated-.gathered.vcf"])
  }
}