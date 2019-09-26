arguments:
- position: 0
  valueFrom: configureStrelkaSomaticWorkflow.py
- position: 2
  shellQuote: false
  valueFrom: $(";{rundir}/runWorkflow.py".replace(/\{rundir\}/g, inputs.rundir))
- position: 3
  prefix: --jobs
  shellQuote: false
  valueFrom: $(inputs.runtime_cpu)
class: CommandLineTool
cwlVersion: v1.0
doc: "Usage: configureStrelkaSomaticWorkflow.py [options]\nVersion: 2.9.10\nThis script\
  \ configures Strelka somatic small variant calling.\nYou must specify an alignment\
  \ file (BAM or CRAM) for each sample of a matched tumor-normal pair.\nConfiguration\
  \ will produce a workflow run script which can execute the workflow on a single\
  \ node or through\nsge and resume any interrupted execution."
id: strelka_somatic
inputs:
- doc: Normal sample BAM or CRAM file. (no default)
  id: normalBam
  inputBinding:
    position: 1
    prefix: --normalBam=
    separate: false
  label: normalBam
  secondaryFiles:
  - ^.bai
  type: File
- doc: (--tumorBam)  Tumor sample BAM or CRAM file. [required] (no default)
  id: tumorBam
  inputBinding:
    position: 1
    prefix: --tumourBam=
    separate: false
  label: tumorBam
  secondaryFiles:
  - ^.bai
  type: File
- doc: ' samtools-indexed reference fasta file [required]'
  id: reference
  inputBinding:
    position: 1
    prefix: --referenceFasta=
    separate: false
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
- default: generated-f2473d9a-e018-11e9-af76-a0cec8186c53
  doc: 'Name of directory to be created where all workflow scripts and output will
    be written. Each analysis requires a separate directory. (default: StrelkaSomaticWorkflow)'
  id: rundir
  inputBinding:
    position: 1
    prefix: --runDir=
    separate: false
  label: rundir
  type: string
- doc: "Limit the analysis to one or more genome region(s) for debugging purposes.\
    \ If this argument is provided multiple times the union of all specified regions\
    \ will be analyzed. All regions must be non-overlapping to get a meaningful result.\
    \ Examples: '--region chr20' (whole chromosome), '--region chr2:100-2000 --region\
    \ chr3:2500-3000' (two regions)'. If this option is specified (one or more times)\
    \ together with the 'callRegions' BED file,then all region arguments will be intersected\
    \ with the callRegions BED track."
  id: region
  inputBinding:
    position: 1
    prefix: --region=
    separate: false
  label: region
  type:
  - File
  - 'null'
- doc: provide a configuration file to override defaults in global config file (/opt/strelka/bin/configureStrelkaSomaticWorkflow.py.ini)
  id: config
  inputBinding:
    position: 1
    prefix: --config=
    separate: false
  label: config
  type:
  - File
  - 'null'
- doc: ' Output a bed file describing somatic callable regions of the genome'
  id: outputcallableregions
  inputBinding:
    position: 1
    prefix: --outputCallableRegions
    separate: true
  label: outputcallableregions
  type:
  - File
  - 'null'
- doc: 'Specify a VCF of candidate indel alleles. These alleles are always evaluated
    but only reported in the output when they are inferred to exist in the sample.
    The VCF must be tabix indexed. All indel alleles must be left-shifted/normalized,
    any unnormalized alleles will be ignored. This option may be specified more than
    once, multiple input VCFs will be merged. (default: None)'
  id: indelCandidates
  inputBinding:
    position: 1
    prefix: --indelCandidates=
    separate: false
  label: indelCandidates
  secondaryFiles:
  - .tbi
  type:
  - File
  - 'null'
- doc: 'Specify a VCF of candidate alleles. These alleles are always evaluated and
    reported even if they are unlikely to exist in the sample. The VCF must be tabix
    indexed. All indel alleles must be left- shifted/normalized, any unnormalized
    allele will trigger a runtime error. This option may be specified more than once,
    multiple input VCFs will be merged. Note that for any SNVs provided in the VCF,
    the SNV site will be reported (and for gVCF, excluded from block compression),
    but the specific SNV alleles are ignored. (default: None)'
  id: forcedgt
  inputBinding:
    position: 1
    prefix: --forcedGT=
    separate: false
  label: forcedgt
  type:
  - File
  - 'null'
- doc: '(--exome)  Set options for exome or other targeted input: note in particular
    that this flag turns off high-depth filters'
  id: targeted
  inputBinding:
    position: 1
    prefix: --targeted
    separate: true
  label: targeted
  type:
  - boolean
  - 'null'
