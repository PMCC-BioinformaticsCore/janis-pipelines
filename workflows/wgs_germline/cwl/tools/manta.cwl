arguments:
- position: 0
  shellQuote: false
  valueFrom: configManta.py
- position: 2
  shellQuote: false
  valueFrom: $(";{runDir}/runWorkflow.py".replace(/\{runDir\}/g, inputs.runDir))
- position: 3
  prefix: -j
  shellQuote: false
  valueFrom: $(inputs.runtime_cpu)
class: CommandLineTool
cwlVersion: v1.0
doc: "Manta calls structural variants (SVs) and indels from mapped paired-end sequencing\
  \ reads. \nIt is optimized for analysis of germline variation in small sets of individuals\
  \ and somatic \nvariation in tumor/normal sample pairs. Manta discovers, assembles\
  \ and scores large-scale SVs, \nmedium-sized indels and large insertions within\
  \ a single efficient workflow. The method is \ndesigned for rapid analysis on standard\
  \ compute hardware: NA12878 at 50x genomic coverage is \nanalyzed in less than 20\
  \ minutes on a 20 core server, and most WGS tumor/normal analyses \ncan be completed\
  \ within 2 hours. Manta combines paired and split-read evidence during SV \ndiscovery\
  \ and scoring to improve accuracy, but does not require split-reads or successful\
  \ \nbreakpoint assemblies to report a variant in cases where there is strong evidence\
  \ otherwise. \n\nIt provides scoring models for germline variants in small sets\
  \ of diploid samples and somatic \nvariants in matched tumor/normal sample pairs.\
  \ There is experimental support for analysis of \nunmatched tumor samples as well.\
  \ Manta accepts input read mappings from BAM or CRAM files and \nreports all SV\
  \ and indel inferences in VCF 4.1 format. See the user guide for a full description\
  \ \nof capabilities and limitations."
id: manta
inputs:
- doc: provide a configuration file to override defaults in global config file (/opt/conda/share/manta-1.2.1-0/bin/configManta.py.ini)
  id: config
  inputBinding:
    position: 1
    prefix: --config
    shellQuote: false
  label: config
  type:
  - File
  - 'null'
- doc: FILE Normal sample BAM or CRAM file. May be specified more than once, multiple
    inputs will be treated as each BAM file representing a different sample. [optional]
    (no default)
  id: bam
  inputBinding:
    position: 1
    prefix: --bam
    shellQuote: false
  label: bam
  secondaryFiles:
  - ^.bai
  type: File
- default: generated-d5d49306-e018-11e9-851b-a0cec8186c53
  doc: 'Run script and run output will be written to this directory [required] (default:
    MantaWorkflow)'
  id: runDir
  inputBinding:
    position: 1
    prefix: --runDir
    shellQuote: false
  label: runDir
  type: string
- doc: samtools-indexed reference fasta file [required]
  id: reference
  inputBinding:
    position: 1
    prefix: --referenceFasta
    shellQuote: false
  label: reference
  secondaryFiles:
  - .amb
  - .ann
  - .bwt
  - .pac
  - .sa
  - .fai
  - ^.dict
  type: File
- doc: Tumor sample BAM or CRAM file. Only up to one tumor bam file accepted. [optional=null]
  id: tumorBam
  inputBinding:
    position: 1
    prefix: --tumorBam
    shellQuote: false
  label: tumorBam
  secondaryFiles:
  - ^.bai
  type:
  - File
  - 'null'
- doc: 'Set options for WES input: turn off depth filters'
  id: exome
  inputBinding:
    position: 1
    prefix: --exome
    shellQuote: false
  label: exome
  type:
  - boolean
  - 'null'
- doc: Set options for RNA-Seq input. Must specify exactly one bam input file
  id: rna
  inputBinding:
    position: 1
    prefix: --rna
    shellQuote: false
  label: rna
  type:
  - File
  - 'null'
- doc: 'Set if RNA-Seq input is unstranded: Allows splice-junctions on either strand'
  id: unstrandedRNA
  inputBinding:
    position: 1
    prefix: --unstrandedRNA
    shellQuote: false
  label: unstrandedRNA
  type:
  - File
  - 'null'
