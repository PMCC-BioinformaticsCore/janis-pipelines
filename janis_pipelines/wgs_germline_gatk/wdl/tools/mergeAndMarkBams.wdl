version development

import "Gatk4MergeSamFiles.wdl" as G
import "Gatk4MarkDuplicates.wdl" as G2

workflow mergeAndMarkBams {
  input {
    Array[File] bams
    Array[File] bams_bai
    Boolean? createIndex
    Int? maxRecordsInRam
    String? sampleName
    Boolean? mergeSamFiles_useThreading
    String? mergeSamFiles_validationStringency
  }
  call G.Gatk4MergeSamFiles as mergeSamFiles {
    input:
      bams_bai=bams_bai,
      bams=bams,
      sampleName=sampleName,
      useThreading=select_first([mergeSamFiles_useThreading, true]),
      createIndex=select_first([createIndex, true]),
      maxRecordsInRam=select_first([maxRecordsInRam, 5000000]),
      validationStringency=select_first([mergeSamFiles_validationStringency, "SILENT"])
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