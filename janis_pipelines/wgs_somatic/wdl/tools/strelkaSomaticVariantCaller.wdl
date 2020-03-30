version development

import "manta.wdl" as M
import "strelka_somatic.wdl" as S
import "bcftoolsview.wdl" as B
import "SplitMultiAllele.wdl" as S2

workflow strelkaSomaticVariantCaller {
  input {
    File normal_bam
    File normal_bam_bai
    File tumor_bam
    File tumor_bam_bai
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
    Array[String]? bcf_view_applyFilters
  }
  call M.manta as manta {
    input:
      bam_bai=normal_bam_bai,
      bam=normal_bam,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference,
      tumorBam_bai=tumor_bam_bai,
      tumorBam=tumor_bam,
      exome=is_exome,
      callRegions_tbi=intervals_tbi,
      callRegions=intervals
  }
  call S.strelka_somatic as strelka {
    input:
      normalBam_bai=normal_bam_bai,
      normalBam=normal_bam,
      tumorBam_bai=tumor_bam_bai,
      tumorBam=tumor_bam,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference,
      indelCandidates_tbi=[manta.candidateSmallIndels_tbi],
      indelCandidates=[manta.candidateSmallIndels],
      exome=is_exome,
      callRegions_tbi=intervals_tbi,
      callRegions=intervals
  }
  call B.bcftoolsview as bcf_view {
    input:
      file=strelka.snvs,
      applyFilters=select_first([bcf_view_applyFilters, ["PASS"]])
  }
  call S2.SplitMultiAllele as split_multi_allele {
    input:
      vcf=bcf_view.out,
      reference_fai=reference_fai,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_dict=reference_dict,
      reference=reference
  }
  output {
    File diploid = manta.diploidSV
    File diploid_tbi = manta.diploidSV_tbi
    File variants = strelka.snvs
    File variants_tbi = strelka.snvs_tbi
    File out = split_multi_allele.out
  }
}