version development

task manta {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File? config
    File bam
    File bam_bai
    String? runDir = "generated"
    File reference
    File reference_fai
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
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
  command <<<
     \
      configManta.py \
      ~{if defined(config) then ("--config " +  '"' + config + '"') else ""} \
      --bam ~{bam} \
      ~{if defined(select_first([runDir, "generated"])) then ("--runDir " +  '"' + select_first([runDir, "generated"]) + '"') else ""} \
      --referenceFasta ~{reference} \
      ~{if defined(tumorBam) then ("--tumorBam " +  '"' + tumorBam + '"') else ""} \
      ~{true="--exome" false="" exome} \
      ~{if defined(rna) then ("--rna " +  '"' + rna + '"') else ""} \
      ~{if defined(unstrandedRNA) then ("--unstrandedRNA " +  '"' + unstrandedRNA + '"') else ""} \
      ~{if defined(outputContig) then ("--outputContig " +  '"' + outputContig + '"') else ""} \
      ~{if defined(callRegions) then ("--callRegions " +  '"' + callRegions + '"') else ""} \
      ;~{select_first([runDir, "generated"])}/runWorkflow.py \
      ~{if defined(select_first([mode, "local"])) then ("--mode " +  '"' + select_first([mode, "local"]) + '"') else ""} \
      ~{true="--quiet" false="" quiet} \
      ~{if defined(queue) then ("--queue " +  '"' + queue + '"') else ""} \
      ~{if defined(memgb) then ("--memGb " +  '"' + memgb + '"') else ""} \
      ~{if defined(maxTaskRuntime) then ("--maxTaskRuntime " +  '"' + maxTaskRuntime + '"') else ""} \
      -j ~{select_first([runtime_cpu, 1])}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    docker: "michaelfranklin/manta:1.5.0"
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File python = "~{select_first([runDir, "generated"])}/runWorkflow.py"
    File pickle = "~{select_first([runDir, "generated"])}/runWorkflow.py.config.pickle"
    File candidateSV = "~{select_first([runDir, "generated"])}/results/variants/candidateSV.vcf.gz"
    File candidateSV_tbi = "~{select_first([runDir, "generated"])}/results/variants/candidateSV.vcf.gz.tbi"
    File candidateSmallIndels = "~{select_first([runDir, "generated"])}/results/variants/candidateSmallIndels.vcf.gz"
    File candidateSmallIndels_tbi = "~{select_first([runDir, "generated"])}/results/variants/candidateSmallIndels.vcf.gz.tbi"
    File diploidSV = "~{select_first([runDir, "generated"])}/results/variants/diploidSV.vcf.gz"
    File diploidSV_tbi = "~{select_first([runDir, "generated"])}/results/variants/diploidSV.vcf.gz.tbi"
    File alignmentStatsSummary = "~{select_first([runDir, "generated"])}/results/stats/alignmentStatsSummary.txt"
    File svCandidateGenerationStats = "~{select_first([runDir, "generated"])}/results/stats/svCandidateGenerationStats.tsv"
    File svLocusGraphStats = "~{select_first([runDir, "generated"])}/results/stats/svLocusGraphStats.tsv"
  }
}