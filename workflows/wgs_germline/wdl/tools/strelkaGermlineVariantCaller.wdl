version development

import "manta.wdl" as M
import "strelka_germline.wdl" as S
import "bcftoolsview.wdl" as B
import "SplitMultiAllele.wdl" as S2

workflow strelkaGermlineVariantCaller {
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
    File? intervals
    File? intervals_tbi
    Array[String]? bcfview_applyFilters
  }
  call M.manta as manta {
    input:
      bam_bai=bam_bai,
      bam=bam,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      callRegions_tbi=intervals_tbi,
      callRegions=intervals
  }
  call S.strelka_germline as strelka {
    input:
      bam_bai=bam_bai,
      bam=bam,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      indelCandidates_tbi=manta.candidateSmallIndels_tbi,
      indelCandidates=manta.candidateSmallIndels,
      callRegions_tbi=intervals_tbi,
      callRegions=intervals
  }
  call B.bcftoolsview as bcfview {
    input:
      file=strelka.variants,
      applyFilters=select_first([bcfview_applyFilters, ["PASS"]])
  }
  call S2.SplitMultiAllele as splitMultiAllele {
    input:
      vcf=bcfview.out,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference
  }
  output {
    File diploid = manta.diploidSV
    File diploid_tbi = manta.diploidSV_tbi
    File variants = strelka.variants
    File variants_tbi = strelka.variants_tbi
    File out = splitMultiAllele.out
  }
}