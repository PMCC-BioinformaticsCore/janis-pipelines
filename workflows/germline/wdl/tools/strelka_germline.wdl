version development

task strelka_germline {
  input {
    Int? runtime_cpu
    Int? runtime_memory
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
    String? relativeStrelkaDirectory
    File? ploidy
    File? ploidy_tbi
    File? noCompress
    File? noCompress_tbi
    String? callContinuousVf
    Boolean? rna
    File? indelCandidates
    File? indelCandidates_tbi
    File? forcedGT
    File? forcedGT_tbi
    File? exome
    File? callRegions
    File? callRegions_tbi
    String? mode
    String? queue
    String? memGb
    Boolean? quiet
    String? mailTo
  }
  command {
     \
      ${"--callContinuousVf " + callContinuousVf} \
      configureStrelkaGermlineWorkflow.py \
      --bam ${bam} \
      --referenceFasta ${reference} \
      ${"--runDir " + if defined(relativeStrelkaDirectory) then relativeStrelkaDirectory else "strelka_dir"} \
      ${"--ploidy " + ploidy} \
      ${"--noCompress " + noCompress} \
      ${true="--rna" false="" rna} \
      ${"--indelCandidates " + indelCandidates} \
      ${"--forcedGT " + forcedGT} \
      ${"--exome " + exome} \
      ${"--callRegions=" + callRegions} \
      ;${if defined(relativeStrelkaDirectory) then relativeStrelkaDirectory else "strelka_dir"}/runWorkflow.py \
      ${"--mode " + if defined(mode) then mode else "local"} \
      ${"--queue " + queue} \
      ${"--memGb " + memGb} \
      ${true="--quiet" false="" quiet} \
      ${"--mailTo " + mailTo} \
      --jobs ${if defined(runtime_cpu) then runtime_cpu else 1}
  }
  runtime {
    docker: "michaelfranklin/strelka:2.9.10"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File configPickle = "${if defined(relativeStrelkaDirectory) then relativeStrelkaDirectory else "strelka_dir"}/runWorkflow.py.config.pickle"
    File script = "${if defined(relativeStrelkaDirectory) then relativeStrelkaDirectory else "strelka_dir"}/runWorkflow.py"
    File stats = "${if defined(relativeStrelkaDirectory) then relativeStrelkaDirectory else "strelka_dir"}/results/stats/runStats.tsv"
    File variants = "${if defined(relativeStrelkaDirectory) then relativeStrelkaDirectory else "strelka_dir"}/results/variants/variants.vcf.gz"
    File variants_tbi = "${if defined(relativeStrelkaDirectory) then relativeStrelkaDirectory else "strelka_dir"}/results/variants/variants.vcf.gz.tbi"
    File genome = "${if defined(relativeStrelkaDirectory) then relativeStrelkaDirectory else "strelka_dir"}/results/variants/genome.vcf.gz"
    File genome_tbi = "${if defined(relativeStrelkaDirectory) then relativeStrelkaDirectory else "strelka_dir"}/results/variants/genome.vcf.gz.tbi"
  }
}