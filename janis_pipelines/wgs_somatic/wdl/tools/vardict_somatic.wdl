version development

task vardict_somatic {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File tumorBam
    File tumorBam_bai
    File normalBam
    File normalBam_bai
    File intervals
    File reference
    File reference_fai
    String tumorName
    String normalName
    Float? alleleFreqThreshold
    String outputFilename = "generated-.vardict.vcf"
    Boolean? indels3prime
    Float? amplicon
    Int? minReads
    Boolean? chromNamesAreNumbers
    Int? chromColumn
    Boolean? debug
    String? splitDelimeter
    Int? geneEndCol
    Int? segEndCol
    String? filter
    Int? geneNameCol
    Boolean? printHeaderRow
    Int? indelSize
    Boolean? outputSplice
    Int? performLocalRealignment
    Int? minMatches
    Int? maxMismatches
    String? regexSampleName
    String? mapq
    Float? qratio
    Float? readPosition
    Boolean? pileup
    Int? minMappingQual
    Int? phredScore
    String? region
    Int? minVariantReads
    Int? regStartCol
    Int? segStartCol
    Int? minReadsBeforeTrim
    Boolean? removeDuplicateReads
    Int? threads
    Int? freq
    Boolean? vcfFormat
    String? vs
    Int? bp
    Int? extensionNucleotide
    Boolean? yy
    Int? downsamplingFraction
    Int? zeroBasedCoords
  }
  command <<<
    VarDict \
      -G ~{reference} \
      ~{true="-3" false="" indels3prime} \
      ~{"-a " + amplicon} \
      ~{"-B " + minReads} \
      ~{true="-C" false="" chromNamesAreNumbers} \
      ~{"-c " + chromColumn} \
      ~{true="-D" false="" debug} \
      ~{"-d " + splitDelimeter} \
      ~{"-E " + geneEndCol} \
      ~{"-e " + segEndCol} \
      ~{"-F " + filter} \
      ~{"-g " + geneNameCol} \
      ~{true="-h" false="" printHeaderRow} \
      ~{"-I " + indelSize} \
      ~{true="-i" false="" outputSplice} \
      ~{"-k " + performLocalRealignment} \
      ~{"-M " + minMatches} \
      ~{"-m " + maxMismatches} \
      ~{"-n " + regexSampleName} \
      ~{"-O " + mapq} \
      ~{"-o " + qratio} \
      ~{"-P " + readPosition} \
      ~{true="-p" false="" pileup} \
      ~{"-Q " + minMappingQual} \
      ~{"-q " + phredScore} \
      ~{"-R " + region} \
      ~{"-r " + minVariantReads} \
      ~{"-S " + regStartCol} \
      ~{"-s " + segStartCol} \
      ~{"-T " + minReadsBeforeTrim} \
      ~{true="-t" false="" removeDuplicateReads} \
      ~{"-th " + if defined(threads) then threads else if defined(runtime_cpu) then runtime_cpu else 1} \
      ~{"-V " + freq} \
      ~{true="-v" false="" vcfFormat} \
      ~{"-VS " + vs} \
      ~{"-X " + bp} \
      ~{"-x " + extensionNucleotide} \
      ~{true="-y" false="" yy} \
      ~{"-Z " + downsamplingFraction} \
      ~{"-z " + zeroBasedCoords} \
      -b '~{tumorBam}|~{normalBam}' \
      -N '~{tumorName}' \
      -f ~{alleleFreqThreshold} \
      ~{intervals} \
      | testsomatic.R | \
      var2vcf_paired.pl \
      -N '~{tumorName}|~{normalName}' \
      -f ~{alleleFreqThreshold} \
      | bcftools view -O z \
      ~{"> " + if defined(outputFilename) then outputFilename else "generated-.vardict.vcf"}
  >>>
  runtime {
    docker: "michaelfranklin/vardict:1.6.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "~{runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-.vardict.vcf"
  }
}