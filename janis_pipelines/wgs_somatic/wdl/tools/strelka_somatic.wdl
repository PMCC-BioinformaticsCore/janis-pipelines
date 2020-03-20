version development

task strelka_somatic {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File normalBam
    File normalBam_bai
    File tumorBam
    File tumorBam_bai
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    String? rundir = "generated"
    Array[String]? region
    File? config
    Boolean? outputcallableregions
    Array[File]? indelCandidates
    Array[File]? indelCandidates_tbi
    Array[File]? forcedgt
    Array[File]? forcedgt_tbi
    Boolean? targeted
    Boolean? exome
    File? callRegions
    File? callRegions_tbi
    File? noisevcf
    File? noisevcf_tbi
    Int? scansizemb
    Int? callmemmb
    Boolean? retaintempfiles
    Boolean? disableevs
    Boolean? reportevsfeatures
    File? snvscoringmodelfile
    File? indelscoringmodelfile
    String? mode
    String? queue
    String? memGb
    Boolean? quiet
  }
  command <<<
     \
      'configureStrelkaSomaticWorkflow.py' \
      --normalBam=~{normalBam} \
      --tumourBam=~{tumorBam} \
      --referenceFasta=~{reference} \
      ~{if defined(select_first([rundir, "generated"])) then ('"' + "--runDir=" + select_first([rundir, "generated"]) + '"') else ""} \
      ~{if defined(region) && length(select_first([region, []])) > 0 then "--region " else ""}~{sep=" --region " region} \
      ~{if defined(config) then ('"' + "--config=" + config + '"') else ""} \
      ~{true="--outputCallableRegions" false="" outputcallableregions} \
      ~{if defined(indelCandidates) && length(select_first([indelCandidates, []])) > 0 then "--indelCandidates=" else ""}~{sep=" --indelCandidates=" indelCandidates} \
      ~{if defined(forcedgt) && length(select_first([forcedgt, []])) > 0 then "--forcedGT=" else ""}~{sep=" --forcedGT=" forcedgt} \
      ~{true="--targeted" false="" targeted} \
      ~{true="--exome" false="" exome} \
      ~{if defined(callRegions) then ('"' + "--callRegions=" + callRegions + '"') else ""} \
      ~{if defined(noisevcf) then ('"' + "--noiseVcf=" + noisevcf + '"') else ""} \
      ~{if defined(scansizemb) then ('"' + "--scanSizeMb=" + scansizemb + '"') else ""} \
      ~{if defined(callmemmb) then ('"' + "--callMemMb=" + callmemmb + '"') else ""} \
      ~{true="--retainTempFiles" false="" select_first([retaintempfiles, false])} \
      ~{true="--disableEVS" false="" disableevs} \
      ~{true="--reportEVSFeatures" false="" reportevsfeatures} \
      ~{if defined(snvscoringmodelfile) then ('"' + "--snvScoringModelFile=" + snvscoringmodelfile + '"') else ""} \
      ~{if defined(indelscoringmodelfile) then ('"' + "--indelScoringModelFile=" + indelscoringmodelfile + '"') else ""} \
      ;~{select_first([rundir, "generated"])}/runWorkflow.py \
      ~{if defined(select_first([mode, "local"])) then ("--mode " +  '"' + select_first([mode, "local"]) + '"') else ""} \
      ~{if defined(queue) then ("--queue " +  '"' + queue + '"') else ""} \
      ~{if defined(memGb) then ("--memGb " +  '"' + memGb + '"') else ""} \
      ~{true="--quiet" false="" quiet} \
      --jobs ~{select_first([runtime_cpu, 1])}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    docker: "michaelfranklin/strelka:2.9.10"
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File configPickle = "~{select_first([rundir, "generated"])}/runWorkflow.py.config.pickle"
    File script = "~{select_first([rundir, "generated"])}/runWorkflow.py"
    File stats = "~{select_first([rundir, "generated"])}/results/stats/runStats.tsv"
    File indels = "~{select_first([rundir, "generated"])}/results/variants/somatic.indels.vcf.gz"
    File indels_tbi = "~{select_first([rundir, "generated"])}/results/variants/somatic.indels.vcf.gz.tbi"
    File snvs = "~{select_first([rundir, "generated"])}/results/variants/somatic.snvs.vcf.gz"
    File snvs_tbi = "~{select_first([rundir, "generated"])}/results/variants/somatic.snvs.vcf.gz.tbi"
  }
}