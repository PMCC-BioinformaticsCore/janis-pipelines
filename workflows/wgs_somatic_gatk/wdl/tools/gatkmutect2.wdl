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
    String outputFilename = "generated-98ecb25e-cf9f-11e9-a6a4-acde48001122.vcf.gz"
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
      ${"-O " + if defined(outputFilename) then outputFilename else "generated-98ecbf88-cf9f-11e9-a6a4-acde48001122.vcf.gz"}
  }
  runtime {
    docker: "broadinstitute/gatk:4.0.12.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-98ecb25e-cf9f-11e9-a6a4-acde48001122.vcf.gz"
    File out_tbi = if defined(outputFilename) then outputFilename else "generated-98ecb25e-cf9f-11e9-a6a4-acde48001122.vcf.gz" + ".tbi"
  }
}