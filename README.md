# Janis - Example Pipelines

This repository contains two whole genome sequencing (WGS) workflows written using [Janis](https://github.com/PMCC-BioinformaticsCore/janis).

- [Germline](https://github.com/PMCC-BioinformaticsCore/janis-examplepipelines/tree/master/workflows/germline/)
- [Somatic](https://github.com/PMCC-BioinformaticsCore/janis-examplepipelines/tree/master/workflows/somatic/) 

To use these pipelines, you will need to have Janis with the bioinformatics tools installed:

```bash
pip3 install janis-pipelines[bioinformatics]
```

## WGS Germline pipeline

> See the [germline](https://github.com/PMCC-BioinformaticsCore/janis-examplepipelines/tree/master/workflows/germline/)
folder for more information, the workflow and CWL / WDL translations.

The WGS germline pipeline takes a FASTQ pair, aligns, sorts, marks duplicates and calls variants
across GATK4, Strelka and VarDict. These variants are combined and sorted at the end.

These variants were validated against the [Genome in a Bottle](#) data sets to achieve:

- Recall: 92.25%
- Precision: 92.02%

These results were identical across 3 research institutes (combination of Slurm / PBS / Torque) 
and Google Cloud platform. The pipeline took approximately 27-30 hours to run at a 30x coverage,
depending on the resource constraint.


## WGS Somatic pipeline for tumor-normal variant discovery

> See the [somatic](https://github.com/PMCC-BioinformaticsCore/janis-examplepipelines/tree/master/workflows/somatic/)
folder for more information, the workflow and CWL / WDL translations.

The WGS somatic pipeline takes normal and tumor FASTQ pairs, aligns, sorts and marks duplicates separately, and
 then performs tumor-normal variant discovery across GATK4, Strelka and VarDict (in somatic modes). These variants are combined and sorted at the end.

This pipeline was run successfully across a similar set of research institutes (as germline) and the cloud,
however these variants have not been validated yet.