- doc: Output assembled contig sequences in VCF file
  id: outputContig
  inputBinding:
    position: 1
    prefix: --outputContig
    shellQuote: false
  label: outputContig
  type:
  - File
  - 'null'
- doc: 'Optionally provide a bgzip-compressed/tabix-indexed BED file containing the
    set of regions to call. No VCF output will be provided outside of these regions.
    The full genome will still be used to estimate statistics from the input (such
    as expected depth per chromosome). Only one BED file may be specified. (default:
    call the entire genome)'
  id: callRegions
  inputBinding:
    position: 1
    prefix: --callRegions
    shellQuote: false
  label: callRegions
  secondaryFiles:
  - .tbi
  type:
  - File
  - 'null'
- default: local
  doc: (-m) select run mode (local|sge)
  id: mode
  inputBinding:
    position: 3
    prefix: --mode
    shellQuote: false
  label: mode
  type: string
- doc: Don't write any log output to stderr (but still write to workspace/pyflow.data/logs/pyflow_log.txt)
  id: quiet
  inputBinding:
    position: 3
    prefix: --quiet
    shellQuote: false
  label: quiet
  type:
  - boolean
  - 'null'
- doc: (-q) specify scheduler queue name
  id: queue
  inputBinding:
    position: 3
    prefix: --queue
    shellQuote: false
  label: queue
  type:
  - string
  - 'null'
- doc: "(-g) gigabytes of memory available to run workflow -- only meaningful in local\
    \ mode, must be an integer (default: Estimate the total memory for this node for\
    \ local  mode, 'unlimited' for sge mode)"
  id: memgb
  inputBinding:
    position: 3
    prefix: --memGb
    shellQuote: false
  label: memgb
  type:
  - int
  - 'null'
- doc: "(format: hh:mm:ss) Specify scheduler max runtime per task, argument is provided\
    \ to the 'h_rt' resource limit if using SGE (no default)"
  id: maxTaskRuntime
  inputBinding:
    position: 3
    prefix: --maxTaskRuntime
    shellQuote: false
  label: maxTaskRuntime
  type:
  - string
  - 'null'
label: manta
outputs:
- id: python
  label: python
  outputBinding:
    glob: $("{runDir}/runWorkflow.py".replace(/\{runDir\}/g, inputs.runDir))
  type: File
- id: pickle
  label: pickle
  outputBinding:
    glob: $("{runDir}/runWorkflow.py.config.pickle".replace(/\{runDir\}/g, inputs.runDir))
  type: File
- id: candidateSV
  label: candidateSV
  outputBinding:
    glob: $("{runDir}/results/variants/candidateSV.vcf.gz".replace(/\{runDir\}/g,
      inputs.runDir))
  secondaryFiles:
  - .tbi
  type: File
- id: candidateSmallIndels
  label: candidateSmallIndels
  outputBinding:
    glob: $("{runDir}/results/variants/candidateSmallIndels.vcf.gz".replace(/\{runDir\}/g,
      inputs.runDir))
  secondaryFiles:
  - .tbi
  type: File
- id: diploidSV
  label: diploidSV
  outputBinding:
    glob: $("{runDir}/results/variants/diploidSV.vcf.gz".replace(/\{runDir\}/g, inputs.runDir))
  secondaryFiles:
  - .tbi
  type: File
- id: alignmentStatsSummary
  label: alignmentStatsSummary
  outputBinding:
    glob: $("{runDir}/results/stats/alignmentStatsSummary.txt".replace(/\{runDir\}/g,
      inputs.runDir))
  type: File
- id: svCandidateGenerationStats
  label: svCandidateGenerationStats
  outputBinding:
    glob: $("{runDir}/results/stats/svCandidateGenerationStats.tsv".replace(/\{runDir\}/g,
      inputs.runDir))
  type: File
- id: svLocusGraphStats
  label: svLocusGraphStats
  outputBinding:
    glob: $("{runDir}/results/stats/svLocusGraphStats.tsv".replace(/\{runDir\}/g,
      inputs.runDir))
  type: File
requirements:
  DockerRequirement:
    dockerPull: michaelfranklin/manta:1.5.0
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
