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
      ~{if defined(compressionLevel) then ("--compression-level " +  '"' + compressionLevel + '"') else ""} \
      ~{true="--no-version" false="" noVersion} \
      ~{if defined(regions) then ("--regions " +  '"' + regions + '"') else ""} \
      ~{if defined(regionsFile) then ("--regions-file " +  '"' + regionsFile + '"') else ""} \
      ~{if defined(targets) then ("--targets " +  '"' + targets + '"') else ""} \
      ~{if defined(targetsFile) then ("--targets-file " +  '"' + targetsFile + '"') else ""} \
      ~{if defined(threads) then ("--threads " +  '"' + threads + '"') else ""} \
      ~{true="--trim-alt-alleles" false="" trimAltAlleles} \
      ~{true="--no-update" false="" noUpdate} \
      ~{true="--samples " false="" defined(samples)}~{sep=" " samples} \
      ~{if defined(samplesFile) then ("--samples-file " +  '"' + samplesFile + '"') else ""} \
      ~{true="--force-samples" false="" forceSamples} \
      ~{if defined(minAc) then ("--min-ac " +  '"' + minAc + '"') else ""} \
      ~{if defined(maxAc) then ("--max-ac " +  '"' + maxAc + '"') else ""} \
      ~{true="--apply-filters " false="" defined(applyFilters)}~{sep=" " applyFilters} \
      ~{if defined(genotype) then ("--genotype " +  '"' + genotype + '"') else ""} \
      ~{if defined(include) then ("--include " +  '"' + include + '"') else ""} \
      ~{if defined(exclude) then ("--exclude " +  '"' + exclude + '"') else ""} \
      ~{true="--known" false="" known} \
      ~{true="--novel" false="" novel} \
      ~{if defined(minAlleles) then ("--min-alleles " +  '"' + minAlleles + '"') else ""} \
      ~{if defined(maxAlleles) then ("--max-alleles " +  '"' + maxAlleles + '"') else ""} \
      ~{true="--phased" false="" phased} \
      ~{true="--exclude-phased" false="" excludePhased} \
      ~{if defined(minAf) then ("--min-af " +  '"' + minAf + '"') else ""} \
      ~{if defined(maxAf) then ("--max-af " +  '"' + maxAf + '"') else ""} \
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
    cpu: select_first([runtime_cpu, 1])
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = stdout()
  }
}