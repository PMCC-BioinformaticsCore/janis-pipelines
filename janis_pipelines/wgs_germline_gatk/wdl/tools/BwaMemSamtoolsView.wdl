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
    String outputFilename = "generated-62ed12c4-ea17-11e9-aa6c-acde48001122.bam"
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
  command {
    if [ $(dirname "${reference_amb}") != $(dirname "reference") ]; then mv ${reference_amb} $(dirname ${reference}); fi
    if [ $(dirname "${reference_ann}") != $(dirname "reference") ]; then mv ${reference_ann} $(dirname ${reference}); fi
    if [ $(dirname "${reference_bwt}") != $(dirname "reference") ]; then mv ${reference_bwt} $(dirname ${reference}); fi
    if [ $(dirname "${reference_pac}") != $(dirname "reference") ]; then mv ${reference_pac} $(dirname ${reference}); fi
    if [ $(dirname "${reference_sa}") != $(dirname "reference") ]; then mv ${reference_sa} $(dirname ${reference}); fi
    if [ $(dirname "${reference_fai}") != $(dirname "reference") ]; then mv ${reference_fai} $(dirname ${reference}); fi
    if [ $(dirname "${reference_dict}") != $(dirname "reference") ]; then mv ${reference_dict} $(dirname ${reference}); fi
     \
      bwa \
      mem \
      ${reference} \
      ${"-k " + minimumSeedLength} \
      ${"-w " + bandwidth} \
      ${"-d " + offDiagonalXDropoff} \
      ${"-r " + reseedTrigger} \
      ${"-c " + occurenceDiscard} \
      ${true="-P" false="" performSW} \
      ${"-A " + matchingScore} \
      ${"-B " + mismatchPenalty} \
      ${"-O " + openGapPenalty} \
      ${"-E " + gapExtensionPenalty} \
      ${"-L " + clippingPenalty} \
      ${"-U " + unpairedReadPenalty} \
      ${true="-p" false="" assumeInterleavedFirstInput} \
      ${"-T " + outputAlignmentThreshold} \
      ${true="-a" false="" outputAllElements} \
      ${true="-C" false="" appendComments} \
      ${true="-H" false="" hardClipping} \
      ${true="-M" false="" markShorterSplits} \
      ${"-v " + verboseLevel} \
      -R '@RG\tID:${sampleName}\tSM:${sampleName}\tLB:${sampleName}\tPL:${if defined(platformTechnology) then platformTechnology else "ILLUMINA"}' \
      -t ${if defined(runtime_cpu) then runtime_cpu else 1} \
      ${sep=" " reads} \
      ${true="" false="" defined(mates)}${sep=" " mates} \
      | \
      samtools \
      view \
      ${"-o " + if defined(outputFilename) then outputFilename else "generated-62ed3114-ea17-11e9-aa6c-acde48001122.bam"} \
      ${"-U " + skippedReadsOutputFilename} \
      ${"-t " + referenceIndex} \
      ${"-L " + intervals} \
      ${"-r " + includeReadsInReadGroup} \
      ${"-R " + includeReadsInFile} \
      ${"-q " + includeReadsWithQuality} \
      ${"-l " + includeReadsInLibrary} \
      ${"-m " + includeReadsWithCIGAROps} \
      ${true="-f " false="" defined(includeReadsWithAllFLAGs)}${sep=" " includeReadsWithAllFLAGs} \
      ${true="-F " false="" defined(includeReadsWithoutFLAGs)}${sep=" " includeReadsWithoutFLAGs} \
      ${true="-G " false="" defined(excludeReadsWithAllFLAGs)}${sep=" " excludeReadsWithAllFLAGs} \
      ${true="-M" false="" useMultiRegionIterator} \
      ${"-x " + readTagToStrip} \
      ${true="-B" false="" collapseBackwardCIGAROps} \
      ${"--output-fmt " + outputFmt} \
      -T ${reference} \
      --threads ${if defined(runtime_cpu) then runtime_cpu else 1} \
      -h \
      -b
  }
  runtime {
    docker: "michaelfranklin/bwasamtools:0.7.17-1.9"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-62ed12c4-ea17-11e9-aa6c-acde48001122.bam"
  }
}