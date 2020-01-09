version development

import "fastqc.wdl" as F
import "ParseFastqcAdaptors.wdl" as P
import "BwaAligner.wdl" as B
import "mergeAndMarkBams.wdl" as M

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
    File cutadapt_adapters
    String sampleName
    String? alignAndSort_sortsam_tmpDir
  }
  scatter (r in reads) {
     call F.fastqc as fastqc {
      input:
        reads=r
    }
  }
  scatter (d in fastqc.datafile) {
     call P.ParseFastqcAdaptors as getfastqc_adapters {
      input:
        fastqc_datafiles=d,
        cutadapt_adaptors_lookup=cutadapt_adapters
    }
  }
  scatter (Q in zip(reads, zip(getfastqc_adapters.adaptor_sequences, getfastqc_adapters.adaptor_sequences))) {
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
        fastq=Q.left,
        cutadapt_adapter=Q.right.right,
        cutadapt_removeMiddle3Adapter=Q.right.right,
        sortsam_tmpDir=alignAndSort_sortsam_tmpDir
    }
  }
  call M.mergeAndMarkBams as mergeAndMark {
    input:
      bams_bai=alignAndSort.out_bai,
      bams=alignAndSort.out
  }
  output {
    File out = mergeAndMark.out
    File out_bai = mergeAndMark.out_bai
    Array[Array[File]] reports = fastqc.out
  }
}