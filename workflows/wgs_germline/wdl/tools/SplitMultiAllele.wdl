version development

task SplitMultiAllele {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File vcf
    File reference
    File reference_amb
    File reference_ann
    File reference_bwt
    File reference_pac
    File reference_sa
    File reference_fai
    File reference_dict
    String outputFilename = "generated-d9129c20-e018-11e9-851b-a0cec8186c53.norm.vcf"
  }
  command {
    if [ $(dirname "${reference_amb}") != $(dirname "reference") ]; then mv ${reference_amb} $(dirname ${reference}); fi
    if [ $(dirname "${reference_ann}") != $(dirname "reference") ]; then mv ${reference_ann} $(dirname ${reference}); fi
    if [ $(dirname "${reference_bwt}") != $(dirname "reference") ]; then mv ${reference_bwt} $(dirname ${reference}); fi
    if [ $(dirname "${reference_pac}") != $(dirname "reference") ]; then mv ${reference_pac} $(dirname ${reference}); fi
    if [ $(dirname "${reference_sa}") != $(dirname "reference") ]; then mv ${reference_sa} $(dirname ${reference}); fi
    if [ $(dirname "${reference_fai}") != $(dirname "reference") ]; then mv ${reference_fai} $(dirname ${reference}); fi
    if [ $(dirname "${reference_dict}") != $(dirname "reference") ]; then mv ${reference_dict} $(dirname ${reference}); fi
     \
      zcat \
      | \
      sed 's/ID=AD,Number=./ID=AD,Number=R/' < \
      ${vcf} \
      | \
      vt decompose -s - -o - \
      | \
      vt normalize -n -q - -o - \
      -r ${reference} \
      | \
      ${"> " + if defined(outputFilename) then outputFilename else "generated-d912a2f6-e018-11e9-851b-a0cec8186c53.norm.vcf"} \
      sed 's/ID=AD,Number=./ID=AD,Number=1/'
  }
  runtime {
    docker: "heuermh/vt"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-d9129c20-e018-11e9-851b-a0cec8186c53.norm.vcf"
  }
}