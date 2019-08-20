version development

import "Gatk4MergeSamFiles.wdl" as G
import "Gatk4MarkDuplicates.wdl" as G2

workflow mergeAndMarkBams {
  input {
    Array[File] bams
    Array[File] bams_bai
    Boolean? useThreading
    Boolean? createIndex
    Int? maxRecordsInRam
    String? validationStringency
  }
  call G.Gatk4MergeSamFiles as mergeSamFiles {
    input:
      bams_bai=bams_bai,
      bams=bams,
      useThreading=select_first([useThreading, true]),
      createIndex=select_first([createIndex, true]),
      maxRecordsInRam=select_first([maxRecordsInRam, 5000000]),
      validationStringency=select_first([validationStringency, "SILENT"])
  }
  call G2.Gatk4MarkDuplicates as markDuplicates {
    input:
      bam_bai=mergeSamFiles.out_bai,
      bam=mergeSamFiles.out,
      createIndex=select_first([createIndex, true]),
      maxRecordsInRam=select_first([maxRecordsInRam, 5000000])
  }
  output {
    File out = markDuplicates.out
    File out_bai = markDuplicates.out_bai
  }
}