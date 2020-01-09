version development

task bcftoolsview {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File file
    Boolean? dropGenotypes
    Boolean? headerOnly
    Boolean? noHeader
    Int? compressionLevel
    Boolean? noVersion
    String? regions
    File? regionsFile
    String? targets
    File? targetsFile
    Int? threads
    Boolean? trimAltAlleles
    Boolean? noUpdate
    Array[String]? samples
    File? samplesFile
    Boolean? forceSamples
    Int? minAc
    Int? maxAc
    Array[String]? applyFilters
    String? genotype
    String? include
    String? exclude
    Boolean? known
    Boolean? novel
    Int? minAlleles
    Int? maxAlleles
    Boolean? phased
    Boolean? excludePhased
    Float? minAf
    Float? maxAf
    Boolean? uncalled
    Boolean? excludeUncalled
    Array[String]? types
    Array[String]? excludeTypes
    Boolean? private
    Boolean? excludePrivate
  }
  command <<<
    bcftools view \
      ~{true="--drop-genotypes" false="" dropGenotypes} \
      ~{true="--header-only" false="" headerOnly} \
      ~{true="--no-header" false="" noHeader} \
      ~{"--compression-level " + compressionLevel} \
      ~{true="--no-version" false="" noVersion} \
      ~{"--regions " + regions} \
      ~{"--regions-file " + regionsFile} \
      ~{"--targets " + targets} \
      ~{"--targets-file " + targetsFile} \
      ~{"--threads " + threads} \
      ~{true="--trim-alt-alleles" false="" trimAltAlleles} \
      ~{true="--no-update" false="" noUpdate} \
      ~{true="--samples " false="" defined(samples)}~{sep=" " samples} \
      ~{"--samples-file " + samplesFile} \
      ~{true="--force-samples" false="" forceSamples} \
      ~{"--min-ac " + minAc} \
      ~{"--max-ac " + maxAc} \
      ~{true="--apply-filters " false="" defined(applyFilters)}~{sep=" " applyFilters} \
      ~{"--genotype " + genotype} \
      ~{"--include " + include} \
      ~{"--exclude " + exclude} \
      ~{true="--known" false="" known} \
      ~{true="--novel" false="" novel} \
      ~{"--min-alleles " + minAlleles} \
      ~{"--max-alleles " + maxAlleles} \
      ~{true="--phased" false="" phased} \
      ~{true="--exclude-phased" false="" excludePhased} \
      ~{"--min-af " + minAf} \
      ~{"--max-af " + maxAf} \
      ~{true="--uncalled" false="" uncalled} \
      ~{true="--exclude-uncalled" false="" excludeUncalled} \
      ~{true="--types " false="" defined(types)}~{sep=" " types} \
      ~{true="--exclude-types " false="" defined(excludeTypes)}~{sep=" " excludeTypes} \
      ~{true="--private" false="" private} \
      ~{true="--exclude-private" false="" excludePrivate} \
      --output-type 'z' \
      ~{file}
  >>>
  runtime {
    docker: "biocontainers/bcftools:v1.5_cv2"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "~{runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = stdout()
  }
}