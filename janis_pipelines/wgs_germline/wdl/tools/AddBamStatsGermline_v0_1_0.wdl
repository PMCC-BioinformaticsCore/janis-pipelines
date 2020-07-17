version development

import "SamToolsMpileup_1_9_0.wdl" as S
import "addBamStats_0_0_7.wdl" as A

workflow AddBamStatsGermline {
  input {
    File bam
    File bam_bai
    File vcf
    Boolean? samtoolsmpileup_countOrphans = true
    Boolean? samtoolsmpileup_noBAQ = true
    Int? samtoolsmpileup_minBQ = 0
    Int? samtoolsmpileup_maxDepth = 10000
    String? addbamstats_type = "germline"
  }
  call S.SamToolsMpileup as samtoolsmpileup {
    input:
      countOrphans=select_first([samtoolsmpileup_countOrphans, true]),
      noBAQ=select_first([samtoolsmpileup_noBAQ, true]),
      maxDepth=select_first([samtoolsmpileup_maxDepth, 10000]),
      positions=vcf,
      minBQ=select_first([samtoolsmpileup_minBQ, 0]),
      bam=bam,
      bam_bai=bam_bai
  }
  call A.addBamStats as addbamstats {
    input:
      mpileup=samtoolsmpileup.out,
      inputVcf=vcf,
      type=select_first([addbamstats_type, "germline"])
  }
  output {
    File out = addbamstats.out
  }
}