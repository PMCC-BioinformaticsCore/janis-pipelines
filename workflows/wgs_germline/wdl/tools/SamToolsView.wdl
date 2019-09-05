version development

task SamToolsView {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Boolean? cramOutput
    Boolean? compressedBam
    Boolean? uncompressedBam
    Boolean? onlyOutputHeader
    Boolean? countAlignments
    File? writeAlignments
    File? inputTSV
    File? onlyOverlapping
    Boolean? useMultiRegionIterator
    String? outputAlignmentsInReadGroup
    File? outputAlignmentsInFileReadGroups
    Int? mapqThreshold
    String? outputAlignmentsInLibrary
    Int? outputAlignmentsMeetingCIGARThreshold
    String? outputAlignmentsWithBitsSet
    String? doNotOutputAlignmentsWithBitsSet
    String? doNotOutputAlignmentsWithAllBitsSet
    String? readTagToExclude
    Boolean? collapseBackwardCIGAR
    Float? subsamplingProportion
    Int? threads
    File sam
    File? reference
    File? reference_amb
    File? reference_ann
    File? reference_bwt
    File? reference_pac
    File? reference_sa
    File? reference_fai
    File? reference_dict
    String outputFilename = "generated-6817b6f4-cf83-11e9-b4cb-acde48001122.bam"
  }
  command {
    samtools view \
      '-S' \
      '-h' \
      '-b' \
      ${true="-C" false="" cramOutput} \
      ${true="-1" false="" compressedBam} \
      ${true="-u" false="" uncompressedBam} \
      ${true="-H" false="" onlyOutputHeader} \
      ${true="-c" false="" countAlignments} \
      ${"-U " + writeAlignments} \
      ${"-t " + inputTSV} \
      ${"-L " + onlyOverlapping} \
      ${true="-M" false="" useMultiRegionIterator} \
      ${"-r " + outputAlignmentsInReadGroup} \
      ${"-R " + outputAlignmentsInFileReadGroups} \
      ${"-q " + mapqThreshold} \
      ${"-l " + outputAlignmentsInLibrary} \
      ${"-m " + outputAlignmentsMeetingCIGARThreshold} \
      ${"-f " + outputAlignmentsWithBitsSet} \
      ${"-F " + doNotOutputAlignmentsWithBitsSet} \
      ${"-G " + doNotOutputAlignmentsWithAllBitsSet} \
      ${"-x " + readTagToExclude} \
      ${true="-B" false="" collapseBackwardCIGAR} \
      ${"-s " + subsamplingProportion} \
      ${"-@ " + threads} \
      ${"-o " + if defined(outputFilename) then outputFilename else "generated-6817c55e-cf83-11e9-b4cb-acde48001122.bam"} \
      ${"-T " + reference} \
      ${sam}
  }
  runtime {
    docker: "biocontainers/samtools:v1.7.0_cv3"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-6817b6f4-cf83-11e9-b4cb-acde48001122.bam"
  }
}