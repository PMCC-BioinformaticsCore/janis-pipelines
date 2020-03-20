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
    Boolean? exome
    Boolean? targeted
    File? callRegions
    File? callRegions_tbi
    String? mode
    String? queue
    String? memGb
    Boolean? quiet
    String? mailTo
  }
  command <<<
     \
      ~{if defined(callContinuousVf) then ("--callContinuousVf " +  '"' + callContinuousVf + '"') else ""} \
      configureStrelkaGermlineWorkflow.py \
      --bam ~{bam} \
      --referenceFasta ~{reference} \
      ~{if defined(select_first([relativeStrelkaDirectory, "strelka_dir"])) then ("--runDir " +  '"' + select_first([relativeStrelkaDirectory, "strelka_dir"]) + '"') else ""} \
      ~{if defined(ploidy) then ("--ploidy " +  '"' + ploidy + '"') else ""} \
      ~{if defined(noCompress) then ("--noCompress " +  '"' + noCompress + '"') else ""} \
      ~{true="--rna" false="" rna} \
      ~{if defined(indelCandidates) then ("--indelCandidates " +  '"' + indelCandidates + '"') else ""} \
      ~{if defined(forcedGT) then ("--forcedGT " +  '"' + forcedGT + '"') else ""} \
      ~{true="--exome" false="" exome} \
      ~{true="--exome" false="" targeted} \
      ~{if defined(callRegions) then ('"' + "--callRegions=" + callRegions + '"') else ""} \
      ;~{select_first([relativeStrelkaDirectory, "strelka_dir"])}/runWorkflow.py \
      ~{if defined(select_first([mode, "local"])) then ("--mode " +  '"' + select_first([mode, "local"]) + '"') else ""} \
      ~{if defined(queue) then ("--queue " +  '"' + queue + '"') else ""} \
      ~{if defined(memGb) then ("--memGb " +  '"' + memGb + '"') else ""} \
      ~{true="--quiet" false="" quiet} \
      ~{if defined(mailTo) then ("--mailTo " +  '"' + mailTo + '"') else ""} \
      --jobs ~{select_first([runtime_cpu, 1])}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    docker: "michaelfranklin/strelka:2.9.10"
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File configPickle = "~{select_first([relativeStrelkaDirectory, "strelka_dir"])}/runWorkflow.py.config.pickle"
    File script = "~{select_first([relativeStrelkaDirectory, "strelka_dir"])}/runWorkflow.py"
    File stats = "~{select_first([relativeStrelkaDirectory, "strelka_dir"])}/results/stats/runStats.tsv"
    File variants = "~{select_first([relativeStrelkaDirectory, "strelka_dir"])}/results/variants/variants.vcf.gz"
    File variants_tbi = "~{select_first([relativeStrelkaDirectory, "strelka_dir"])}/results/variants/variants.vcf.gz.tbi"
    File genome = "~{select_first([relativeStrelkaDirectory, "strelka_dir"])}/results/variants/genome.vcf.gz"
    File genome_tbi = "~{select_first([relativeStrelkaDirectory, "strelka_dir"])}/results/variants/genome.vcf.gz.tbi"
  }
}