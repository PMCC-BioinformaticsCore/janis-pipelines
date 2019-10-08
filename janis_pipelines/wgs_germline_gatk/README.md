# Janis - WGS Germline (GATK) Pipeline

This workflow is a reference pipeline using the [Janis](https://github.com/PMCC-BioinformaticsCore/janis) Python framework (pipelines assistant).

> This workflow is an abridged version of the full mult-variant caller germline pipeline. 
    
1. Takes raw sequence data in the FASTQ format;
2. align to the reference genome using BWA MEM;
3. Marks duplicates using Picard;
4. Call the GATK variant caller
5. Outputs the final variants in the VCF format. 

## Validation

These variants were validated against the [Genome in a Bottle](https://github.com/PMCC-BioinformaticsCore/janis-workshops#data)
data sets to achieve:

- Recall: 98.15%
- Precision: 99.69%

These results were identical across 3 research institutes (combination of Slurm / PBS / Torque) 
and Google Cloud platform.

## How to use

[`janis-runner`](https://github.com/PMCC-BioinformaticsCore/janis-runner) can be used to generate an inputs template and run, or just to translate the 
workflow for you to use. `janis-runner` has basic support for CWLTool and Cromwell.

```bash
# View the translated workflow
janis translate germline.py wdl

# Generate an input template for a workflow
janis inputs germline.py > germlineInp.yml

# Run the workflow with Cromwell
janis run germline.py --inputs germlineInp.yml --engine cromwell
```

This pipeline has been run on a 30x level (with `--hint-captureType 30X`) with
Cromwell (HPC w/ Singularity + GCP), and also run on a targeted panel (GiaB BRCA1) with
CWLTool and Toil. 

The pipeline takes approximately 27-30 hours to run at a 30x coverage,
depending on the allocated resources. A sample `resources.json` is provided for a 30x coverage, 
however this disk sizes **will** need to be adjusted for GCP.


### Alternatively

You can download the CWL or WDL representations, fill out the job (`.yml` / `.json`) file
and run using your preferred engine. 


## Variant callers

This pipeline uses 3 variant callers:

### GATK4

> Documentation: [GATK4 Germline Variant Caller](https://janis.readthedocs.io/en/latest/tools/bioinformatics/variant%20callers/gatk4_variantcaller.html)

1. BaseRecalibrator
1. ApplyBQSR
1. HaplotypeCaller
1. SplitMultiAllele


### Strelka (Illumina)

> Documentation: [Strelka Germline Variant Caller](https://janis.readthedocs.io/en/latest/tools/bioinformatics/variant%20callers/strelkagermlinevariantcaller.html)

1. Manta
1. Strelka
1. BCFTools View
1. SplitMultiAllele


### VarDict

1. VarDict
1. BCFTools Annotate
1. SplitMultiAllele
1. Trim 


## Tools

The following table lists all of the tools, versions and OCI containers used in the 

| tool                                                            | version     | container |
| :-------------------------------------------------------------- |:----------: | :--------------------------------------------------- |
| Bwa mem + Samtools View (BwaMemSamtoolsView)                    | 0.7.17|1.9  | michaelfranklin/bwasamtools:0.7.17-1.9 |
| BCFTools: View (bcftoolsview)                                   | v1.5        | biocontainers/bcftools:v1.5_cv2 |
| BCFTools: Annotate (bcftoolsAnnotate)                           | v1.5        | biocontainers/bcftools:v1.5_cv2 |
| BCFTools: Sort (bcftoolssort)                                   | v1.9        | michaelfranklin/bcftools:1.9 |
| Cutadapt (cutadapt)                                             | 1.18        | quay.io/biocontainers/cutadapt:1.18--py37h14c3975_1 |
| Combine Variants (combinevariants)                              | 0.0.4       | michaelfranklin/pmacutil:0.0.4 |
| FastQC (fastqc)                                                 | v0.11.5     | biocontainers/fastqc:v0.11.5_cv3 |
| GATK4: SortSAM (gatk4sortsam)                                   | 4.0.12.0    | broadinstitute/gatk:4.0.12.0 |
| GATK4: Merge SAM Files (Gatk4MergeSamFiles)                     | 4.0.12.0    | broadinstitute/gatk:4.0.12.0 |
| GATK4: Mark Duplicates (Gatk4MarkDuplicates)                    | 4.0.12.0    | broadinstitute/gatk:4.0.12.0 |
| GATK4: Base Recalibrator (Gatk4BaseRecalibrator)                | 4.0.12.0    | broadinstitute/gatk:4.0.12.0 |
| GATK4: Apply base quality score recalibration (GATK4ApplyBQSR)  | 4.0.12.0    | broadinstitute/gatk:4.0.12.0 |
| GATK4: Haplotype Caller (GatkHaplotypeCaller)                   | 4.0.12.0    | broadinstitute/gatk:4.0.12.0 |
| GATK4: Gather VCFs (Gatk4GatherVcfs)                            | 4.0.12.0    | broadinstitute/gatk:4.0.12.0 |
| Manta (manta)                                                   | 1.5.0       | michaelfranklin/manta:1.5.0 |
| Split Multiple Alleles (SplitMultiAllele)                       | v0.5772     | heuermh/vt |
| Strelka (Germline) (strelka_germline)                           | 2.9.10      | michaelfranklin/strelka:2.9.10 |
| Trim IUPAC Bases (trimIUPAC)                                    | 0.0.4       | michaelfranklin/pmacutil:0.0.4 |
| VarDict (Germline) (vardict_germline)                           | 1.5.8       | michaelfranklin/vardict:1.5.8 | 