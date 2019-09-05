version development

task manta {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File? config
    File bam
    File bam_bai
    String runDir = "generated-8bfa941c-cf9f-11e9-b76d-acde48001122"
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    File? tumorBam
    File? tumorBam_bai
    Boolean? exome
    File? rna
    File? unstrandedRNA
    File? outputContig
    File? callRegions
    File? callRegions_tbi
    String? mode
    Boolean? quiet
    String? queue
    Int? memgb
    String? maxTaskRuntime
  }
  command {
     \
      configManta.py \
      ${"--config " + config} \
      --bam ${bam} \
      ${"--runDir " + if defined(runDir) then runDir else "generated-8bfa941c-cf9f-11e9-b76d-acde48001122"} \
      --referenceFasta ${reference} \
      ${"--tumorBam " + tumorBam} \
      ${true="--exome" false="" exome} \
      ${"--rna " + rna} \
      ${"--unstrandedRNA " + unstrandedRNA} \
      ${"--outputContig " + outputContig} \
      ${"--callRegions " + callRegions} \
      ;${if defined(runDir) then runDir else "generated-8bfa941c-cf9f-11e9-b76d-acde48001122"}/runWorkflow.py \
      ${"--mode " + if defined(mode) then mode else "local"} \
      ${true="--quiet" false="" quiet} \
      ${"--queue " + queue} \
      ${"--memGb " + memgb} \
      ${"--maxTaskRuntime " + maxTaskRuntime} \
      -j ${if defined(runtime_cpu) then runtime_cpu else 1}
  }
  runtime {
    docker: "michaelfranklin/manta:1.5.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File python = "${if defined(runDir) then runDir else "generated-8bfa941c-cf9f-11e9-b76d-acde48001122"}/runWorkflow.py"
    File pickle = "${if defined(runDir) then runDir else "generated-8bfa941c-cf9f-11e9-b76d-acde48001122"}/runWorkflow.py.config.pickle"
    File candidateSV = "${if defined(runDir) then runDir else "generated-8bfa941c-cf9f-11e9-b76d-acde48001122"}/results/variants/candidateSV.vcf.gz"
    File candidateSV_tbi = "${if defined(runDir) then runDir else "generated-8bfa941c-cf9f-11e9-b76d-acde48001122"}/results/variants/candidateSV.vcf.gz.tbi"
    File candidateSmallIndels = "${if defined(runDir) then runDir else "generated-8bfa941c-cf9f-11e9-b76d-acde48001122"}/results/variants/candidateSmallIndels.vcf.gz"
    File candidateSmallIndels_tbi = "${if defined(runDir) then runDir else "generated-8bfa941c-cf9f-11e9-b76d-acde48001122"}/results/variants/candidateSmallIndels.vcf.gz.tbi"
    File diploidSV = "${if defined(runDir) then runDir else "generated-8bfa941c-cf9f-11e9-b76d-acde48001122"}/results/variants/diploidSV.vcf.gz"
    File diploidSV_tbi = "${if defined(runDir) then runDir else "generated-8bfa941c-cf9f-11e9-b76d-acde48001122"}/results/variants/diploidSV.vcf.gz.tbi"
    File alignmentStatsSummary = "${if defined(runDir) then runDir else "generated-8bfa941c-cf9f-11e9-b76d-acde48001122"}/results/stats/alignmentStatsSummary.txt"
    File svCandidateGenerationStats = "${if defined(runDir) then runDir else "generated-8bfa941c-cf9f-11e9-b76d-acde48001122"}/results/stats/svCandidateGenerationStats.tsv"
    File svLocusGraphStats = "${if defined(runDir) then runDir else "generated-8bfa941c-cf9f-11e9-b76d-acde48001122"}/results/stats/svLocusGraphStats.tsv"
  }
}