#!/usr/bin/env cwl-runner
class: CommandLineTool
cwlVersion: v1.0
label: 'GATK4: Haplotype Caller'
doc: |-
  Call germline SNPs and indels via local re-assembly of haplotypes
      
  The HaplotypeCaller is capable of calling SNPs and indels simultaneously via local de-novo assembly of haplotypes 
  in an active region. In other words, whenever the program encounters a region showing signs of variation, it 
  discards the existing mapping information and completely reassembles the reads in that region. This allows the 
  HaplotypeCaller to be more accurate when calling regions that are traditionally difficult to call, for example when 
  they contain different types of variants close to each other. It also makes the HaplotypeCaller much better at 
  calling indels than position-based callers like UnifiedGenotyper.

  In the GVCF workflow used for scalable variant calling in DNA sequence data, HaplotypeCaller runs per-sample to 
  generate an intermediate GVCF (not to be used in final analysis), which can then be used in GenotypeGVCFs for joint 
  genotyping of multiple samples in a very efficient way. The GVCF workflow enables rapid incremental processing of 
  samples as they roll off the sequencer, as well as scaling to very large cohort sizes (e.g. the 92K exomes of ExAC).

  In addition, HaplotypeCaller is able to handle non-diploid organisms as well as pooled experiment data. 
  Note however that the algorithms used to calculate variant likelihoods is not well suited to extreme allele 
  frequencies (relative to ploidy) so its use is not recommended for somatic (cancer) variant discovery. 
  For that purpose, use Mutect2 instead.

  Finally, HaplotypeCaller is also able to correctly handle the splice junctions that make RNAseq a challenge 
  for most variant callers, on the condition that the input read data has previously been processed according 
  to our recommendations as documented (https://software.broadinstitute.org/gatk/documentation/article?id=4067).

requirements:
- class: ShellCommandRequirement
- class: InlineJavascriptRequirement
- class: DockerRequirement
  dockerPull: broadinstitute/gatk:4.1.3.0

inputs:
- id: activityProfileOut
  label: activityProfileOut
  doc: 'Output the raw activity profile results in IGV format (default: null)'
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --activity-profile-out
- id: alleles
  label: alleles
  doc: |-
    (default: null) The set of alleles at which to genotype when --genotyping_mode is GENOTYPE_GIVEN_ALLELES
  type:
  - File
  - 'null'
  inputBinding:
    prefix: --alleles
- id: annotateWithNumDiscoveredAlleles
  label: annotateWithNumDiscoveredAlleles
  doc: |-
    If provided, we will annotate records with the number of alternate alleles that were discovered (but not necessarily genotyped) at a given site
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --annotate-with-num-discovered-alleles
- id: annotation
  label: annotation
  doc: '-A: One or more specific annotations to add to variant calls'
  type:
  - type: array
    items: string
  - 'null'
  inputBinding:
    prefix: --annotation
- id: annotationGroup
  label: annotationGroup
  doc: "-G\tOne or more groups of annotations to apply to variant calls"
  type:
  - type: array
    items: string
  - 'null'
  inputBinding:
    prefix: --annotation-group
- id: annotationsToExclude
  label: annotationsToExclude
  doc: "-AX\tOne or more specific annotations to exclude from variant calls"
  type:
  - type: array
    items: string
  - 'null'
  inputBinding:
    prefix: --annotations-to-exclude
- id: arguments_file
  label: arguments_file
  doc: read one or more arguments files and add them to the command line
  type:
  - type: array
    items: File
  - 'null'
  inputBinding:
    prefix: --arguments_file
- id: assemblyRegionOut
  label: assemblyRegionOut
  doc: |-
    (default: null) Output the assembly region to this IGV formatted file. Which annotations to exclude from output in the variant calls. Note that this argument has higher priority than the -A or -G arguments, so these annotations will be excluded even if they are explicitly included with the other options.
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --assembly-region-out
- id: baseQualityScoreThreshold
  label: baseQualityScoreThreshold
  doc: |-
    (default: 18) Base qualities below this threshold will be reduced to the minimum (6)
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --base-quality-score-threshold
- id: cloudIndexPrefetchBuffer
  label: cloudIndexPrefetchBuffer
  doc: |-
    -CIPB (default: -1) Size of the cloud-only prefetch buffer (in MB; 0 to disable). Defaults to cloudPrefetchBuffer if unset.
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --cloud-index-prefetch-buffer
- id: cloudPrefetchBuffer
  label: cloudPrefetchBuffer
  doc: '-CPB (default: 40) Size of the cloud-only prefetch buffer (in MB; 0 to disable).'
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --cloud-prefetch-buffer
- id: contaminationFractionToFilter
  label: contaminationFractionToFilter
  doc: |-
    -contamination (default: 0.0) Fraction of contamination in sequencing data (for all samples) to aggressively remove
  type:
  - double
  - 'null'
  inputBinding:
    prefix: --contamination-fraction-to-filter
- id: correctOverlappingQuality
  label: correctOverlappingQuality
  doc: Undocumented option
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --correct-overlapping-quality
- id: disableBamIndexCaching
  label: disableBamIndexCaching
  doc: |-
    -DBIC. If true, don't cache bam indexes, this will reduce memory requirements but may harm performance if many intervals are specified. Caching is automatically disabled if there are no intervals specified.
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --disable-bam-index-caching
- id: founderId
  label: founderId
  doc: Samples representing the population "founders"
  type:
  - type: array
    items: string
  - 'null'
  inputBinding:
    prefix: --founder-id
- id: genotypingMode
  label: genotypingMode
  doc: |-
    (default: DISCOVERY) Specifies how to determine the alternate alleles to use for genotyping. The --genotyping-mode argument is an enumerated type (GenotypingOutputMode), which can have one of the following values: DISCOVERY (The genotyper will choose the most likely alternate allele) or GENOTYPE_GIVEN_ALLELES (Only the alleles passed by the user should be considered).
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --genotyping-mode
- id: heterozygosity
  label: heterozygosity
  doc: |-
    (default: 0.001) Heterozygosity value used to compute prior likelihoods for any locus. The expected heterozygosity value used to compute prior probability that a locus is non-reference. The default priors are for provided for humans: het = 1e-3 which means that the probability of N samples being hom-ref at a site is: 1 - sum_i_2N (het / i) Note that heterozygosity as used here is the population genetics concept: http://en.wikipedia.org/wiki/Zygosity#Heterozygosity_in_population_genetics . That is, a hets value of 0.01 implies that two randomly chosen chromosomes from the population of organisms would differ from each other (one being A and the other B) at a rate of 1 in 100 bp. Note that this quantity has nothing to do with the likelihood of any given sample having a heterozygous genotype, which in the GATK is purely determined by the probability of the observed data P(D | AB) under the model that there may be a AB het genotype. The posterior probability of this AB genotype would use the het prior, but the GATK only uses this posterior probability in determining the prob. that a site is polymorphic. So changing the het parameters only increases the chance that a site will be called non-reference across all samples, but doesn't actually change the output genotype likelihoods at all, as these aren't posterior probabilities at all. The quantity that changes whether the GATK considers the possibility of a het genotype at all is the ploidy, which determines how many chromosomes each individual in the species carries.
  type:
  - double
  - 'null'
  inputBinding:
    prefix: --heterozygosity
- id: heterozygosityStdev
  label: heterozygosityStdev
  doc: (default 0.01) Standard deviation of heterozygosity for SNP and indel calling.
  type:
  - double
  - 'null'
  inputBinding:
    prefix: --heterozygosity-stdev
- id: indelHeterozygosity
  label: indelHeterozygosity
  doc: |-
    (default: 1.25E-4) Heterozygosity for indel calling. This argument informs the prior probability of having an indel at a site. (See heterozygosity)
  type:
  - double
  - 'null'
  inputBinding:
    prefix: --indel-heterozygosity
- id: intervalMergingRule
  label: intervalMergingRule
  doc: |-
    -imr (default: ALL) Interval merging rule for abutting intervals. By default, the program merges abutting intervals (i.e. intervals that are directly side-by-side but do not actually overlap) into a single continuous interval. However you can change this behavior if you want them to be treated as separate intervals instead. The --interval-merging-rule argument is an enumerated type (IntervalMergingRule), which can have one of the following values:[ALL, OVERLAPPING]
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --interval-merging-rule
- id: maxReadsPerAlignmentStart
  label: maxReadsPerAlignmentStart
  doc: |-
    (default: 50) Maximum number of reads to retain per alignment start position. Reads above this threshold will be downsampled. Set to 0 to disable.
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --max-reads-per-alignment-start
- id: minBaseQualityScore
  label: minBaseQualityScore
  doc: '-mbq (default: 10) Minimum base quality required to consider a base for calling'
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --min-base-quality-score
- id: nativePairHmmThreads
  label: nativePairHmmThreads
  doc: '(default: 4) How many threads should a native pairHMM implementation use'
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --native-pair-hmm-threads
- id: nativePairHmmUseDoublePrecision
  label: nativePairHmmUseDoublePrecision
  doc: |-
    use double precision in the native pairHmm. This is slower but matches the java implementation better
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --native-pair-hmm-use-double-precision
- id: numReferenceSamplesIfNoCall
  label: numReferenceSamplesIfNoCall
  doc: |-
    (default: 0) Number of hom-ref genotypes to infer at sites not present in a panel. When a variant is not seen in any panel, this argument controls whether to infer (and with what effective strength) that only reference alleles were observed at that site. E.g. "If not seen in 1000Genomes, treat it as AC=0, AN=2000".
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --num-reference-samples-if-no-call
- id: outputMode
  label: outputMode
  doc: |-
    (default: EMIT_VARIANTS_ONLY) Specifies which type of calls we should output. The --output-mode argument is an enumerated type (OutputMode), which can have one of the following values: [EMIT_VARIANTS_ONLY (produces calls only at variant sites), EMIT_ALL_CONFIDENT_SITES (produces calls at variant sites and confident reference sites), EMIT_ALL_SITES (produces calls at any callable site regardless of confidence; this argument is intended only for point mutations (SNPs) in DISCOVERY mode or generally when running in GENOTYPE_GIVEN_ALLELES mode; it will by no means produce a comprehensive set of indels in DISCOVERY mode)]
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --output-mode
- id: pedigree
  label: pedigree
  doc: '-ped (default: null) Pedigree file for determining the population "founders"'
  type:
  - File
  - 'null'
  inputBinding:
    prefix: --pedigree
- id: populationCallset
  label: populationCallset
  doc: '-population (default: null) Callset to use in calculating genotype priors'
  type:
  - File
  - 'null'
  inputBinding:
    prefix: --population-callset
- id: sampleName
  label: sampleName
  doc: |-
    -ALIAS (default: null) Name of single sample to use from a multi-sample bam. You can use this argument to specify that HC should process a single sample out of a multisample BAM file. This is especially useful if your samples are all in the same file but you need to run them individually through HC in -ERC GVC mode (which is the recommended usage). Note that the name is case-sensitive.
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --sample-name
- id: samplePloidy
  label: samplePloidy
  doc: |-
    -ploidy (default: 2) Ploidy (number of chromosomes) per sample. For pooled data, set to (Number of samples in each pool * Sample Ploidy). Sample ploidy - equivalent to number of chromosomes per pool. In pooled experiments this should be = # of samples in pool * individual sample ploidy
  type:
  - int
  - 'null'
  inputBinding:
    prefix: --sample-ploidy
- id: sitesOnlyVcfOutput
  label: sitesOnlyVcfOutput
  doc: |-
    (default: false) If true, don't emit genotype fields when writing vcf file output.
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --sites-only-vcf-output
- id: standardMinConfidenceThresholdForCalling
  label: standardMinConfidenceThresholdForCalling
  doc: |-
    -stand-call-conf (default: 10.0) The minimum phred-scaled confidence threshold at which variants should be called
  type:
  - double
  - 'null'
  inputBinding:
    prefix: --standard-min-confidence-threshold-for-calling
- id: useNewQualCalculator
  label: useNewQualCalculator
  doc: |-
    -new-qual If provided, we will use the new AF model instead of the so-called exact model
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --use-new-qual-calculator
- id: inputRead
  label: inputRead
  doc: BAM/SAM/CRAM file containing reads
  type: File
  secondaryFiles: |-
    ${

            function resolveSecondary(base, secPattern) {
              if (secPattern[0] == "^") {
                var spl = base.split(".");
                var endIndex = spl.length > 1 ? spl.length - 1 : 1;
                return resolveSecondary(spl.slice(undefined, endIndex).join("."), secPattern.slice(1));
              }
              return base + secPattern
            }

            return [
                    {
                        location: resolveSecondary(self.location, "^.bai"),
                        basename: resolveSecondary(self.basename, ".bai"),
                        class: "File",
                    }
            ];

    }
  inputBinding:
    prefix: --input
- id: reference
  label: reference
  doc: Reference sequence file
  type: File
  secondaryFiles:
  - .fai
  - .amb
  - .ann
  - .bwt
  - .pac
  - .sa
  - ^.dict
  inputBinding:
    prefix: --reference
    position: 5
- id: outputFilename
  label: outputFilename
  doc: File to which variants should be written
  type:
  - string
  - 'null'
  default: generated.vcf.gz
  inputBinding:
    prefix: --output
    position: 8
    valueFrom: $(inputs.inputRead.basename.replace(/.bam$/, "")).vcf.gz
- id: dbsnp
  label: dbsnp
  doc: '(Also: -D) A dbSNP VCF file.'
  type: File
  secondaryFiles:
  - .tbi
  inputBinding:
    prefix: --dbsnp
    position: 7
- id: intervals
  label: intervals
  doc: -L (BASE) One or more genomic intervals over which to operate
  type:
  - File
  - 'null'
  inputBinding:
    prefix: --intervals

outputs:
- id: out
  label: out
  doc: |-
    A raw, unfiltered, highly sensitive callset in VCF format. File to which variants should be written
  type: File
  outputBinding:
    glob: $(inputs.inputRead.basename.replace(/.bam$/, "")).vcf.gz

baseCommand:
- gatk
- HaplotypeCaller
arguments: []
id: Gatk4HaplotypeCaller
