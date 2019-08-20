# Janis - Example Pipelines

This repository contains workflows written using [Janis](https://github.com/PMCC-BioinformaticsCore/janis).

**Whole genome sequencing (WGS) pipelines**:

- [Germline](https://github.com/PMCC-BioinformaticsCore/janis-examplepipelines/tree/master/workflows/wgs_germline/)
    - [Germline (GATK only)](https://github.com/PMCC-BioinformaticsCore/janis-examplepipelines/tree/master/workflows/wgs_germline_gatk)
- [Somatic](https://github.com/PMCC-BioinformaticsCore/janis-examplepipelines/tree/master/workflows/wgs_somatic/) 
    - [Somatic (GATK only)](https://github.com/PMCC-BioinformaticsCore/janis-examplepipelines/tree/master/workflows/wgs_somatic_gatk)

**Other**:

- [Alignment](https://github.com/PMCC-BioinformaticsCore/janis-examplepipelines/tree/master/workflows/alignment/)

## Quickstart

To use these pipelines, you will need to have Janis installed:

```bash
pip3 install janis-pipelines
```

Then you can run the pipeline through it's direct (raw) URL, eg:

```bash
WORKFLOW="https://raw.githubusercontent.com/PMCC-BioinformaticsCore/janis-pipelines/master/workflows/alignment/alignment.py"

# Generate inputs file
janis inputs $WORKFLOW > myinps.yml

# Run workflow
janis run $WORKFLOW --inputs myinps.yml
```


## WGS Germline pipeline

> See the - [germline](https://github.com/PMCC-BioinformaticsCore/janis-examplepipelines/tree/master/workflows/wgs_germline/)
folder for more information, the workflow and CWL / WDL translations.

The WGS germline pipeline takes a FASTQ pair, aligns, sorts, marks duplicates and calls variants
across GATK4, Strelka and VarDict. These variants are combined and sorted at the end.

These variants were validated against the [Genome in a Bottle](#) data sets to achieve:

- Recall: 99.25%
- Precision: 92.02%

These results were identical across 3 research institutes (combination of Slurm / PBS / Torque) 
and Google Cloud platform. The pipeline took approximately 27-30 hours to run at a 30x coverage,
depending on the resource constraint.


## WGS Somatic pipeline for tumor-normal variant discovery

> See the [somatic](https://github.com/PMCC-BioinformaticsCore/janis-examplepipelines/tree/master/workflows/wgs_somatic/)
folder for more information, the workflow and CWL / WDL translations.

The WGS somatic pipeline takes normal and tumor FASTQ pairs, aligns, sorts and marks duplicates separately, and
 then performs tumor-normal variant discovery across GATK4, Strelka and VarDict (in somatic modes). These variants are combined and sorted at the end.

This pipeline was run successfully across a similar set of research institutes (as germline) and the cloud,
however these variants have not been validated yet.
