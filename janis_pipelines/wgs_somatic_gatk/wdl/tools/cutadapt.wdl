version development

task cutadapt {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Array[File] fastq
    String? adapter
    String outputFilename = "generated-8a44494a-0fca-11ea-a7d3-acde48001122-R1.fastq.gz"
    String secondReadFile = "generated-8a44494a-0fca-11ea-a7d3-acde48001122-R2.fastq.gz"
    Boolean? debug
    Boolean? noIndels
    Boolean? matchReadWildcards
    Boolean? trimN
    Boolean? discardCasava
    Boolean? quiet
    Boolean? stripF3
    Boolean? noZeroCap
    Boolean? interleaved
    Boolean? discardTrimmed
    Boolean? discardUntrimmed
    Boolean? maq
    String? pairFilter
    String? nextseqTrim
    String? action
    String? qualityBase
    String? lengthTag
    String? stripSuffix
    Int? maxN
    String? report
    String? infoFile
    String? wildcardFile
    String? tooShortOutput
    String? tooLongOutput
    String? untrimmedOutput
    String? untrimmedPairedOutput
    String? tooShortPairedOutput
    String? tooLongPairedOutput
    String? inputFileFormat
    Int? cores
    String? adapter_g
    String? adapter_both
    Float? maximumErrorRate
    Int? removeNAdapters
    Int? overlapRequirement
    Int? removeNBases
    Int? qualityCutoff
    Int? shortenReadsToLength
    String? readNamesPrefix
    String? readNamesSuffix
    Int? minReadLength
    Int? maxReadsLength
    String? middleReadMatchFile
    String? removeMiddle3Adapter
    String? removeMiddle5Adapter
    String? removeMiddleBothAdapter
    Int? removeNBasesFromSecondRead
    Boolean? noMatchAdapterWildcards
    Boolean? colorspace
    Boolean? doubleEncode
    Boolean? trimPrimer
    Boolean? zeroCap
  }
  command {
    cutadapt \
      ${"-a " + adapter} \
      ${"-o " + if defined(outputFilename) then outputFilename else "generated-8a44672c-0fca-11ea-a7d3-acde48001122-R1.fastq.gz"} \
      ${"-p " + if defined(secondReadFile) then secondReadFile else "generated-8a44672c-0fca-11ea-a7d3-acde48001122-R2.fastq.gz"} \
      ${true="--debug" false="" debug} \
      ${true="--no-indels" false="" noIndels} \
      ${true="--match-read-wildcards" false="" matchReadWildcards} \
      ${true="--trim-n" false="" trimN} \
      ${true="--discard-casava" false="" discardCasava} \
      ${true="--quiet" false="" quiet} \
      ${true="--strip-f3" false="" stripF3} \
      ${true="--no-zero-cap" false="" noZeroCap} \
      ${true="--interleaved" false="" interleaved} \
      ${true="--discard-trimmed" false="" discardTrimmed} \
      ${true="--discard-untrimmed" false="" discardUntrimmed} \
      ${true="--maq" false="" maq} \
      ${"--pair-filter= " + pairFilter} \
      ${"--nextseq-trim= " + nextseqTrim} \
      ${"--action= " + action} \
      ${"--quality-base= " + qualityBase} \
      ${"--length-tag= " + lengthTag} \
      ${"--strip-suffix= " + stripSuffix} \
      ${"--max-n= " + maxN} \
      ${"--report= " + report} \
      ${"--info-file= " + infoFile} \
      ${"--wildcard-file= " + wildcardFile} \
      ${"--too-short-output= " + tooShortOutput} \
      ${"--too-long-output= " + tooLongOutput} \
      ${"--untrimmed-output= " + untrimmedOutput} \
      ${"--untrimmed-paired-output= " + untrimmedPairedOutput} \
      ${"--too-short-paired-output= " + tooShortPairedOutput} \
      ${"--too-long-paired-output= " + tooLongPairedOutput} \
      ${"-f " + inputFileFormat} \
      ${"-j " + cores} \
      ${"-g " + adapter_g} \
      ${"-b " + adapter_both} \
      ${"-e " + maximumErrorRate} \
      ${"-n " + removeNAdapters} \
      ${"-O " + overlapRequirement} \
      ${"-u " + removeNBases} \
      ${"-q " + qualityCutoff} \
      ${"-l " + shortenReadsToLength} \
      ${"-x " + readNamesPrefix} \
      ${"-y " + readNamesSuffix} \
      ${"-m " + minReadLength} \
      ${"-M " + maxReadsLength} \
      ${"-r " + middleReadMatchFile} \
      ${"-A " + removeMiddle3Adapter} \
      ${"-G " + removeMiddle5Adapter} \
      ${"-B " + removeMiddleBothAdapter} \
      ${"-U " + removeNBasesFromSecondRead} \
      ${true="-N" false="" noMatchAdapterWildcards} \
      ${true="-c" false="" colorspace} \
      ${true="-d" false="" doubleEncode} \
      ${true="-t" false="" trimPrimer} \
      ${true="-z" false="" zeroCap} \
      ${sep=" " fastq}
  }
  runtime {
    docker: "quay.io/biocontainers/cutadapt:1.18--py37h14c3975_1"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    Array[File] out = glob("*.fastq.gz")
  }
}