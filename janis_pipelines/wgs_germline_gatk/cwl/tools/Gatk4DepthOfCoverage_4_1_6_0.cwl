#!/usr/bin/env cwl-runner
class: CommandLineTool
cwlVersion: v1.0
label: 'GATK4: Generate coverage summary information for reads data'
doc: |-
  Generate coverage summary information for reads data

  Category Coverage Analysis
  Overview
  Assess sequence coverage by a wide array of metrics, partitioned by sample, read group, or library
  This tool processes a set of bam files to determine coverage at different levels of partitioning and aggregation. Coverage can be analyzed per locus, per interval, per gene, or in total; can be partitioned by sample, by read group, by technology, by center, or by library; and can be summarized by mean, median, quartiles, and/or percentage of bases covered to or beyond a threshold. Additionally, reads and bases can be filtered by mapping or base quality score.

requirements:
- class: ShellCommandRequirement
- class: InlineJavascriptRequirement
- class: DockerRequirement
  dockerPull: broadinstitute/gatk:4.1.6.0

inputs:
- id: javaOptions
  label: javaOptions
  type:
  - type: array
    items: string
  - 'null'
- id: compression_level
  label: compression_level
  doc: |-
    Compression level for all compressed files created (e.g. BAM and VCF). Default value: 2.
  type:
  - int
  - 'null'
- id: bam
  label: bam
  doc: The SAM/BAM/CRAM file containing reads.
  type: File
  secondaryFiles:
  - |-
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
    prefix: -I
- id: reference
  label: reference
  doc: Reference sequence
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
    prefix: -R
- id: outputPrefix
  label: outputPrefix
  doc: An output file created by the walker. Will overwrite contents if file exists
  type: string
  inputBinding:
    prefix: -O
- id: intervals
  label: intervals
  doc: -L (BASE) One or more genomic intervals over which to operate
  type:
    type: array
    inputBinding:
      prefix: --intervals
    items: File
  inputBinding: {}
- id: countType
  label: countType
  doc: |-
    overlapping reads from the same  fragment be handled? (COUNT_READS|COUNT_FRAGMENTS|COUNT_FRAGMENTS_REQUIRE_SAME_BASE)
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --count-type
- id: summaryCoverageThreshold
  label: summaryCoverageThreshold
  doc: Coverage threshold (in percent) for summarizing statistics
  type:
  - type: array
    inputBinding:
      prefix: --summary-coverage-threshold
    items: int
  - 'null'
  inputBinding: {}
- id: omitDepthOutputAtEachBase
  label: omitDepthOutputAtEachBase
  doc: Do not output depth of coverage at each base
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --omit-depth-output-at-each-base
- id: omitGenesNotEntirelyCoveredByTraversal
  label: omitGenesNotEntirelyCoveredByTraversal
  doc: |-
    Do not output gene summary if it was not completely covered by traversal intervals
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --omit-genes-not-entirely-covered-by-traversal
- id: omitIntervalStatistics
  label: omitIntervalStatistics
  doc: Do not calculate per-interval statistics
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --omit-interval-statistics
- id: omitLocusTable
  label: omitLocusTable
  doc: Do not calculate per-sample per-depth counts of loci
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --omit-locus-table
- id: omitPerSampleStatistics
  label: omitPerSampleStatistics
  doc: Do not output the summary files per-sample
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --omit-per-sample-statistics

outputs:
- id: out_sample
  label: out_sample
  doc: per locus coverage
  type:
  - File
  - 'null'
  outputBinding:
    glob: $(inputs.outputPrefix)
    loadContents: false
- id: out_sampleCumulativeCoverageCounts
  label: out_sampleCumulativeCoverageCounts
  doc: coverage histograms (# locus with >= X coverage), aggregated over all bases
  type: File
  outputBinding:
    glob: $((inputs.outputPrefix + ".sample_cumulative_coverage_counts"))
    outputEval: $((inputs.outputPrefix + ".sample_cumulative_coverage_counts"))
    loadContents: false
- id: out_sampleCumulativeCoverageProportions
  label: out_sampleCumulativeCoverageProportions
  doc: proprotions of loci with >= X coverage, aggregated over all bases
  type: File
  outputBinding:
    glob: $((inputs.outputPrefix + ".sample_cumulative_coverage_proportions"))
    outputEval: $((inputs.outputPrefix + ".sample_cumulative_coverage_proportions"))
    loadContents: false
- id: out_sampleIntervalStatistics
  label: out_sampleIntervalStatistics
  doc: |-
    total, mean, median, quartiles, and threshold proportions, aggregated per interval
  type: File
  outputBinding:
    glob: $((inputs.outputPrefix + ".sample_interval_statistics"))
    outputEval: $((inputs.outputPrefix + ".sample_interval_statistics"))
    loadContents: false
- id: out_sampleIntervalSummary
  label: out_sampleIntervalSummary
  doc: '2x2 table of # of intervals covered to >= X depth in >=Y samples'
  type: File
  outputBinding:
    glob: $((inputs.outputPrefix + ".sample_interval_summary"))
    outputEval: $((inputs.outputPrefix + ".sample_interval_summary"))
    loadContents: false
- id: out_sampleStatistics
  label: out_sampleStatistics
  doc: coverage histograms (# locus with X coverage), aggregated over all bases
  type: File
  outputBinding:
    glob: $((inputs.outputPrefix + ".sample_statistics"))
    outputEval: $((inputs.outputPrefix + ".sample_statistics"))
    loadContents: false
- id: out_sampleSummary
  label: out_sampleSummary
  doc: |-
    total, mean, median, quartiles, and threshold proportions, aggregated over all bases
  type: File
  outputBinding:
    glob: $((inputs.outputPrefix + ".sample_summary"))
    outputEval: $((inputs.outputPrefix + ".sample_summary"))
    loadContents: false
stdout: _stdout
stderr: _stderr

baseCommand:
- gatk
- DepthOfCoverage
arguments:
- prefix: --java-options
  position: -1
  valueFrom: |-
    $("-Xmx{memory}G {compression} {otherargs}".replace(/\{memory\}/g, (([inputs.runtime_memory, 8, 4].filter(function (inner) { return inner != null })[0] * 3) / 4)).replace(/\{compression\}/g, (inputs.compression_level != null) ? ("-Dsamjdk.compress_level=" + inputs.compression_level) : "").replace(/\{otherargs\}/g, [inputs.javaOptions, []].filter(function (inner) { return inner != null })[0].join(" ")))
id: Gatk4DepthOfCoverage
