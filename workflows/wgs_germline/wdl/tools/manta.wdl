version development

task manta {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File? config
    File bam
    File bam_bai
    String runDir = "generated-d5d49306-e018-11e9-851b-a0cec8186c53"
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
    if [ $(dirname "${bam_bai}") != $(dirname "bam") ]; then mv ${bam_bai} $(dirname ${bam}); fi
    if [ $(dirname "${reference_amb}") != $(dirname "reference") ]; then mv ${reference_amb} $(dirname ${reference}); fi
    if [ $(dirname "${reference_ann}") != $(dirname "reference") ]; then mv ${reference_ann} $(dirname ${reference}); fi
    if [ $(dirname "${reference_bwt}") != $(dirname "reference") ]; then mv ${reference_bwt} $(dirname ${reference}); fi
    if [ $(dirname "${reference_pac}") != $(dirname "reference") ]; then mv ${reference_pac} $(dirname ${reference}); fi
    if [ $(dirname "${reference_sa}") != $(dirname "reference") ]; then mv ${reference_sa} $(dirname ${reference}); fi
    if [ $(dirname "${reference_fai}") != $(dirname "reference") ]; then mv ${reference_fai} $(dirname ${reference}); fi
    if [ $(dirname "${reference_dict}") != $(dirname "reference") ]; then mv ${reference_dict} $(dirname ${reference}); fi
    if [ $(dirname "${tumorBam_bai}") != $(dirname "tumorBam") ]; then mv ${tumorBam_bai} $(dirname ${tumorBam}); fi
    if [ $(dirname "${callRegions_tbi}") != $(dirname "callRegions") ]; then mv ${callRegions_tbi} $(dirname ${callRegions}); fi
     \
      configManta.py \
      ${"--config " + config} \
      --bam ${bam} \
      ${"--runDir " + if defined(runDir) then runDir else "generated-d5d49306-e018-11e9-851b-a0cec8186c53"} \
      --referenceFasta ${reference} \
      ${"--tumorBam " + tumorBam} \
      ${true="--exome" false="" exome} \
      ${"--rna " + rna} \
      ${"--unstrandedRNA " + unstrandedRNA} \
      ${"--outputContig " + outputContig} \
      ${"--callRegions " + callRegions} \
      ;${if defined(runDir) then runDir else "generated-d5d49306-e018-11e9-851b-a0cec8186c53"}/runWorkflow.py \
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
    File python = "${if defined(runDir) then runDir else "generated-d5d49306-e018-11e9-851b-a0cec8186c53"}/runWorkflow.py"
    File pickle = "${if defined(runDir) then runDir else "generated-d5d49306-e018-11e9-851b-a0cec8186c53"}/runWorkflow.py.config.pickle"
    File candidateSV = "${if defined(runDir) then runDir else "generated-d5d49306-e018-11e9-851b-a0cec8186c53"}/results/variants/candidateSV.vcf.gz"
    File candidateSV_tbi = "${if defined(runDir) then runDir else "generated-d5d49306-e018-11e9-851b-a0cec8186c53"}/results/variants/candidateSV.vcf.gz.tbi"
    File candidateSmallIndels = "${if defined(runDir) then runDir else "generated-d5d49306-e018-11e9-851b-a0cec8186c53"}/results/variants/candidateSmallIndels.vcf.gz"
    File candidateSmallIndels_tbi = "${if defined(runDir) then runDir else "generated-d5d49306-e018-11e9-851b-a0cec8186c53"}/results/variants/candidateSmallIndels.vcf.gz.tbi"
    File diploidSV = "${if defined(runDir) then runDir else "generated-d5d49306-e018-11e9-851b-a0cec8186c53"}/results/variants/diploidSV.vcf.gz"
    File diploidSV_tbi = "${if defined(runDir) then runDir else "generated-d5d49306-e018-11e9-851b-a0cec8186c53"}/results/variants/diploidSV.vcf.gz.tbi"
    File alignmentStatsSummary = "${if defined(runDir) then runDir else "generated-d5d49306-e018-11e9-851b-a0cec8186c53"}/results/stats/alignmentStatsSummary.txt"
    File svCandidateGenerationStats = "${if defined(runDir) then runDir else "generated-d5d49306-e018-11e9-851b-a0cec8186c53"}/results/stats/svCandidateGenerationStats.tsv"
    File svLocusGraphStats = "${if defined(runDir) then runDir else "generated-d5d49306-e018-11e9-851b-a0cec8186c53"}/results/stats/svLocusGraphStats.tsv"
  }
}