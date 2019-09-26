version development

import "cutadapt.wdl" as C
import "BwaMemSamtoolsView.wdl" as B
import "gatk4sortsam.wdl" as G

workflow BwaAligner {
  input {
    String name
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    Array[File] fastq
    String? cutadapt_adapter
    String? cutadapt_adapter_g
    String? cutadapt_removeMiddle5Adapter
    String? cutadapt_removeMiddle3Adapter
    Int? cutadapt_qualityCutoff
    Int? cutadapt_minReadLength
    Boolean? bwamem_markShorterSplits
    String? sortsam_sortOrder
    Boolean? sortsam_createIndex
    String? sortsam_validationStringency
    Int? sortsam_maxRecordsInRam
    String? sortsam_tmpDir
  }
  call C.cutadapt as cutadapt {
    input:
      fastq=fastq,
      adapter=cutadapt_adapter,
      adapter_g=cutadapt_adapter_g,
      qualityCutoff=select_first([cutadapt_qualityCutoff, 15]),
      minReadLength=select_first([cutadapt_minReadLength, 50]),
      removeMiddle3Adapter=cutadapt_removeMiddle3Adapter,
      removeMiddle5Adapter=cutadapt_removeMiddle5Adapter
  }
  call B.BwaMemSamtoolsView as bwamem {
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
      sampleName=name,
      markShorterSplits=select_first([bwamem_markShorterSplits, true])
  }
  call G.gatk4sortsam as sortsam {
    input:
      bam=bwamem.out,
      sortOrder=select_first([sortsam_sortOrder, "coordinate"]),
      createIndex=select_first([sortsam_createIndex, true]),
      maxRecordsInRam=select_first([sortsam_maxRecordsInRam, 5000000]),
      tmpDir=select_first([sortsam_tmpDir, "."]),
      validationStringency=select_first([sortsam_validationStringency, "SILENT"])
  }
  output {
    File out = sortsam.out
    File out_bai = sortsam.out_bai
  }
}