- doc: 'Optionally provide a bgzip-compressed/tabix-indexed BED file containing the
    set of regions to call. No VCF output will be provided outside of these regions.
    The full genome will still be used to estimate statistics from the input (such
    as expected depth per chromosome). Only one BED file may be specified. (default:
    call the entire genome)'
  id: callRegions
  inputBinding:
    position: 1
    prefix: --callRegions=
    separate: false
  label: callRegions
  secondaryFiles:
  - .tbi
  type:
  - File
  - 'null'
- doc: Noise vcf file (submit argument multiple times for more than one file)
  id: noisevcf
  inputBinding:
    position: 1
    prefix: --noiseVcf=
    separate: false
  label: noisevcf
  type:
  - File
  - 'null'
- doc: 'Maximum sequence region size (in megabases) scanned by each task during genome
    variant calling. (default: 12)'
  id: scansizemb
  inputBinding:
    position: 1
    prefix: --scanSizeMb=
    separate: false
  label: scansizemb
  type:
  - int
  - 'null'
- doc: Set variant calling task memory limit (in megabytes). It is not recommended
    to change the default in most cases, but this might be required for a sample of
    unusual depth.
  id: callmemmb
  inputBinding:
    position: 1
    prefix: --callMemMb=
    separate: false
  label: callmemmb
  type:
  - int
  - 'null'
- default: false
  doc: Keep all temporary files (for workflow debugging)
  id: retaintempfiles
  inputBinding:
    position: 1
    prefix: --retainTempFiles
    separate: true
  label: retaintempfiles
  type: boolean
- doc: Disable empirical variant scoring (EVS).
  id: disableevs
  inputBinding:
    position: 1
    prefix: --disableEVS
    separate: true
  label: disableevs
  type:
  - boolean
  - 'null'
- doc: ' Report all empirical variant scoring features in VCF output.'
  id: reportevsfeatures
  inputBinding:
    position: 1
    prefix: --reportEVSFeatures
    separate: true
  label: reportevsfeatures
  type:
  - boolean
  - 'null'
- doc: ' Provide a custom empirical scoring model file for SNVs (default: /opt/strelka/share/config/somaticSNVScoringM
    odels.json)'
  id: snvscoringmodelfile
  inputBinding:
    position: 1
    prefix: --snvScoringModelFile=
    separate: false
  label: snvscoringmodelfile
  type:
  - File
  - 'null'
- doc: ' Provide a custom empirical scoring model file for indels (default: /opt/strelka/share/config/somaticInde
    lScoringModels.json)'
  id: indelscoringmodelfile
  inputBinding:
    position: 1
    prefix: --indelScoringModelFile=
    separate: false
  label: indelscoringmodelfile
  type:
  - File
  - 'null'
- default: local
  doc: (-m MODE)  select run mode (local|sge)
  id: mode
  inputBinding:
    position: 3
    prefix: --mode
    shellQuote: false
  label: mode
  type: string
- doc: (-q QUEUE) specify scheduler queue name
  id: queue
  inputBinding:
    position: 3
    prefix: --queue
    shellQuote: false
  label: queue
  type:
  - string
  - 'null'
- doc: " (-g MEMGB) gigabytes of memory available to run workflow -- only meaningful\
    \ in local mode, must be an integer (default: Estimate the total memory for this\
    \ node for local mode, 'unlimited' for sge mode)"
  id: memGb
  inputBinding:
    position: 3
    prefix: --memGb
    shellQuote: false
  label: memGb
  type:
  - string
  - 'null'
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
label: strelka_somatic
outputs:
- id: configPickle
  label: configPickle
  outputBinding:
    glob: $("{rundir}/runWorkflow.py.config.pickle".replace(/\{rundir\}/g, inputs.rundir))
  type: File
- id: script
  label: script
  outputBinding:
    glob: $("{rundir}/runWorkflow.py".replace(/\{rundir\}/g, inputs.rundir))
  type: File
- doc: 'A tab-delimited report of various internal statistics from the variant calling
    process: Runtime information accumulated for each genome segment, excluding auxiliary
    steps such as BAM indexing and vcf merging. Indel candidacy statistics'
  id: stats
  label: stats
  outputBinding:
    glob: $("{rundir}/results/stats/runStats.tsv".replace(/\{rundir\}/g, inputs.rundir))
  type: File
- doc: ''
  id: indels
  label: indels
  outputBinding:
    glob: $("{rundir}/results/variants/somatic.indels.vcf.gz".replace(/\{rundir\}/g,
      inputs.rundir))
  secondaryFiles:
  - .tbi
  type: File
- doc: ''
  id: snvs
  label: snvs
  outputBinding:
    glob: $("{rundir}/results/variants/somatic.snvs.vcf.gz".replace(/\{rundir\}/g,
      inputs.rundir))
  secondaryFiles:
  - .tbi
  type: File
requirements:
  DockerRequirement:
    dockerPull: michaelfranklin/strelka:2.9.10
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
