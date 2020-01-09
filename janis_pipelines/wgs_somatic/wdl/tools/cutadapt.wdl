version development

task cutadapt {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Array[File] fastq
    Array[String]? adapter
    String outputFilename = "generated--R1.fastq.gz"
    String secondReadFile = "generated--R2.fastq.gz"
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
      ~{"-o " + if defined(outputFilename) then outputFilename else "generated--R1.fastq.gz"} \
      ~{"-p " + if defined(secondReadFile) then secondReadFile else "generated--R2.fastq.gz"} \
      ~{"--cores " + cores} \
      ~{"--front " + front} \
      ~{"--anywhere " + anywhere} \
      ~{"--error-rate " + errorRate} \
      ~{true="--no-indels" false="" noIndels} \
      ~{"--times " + times} \
      ~{"--overlap " + overlap} \
      ~{true="--match-read-wildcards" false="" matchReadWildcards} \
      ~{true="--no-match-adapter-wildcards" false="" noMatchAdapterWildcards} \
      ~{"--action " + action} \
      ~{"--cut " + cut} \
      ~{"--nextseq-trim " + nextseqTrim} \
      ~{"--quality-cutoff " + qualityCutoff} \
      ~{true="--quality-base" false="" qualityBase} \
      ~{"--length " + length} \
      ~{"--trim-n " + trimN} \
      ~{"--length-tag " + lengthTag} \
      ~{"--strip-suffix " + stripSuffix} \
      ~{"--prefix " + prefix} \
      ~{"--suffix " + suffix} \
      ~{true="--zero-cap" false="" zeroCap} \
      ~{"--minimum-length " + minimumLength} \
      ~{"--maximum-length " + maximumLength} \
      ~{"--max-n " + maxN} \
      ~{true="--discard-trimmed" false="" discardTrimmed} \
      ~{true="--discard-untrimmed" false="" discardUntrimmed} \
      ~{true="--discard-casava" false="" discardCasava} \
      ~{true="--quiet" false="" quiet} \
      ~{"-Z " + compressionLevel} \
      ~{"--info-file " + infoFile} \
      ~{"--rest-file " + restFile} \
      ~{"--wildcard-file " + wildcardFile} \
      ~{"--too-short-output " + tooShortOutput} \
      ~{"--too-long-output " + tooLongOutput} \
      ~{"--untrimmed-output " + untrimmedOutput} \
      ~{if defined(removeMiddle3Adapter) && length(select_first([removeMiddle3Adapter, []])) > 0 then "-A " else ""}~{sep=" -A " removeMiddle3Adapter} \
      ~{"-G " + removeMiddle5Adapter} \
      ~{"-B " + removeMiddleBothAdapter} \
      ~{"-U " + removeNBasesFromSecondRead} \
      ~{"--pair-adapters " + pairAdapters} \
      ~{"--pair-filter " + pairFilter} \
      ~{true="--interleaved" false="" interleaved} \
      ~{"--untrimmed-paired-output " + untrimmedPairedOutput} \
      ~{"--too-short-paired-output " + tooShortPairedOutput} \
      ~{"--too-long-paired-output " + tooLongPairedOutput} \
      ~{sep=" " fastq}
  >>>
  runtime {
    docker: "quay.io/biocontainers/cutadapt:2.6--py36h516909a_0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "~{runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    Array[File] out = glob("*.fastq.gz")
  }
}