from janis_core import InputQualityType


REFERENCE_INPUTS = {
    "reference": {
        "doc": """\
    The reference genome from which to align the reads. This requires a number indexes (can be generated \
    with the 'IndexFasta' pipeline This pipeline has been tested using the HG38 reference set.

    This pipeline expects the assembly references to be as they appear in the GCP example. For example:
        - HG38: https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/

    - (".fai", ".amb", ".ann", ".bwt", ".pac", ".sa", "^.dict").""",
        "quality": "static",
        "example": "Homo_sapiens_assembly38.fasta",
        "source": {
            "hg38": "gs://genomics-public-data/references/hg38/v0/Homo_sapiens_assembly38.fasta"
        },
        "skip_sourcing_secondary_files": True,
    },
    "snps_dbsnp": {
        "doc": "From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
        "quality": "static",
        "example": "Homo_sapiens_assembly38.dbsnp138.vcf.gz",
        "source": {
            "hg38": "gs://genomics-public-data/references/hg38/v0/Homo_sapiens_assembly38.dbsnp138.vcf"
        },
    },
    "snps_1000gp": {
        "doc": "From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``. Accessible from the HG38 genomics-public-data google cloud bucket: https://console.cloud.google.com/storage/browser/genomics-public-data/references/hg38/v0/ ",
        "quality": "static",
        "example": "1000G_phase1.snps.high_confidence.hg38.vcf.gz",
        "source": {
            "hg38": "gs://genomics-public-data/references/hg38/v0/1000G_phase1.snps.high_confidence.hg38.vcf.gz"
        },
    },
    "known_indels": {
        "doc": "From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
        "quality": "static",
        "example": "Homo_sapiens_assembly38.known_indels.vcf.gz",
        "source": {
            "hg38": "gs://genomics-public-data/references/hg38/v0/Homo_sapiens_assembly38.known_indels.vcf.gz"
        },
    },
    "mills_indels": {
        "doc": "From the GATK resource bundle, passed to BaseRecalibrator as ``known_sites``",
        "quality": "static",
        "example": "Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        "source": {
            "hg38": "gs://genomics-public-data/references/hg38/v0/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz"
        },
    },
    "gnomad": {
        "doc": "The genome Aggregation Database (gnomAD). This VCF must be compressed and tabix indexed. This is specific for your genome (eg: hg38 / br37) and can usually be found with your reference. For example for HG38, the Broad institute provide the following af-only-gnomad compressed and tabix indexed VCF: https://console.cloud.google.com/storage/browser/gatk-best-practices/somatic-hg38;tab=objects?prefix=af-only",
        "quality": "static",
        "example": "af-only-gnomad.hg38.vcf.gz",
        "source": {
            "hg38": "gs://gatk-best-practices/somatic-hg38/af-only-gnomad.hg38.vcf.gz",
            "b37": "gs://gatk-best-practices/somatic-b37/af-only-gnomad.raw.sites.vcf",
        },
    },
    "panel_of_normals": {
        "doc": "VCF file of sites observed in normal.",
        "quality": "static",
        "example": "Mutect2-WGS-panel-b37.vcf",
        "source": {
            "b37": "gs://gatk-best-practices/somatic-b37/Mutect2-WGS-panel-b37.vcf",
            "b37-exome": "gs://gatk-best-practices/somatic-b37/Mutect2-exome-panel.vcf",
        },
    },
}


INTERVAL_INPUTS = {
    "gatk_intervals": {
        "doc": "List of intervals over which to split the GATK variant calling. If no interval is provided, one interval for each chromosome in the reference will be generated.",
        "quality": "static",
        "example": "BRCA1.bed",
    },
    "vardict_intervals": {
        "doc": "List of intervals over which to split the VarDict variant calling. If no interval is provided, a set of intervals will be generated for each chromosome in the reference.",
        "quality": "static",
        "example": "BRCA1.bed",
    },
    "strelka_intervals": {
        "doc": "An interval for which to restrict the analysis to.",
        "quality": "static",
        "example": "BRCA1.bed.gz",
        "source": {
            "hg38": "https://swift.rc.nectar.org.au/v1/AUTH_4df6e734a509497692be237549bbe9af/janis-test-data/bioinformatics/hg38/hg38.bed.gz"
        },
    },
    "gridss_blacklist": {
        "doc": "BED file containing regions to ignore. For more information, visit: https://github.com/PapenfussLab/gridss#blacklist",
        "quality": "static",
        "source": {
            "hg19": "https://www.encodeproject.org/files/ENCFF001TDO/@@download/ENCFF001TDO.bed.gz",
            "hg38": "https://www.encodeproject.org/files/ENCFF356LFX/@@download/ENCFF356LFX.bed.gz",
        },
    },
}


WGS_INPUTS = {
    **INTERVAL_INPUTS,
    **REFERENCE_INPUTS,
    "cutadapt_adapters": {
        "doc": """\
                Specifies a containment list for cutadapt, which contains a list of sequences to determine valid
                overrepresented sequences from the FastQC report to trim with Cuatadapt. The file must contain sets
                of named adapters in the form: ``name[tab]sequence``. Lines prefixed with a hash will be ignored.""",
        "quality": "static",
        "example": "contaminant_list.txt",
        "source": "https://raw.githubusercontent.com/csf-ngs/fastqc/master/Contaminants/contaminant_list.txt",
    },
}
