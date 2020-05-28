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
    String? outputFilename
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
      ~{if defined(amplicon) then ("-a " +  '"' + amplicon + '"') else ""} \
      ~{if defined(minReads) then ("-B " +  '"' + minReads + '"') else ""} \
      ~{true="-C" false="" chromNamesAreNumbers} \
      ~{if defined(chromColumn) then ("-c " +  '"' + chromColumn + '"') else ""} \
      ~{true="-D" false="" debug} \
      ~{if defined(splitDelimeter) then ("-d " +  '"' + splitDelimeter + '"') else ""} \
      ~{if defined(geneEndCol) then ("-E " +  '"' + geneEndCol + '"') else ""} \
      ~{if defined(segEndCol) then ("-e " +  '"' + segEndCol + '"') else ""} \
      ~{if defined(filter) then ("-F " +  '"' + filter + '"') else ""} \
      ~{if defined(geneNameCol) then ("-g " +  '"' + geneNameCol + '"') else ""} \
      ~{true="-h" false="" printHeaderRow} \
      ~{if defined(indelSize) then ("-I " +  '"' + indelSize + '"') else ""} \
      ~{true="-i" false="" outputSplice} \
      ~{if defined(performLocalRealignment) then ("-k " +  '"' + performLocalRealignment + '"') else ""} \
      ~{if defined(minMatches) then ("-M " +  '"' + minMatches + '"') else ""} \
      ~{if defined(maxMismatches) then ("-m " +  '"' + maxMismatches + '"') else ""} \
      ~{if defined(regexSampleName) then ("-n " +  '"' + regexSampleName + '"') else ""} \
      ~{if defined(mapq) then ("-O " +  '"' + mapq + '"') else ""} \
      ~{if defined(qratio) then ("-o " +  '"' + qratio + '"') else ""} \
      ~{if defined(readPosition) then ("-P " +  '"' + readPosition + '"') else ""} \
      ~{true="-p" false="" pileup} \
      ~{if defined(minMappingQual) then ("-Q " +  '"' + minMappingQual + '"') else ""} \
      ~{if defined(phredScore) then ("-q " +  '"' + phredScore + '"') else ""} \
      ~{if defined(region) then ("-R " +  '"' + region + '"') else ""} \
      ~{if defined(minVariantReads) then ("-r " +  '"' + minVariantReads + '"') else ""} \
      ~{if defined(regStartCol) then ("-S " +  '"' + regStartCol + '"') else ""} \
      ~{if defined(segStartCol) then ("-s " +  '"' + segStartCol + '"') else ""} \
      ~{if defined(minReadsBeforeTrim) then ("-T " +  '"' + minReadsBeforeTrim + '"') else ""} \
      ~{true="-t" false="" removeDuplicateReads} \
      ~{if defined(select_first([threads, select_first([runtime_cpu, 1])])) then ("-th " +  '"' + select_first([threads, select_first([runtime_cpu, 1])]) + '"') else ""} \
      ~{if defined(freq) then ("-V " +  '"' + freq + '"') else ""} \
      ~{true="-v" false="" vcfFormat} \
      ~{if defined(vs) then ("-VS " +  '"' + vs + '"') else ""} \
      ~{if defined(bp) then ("-X " +  '"' + bp + '"') else ""} \
      ~{if defined(extensionNucleotide) then ("-x " +  '"' + extensionNucleotide + '"') else ""} \
      ~{true="-y" false="" yy} \
      ~{if defined(downsamplingFraction) then ("-Z " +  '"' + downsamplingFraction + '"') else ""} \
      ~{if defined(zeroBasedCoords) then ("-z " +  '"' + zeroBasedCoords + '"') else ""} \
      -b '~{tumorBam}|~{normalBam}' \
      -N '~{tumorName}' \
      -f ~{alleleFreqThreshold} \
      ~{intervals} \
      | testsomatic.R | \
      var2vcf_paired.pl \
      -N '~{tumorName}|~{normalName}' \
      -f ~{alleleFreqThreshold} \
      | bcftools view -O z \
      ~{if defined(select_first([outputFilename, "generated.vardict.vcf"])) then ("> " +  '"' + select_first([outputFilename, "generated.vardict.vcf"]) + '"') else ""}
  >>>
  runtime {
    cpu: select_first([runtime_cpu, 1])
    docker: "michaelfranklin/vardict:1.6.0"
    memory: "~{select_first([runtime_memory, 4])}G"
    preemptible: 2
  }
  output {
    File out = select_first([outputFilename, "generated.vardict.vcf"])
  }
}