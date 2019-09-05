version development

import "tools/somatic_subpipeline.wdl" as S
import "tools/GATK4_SomaticVariantCaller.wdl" as G
import "tools/Gatk4GatherVcfs.wdl" as G2
import "tools/bcftoolssort.wdl" as B

workflow WGSSomaticGATK {
  input {
    Array[Array[File]] normalInputs
    Array[Array[File]] tumorInputs
    String? normalName
    String? tumorName
    Array[File] gatkIntervals
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    File snps_dbsnp
    File snps_dbsnp_tbi
    File snps_1000gp
    File snps_1000gp_tbi
    File known_indels
    File known_indels_tbi
    File mills_indels
    File mills_indels_tbi
  }
  call S.somatic_subpipeline as normal {
    input:
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      reads=tumorInputs,
      sampleName=select_first([tumorName, "NA24385_tumour"])
  }
  call S.somatic_subpipeline as tumor {
    input:
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      reads=normalInputs,
      sampleName=select_first([normalName, "NA24385_normal"])
  }
  scatter (g in gatkIntervals) {
     call G.GATK4_SomaticVariantCaller as variantCaller_GATK {
      input:
        normalBam_bai=tumor.out_bai,
        normalBam=tumor.out,
        tumorBam_bai=normal.out_bai,
        tumorBam=normal.out,
        normalName=select_first([normalName, "NA24385_normal"]),
        tumorName=select_first([tumorName, "NA24385_tumour"]),
        intervals=g,
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_fai=reference_fai,
        reference_dict=reference_dict,
        reference=reference,
        snps_dbsnp_tbi=snps_dbsnp_tbi,
        snps_dbsnp=snps_dbsnp,
        snps_1000gp_tbi=snps_1000gp_tbi,
        snps_1000gp=snps_1000gp,
        knownIndels_tbi=known_indels_tbi,
        knownIndels=known_indels,
        millsIndels_tbi=mills_indels_tbi,
        millsIndels=mills_indels
    }
  }
  call G2.Gatk4GatherVcfs as variantCaller_GATK_merge {
    input:
      vcfs=variantCaller_GATK.out
  }
  call B.bcftoolssort as sorted {
    input:
      vcf=variantCaller_GATK_merge.out
  }
  output {
    File normalBam = normal.out
    File normalBam_bai = normal.out_bai
    File tumorBam = tumor.out
    File tumorBam_bai = tumor.out_bai
    Array[File] normalReport = normal.reports
    Array[File] tumorReport = tumor.reports
    File variants_gatk = sorted.out
  }
}