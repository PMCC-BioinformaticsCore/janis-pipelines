version development

import "cutadapt.wdl" as C
import "BwaMemSamtoolsView.wdl" as B
import "gatk4sortsam.wdl" as G

workflow alignsortedbam {
  input {
    Array[File] fastq
    String? adapter
    String? adapter_g
    String? removeMiddle5Adapter
    String? removeMiddle3Adapter
    Int? qualityCutoff
    Int? minReadLength
    String sampleName
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    String? sortOrder
    Boolean? createIndex
    String? validationStringency
    Int? maxRecordsInRam
    String? sortSamTmpDir
  }
  call C.cutadapt as cutadapt {
    input:
      fastq=fastq,
      adapter=adapter,
      adapter_g=adapter_g,
      qualityCutoff=select_first([qualityCutoff, 15]),
      minReadLength=select_first([minReadLength, 50]),
      removeMiddle3Adapter=removeMiddle3Adapter,
      removeMiddle5Adapter=removeMiddle5Adapter
  }
  call B.BwaMemSamtoolsView as bwa_sam {
    input:
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      reads=cutadapt.out,
      sampleName=sampleName
  }
  call G.gatk4sortsam as sortsam {
    input:
      bam=bwa_sam.out,
      sortOrder=select_first([sortOrder, "coordinate"]),
      createIndex=select_first([createIndex, true]),
      maxRecordsInRam=select_first([maxRecordsInRam, 5000000]),
      tmpDir=sortSamTmpDir,
      validationStringency=select_first([validationStringency, "SILENT"])
  }
  output {
    File out_bwa = bwa_sam.out
    File out = sortsam.out
    File out_bai = sortsam.out_bai
  }
}