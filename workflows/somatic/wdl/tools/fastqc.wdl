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
  command {
    fastqc \
      ${"--outdir " + if defined(outdir) then outdir else "."} \
      ${true="--casava" false="" casava} \
      ${true="--nano" false="" nano} \
      ${true="--nofilter" false="" nofilter} \
      ${true="--extract" false="" extract} \
      ${"--java " + java} \
      ${true="--noextract" false="" if defined(noextract) then noextract else true} \
      ${true="--nogroup" false="" nogroup} \
      ${"--format " + format} \
      ${"--threads " + if defined(threads) then threads else 1} \
      ${"--contaminants " + contaminants} \
      ${"--adapters " + adapters} \
      ${"--limits " + limits} \
      ${"--kmers " + kmers} \
      ${true="--quiet" false="" quiet} \
      ${"--dir " + dir} \
      ${sep=" " prefix("", reads)}
  }
  runtime {
    docker: "biocontainers/fastqc:v0.11.5_cv3"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    Array[File] out = glob("*.zip")
  }
}