version development

task vardict_germline {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File intervals
    String outputFilename = "generated-363edfa6-c3b0-11e9-81d9-f218985ebfa7.vardict.vcf"
    File bam
    File bam_bai
    File reference
    File reference_fai
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
    Float? alleleFreqThreshold
    Int? geneNameCol
    Boolean? printHeaderRow
    Int? indelSize
    Boolean? outputSplice
    Int? performLocalRealignment
    Int? minMatches
    Int? maxMismatches
    String sampleName
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
    String var2vcfSampleName
    Float var2vcfAlleleFreqThreshold
  }
  command {
    VarDict \
      -b ${bam} \
      -G ${reference} \
      ${true="-3" false="" indels3prime} \
      ${"-a " + amplicon} \
      ${"-B " + minReads} \
      ${true="-C" false="" chromNamesAreNumbers} \
      ${"-c " + chromColumn} \
      ${true="-D" false="" debug} \
      ${"-d " + splitDelimeter} \
      ${"-E " + geneEndCol} \
      ${"-e " + segEndCol} \
      ${"-F " + filter} \
      ${"-f " + alleleFreqThreshold} \
      ${"-g " + geneNameCol} \
      ${true="-h" false="" printHeaderRow} \
      ${"-I " + indelSize} \
      ${true="-i" false="" outputSplice} \
      ${"-k " + performLocalRealignment} \
      ${"-M " + minMatches} \
      ${"-m " + maxMismatches} \
      -N ${sampleName} \
      ${"-n " + regexSampleName} \
      ${"-O " + mapq} \
      ${"-o " + qratio} \
      ${"-P " + readPosition} \
      ${true="-p" false="" pileup} \
      ${"-Q " + minMappingQual} \
      ${"-q " + phredScore} \
      ${"-R " + region} \
      ${"-r " + minVariantReads} \
      ${"-S " + regStartCol} \
      ${"-s " + segStartCol} \
      ${"-T " + minReadsBeforeTrim} \
      ${true="-t" false="" removeDuplicateReads} \
      ${"-th " + if defined(threads) then threads else 1} \
      ${"-V " + freq} \
      ${true="-v" false="" vcfFormat} \
      ${"-VS " + vs} \
      ${"-X " + bp} \
      ${"-x " + extensionNucleotide} \
      ${true="-y" false="" yy} \
      ${"-Z " + downsamplingFraction} \
      ${"-z " + zeroBasedCoords} \
      ${intervals} \
      | teststrandbias.R | \
      var2vcf_valid.pl \
      -N ${var2vcfSampleName} \
      -f ${var2vcfAlleleFreqThreshold} \
      ${"> " + if defined(outputFilename) then outputFilename else "generated-363ef5fe-c3b0-11e9-81d9-f218985ebfa7.vardict.vcf"}
  }
  runtime {
    docker: "michaelfranklin/vardict:1.5.8"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-363edfa6-c3b0-11e9-81d9-f218985ebfa7.vardict.vcf"
  }
}