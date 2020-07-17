version development

task UncompressArchive {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Int? runtime_seconds
    Int? runtime_disks
    File file
    Boolean? stdout
    Boolean? decompress
    Boolean? force
    Boolean? keep
    Boolean? list
    Boolean? noName
    Boolean? name
    Boolean? quiet
    Boolean? recursive
    String? suffix
    Boolean? test
    Boolean? fast
    Boolean? best
    Boolean? rsyncable
  }
  command <<<
    gunzip \
      ~{if defined(select_first([stdout, true])) then "-c" else ""} \
      ~{if defined(decompress) then "-d" else ""} \
      ~{if defined(force) then "-f" else ""} \
      ~{if defined(keep) then "-k" else ""} \
      ~{if defined(list) then "-l" else ""} \
      ~{if defined(noName) then "-n" else ""} \
      ~{if defined(name) then "-N" else ""} \
      ~{if defined(quiet) then "-q" else ""} \
      ~{if defined(recursive) then "-r" else ""} \
      ~{if defined(suffix) then ("-s '" + suffix + "'") else ""} \
      ~{if defined(test) then "-t" else ""} \
      ~{if defined(fast) then "-1" else ""} \
      ~{if defined(best) then "-9" else ""} \
      ~{if defined(rsyncable) then "--rsyncable" else ""} \
      ~{file}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    disks: "local-disk ~{select_first([runtime_disks, 20])} SSD"
    docker: "ubuntu:latest"
    duration: select_first([runtime_seconds, 86400])
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = stdout()
  }
}