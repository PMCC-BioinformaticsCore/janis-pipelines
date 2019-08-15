version development

import "alignsortedbam.wdl" as A
import "fastqc.wdl" as F
import "processbamfiles.wdl" as P

workflow somatic_subpipeline {
  input {
    Array[Array[File]] inputs
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    String sampleName
    String? sortSamTmpDir
  }
  scatter (i in inputs) {
     call A.alignsortedbam as alignAndSort {
      input:
        fastq=i,
        sampleName=sampleName,
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_fai=reference_fai,
        reference_dict=reference_dict,
        reference=reference,
        sortSamTmpDir=sortSamTmpDir
    }
  }
  scatter (i in inputs) {
     call F.fastqc as fastqc {
      input:
        reads=i
    }
  }
  call P.processbamfiles as mergeAndMark {
    input:
      bams_bai=alignAndSort.out_bai,
      bams=alignAndSort.out
  }
  output {
    File out = mergeAndMark.out
    File out_bai = mergeAndMark.out_bai
    Array[Array[File]] fastq = fastqc.out
  }
}