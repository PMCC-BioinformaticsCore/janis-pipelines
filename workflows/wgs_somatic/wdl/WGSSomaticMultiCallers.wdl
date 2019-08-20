version development

import "tools/somatic_subpipeline.wdl" as S
import "tools/GATK4_SomaticVariantCaller.wdl" as G
import "tools/Gatk4GatherVcfs.wdl" as G2
import "tools/strelkaSomaticVariantCaller.wdl" as S2
import "tools/vardictSomaticVariantCaller.wdl" as V
import "tools/combinevariants.wdl" as C
import "tools/bcftoolssort.wdl" as B

workflow WGSSomaticMultiCallers {
  input {
    Array[Array[File]] normalInputs
    String normalName
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    String? sortSamTmpDir
    Array[Array[File]] tumorInputs
    String tumorName
    Array[File] gatkIntervals
    File snps_dbsnp
    File snps_dbsnp_tbi
    File snps_1000gp
    File snps_1000gp_tbi
    File known_indels
    File known_indels_tbi
    File mills_1000gp_indels
    File mills_1000gp_indels_tbi
    File? strelkaIntervals
    File? strelkaIntervals_tbi
    File vardictHeaderLines
    Array[File] vardictIntervals
    Float allelFreqThreshold
    String? variant_type
    Array[String]? columns
  }
  call S.somatic_subpipeline as normal {
    input:
      inputs=normalInputs,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      sampleName=normalName,
      sortSamTmpDir=sortSamTmpDir
  }
  call S.somatic_subpipeline as tumor {
    input:
      inputs=tumorInputs,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      sampleName=tumorName,
      sortSamTmpDir=sortSamTmpDir
  }
  scatter (g in gatkIntervals) {
     call G.GATK4_SomaticVariantCaller as GATK_VariantCaller {
      input:
        normalBam_bai=normal.out_bai,
        normalBam=normal.out,
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
        millsIndels_tbi=mills_1000gp_indels_tbi,
        millsIndels=mills_1000gp_indels,
        tumorBam_bai=tumor.out_bai,
        tumorBam=tumor.out,
        normalName=normalName,
        tumorName=tumorName
    }
  }
  call G2.Gatk4GatherVcfs as variantCaller_merge_GATK {
    input:
      vcfs=[GATK_VariantCaller.out]
  }
  call S2.strelkaSomaticVariantCaller as Strelka_VariantCaller {
    input:
      normalBam_bai=normal.out_bai,
      normalBam=normal.out,
      tumorBam_bai=tumor.out_bai,
      tumorBam=tumor.out,
      reference_amb=reference_amb,
      reference_ann=reference_ann,
      reference_bwt=reference_bwt,
      reference_pac=reference_pac,
      reference_sa=reference_sa,
      reference_fai=reference_fai,
      reference_dict=reference_dict,
      reference=reference,
      intervals_tbi=strelkaIntervals_tbi,
      intervals=strelkaIntervals
  }
  scatter (v in vardictIntervals) {
     call V.vardictSomaticVariantCaller as VarDict_VariantCaller {
      input:
        normalBam_bai=normal.out_bai,
        normalBam=normal.out,
        tumorBam_bai=tumor.out_bai,
        tumorBam=tumor.out,
        intervals=v,
        reference_amb=reference_amb,
        reference_ann=reference_ann,
        reference_bwt=reference_bwt,
        reference_pac=reference_pac,
        reference_sa=reference_sa,
        reference_fai=reference_fai,
        reference_dict=reference_dict,
        reference=reference,
        normalName=normalName,
        tumorName=tumorName,
        alleleFreqThreshold=allelFreqThreshold,
        headerLines=vardictHeaderLines
    }
  }
  call G2.Gatk4GatherVcfs as variantCaller_merge_Vardict {
    input:
      vcfs=[VarDict_VariantCaller.out]
  }
  call C.combinevariants as combineVariants {
    input:
      vcfs=[variantCaller_merge_GATK.out, Strelka_VariantCaller.out, variantCaller_merge_Vardict.out],
      type=select_first([variant_type, "somatic"]),
      columns=select_first([columns, ["AD", "DP", "GT"]]),
      normal=normalName,
      tumor=tumorName
  }
  call B.bcftoolssort as sortCombined {
    input:
      vcf=combineVariants.vcf
  }
  output {
    File normalBam = normal.out
    File normalBam_bai = normal.out_bai
    File tumorBam = tumor.out
    File tumorBam_bai = tumor.out_bai
    Array[Array[File]] normalReport = normal.fastq
    Array[Array[File]] tumorReport = tumor.fastq
    File variants_strelka = Strelka_VariantCaller.out
    File variants_vardict = variantCaller_merge_Vardict.out
    File variants_gatk = variantCaller_merge_GATK.out
    File variants_combined = sortCombined.out
  }
}