version development

import "BwaAligner.wdl" as B
import "mergeAndMarkBams.wdl" as M
import "fastqc.wdl" as F

workflow somatic_subpipeline {
  input {
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    Array[Array[File]] reads
    String sampleName
    String? alignAndSort_sortsam_tmpDir
  }
  scatter (r in reads) {
     call B.BwaAligner as alignAndSort {
      input:
        sampleName=sampleName,
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_fai=reference_fai,
        reference_dict=reference_dict,
        reference=reference,
        fastq=r,
        sortsam_tmpDir=alignAndSort_sortsam_tmpDir
    }
  }
  call M.mergeAndMarkBams as mergeAndMark {
    input:
      bams_bai=alignAndSort.out_bai,
      bams=alignAndSort.out
  }
  scatter (r in reads) {
     call F.fastqc as fastqc {
      input:
        reads=r
    }
  }
  output {
    File out = mergeAndMark.out
    File out_bai = mergeAndMark.out_bai
    Array[Array[File]] reports = fastqc.out
  }
}