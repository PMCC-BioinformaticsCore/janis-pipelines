version development

import "fastqc.wdl" as F
import "ParseFastqcAdaptors.wdl" as P
import "BwaAligner.wdl" as B
import "mergeAndMarkBams.wdl" as M

workflow somatic_subpipeline {
  input {
    File reference
    File reference_fai
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_dict
    Array[Array[File]] reads
    File? cutadapt_adapters
    String sample_name
    String? align_and_sort_sortsam_tmpDir
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
     call B.BwaAligner as align_and_sort {
      input:
        sample_name=sample_name,
        reference_fai=reference_fai,
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_dict=reference_dict,
        reference=reference,
        fastq=Q.left,
        cutadapt_adapter=Q.right.right,
        cutadapt_removeMiddle3Adapter=Q.right.right,
        sortsam_tmpDir=align_and_sort_sortsam_tmpDir
    }
  }
  call M.mergeAndMarkBams as merge_and_mark {
    input:
      bams_bai=align_and_sort.out_bai,
      bams=align_and_sort.out,
      sampleName=sample_name
  }
  output {
    File out = merge_and_mark.out
    File out_bai = merge_and_mark.out_bai
    Array[Array[File]] reports = fastqc.out
  }
}