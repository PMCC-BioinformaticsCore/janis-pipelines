version development

import "SamToolsView.wdl" as S
import "gridss.wdl" as G

workflow gridssGermlineVariantCaller {
  input {
    File bam
    File bam_bai
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    File blacklist
    String? samtools_doNotOutputAlignmentsWithBitsSet
  }
  call S.SamToolsView as samtools {
    input:
      doNotOutputAlignmentsWithBitsSet=select_first([samtools_doNotOutputAlignmentsWithBitsSet, "0x100"]),
      sam=bam
  }
  call G.gridss as gridss {
    input:
      bams=[samtools.out],
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      blacklist=blacklist
  }
  output {
    File out = gridss.out
    File assembly = gridss.assembly
  }
}