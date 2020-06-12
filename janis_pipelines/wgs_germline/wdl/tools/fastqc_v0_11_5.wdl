version development

task fastqc {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Array[File] reads
    String? outdir
    Boolean? casava
    Boolean? nano
    Boolean? nofilter
    Boolean? extract
    String? java
    Boolean? noextract
    Boolean? nogroup
    String? format
    Int? threads
    File? contaminants
    File? adapters
    File? limits
    Int? kmers
    Boolean? quiet
    String? dir
  }
  command <<<
    fastqc \
      ~{if defined(select_first([outdir, "."])) then ("--outdir " +  '"' + select_first([outdir, "."]) + '"') else ""} \
      ~{true="--casava" false="" casava} \
      ~{true="--nano" false="" nano} \
      ~{true="--nofilter" false="" nofilter} \
      ~{true="--extract" false="" select_first([extract, true])} \
      ~{if defined(java) then ("--java " +  '"' + java + '"') else ""} \
      ~{true="--noextract" false="" noextract} \
      ~{true="--nogroup" false="" nogroup} \
      ~{if defined(format) then ("--format " +  '"' + format + '"') else ""} \
      ~{if defined(select_first([threads, select_first([runtime_cpu, 1])])) then ("--threads " +  '"' + select_first([threads, select_first([runtime_cpu, 1])]) + '"') else ""} \
      ~{if defined(contaminants) then ("--contaminants " +  '"' + contaminants + '"') else ""} \
      ~{if defined(adapters) then ("--adapters " +  '"' + adapters + '"') else ""} \
      ~{if defined(limits) then ("--limits " +  '"' + limits + '"') else ""} \
      ~{if defined(kmers) then ("--kmers " +  '"' + kmers + '"') else ""} \
      ~{true="--quiet" false="" quiet} \
      ~{if defined(dir) then ("--dir " +  '"' + dir + '"') else ""} \
      ~{sep=" " reads}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    docker: "biocontainers/fastqc:v0.11.5_cv3"
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    Array[File] out = glob("*.zip")
    Array[File] datafile = glob("*/fastqc_data.txt")
  }
}