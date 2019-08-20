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
    File? outputFile
    String? outputType
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
  command {
    bcftools view \
      ${true="--drop-genotypes" false="" dropGenotypes} \
      ${true="--header-only" false="" headerOnly} \
      ${true="--no-header" false="" noHeader} \
      ${"--compression-level " + compressionLevel} \
      ${true="--no-version" false="" noVersion} \
      ${"--output-file " + outputFile} \
      ${"--output-type " + outputType} \
      ${"--regions " + regions} \
      ${"--regions-file " + regionsFile} \
      ${"--targets " + targets} \
      ${"--targets-file " + targetsFile} \
      ${"--threads " + threads} \
      ${true="--trim-alt-alleles" false="" trimAltAlleles} \
      ${true="--no-update" false="" noUpdate} \
      ${if defined(samples) then "--samples " else ""}${sep=" --samples " samples} \
      ${"--samples-file " + samplesFile} \
      ${true="--force-samples" false="" forceSamples} \
      ${"--min-ac " + minAc} \
      ${"--max-ac " + maxAc} \
      ${if defined(applyFilters) then "--apply-filters " else ""}${sep=" --apply-filters " applyFilters} \
      ${"--genotype " + genotype} \
      ${"--include " + include} \
      ${"--exclude " + exclude} \
      ${true="--known" false="" known} \
      ${true="--novel" false="" novel} \
      ${"--min-alleles " + minAlleles} \
      ${"--max-alleles " + maxAlleles} \
      ${true="--phased" false="" phased} \
      ${true="--exclude-phased" false="" excludePhased} \
      ${"--min-af " + minAf} \
      ${"--max-af " + maxAf} \
      ${true="--uncalled" false="" uncalled} \
      ${true="--exclude-uncalled" false="" excludeUncalled} \
      ${if defined(types) then "--types " else ""}${sep=" --types " types} \
      ${if defined(excludeTypes) then "--exclude-types " else ""}${sep=" --exclude-types " excludeTypes} \
      ${true="--private" false="" private} \
      ${true="--exclude-private" false="" excludePrivate} \
      ${file}
  }
  runtime {
    docker: "biocontainers/bcftools:v1.5_cv2"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = stdout()
  }
}