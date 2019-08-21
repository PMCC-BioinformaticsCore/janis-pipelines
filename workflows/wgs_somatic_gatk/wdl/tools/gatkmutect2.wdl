version development

task gatkmutect2 {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File tumor
    File tumor_bai
    String tumorName
    File normal
    File normal_bai
    String normalName
    File? intervals
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    String outputFilename = "generated-50148304-c3b0-11e9-9ec0-f218985ebfa7.vcf.gz"
    File? germlineResource
    File? germlineResource_idx
    Float? afOfAllelesNotInResource
    File? panelOfNormals
    File? panelOfNormals_idx
  }
  command {
    gatk Mutect2 \
      -I ${normal} \
      -I ${tumor} \
      -tumor ${tumorName} \
      -normal ${normalName} \
      ${"-L " + intervals} \
      -R ${reference} \
      ${"--germline-resource " + germlineResource} \
      ${"--panel-of-normals " + panelOfNormals} \
      ${"--af-of-alleles-not-in-resource " + afOfAllelesNotInResource} \
      ${"-O " + if defined(outputFilename) then outputFilename else "generated-50148aa2-c3b0-11e9-9ec0-f218985ebfa7.vcf.gz"}
  }
  runtime {
    docker: "broadinstitute/gatk:4.0.12.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-50148304-c3b0-11e9-9ec0-f218985ebfa7.vcf.gz"
    File out_tbi = if defined(outputFilename) then outputFilename else "generated-50148304-c3b0-11e9-9ec0-f218985ebfa7.vcf.gz" + ".tbi"
  }
}