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
    String rundir = "generated-f8d2cc6a-cf83-11e9-8e32-acde48001122"
    File? region
    File? config
    File? outputcallableregions
    File? indelCandidates
    File? indelCandidates_tbi
    File? forcedgt
    Boolean? targeted
    File? callRegions
    File? callRegions_tbi
    File? noisevcf
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
  command {
     \
      'configureStrelkaSomaticWorkflow.py' \
      --normalBam=${normalBam} \
      --tumourBam=${tumorBam} \
      --referenceFasta=${reference} \
      ${"--runDir=" + if defined(rundir) then rundir else "generated-f8d2f51e-cf83-11e9-8e32-acde48001122"} \
      ${"--region=" + region} \
      ${"--config=" + config} \
      ${"--outputCallableRegions " + outputcallableregions} \
      ${"--indelCandidates=" + indelCandidates} \
      ${"--forcedGT=" + forcedgt} \
      ${true="--targeted" false="" targeted} \
      ${"--callRegions=" + callRegions} \
      ${"--noiseVcf=" + noisevcf} \
      ${"--scanSizeMb=" + scansizemb} \
      ${"--callMemMb=" + callmemmb} \
      ${true="--retainTempFiles" false="" if defined(retaintempfiles) then retaintempfiles else false} \
      ${true="--disableEVS" false="" disableevs} \
      ${true="--reportEVSFeatures" false="" reportevsfeatures} \
      ${"--snvScoringModelFile=" + snvscoringmodelfile} \
      ${"--indelScoringModelFile=" + indelscoringmodelfile} \
      ;${if defined(rundir) then rundir else "generated-f8d2cc6a-cf83-11e9-8e32-acde48001122"}/runWorkflow.py \
      ${"--mode " + if defined(mode) then mode else "local"} \
      ${"--queue " + queue} \
      ${"--memGb " + memGb} \
      ${true="--quiet" false="" quiet} \
      --jobs ${if defined(runtime_cpu) then runtime_cpu else 1}
  }
  runtime {
    docker: "michaelfranklin/strelka:2.9.10"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File configPickle = "${if defined(rundir) then rundir else "generated-f8d2cc6a-cf83-11e9-8e32-acde48001122"}/runWorkflow.py.config.pickle"
    File script = "${if defined(rundir) then rundir else "generated-f8d2cc6a-cf83-11e9-8e32-acde48001122"}/runWorkflow.py"
    File stats = "${if defined(rundir) then rundir else "generated-f8d2cc6a-cf83-11e9-8e32-acde48001122"}/results/stats/runStats.tsv"
    File indels = "${if defined(rundir) then rundir else "generated-f8d2cc6a-cf83-11e9-8e32-acde48001122"}/results/variants/somatic.indels.vcf.gz"
    File indels_tbi = "${if defined(rundir) then rundir else "generated-f8d2cc6a-cf83-11e9-8e32-acde48001122"}/results/variants/somatic.indels.vcf.gz.tbi"
    File snvs = "${if defined(rundir) then rundir else "generated-f8d2cc6a-cf83-11e9-8e32-acde48001122"}/results/variants/somatic.snvs.vcf.gz"
    File snvs_tbi = "${if defined(rundir) then rundir else "generated-f8d2cc6a-cf83-11e9-8e32-acde48001122"}/results/variants/somatic.snvs.vcf.gz.tbi"
  }
}