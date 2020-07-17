version development

task vardict_germline {
  input {
    Int? runtime_cpu
    Int? runtime_memory
    Int? runtime_seconds
    Int? runtime_disks
    File intervals
    String? outputFilename
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
  command <<<
    VarDict \
      -b ~{bam} \
      -G ~{reference} \
      ~{if defined(indels3prime) then "-3" else ""} \
      ~{if defined(amplicon) then ("-a " + amplicon) else ''} \
      ~{if defined(minReads) then ("-B " + minReads) else ''} \
      ~{if defined(chromNamesAreNumbers) then "-C" else ""} \
      ~{if defined(chromColumn) then ("-c " + chromColumn) else ''} \
      ~{if defined(debug) then "-D" else ""} \
      ~{if defined(splitDelimeter) then ("-d " + splitDelimeter) else ''} \
      ~{if defined(geneEndCol) then ("-E " + geneEndCol) else ''} \
      ~{if defined(segEndCol) then ("-e " + segEndCol) else ''} \
      ~{if defined(filter) then ("-F " + filter) else ''} \
      ~{if defined(alleleFreqThreshold) then ("-f " + alleleFreqThreshold) else ''} \
      ~{if defined(geneNameCol) then ("-g " + geneNameCol) else ''} \
      ~{if defined(printHeaderRow) then "-h" else ""} \
      ~{if defined(indelSize) then ("-I " + indelSize) else ''} \
      ~{if defined(outputSplice) then "-i" else ""} \
      ~{if defined(performLocalRealignment) then ("-k " + performLocalRealignment) else ''} \
      ~{if defined(minMatches) then ("-M " + minMatches) else ''} \
      ~{if defined(maxMismatches) then ("-m " + maxMismatches) else ''} \
      -N ~{sampleName} \
      ~{if defined(regexSampleName) then ("-n " + regexSampleName) else ''} \
      ~{if defined(mapq) then ("-O " + mapq) else ''} \
      ~{if defined(qratio) then ("-o " + qratio) else ''} \
      ~{if defined(readPosition) then ("-P " + readPosition) else ''} \
      ~{if defined(pileup) then "-p" else ""} \
      ~{if defined(minMappingQual) then ("-Q " + minMappingQual) else ''} \
      ~{if defined(phredScore) then ("-q " + phredScore) else ''} \
      ~{if defined(region) then ("-R " + region) else ''} \
      ~{if defined(minVariantReads) then ("-r " + minVariantReads) else ''} \
      ~{if defined(regStartCol) then ("-S " + regStartCol) else ''} \
      ~{if defined(segStartCol) then ("-s " + segStartCol) else ''} \
      ~{if defined(minReadsBeforeTrim) then ("-T " + minReadsBeforeTrim) else ''} \
      ~{if defined(removeDuplicateReads) then "-t" else ""} \
      ~{if defined(select_first([threads, select_first([runtime_cpu, 1])])) then ("-th " + select_first([threads, select_first([runtime_cpu, 1])])) else ''} \
      ~{if defined(freq) then ("-V " + freq) else ''} \
      ~{if defined(vcfFormat) then "-v" else ""} \
      ~{if defined(vs) then ("-VS " + vs) else ''} \
      ~{if defined(bp) then ("-X " + bp) else ''} \
      ~{if defined(extensionNucleotide) then ("-x " + extensionNucleotide) else ''} \
      ~{if defined(yy) then "-y" else ""} \
      ~{if defined(downsamplingFraction) then ("-Z " + downsamplingFraction) else ''} \
      ~{if defined(zeroBasedCoords) then ("-z " + zeroBasedCoords) else ''} \
      ~{intervals} \
      | teststrandbias.R | \
      var2vcf_valid.pl \
      -N ~{var2vcfSampleName} \
      -f ~{var2vcfAlleleFreqThreshold} \
      > ~{select_first([outputFilename, "generated.vardict.vcf"])}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 4, 1])
    disks: "local-disk ~{select_first([runtime_disks, 20])} SSD"
    docker: "michaelfranklin/vardict:1.6.0"
    duration: select_first([runtime_seconds, 86400])
    memory: "~{select_first([runtime_memory, 8, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated.vardict.vcf"])
  }
}