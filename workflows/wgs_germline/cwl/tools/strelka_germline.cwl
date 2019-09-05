arguments:
- position: 0
  shellQuote: false
  valueFrom: configureStrelkaGermlineWorkflow.py
- position: 2
  shellQuote: false
  valueFrom: $(";{relativeStrelkaDirectory}/runWorkflow.py".replace(/\{relativeStrelkaDirectory\}/g,
    inputs.relativeStrelkaDirectory))
- position: 3
  prefix: --jobs
  shellQuote: false
  valueFrom: $(inputs.runtime_cpu)
class: CommandLineTool
cwlVersion: v1.0
doc: "Strelka2 is a fast and accurate small variant caller optimized for analysis\
  \ of germline variation \nin small cohorts and somatic variation in tumor/normal\
  \ sample pairs. The germline caller employs \nan efficient tiered haplotype model\
  \ to improve accuracy and provide read-backed phasing, adaptively \nselecting between\
  \ assembly and a faster alignment-based haplotyping approach at each variant locus.\
  \ \nThe germline caller also analyzes input sequencing data using a mixture-model\
  \ indel error estimation \nmethod to improve robustness to indel noise. The somatic\
  \ calling model improves on the original \nStrelka method for liquid and late-stage\
  \ tumor analysis by accounting for possible tumor cell \ncontamination in the normal\
  \ sample. A final empirical variant re-scoring step using random forest \nmodels\
  \ trained on various call quality features has been added to both callers to further\
  \ improve precision.\n\nCompared with submissions to the recent PrecisonFDA Consistency\
  \ and Truth challenges, the average \nindel F-score for Strelka2 running in its\
  \ default configuration is 3.1% and 0.08% higher, respectively, \nthan the best\
  \ challenge submissions. Runtime on a 28-core server is ~40 minutes for 40x WGS\
  \ germline \nanalysis and ~3 hours for a 110x/40x WGS tumor-normal somatic analysis\n\
  \nStrelka accepts input read mappings from BAM or CRAM files, and optionally candidate\
  \ and/or forced-call \nalleles from VCF. It reports all small variant predictions\
  \ in VCF 4.1 format. Germline variant \nreporting uses the gVCF conventions to represent\
  \ both variant and reference call confidence. \nFor best somatic indel performance,\
  \ Strelka is designed to be run with the Manta structural variant \nand indel caller,\
  \ which provides additional indel candidates up to a given maxiumum indel size \n\
  (49 by default). By design, Manta and Strelka run together with default settings\
  \ provide complete \ncoverage over all indel sizes (in additional to SVs and SNVs).\
  \ \n\nSee the user guide for a full description of capabilities and limitations"
id: strelka_germline
inputs:
- doc: Sample BAM or CRAM file. May be specified more than once, multiple inputs will
    be treated as each BAM file representing a different sample. [required] (no default)
  id: bam
  inputBinding:
    position: 1
    prefix: --bam
    shellQuote: false
  label: bam
  secondaryFiles:
  - ^.bai
  type: File
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
- default: strelka_dir
  doc: Name of directory to be created where all workflow scripts and output will
    be written. Each analysis requires a separate directory.
  id: relativeStrelkaDirectory
  inputBinding:
    position: 1
    prefix: --runDir
    shellQuote: false
  label: relativeStrelkaDirectory
  type: string
- doc: Provide ploidy file in VCF. The VCF should include one sample column per input
    sample labeled with the same sample names found in the input BAM/CRAM RG header
    sections. Ploidy should be provided in records using the FORMAT/CN field, which
    are interpreted to span the range [POS+1, INFO/END]. Any CN value besides 1 or
    0 will be treated as 2. File must be tabix indexed. (no default)
  id: ploidy
  inputBinding:
    position: 1
    prefix: --ploidy
    shellQuote: false
  label: ploidy
  secondaryFiles:
  - .tbi
  type:
  - File
  - 'null'
