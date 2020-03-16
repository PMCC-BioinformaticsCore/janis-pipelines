version development

task BwaMemSamtoolsView {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    Array[File] reads
    Array[File]? mates
    String? outputFilename = "generated.bam"
    String sampleName
    String? platformTechnology
    Int? minimumSeedLength
    Int? bandwidth
    Int? offDiagonalXDropoff
    Float? reseedTrigger
    Int? occurenceDiscard
    Boolean? performSW
    Int? matchingScore
    Int? mismatchPenalty
    Int? openGapPenalty
    Int? gapExtensionPenalty
    Int? clippingPenalty
    Int? unpairedReadPenalty
    Boolean? assumeInterleavedFirstInput
    Int? outputAlignmentThreshold
    Boolean? outputAllElements
    Boolean? appendComments
    Boolean? hardClipping
    Boolean? markShorterSplits
    Int? verboseLevel
    String? skippedReadsOutputFilename
    File? referenceIndex
    File? intervals
    String? includeReadsInReadGroup
    File? includeReadsInFile
    Int? includeReadsWithQuality
    String? includeReadsInLibrary
    Int? includeReadsWithCIGAROps
    Array[Int]? includeReadsWithAllFLAGs
    Array[Int]? includeReadsWithoutFLAGs
    Array[Int]? excludeReadsWithAllFLAGs
    Boolean? useMultiRegionIterator
    String? readTagToStrip
    Boolean? collapseBackwardCIGAROps
    String? outputFmt
  }
  command <<<
     \
      bwa \
      mem \
      ~{reference} \
      ~{if defined(minimumSeedLength) then ("-k " +  '"' + minimumSeedLength + '"') else ""} \
      ~{if defined(bandwidth) then ("-w " +  '"' + bandwidth + '"') else ""} \
      ~{if defined(offDiagonalXDropoff) then ("-d " +  '"' + offDiagonalXDropoff + '"') else ""} \
      ~{if defined(reseedTrigger) then ("-r " +  '"' + reseedTrigger + '"') else ""} \
      ~{if defined(occurenceDiscard) then ("-c " +  '"' + occurenceDiscard + '"') else ""} \
      ~{true="-P" false="" performSW} \
      ~{if defined(matchingScore) then ("-A " +  '"' + matchingScore + '"') else ""} \
      ~{if defined(mismatchPenalty) then ("-B " +  '"' + mismatchPenalty + '"') else ""} \
      ~{if defined(openGapPenalty) then ("-O " +  '"' + openGapPenalty + '"') else ""} \
      ~{if defined(gapExtensionPenalty) then ("-E " +  '"' + gapExtensionPenalty + '"') else ""} \
      ~{if defined(clippingPenalty) then ("-L " +  '"' + clippingPenalty + '"') else ""} \
      ~{if defined(unpairedReadPenalty) then ("-U " +  '"' + unpairedReadPenalty + '"') else ""} \
      ~{true="-p" false="" assumeInterleavedFirstInput} \
      ~{if defined(outputAlignmentThreshold) then ("-T " +  '"' + outputAlignmentThreshold + '"') else ""} \
      ~{true="-a" false="" outputAllElements} \
      ~{true="-C" false="" appendComments} \
      ~{true="-H" false="" hardClipping} \
      ~{true="-M" false="" markShorterSplits} \
      ~{if defined(verboseLevel) then ("-v " +  '"' + verboseLevel + '"') else ""} \
      -R '@RG\tID:~{sampleName}\tSM:~{sampleName}\tLB:~{sampleName}\tPL:~{select_first([platformTechnology, "ILLUMINA"])}' \
      -t ~{select_first([runtime_cpu, 1])} \
      ~{sep=" " reads} \
      ~{true="" false="" defined(mates)}~{sep=" " mates} \
      | \
      samtools \
      view \
      ~{if defined(select_first([outputFilename, "generated.bam"])) then ("-o " +  '"' + select_first([outputFilename, "generated.bam"]) + '"') else ""} \
      ~{if defined(skippedReadsOutputFilename) then ("-U " +  '"' + skippedReadsOutputFilename + '"') else ""} \
      ~{if defined(referenceIndex) then ("-t " +  '"' + referenceIndex + '"') else ""} \
      ~{if defined(intervals) then ("-L " +  '"' + intervals + '"') else ""} \
      ~{if defined(includeReadsInReadGroup) then ("-r " +  '"' + includeReadsInReadGroup + '"') else ""} \
      ~{if defined(includeReadsInFile) then ("-R " +  '"' + includeReadsInFile + '"') else ""} \
      ~{if defined(includeReadsWithQuality) then ("-q " +  '"' + includeReadsWithQuality + '"') else ""} \
      ~{if defined(includeReadsInLibrary) then ("-l " +  '"' + includeReadsInLibrary + '"') else ""} \
      ~{if defined(includeReadsWithCIGAROps) then ("-m " +  '"' + includeReadsWithCIGAROps + '"') else ""} \
      ~{true="-f " false="" defined(includeReadsWithAllFLAGs)}~{sep=" " includeReadsWithAllFLAGs} \
      ~{true="-F " false="" defined(includeReadsWithoutFLAGs)}~{sep=" " includeReadsWithoutFLAGs} \
      ~{true="-G " false="" defined(excludeReadsWithAllFLAGs)}~{sep=" " excludeReadsWithAllFLAGs} \
      ~{true="-M" false="" useMultiRegionIterator} \
      ~{if defined(readTagToStrip) then ("-x " +  '"' + readTagToStrip + '"') else ""} \
      ~{true="-B" false="" collapseBackwardCIGAROps} \
      ~{if defined(outputFmt) then ("--output-fmt " +  '"' + outputFmt + '"') else ""} \
      -T ~{reference} \
      --threads ~{select_first([runtime_cpu, 1])} \
      -h \
      -b
  >>>
  runtime {
    docker: "michaelfranklin/bwasamtools:0.7.17-1.9"
    cpu: select_first([runtime_cpu, 1])
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated.bam"])
  }
}