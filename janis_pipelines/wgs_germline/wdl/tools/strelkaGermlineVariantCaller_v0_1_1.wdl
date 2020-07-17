version development

import "manta_1_5_0.wdl" as M
import "strelka_germline_2_9_10.wdl" as S
import "UncompressArchive_v1_0_0.wdl" as U
import "SplitMultiAllele_v0_5772.wdl" as S2
import "VcfTools_0_1_16.wdl" as V

workflow strelkaGermlineVariantCaller {
  input {
    File bam
    File bam_bai
    File reference
    File reference_fai
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_dict
    File? intervals
    File? intervals_tbi
    Boolean? is_exome
    Boolean? filterpass_removeFileteredAll = true
    Boolean? filterpass_recode = true
    Boolean? filterpass_recodeINFOAll = true
  }
  call M.manta as manta {
    input:
      bam=bam,
      bam_bai=bam_bai,
      reference=reference,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      exome=is_exome,
      callRegions=intervals,
      callRegions_tbi=intervals_tbi
  }
  call S.strelka_germline as strelka {
    input:
      bam=bam,
      bam_bai=bam_bai,
      reference=reference,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      indelCandidates=manta.candidateSmallIndels,
      indelCandidates_tbi=manta.candidateSmallIndels_tbi,
      exome=is_exome,
      callRegions=intervals,
      callRegions_tbi=intervals_tbi
  }
  call U.UncompressArchive as uncompressvcf {
    input:
      file=strelka.variants
  }
  call S2.SplitMultiAllele as splitnormalisevcf {
    input:
      vcf=uncompressvcf.out,
      reference=reference,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict
  }
  call V.VcfTools as filterpass {
    input:
      vcf=splitnormalisevcf.out,
      removeFileteredAll=select_first([filterpass_removeFileteredAll, true]),
      recode=select_first([filterpass_recode, true]),
      recodeINFOAll=select_first([filterpass_recodeINFOAll, true])
  }
  output {
    File sv = manta.diploidSV
    File sv_tbi = manta.diploidSV_tbi
    File variants = strelka.variants
    File variants_tbi = strelka.variants_tbi
    File out = filterpass.out
  }
}