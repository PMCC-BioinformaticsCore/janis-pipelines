version development

task ConcatStrelkaSomaticVcf {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Int? runtime_seconds
    Int? runtime_disks
    Array[File] headerVcfs
    Array[File] headerVcfs_tbi
    Array[File] contentVcfs
    Array[File] contentVcfs_tbi
    String? outputFilename
  }
  command <<<
     \
      vcf-concat \
      ~{"'" + sep("' '", headerVcfs) + "'"} \
      | grep '^##' > header.vcf; \
      vcf-merge \
      ~{"'" + sep("' '", contentVcfs) + "'"} \
      | grep -v '^##' > content.vcf; cat header.vcf content.vcf | bgzip -c \
      > ~{select_first([outputFilename, "generated.strelka.vcf.gz"])}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    disks: "local-disk ~{select_first([runtime_disks, 20])} SSD"
    docker: "biocontainers/vcftools:v0.1.16-1-deb_cv1"
    duration: select_first([runtime_seconds, 86400])
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated.strelka.vcf.gz"])
  }
}