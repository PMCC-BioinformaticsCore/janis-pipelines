version development

task vardict_germline {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    File intervals
    String outputFilename = "generated-d9120cc4-e018-11e9-851b-a0cec8186c53.vardict.vcf.gz"
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
    if [ $(dirname "${bam_bai}") != $(dirname "bam") ]; then mv ${bam_bai} $(dirname ${bam}); fi
    if [ $(dirname "${reference_fai}") != $(dirname "reference") ]; then mv ${reference_fai} $(dirname ${reference}); fi
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
      ${"-th " + if defined(threads) then threads else if defined(runtime_cpu) then runtime_cpu else 1} \
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
      | bcftools view -O z \
      ${"> " + if defined(outputFilename) then outputFilename else "generated-d91223a8-e018-11e9-851b-a0cec8186c53.vardict.vcf.gz"}
  }
  runtime {
    docker: "michaelfranklin/vardict:1.6.0"
    cpu: if defined(runtime_cpu) then runtime_cpu else 1
    memory: if defined(runtime_memory) then "${runtime_memory}G" else "4G"
    preemptible: 2
  }
  output {
    File out = if defined(outputFilename) then outputFilename else "generated-d9120cc4-e018-11e9-851b-a0cec8186c53.vardict.vcf.gz"
  }
}