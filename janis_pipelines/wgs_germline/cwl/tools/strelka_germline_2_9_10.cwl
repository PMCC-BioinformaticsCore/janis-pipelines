#!/usr/bin/env cwl-runner
class: CommandLineTool
cwlVersion: v1.0
label: Strelka (Germline)
doc: |-
  Strelka2 is a fast and accurate small variant caller optimized for analysis of germline variation 
  in small cohorts and somatic variation in tumor/normal sample pairs. The germline caller employs 
  an efficient tiered haplotype model to improve accuracy and provide read-backed phasing, adaptively 
  selecting between assembly and a faster alignment-based haplotyping approach at each variant locus. 
  The germline caller also analyzes input sequencing data using a mixture-model indel error estimation 
  method to improve robustness to indel noise. The somatic calling model improves on the original 
  Strelka method for liquid and late-stage tumor analysis by accounting for possible tumor cell 
  contamination in the normal sample. A final empirical variant re-scoring step using random forest 
  models trained on various call quality features has been added to both callers to further improve precision.

  Compared with submissions to the recent PrecisonFDA Consistency and Truth challenges, the average 
  indel F-score for Strelka2 running in its default configuration is 3.1% and 0.08% higher, respectively, 
  than the best challenge submissions. Runtime on a 28-core server is ~40 minutes for 40x WGS germline 
  analysis and ~3 hours for a 110x/40x WGS tumor-normal somatic analysis

  Strelka accepts input read mappings from BAM or CRAM files, and optionally candidate and/or forced-call 
  alleles from VCF. It reports all small variant predictions in VCF 4.1 format. Germline variant 
  reporting uses the gVCF conventions to represent both variant and reference call confidence. 
  For best somatic indel performance, Strelka is designed to be run with the Manta structural variant 
  and indel caller, which provides additional indel candidates up to a given maxiumum indel size 
  (49 by default). By design, Manta and Strelka run together with default settings provide complete 
  coverage over all indel sizes (in additional to SVs and SNVs). 

  See the user guide for a full description of capabilities and limitations

requirements:
- class: ShellCommandRequirement
- class: InlineJavascriptRequirement
- class: DockerRequirement
  dockerPull: michaelfranklin/strelka:2.9.10

inputs:
- id: bam
  label: bam
  doc: |-
    Sample BAM or CRAM file. May be specified more than once, multiple inputs will be treated as each BAM file representing a different sample. [required] (no default)
  type: File
  secondaryFiles:
  - .bai
  inputBinding:
    prefix: --bam
    position: 1
    shellQuote: false
- id: reference
  label: reference
  doc: samtools-indexed reference fasta file [required]
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
    prefix: --referenceFasta
    position: 1
    shellQuote: false
- id: relativeStrelkaDirectory
  label: relativeStrelkaDirectory
  doc: |-
    Name of directory to be created where all workflow scripts and output will be written. Each analysis requires a separate directory.
  type: string
  default: strelka_dir
  inputBinding:
    prefix: --runDir
    position: 1
    shellQuote: false
- id: ploidy
  label: ploidy
  doc: |-
    Provide ploidy file in VCF. The VCF should include one sample column per input sample labeled with the same sample names found in the input BAM/CRAM RG header sections. Ploidy should be provided in records using the FORMAT/CN field, which are interpreted to span the range [POS+1, INFO/END]. Any CN value besides 1 or 0 will be treated as 2. File must be tabix indexed. (no default)
  type:
  - File
  - 'null'
  secondaryFiles:
  - .tbi
  inputBinding:
    prefix: --ploidy
    position: 1
    shellQuote: false
- id: noCompress
  label: noCompress
  doc: |-
    Provide BED file of regions where gVCF block compression is not allowed. File must be bgzip- compressed/tabix-indexed. (no default)
  type:
  - File
  - 'null'
  secondaryFiles:
  - .tbi
  inputBinding:
    prefix: --noCompress
    position: 1
    shellQuote: false
- id: callContinuousVf
  label: callContinuousVf
  doc: |-
    Call variants on CHROM without a ploidy prior assumption, issuing calls with continuous variant frequencies (no default)
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --callContinuousVf
- id: rna
  label: rna
  doc: Set options for RNA-Seq input.
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --rna
    position: 1
    shellQuote: false
- id: indelCandidates
  label: indelCandidates
  doc: |-
    Specify a VCF of candidate indel alleles. These alleles are always evaluated but only reported in the output when they are inferred to exist in the sample. The VCF must be tabix indexed. All indel alleles must be left-shifted/normalized, any unnormalized alleles will be ignored. This option may be specified more than once, multiple input VCFs will be merged. (default: None)
  type:
  - File
  - 'null'
  secondaryFiles:
  - .tbi
  inputBinding:
    prefix: --indelCandidates
    position: 1
    shellQuote: false