- doc: Provide BED file of regions where gVCF block compression is not allowed. File
    must be bgzip- compressed/tabix-indexed. (no default)
  id: noCompress
  inputBinding:
    position: 1
    prefix: --noCompress
    shellQuote: false
  label: noCompress
  secondaryFiles:
  - .tbi
  type:
  - File
  - 'null'
- doc: Call variants on CHROM without a ploidy prior assumption, issuing calls with
    continuous variant frequencies (no default)
  id: callContinuousVf
  inputBinding:
    prefix: --callContinuousVf
  label: callContinuousVf
  type:
  - string
  - 'null'
- doc: Set options for RNA-Seq input.
  id: rna
  inputBinding:
    position: 1
    prefix: --rna
    shellQuote: false
  label: rna
  type:
  - boolean
  - 'null'
- doc: 'Specify a VCF of candidate indel alleles. These alleles are always evaluated
    but only reported in the output when they are inferred to exist in the sample.
    The VCF must be tabix indexed. All indel alleles must be left-shifted/normalized,
    any unnormalized alleles will be ignored. This option may be specified more than
    once, multiple input VCFs will be merged. (default: None)'
  id: indelCandidates
  inputBinding:
    position: 1
    prefix: --indelCandidates
    shellQuote: false
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
  id: forcedGT
  inputBinding:
    position: 1
    prefix: --forcedGT
    shellQuote: false
  label: forcedGT
  secondaryFiles:
  - .tbi
  type:
  - File
  - 'null'
- doc: '--targeted Set options for exome or other targeted input: note in particular
    that this flag turns off high-depth filters'
  id: exome
  inputBinding:
    position: 1
    prefix: --exome
    shellQuote: false
  label: exome
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
    prefix: --callRegions=
    separate: false
  label: callRegions
  secondaryFiles:
  - .tbi
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
- doc: (-e) send email notification of job completion status to this address (may
    be provided multiple times for more than one email address)
  id: mailTo
  inputBinding:
    position: 3
    prefix: --mailTo
    shellQuote: false
  label: mailTo
  type:
  - string
  - 'null'
label: strelka_germline
outputs:
- id: configPickle
  label: configPickle
  outputBinding:
    glob: $("{relativeStrelkaDirectory}/runWorkflow.py.config.pickle".replace(/\{relativeStrelkaDirectory\}/g,
      inputs.relativeStrelkaDirectory))
  type: File
- id: script
  label: script
  outputBinding:
    glob: $("{relativeStrelkaDirectory}/runWorkflow.py".replace(/\{relativeStrelkaDirectory\}/g,
      inputs.relativeStrelkaDirectory))
  type: File
- doc: 'A tab-delimited report of various internal statistics from the variant calling
    process: Runtime information accumulated for each genome segment, excluding auxiliary
    steps such as BAM indexing and vcf merging. Indel candidacy statistics'
  id: stats
  label: stats
  outputBinding:
    glob: $("{relativeStrelkaDirectory}/results/stats/runStats.tsv".replace(/\{relativeStrelkaDirectory\}/g,
      inputs.relativeStrelkaDirectory))
  type: File
- doc: Primary variant inferences are provided as a series of VCF 4.1 files
  id: variants
  label: variants
  outputBinding:
    glob: $("{relativeStrelkaDirectory}/results/variants/variants.vcf.gz".replace(/\{relativeStrelkaDirectory\}/g,
      inputs.relativeStrelkaDirectory))
  secondaryFiles:
  - .tbi
  type: File
- id: genome
  label: genome
  outputBinding:
    glob: $("{relativeStrelkaDirectory}/results/variants/genome.vcf.gz".replace(/\{relativeStrelkaDirectory\}/g,
      inputs.relativeStrelkaDirectory))
  secondaryFiles:
  - .tbi
  type: File
requirements:
  DockerRequirement:
    dockerPull: michaelfranklin/strelka:2.9.10
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
