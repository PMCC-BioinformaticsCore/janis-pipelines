from janis import Input, String, Step, Workflow, Array, Output, Float, File
from janis.hints import CaptureType

from janis_bioinformatics.data_types import FastaWithDict, VcfTabix, Fastq, Bed
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_5
from janis_bioinformatics.tools.bcftools import BcfToolsSort_1_9
from janis_bioinformatics.tools.common import AlignSortedBam
from janis_bioinformatics.tools.common.processbam import MergeAndMarkBams_4_0
from janis_bioinformatics.tools.gatk4 import Gatk4GatherVcfs_4_0
from janis_bioinformatics.tools.pmac import CombineVariants_0_0_4
from janis_bioinformatics.tools.variantcallers import GatkGermlineVariantCaller, IlluminaGermlineVariantCaller, \
    VardictGermlineVariantCaller


ENVIRONMENT = "pmac"
CAPTURE_TYPE = CaptureType.THIRTYX

# "truthVCF": "/data/cephfs/punim0755/wgs/inputs/BRCA1.vcf",
inputs_map = {
    CaptureType.TARGETED: {
        "local": {
            "fastqs": [[
                "/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/5-brca1/BRCA1_R1.fastq.gz",
                "/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/5-brca1/BRCA1_R2.fastq.gz"
            ]],
            "vardictIntervals": ["/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/5-brca1/BRCA1.bed"],
            "vardictHeaderLines": "/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/vardictHeader.txt",

            "reference": "/Users/franklinmichael/reference/hg38/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/Users/franklinmichael/reference/hg38/dbsnp_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/Users/franklinmichael/reference/hg38/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/Users/franklinmichael/reference/hg38/known_indels_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/Users/franklinmichael/reference/hg38/mills_indels/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",

        },
        "pmac": {
            "fastqs": [[
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test5_BRCA1_30X/BRCA1_R1.fastq.gz",
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test5_BRCA1_30X/BRCA1_R2.fastq.gz"
            ]],
            "vardictIntervals": ["/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test5_BRCA1_30X/BRCA1.bed"],
            "vardictHeaderLines": "/researchers/jiaan.yu/WGS_pipeline/header_added_to_vardict.txt",

            "reference": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        },
        "spartan": {
            "fastqs": [[
                "/data/cephfs/punim0755/wgs/inputs/BRCA1_R1.fastq.gz",
                "/data/cephfs/punim0755/wgs/inputs/BRCA1_R2.fastq.gz"
            ]],
            "vardictIntervals": ["/data/cephfs/punim0755/wgs/inputs/BRCA1.bed"],
            "vardictHeaderLines": 0,

            "reference": "/data/projects/punim0755/hg38/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/data/cephfs/punim0755/hg38/dbsnp_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/data/cephfs/punim0755/hg38/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/data/cephfs/punim0755/hg38/known_indels_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/data/cephfs/punim0755/hg38/mills_indels/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        },
        "gcp": {
            "fastqs": [[
                "gs://pmccromwelltests/wgs-inputs/BRCA1_R1.fastq.gz",
                "gs://pmccromwelltests/wgs-inputs/BRCA1_R2.fastq.gz"
            ]],
            "vardictIntervals": ["gs://pmccromwelltests/wgs-inputs/BRCA1.bed"],
            "vardictHeaderLines": 0,

            "reference": "gs://pmccromwelltests/reference/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "gs://pmccromwelltests/reference/dbsnp_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "gs://pmccromwelltests/reference/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "gs://pmccromwelltests/reference/known_indels_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "gs://pmccromwelltests/reference/mills_indels/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",

        },
        "empty": {
            "fastqs": [[
                None,
                None
            ]],
            "bedIntervals": None,
            "readGroupHeaderLine": "'@RG\\tID:NA12878\\tSM:NA12878\\tLB:NA12878\\tPL:ILLUMINA'",

            "reference": None,
            "snps_dbsnp": None,
            "snps_1000gp": None,
            "known_indels": None,
            "mills_1000gp_indels": None,
        },
    },
    CaptureType.CHROMOSOME: {
        "local": {
            "fastqs": [[
                "/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/4-chromosome/chr19_R1.fastq.gz",
                "/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/4-chromosome/chr19_R2.fastq.gz"
            ]],
            "vardictIntervals": ["/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/4-chromosome/chr19.intersect.bed"],
            "vardictHeaderLines": "/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/vardictHeader.txt",

            "reference": "/Users/franklinmichael/reference/hg38/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/Users/franklinmichael/reference/hg38/dbsnp_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/Users/franklinmichael/reference/hg38/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/Users/franklinmichael/reference/hg38/known_indels_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/Users/franklinmichael/reference/hg38/mills_indels/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        },
        "pmac": {
            "fastqs": [[
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test4_chr19_30X/chr19_R1.fastq.gz",
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test4_chr19_30X/chr19_R2.fastq.gz"
            ]],
            "vardictIntervals": ["/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test4_chr19_30X/other_files/chr19.bed"],
            "vardictHeaderLines": "/researchers/jiaan.yu/WGS_pipeline/header_added_to_vardict.txt",

            "reference": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        },
        "spartan": {
            "fastqs": [[
                "/data/cephfs/punim0755/wgs/inputs/4-chromosome/chr19_R1.fastq.gz",
                "/data/cephfs/punim0755/wgs/inputs/4-chromosome/chr19_R2.fastq.gz"
            ]],
            "vardictIntervals": ["/data/cephfs/punim0755/wgs/inputs/4-chromosome/chr19.bed"],
            "vardictHeaderLines": 0,

            "reference": "/data/projects/punim0755/hg38/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/data/cephfs/punim0755/hg38/dbsnp_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/data/cephfs/punim0755/hg38/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/data/cephfs/punim0755/hg38/known_indels_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/data/cephfs/punim0755/hg38/mills_indels/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        },
        "gcp": {
            "fastqs": [[
                "gs://peter-mac-cromwell/wgs-inputs/chr19/chr19_R1.fastq.gz",
                "gs://peter-mac-cromwell/wgs-inputs/chr19/chr19_R2.fastq.gz"
            ]],
            "vardictIntervals": ["gs://peter-mac-cromwell/wgs-inputs/chr19/chr19.bed"],

            "reference": "gs://peter-mac-cromwell/reference/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "gs://peter-mac-cromwell/reference/dbsnp_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "gs://peter-mac-cromwell/reference/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "gs://peter-mac-cromwell/reference/known_indels_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "gs://peter-mac-cromwell/reference/mills_indels/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",

        }
    },
    CaptureType.EXOME: {
        "pmac": {
            "fastqs": [[
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test3_WES_30X/WES_30X_R1.fastq.gz",
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test3_WES_30X/WES_30X_R2.fastq.gz"
            ]],
            "vardictIntervals": ["/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test3_WES_30X/WES_30X.bed"],
            "vardictHeaderLines": "/researchers/jiaan.yu/WGS_pipeline/header_added_to_vardict.txt",

            "reference": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        }
    },
    CaptureType.THIRTYX: {
        "pmac": {
            "fastqs": [[
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test2_WGS_30X/WGS_30X_R1.fastq.gz",
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test2_WGS_30X/WGS_30X_R2.fastq.gz"
            ]],
            "vardictIntervals": [
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr1.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr2.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr3.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr4.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr5.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr6.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr7.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr8.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr9.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr10.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr11.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr12.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr13.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr14.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr15.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr16.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr17.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr18.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr19.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr20.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr21.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chr22.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chrX.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chrY.bed",
                "/researchers/jiaan.yu/WGS_pipeline/vardict_beds/chrM.bed"
            ],
            "gatkIntervals": [
                "/home/mfranklin/hg38_beds/1.bed",
                "/home/mfranklin/hg38_beds/2.bed",
                "/home/mfranklin/hg38_beds/3.bed",
                "/home/mfranklin/hg38_beds/4.bed",
                "/home/mfranklin/hg38_beds/5.bed",
                "/home/mfranklin/hg38_beds/6.bed",
                "/home/mfranklin/hg38_beds/7.bed",
                "/home/mfranklin/hg38_beds/8.bed",
                "/home/mfranklin/hg38_beds/9.bed",
                "/home/mfranklin/hg38_beds/10.bed",
                "/home/mfranklin/hg38_beds/11.bed",
                "/home/mfranklin/hg38_beds/12.bed",
                "/home/mfranklin/hg38_beds/13.bed",
                "/home/mfranklin/hg38_beds/14.bed",
                "/home/mfranklin/hg38_beds/15.bed",
                "/home/mfranklin/hg38_beds/16.bed",
                "/home/mfranklin/hg38_beds/17.bed",
                "/home/mfranklin/hg38_beds/18.bed",
                "/home/mfranklin/hg38_beds/19.bed",
                "/home/mfranklin/hg38_beds/20.bed",
                "/home/mfranklin/hg38_beds/21.bed",
                "/home/mfranklin/hg38_beds/22.bed",
                "/home/mfranklin/hg38_beds/X.bed",
                "/home/mfranklin/hg38_beds/Y.bed",
                "/home/mfranklin/hg38_beds/M.bed",
            ],
            
            "vardictHeaderLines": "/researchers/jiaan.yu/WGS_pipeline/header_added_to_vardict.txt",

            "reference": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        },
        "gcp": {
            "fastqs": [[
              "gs://peter-mac-cromwell/wgs-inputs/wgs30x/WGS_30X_R1.fastq.gz",
              "gs://peter-mac-cromwell/wgs-inputs/wgs30x/WGS_30X_R2.fastq.gz"
            ]],
            "gatkIntervals": [
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/1.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/2.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/3.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/4.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/5.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/6.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/7.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/8.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/9.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/10.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/11.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/12.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/13.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/14.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/15.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/16.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/17.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/18.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/19.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/20.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/21.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/22.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/X.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/Y.bed",
                "gs://peter-mac-cromwell/wgs-inputs/wgs30x/gatk_intervals/M.bed",
            ],
            "vardictIntervals": None,       # fill this one here with all the VarDict intervals
            "vardictHeaderLines": None,     # may need to upload this one

            "reference":            "gs://peter-mac-cromwell/reference/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp":           "gs://peter-mac-cromwell/reference/dbsnp_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp":          "gs://peter-mac-cromwell/reference/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels":         "gs://peter-mac-cromwell/reference/known_indels_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels":  "gs://peter-mac-cromwell/reference/mills_indels/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        },
        "spartan": {
            "fastqs": [[
                "/data/cephfs/punim0755/wgs/inputs/2-30x/WGS_30X_R1.fastq.gz",
                "/data/cephfs/punim0755/wgs/inputs/2-30x/WGS_30X_R2.fastq.gz"
            ]],
            "vardictIntervals": "/data/cephfs/punim0755/wgs/inputs/vardictHeader.txt",
            "vardictHeaderLines": [
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr1.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr2.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr3.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr4.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr5.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr6.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr7.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr8.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr9.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr10.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr11.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr12.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr13.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr14.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr15.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr16.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr17.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr18.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr19.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr20.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr21.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chr22.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chrX.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chrY.bed",
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chrM.bed"
            ],

            "gatkIntervals": [
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/1.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/2.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/3.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/4.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/5.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/6.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/7.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/8.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/9.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/10.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/11.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/12.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/13.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/14.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/15.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/16.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/17.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/18.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/19.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/20.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/21.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/22.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/X.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/Y.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatk_intervals/M.bed",
            ],
            "reference": "/data/projects/punim0755/hg38/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/data/cephfs/punim0755/hg38/dbsnp_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/data/cephfs/punim0755/hg38/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/data/cephfs/punim0755/hg38/known_indels_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/data/cephfs/punim0755/hg38/mills_indels/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        }
    }
}


class WholeGenomeGermlineWorkflow(Workflow):

    @staticmethod
    def version():
        return "1.0.0"

    def __init__(self):
        Workflow.__init__(self, "WgGermline")

        fastqInputs = Input("fastqs", Array(Fastq()))
        reference = Input("reference", FastaWithDict())

        # readgroupheaderline = Input("readGroupHeaderLine", String(), "'@RG\\tID:NA12878\\tSM:NA12878\\tLB:NA12878\\tPL:ILLUMINA'")

        gatk_intervals = Input("gatkIntervals", Array(Bed(optional=True)), default=[None],
                               include_in_inputs_file_if_none=False)

        vardict_intervals = Input("vardictIntervals", Array(Bed()))    # change to array after gathervcfs testing
        header_lines = Input("vardictHeaderLines", File())

        sample_name = Input("sampleName", String(), "NA12878")
        allele_freq_threshold = Input("allelFreqThreshold", Float(), 0.05)

        snps_dbsnp = Input("snps_dbsnp", VcfTabix())
        snps_1000gp = Input("snps_1000gp", VcfTabix())
        known_indels = Input("known_indels", VcfTabix())
        mills_indels = Input("mills_1000gp_indels", VcfTabix())

        s1_sw = Step("alignSortedBam", AlignSortedBam())
        fastqc = Step("fastqc", FastQC_0_11_5())
        s2_process = Step("processBamFiles", MergeAndMarkBams_4_0())

        vc_gatk = Step("variantCaller_GATK", GatkGermlineVariantCaller())
        vc_strelka = Step("variantCaller_Strelka", IlluminaGermlineVariantCaller())
        vc_vardict = Step("variantCaller_Vardict", VardictGermlineVariantCaller())

        vc_merge_gatk = Step("variantCaller_merge_GATK", Gatk4GatherVcfs_4_0())
        vc_merge_vardict = Step("variantCaller_merge_Vardict", Gatk4GatherVcfs_4_0())

        combine_vcs = Step("combineVariants", CombineVariants_0_0_4())
        sort_combined_vcfs = Step("sortCombined", BcfToolsSort_1_9())

        # step1
        self.add_edge(fastqInputs, s1_sw.fastq)
        self.add_edges([
            (reference, s1_sw.reference),
            (sample_name, s1_sw.sampleName),
        ])

        # step1 sidestep
        self.add_edge(fastqInputs, fastqc.reads)

        # step2 - process bam files
        self.add_edges([
            (s1_sw.out, s2_process.bams)
        ])

        # VARIANT CALLERS

        # GATK VariantCaller + Merge
        self.add_edges([
            (s2_process.out, vc_gatk.bam),
            (gatk_intervals, vc_gatk.intervals),
            (reference, vc_gatk.reference),
            (snps_dbsnp, vc_gatk.snps_dbsnp),
            (snps_1000gp, vc_gatk.snps_1000gp),
            (known_indels, vc_gatk.knownIndels),
            (mills_indels, vc_gatk.millsIndels),

            (vc_gatk.out, vc_merge_gatk.vcfs)
        ])

        # Strelka VariantCaller
        self.add_edges([
            (s2_process.out, vc_strelka.bam),
            (reference, vc_strelka.reference)
        ])

        # Vardict VariantCaller
        self.add_edges([
            (vardict_intervals, vc_vardict.intervals),
            (s2_process.out, vc_vardict.bam),
            (reference, vc_vardict.reference),
            (sample_name, vc_vardict),
            (allele_freq_threshold, vc_vardict.allelFreqThreshold),
            (header_lines, vc_vardict.headerLines),

            (vc_vardict.out, vc_merge_vardict.vcfs)
        ])

        # Output the Variants
        self.add_edges([
            (vc_gatk.out, Output("variants_gatk_split")),
            (vc_vardict.out, Output("variants_vardict_split")),

            (vc_strelka.out, Output("variants_strelka")),
            (vc_merge_gatk.out, Output("variants_gatk")),
            (vc_merge_vardict.out, Output("variants_vardict"))
        ])

        # Combine
        self.add_edges([
            (Input("variant_type", String(), default="germline", include_in_inputs_file_if_none=False), combine_vcs.type),
            (Input("columns", Array(String()), default=["AC", "AN", "AF", "AD", "DP", "GT"], include_in_inputs_file_if_none=False), combine_vcs.columns),

            (vc_merge_gatk.out, combine_vcs.vcfs),
            (vc_strelka.out, combine_vcs.vcfs),
            (vc_merge_vardict.out, combine_vcs.vcfs),
        ])
        self.add_edge(combine_vcs.vcf, sort_combined_vcfs.vcf)

        # Outputs

        self.add_edges([
            (s2_process.out, Output("bam")),
            (fastqc.out, Output("reports")),
            (sort_combined_vcfs.out, Output("combinedVariants"))
        ])


if __name__ == "__main__":

    wf = WholeGenomeGermlineWorkflow()

    hints = { CaptureType.key(): CAPTURE_TYPE }

    im = inputs_map[CAPTURE_TYPE][ENVIRONMENT]
    for inp in wf._inputs:
        if inp.id() in im:
            inp.input.value = im[inp.id()]

    # wf.translate("wdl", with_resource_overrides=True, merge_resources=True)
    # wf.generate_resources_file("wdl", hints=hints)
    wf.generate_resources_table(hints, to_console=False, to_disk=True)

    # env = shepherd.Environment.get_predefined_environment_by_id("local")
    # shepherd.TaskManager.from_janis(wf, env, shepherd.ValidationRequirements(
    #     truthVCF="/Users/franklinmichael/Desktop/variants/gold.vcf",
    #     intervals="/Users/franklinmichael/Desktop/variants/BRCA1.bed",
    #     reference="/Users/franklinmichael/reference/hg38/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta",
    #     fields=["variants_gatk", "variants_strelka", "variants_vardict", "combinedVariants"]
    # ))