- id: forcedGT
  label: forcedGT
  doc: |-
    Specify a VCF of candidate alleles. These alleles are always evaluated and reported even if they are unlikely to exist in the sample. The VCF must be tabix indexed. All indel alleles must be left- shifted/normalized, any unnormalized allele will trigger a runtime error. This option may be specified more than once, multiple input VCFs will be merged. Note that for any SNVs provided in the VCF, the SNV site will be reported (and for gVCF, excluded from block compression), but the specific SNV alleles are ignored. (default: None)
  type:
  - File
  - 'null'
  secondaryFiles:
  - .tbi
  inputBinding:
    prefix: --forcedGT
    position: 1
    shellQuote: false
- id: exome
  label: exome
  doc: |-
    Set options for exome note in particular that this flag turns off high-depth filters
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --exome
    position: 1
    shellQuote: false
- id: targeted
  label: targeted
  doc: |-
    Set options for other targeted input: note in particular that this flag turns off high-depth filters
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --exome
    position: 1
    shellQuote: false
- id: callRegions
  label: callRegions
  doc: |-
    Optionally provide a bgzip-compressed/tabix-indexed BED file containing the set of regions to call. No VCF output will be provided outside of these regions. The full genome will still be used to estimate statistics from the input (such as expected depth per chromosome). Only one BED file may be specified. (default: call the entire genome)
  type:
  - File
  - 'null'
  secondaryFiles:
  - .tbi
  inputBinding:
    prefix: --callRegions=
    position: 1
    separate: false
- id: mode
  label: mode
  doc: (-m MODE)  select run mode (local|sge)
  type: string
  default: local
  inputBinding:
    prefix: --mode
    position: 3
    shellQuote: false
- id: queue
  label: queue
  doc: (-q QUEUE) specify scheduler queue name
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --queue
    position: 3
    shellQuote: false
- id: memGb
  label: memGb
  doc: |2-
     (-g MEMGB) gigabytes of memory available to run workflow -- only meaningful in local mode, must be an integer (default: Estimate the total memory for this node for local mode, 'unlimited' for sge mode)
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --memGb
    position: 3
    shellQuote: false
- id: quiet
  label: quiet
  doc: |-
    Don't write any log output to stderr (but still write to workspace/pyflow.data/logs/pyflow_log.txt)
  type:
  - boolean
  - 'null'
  inputBinding:
    prefix: --quiet
    position: 3
    shellQuote: false
- id: mailTo
  label: mailTo
  doc: |-
    (-e) send email notification of job completion status to this address (may be provided multiple times for more than one email address)
  type:
  - string
  - 'null'
  inputBinding:
    prefix: --mailTo
    position: 3
    shellQuote: false

outputs:
- id: configPickle
  label: configPickle
  type: File
  outputBinding:
    glob: $((inputs.relativeStrelkaDirectory + "/runWorkflow.py.config.pickle"))
    outputEval: $((inputs.relativeStrelkaDirectory + "/runWorkflow.py.config.pickle"))
    loadContents: false
- id: script
  label: script
  type: File
  outputBinding:
    glob: $((inputs.relativeStrelkaDirectory + "/runWorkflow.py"))
    outputEval: $((inputs.relativeStrelkaDirectory + "/runWorkflow.py"))
    loadContents: false
- id: stats
  label: stats
  doc: |-
    A tab-delimited report of various internal statistics from the variant calling process: Runtime information accumulated for each genome segment, excluding auxiliary steps such as BAM indexing and vcf merging. Indel candidacy statistics
  type: File
  outputBinding:
    glob: $((inputs.relativeStrelkaDirectory + "/results/stats/runStats.tsv"))
    outputEval: $((inputs.relativeStrelkaDirectory + "/results/stats/runStats.tsv"))
    loadContents: false
- id: variants
  label: variants
  doc: Primary variant inferences are provided as a series of VCF 4.1 files
  type: File
  secondaryFiles:
  - .tbi
  outputBinding:
    glob: $((inputs.relativeStrelkaDirectory + "/results/variants/variants.vcf.gz"))
    outputEval: $((inputs.relativeStrelkaDirectory + "/results/variants/variants.vcf.gz"))
    loadContents: false
- id: genome
  label: genome
  type: File
  secondaryFiles:
  - .tbi
  outputBinding:
    glob: $((inputs.relativeStrelkaDirectory + "/results/variants/genome.vcf.gz"))
    outputEval: $((inputs.relativeStrelkaDirectory + "/results/variants/genome.vcf.gz"))
    loadContents: false
stdout: _stdout
stderr: _stderr
arguments:
- position: 0
  valueFrom: configureStrelkaGermlineWorkflow.py
  shellQuote: false
- position: 2
  valueFrom: |-
    $(";{relativeStrelkaDirectory}/runWorkflow.py".replace(/\{relativeStrelkaDirectory\}/g, inputs.relativeStrelkaDirectory))
  shellQuote: false
- prefix: --jobs
  position: 3
  valueFrom: |-
    $([inputs.runtime_cpu, 4, 1].filter(function (inner) { return inner != null })[0])
  shellQuote: false
id: strelka_germline
