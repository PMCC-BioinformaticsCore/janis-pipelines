version development

task GATK4ApplyBQSR {
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
    String outputFilename = "generated-7e98d0bc-ea17-11e9-b34c-acde48001122.bam"
    File? recalFile
    File? intervals
    String? tmpDir
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
    gatk ApplyBQSR \
      -R ${reference} \
      ${"-O " + if defined(outputFilename) then outputFilename else "generated-7e98d788-ea17-11e9-b34c-acde48001122.bam"} \
      ${"--bqsr-recal-file " + recalFile} \
      ${"--intervals " + intervals} \
      -I ${bam} \
      ${"--tmp-dir " + if defined(tmpDir) then tmpDir else "/tmp/"}
  }
  runtime {
    docker: "broadinstitute/gatk:4.1.3.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-7e98d0bc-ea17-11e9-b34c-acde48001122.bam"
    File out_bai = sub(if defined(outputFilename) then outputFilename else "generated-7e98d0bc-ea17-11e9-b34c-acde48001122.bam", "\\.bam$", ".bai")
  }
}