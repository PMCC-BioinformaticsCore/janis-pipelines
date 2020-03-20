version development

task cutadapt {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Array[File] fastq
    Array[String]? adapter
    String? outputFilename = "generated--R1.fastq.gz"
    String? secondReadFile = "generated--R2.fastq.gz"
    Int? cores
    String? front
    String? anywhere
    Float? errorRate
    Boolean? noIndels
    Int? times
    Int? overlap
    Boolean? matchReadWildcards
    Boolean? noMatchAdapterWildcards
    String? action
    Int? cut
    String? nextseqTrim
    Int? qualityCutoff
    Boolean? qualityBase
    Int? length
    Int? trimN
    Int? lengthTag
    String? stripSuffix
    String? prefix
    String? suffix
    Boolean? zeroCap
    Int? minimumLength
    Int? maximumLength
    Float? maxN
    Boolean? discardTrimmed
    Boolean? discardUntrimmed
    Boolean? discardCasava
    Boolean? quiet
    String? compressionLevel
    String? infoFile
    String? restFile
    String? wildcardFile
    String? tooShortOutput
    String? tooLongOutput
    String? untrimmedOutput
    Array[String]? removeMiddle3Adapter
    String? removeMiddle5Adapter
    String? removeMiddleBothAdapter
    String? removeNBasesFromSecondRead
    String? pairAdapters
    String? pairFilter
    Boolean? interleaved
    String? untrimmedPairedOutput
    String? tooShortPairedOutput
    String? tooLongPairedOutput
  }
  command <<<
    cutadapt \
      ~{if defined(adapter) && length(select_first([adapter, []])) > 0 then "-a " else ""}~{sep=" -a " adapter} \
      ~{if defined(select_first([outputFilename, "generated--R1.fastq.gz"])) then ("-o " +  '"' + select_first([outputFilename, "generated--R1.fastq.gz"]) + '"') else ""} \
      ~{if defined(select_first([secondReadFile, "generated--R2.fastq.gz"])) then ("-p " +  '"' + select_first([secondReadFile, "generated--R2.fastq.gz"]) + '"') else ""} \
      ~{if defined(cores) then ("--cores " +  '"' + cores + '"') else ""} \
      ~{if defined(front) then ("--front " +  '"' + front + '"') else ""} \
      ~{if defined(anywhere) then ("--anywhere " +  '"' + anywhere + '"') else ""} \
      ~{if defined(errorRate) then ("--error-rate " +  '"' + errorRate + '"') else ""} \
      ~{true="--no-indels" false="" noIndels} \
      ~{if defined(times) then ("--times " +  '"' + times + '"') else ""} \
      ~{if defined(overlap) then ("--overlap " +  '"' + overlap + '"') else ""} \
      ~{true="--match-read-wildcards" false="" matchReadWildcards} \
      ~{true="--no-match-adapter-wildcards" false="" noMatchAdapterWildcards} \
      ~{if defined(action) then ("--action " +  '"' + action + '"') else ""} \
      ~{if defined(cut) then ("--cut " +  '"' + cut + '"') else ""} \
      ~{if defined(nextseqTrim) then ("--nextseq-trim " +  '"' + nextseqTrim + '"') else ""} \
      ~{if defined(qualityCutoff) then ("--quality-cutoff " +  '"' + qualityCutoff + '"') else ""} \
      ~{true="--quality-base" false="" qualityBase} \
      ~{if defined(length) then ("--length " +  '"' + length + '"') else ""} \
      ~{if defined(trimN) then ("--trim-n " +  '"' + trimN + '"') else ""} \
      ~{if defined(lengthTag) then ("--length-tag " +  '"' + lengthTag + '"') else ""} \
      ~{if defined(stripSuffix) then ("--strip-suffix " +  '"' + stripSuffix + '"') else ""} \
      ~{if defined(prefix) then ("--prefix " +  '"' + prefix + '"') else ""} \
      ~{if defined(suffix) then ("--suffix " +  '"' + suffix + '"') else ""} \
      ~{true="--zero-cap" false="" zeroCap} \
      ~{if defined(minimumLength) then ("--minimum-length " +  '"' + minimumLength + '"') else ""} \
      ~{if defined(maximumLength) then ("--maximum-length " +  '"' + maximumLength + '"') else ""} \
      ~{if defined(maxN) then ("--max-n " +  '"' + maxN + '"') else ""} \
      ~{true="--discard-trimmed" false="" discardTrimmed} \
      ~{true="--discard-untrimmed" false="" discardUntrimmed} \
      ~{true="--discard-casava" false="" discardCasava} \
      ~{true="--quiet" false="" quiet} \
      ~{if defined(compressionLevel) then ("-Z " +  '"' + compressionLevel + '"') else ""} \
      ~{if defined(infoFile) then ("--info-file " +  '"' + infoFile + '"') else ""} \
      ~{if defined(restFile) then ("--rest-file " +  '"' + restFile + '"') else ""} \
      ~{if defined(wildcardFile) then ("--wildcard-file " +  '"' + wildcardFile + '"') else ""} \
      ~{if defined(tooShortOutput) then ("--too-short-output " +  '"' + tooShortOutput + '"') else ""} \
      ~{if defined(tooLongOutput) then ("--too-long-output " +  '"' + tooLongOutput + '"') else ""} \
      ~{if defined(untrimmedOutput) then ("--untrimmed-output " +  '"' + untrimmedOutput + '"') else ""} \
      ~{if defined(removeMiddle3Adapter) && length(select_first([removeMiddle3Adapter, []])) > 0 then "-A " else ""}~{sep=" -A " removeMiddle3Adapter} \
      ~{if defined(removeMiddle5Adapter) then ("-G " +  '"' + removeMiddle5Adapter + '"') else ""} \
      ~{if defined(removeMiddleBothAdapter) then ("-B " +  '"' + removeMiddleBothAdapter + '"') else ""} \
      ~{if defined(removeNBasesFromSecondRead) then ("-U " +  '"' + removeNBasesFromSecondRead + '"') else ""} \
      ~{if defined(pairAdapters) then ("--pair-adapters " +  '"' + pairAdapters + '"') else ""} \
      ~{if defined(pairFilter) then ("--pair-filter " +  '"' + pairFilter + '"') else ""} \
      ~{true="--interleaved" false="" interleaved} \
      ~{if defined(untrimmedPairedOutput) then ("--untrimmed-paired-output " +  '"' + untrimmedPairedOutput + '"') else ""} \
      ~{if defined(tooShortPairedOutput) then ("--too-short-paired-output " +  '"' + tooShortPairedOutput + '"') else ""} \
      ~{if defined(tooLongPairedOutput) then ("--too-long-paired-output " +  '"' + tooLongPairedOutput + '"') else ""} \
      ~{sep=" " fastq}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    docker: "quay.io/biocontainers/cutadapt:2.6--py36h516909a_0"
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    Array[File] out = glob("*.fastq.gz")
  }
}