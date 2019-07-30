from janis import CaptureType
from workflows.germline.germlinepipeline import WholeGenomeGermlineWorkflow

ENVIRONMENT = "local"
CAPTURE_TYPE = CaptureType.TARGETED

inputs_map = {
    CaptureType.TARGETED: {
        "local": {
            "fastqs": [[
                "/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/5-brca1/BRCA1_R1.fastq.gz",
                "/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/5-brca1/BRCA1_R2.fastq.gz"
            ]],
            "vardictIntervals": ["/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/5-brca1/BRCA1.intersect.bed"],
            "vardictHeaderLines": "/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/vardictHeader.txt",
            "gatkIntervals": ["/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/5-brca1/BRCA1.bed"],
            "strelkaIntervals": "/Users/franklinmichael/reference/strelkaintervals/hg38.bed.gz",

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
            "vardictIntervals": [
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test5_BRCA1_30X/other_files/BRCA1.intersect.bed"
            ],
            "vardictHeaderLines": "/researchers/jiaan.yu/WGS_pipeline/header_added_to_vardict.txt",
            "gatkIntervals": [
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test5_BRCA1_30X/BRCA1.bed"],

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
            "vardictIntervals": [
                "/Users/franklinmichael/Desktop/workflows-for-testing/wgs/inputs/4-chromosome/chr19.intersect.bed"],
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
            "vardictIntervals": [
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test4_chr19_30X/other_files/chr19.bed"],
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
            "vardictIntervals": [
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test3_WES_30X/WES_30X.bed"],
            "vardictHeaderLines": "/researchers/jiaan.yu/WGS_pipeline/header_added_to_vardict.txt",

            "reference": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/bioinf_core/Proj/hg38_testing/Resources/Gatk_Resource_Bundle_hg38/hg38_contigs_renamed/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        }
    },
    CaptureType.THIRTYX: {
        "local": {},
        "pmac": {
            "fastqs": [[
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test2_WGS_30X/WGS_30X_R1.fastq.gz",
                "/researchers/jiaan.yu/WGS_pipeline/germline/GIAB_NA12878/test_cases/test2_WGS_30X/WGS_30X_R2.fastq.gz"
            ]],
            "strelkaIntervals": "/home/mfranklin/strelkaintervals/hg38.bed.gz",
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
                "gs://peter-mac-cromwell/wgs-inputs/germline/wgs30x/WGS_30X_R1.fastq.gz",
                "gs://peter-mac-cromwell/wgs-inputs/germline/wgs30x/WGS_30X_R2.fastq.gz"
            ]],
            "gatkIntervals": [
                "gs://peter-mac-cromwell/reference/gatk_intervals/1.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/2.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/3.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/4.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/5.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/6.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/7.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/8.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/9.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/10.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/11.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/12.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/13.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/14.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/15.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/16.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/17.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/18.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/19.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/20.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/21.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/22.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/X.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/Y.bed",
                "gs://peter-mac-cromwell/reference/gatk_intervals/M.bed",
            ],
            "vardictIntervals": None,  # fill this one here with all the VarDict intervals
            "vardictHeaderLines": None,  # may need to upload this one

            "reference": "gs://peter-mac-cromwell/reference/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "gs://peter-mac-cromwell/reference/dbsnp_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "gs://peter-mac-cromwell/reference/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "gs://peter-mac-cromwell/reference/known_indels_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "gs://peter-mac-cromwell/reference/mills_indels/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        },
        "spartan": {
            "fastqs": [[
                "/data/cephfs/punim0755/wgs/inputs/2-30x/WGS_30X_R1.fastq.gz",
                "/data/cephfs/punim0755/wgs/inputs/2-30x/WGS_30X_R2.fastq.gz"
            ]],
            "vardictHeaderLines": "/data/cephfs/punim0755/wgs/inputs/vardictHeader.txt",
            "vardictIntervals": [
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
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/1.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/2.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/3.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/4.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/5.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/6.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/7.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/8.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/9.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/10.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/11.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/12.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/13.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/14.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/15.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/16.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/17.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/18.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/19.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/20.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/21.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/22.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/X.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/Y.bed",
                "/data/cephfs/punim0755/wgs/inputs/gatkintervals/M.bed",
            ],
            "reference": "/data/projects/punim0755/hg38/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/data/cephfs/punim0755/hg38/dbsnp_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/data/cephfs/punim0755/hg38/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/data/cephfs/punim0755/hg38/known_indels_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/data/cephfs/punim0755/hg38/mills_indels/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        },
        "wehi": {
            "fastqs": [[
                "/home/franklin.m/wgs/germline/30x/WGS_30X_R1.fastq.gz",
                "/home/franklin.m/wgs/germline/30x/WGS_30X_R2.fastq.gz"
            ]],
            "vardictHeaderLines": "/home/franklin.m/wgs/vardictHeader.txt",
            "vardictIntervals": [
                "/home/franklin.m/vardictintervals/chr1.bed",
                "/home/franklin.m/vardictintervals/chr2.bed",
                "/home/franklin.m/vardictintervals/chr3.bed",
                "/home/franklin.m/vardictintervals/chr4.bed",
                "/home/franklin.m/vardictintervals/chr5.bed",
                "/home/franklin.m/vardictintervals/chr6.bed",
                "/home/franklin.m/vardictintervals/chr7.bed",
                "/home/franklin.m/vardictintervals/chr8.bed",
                "/home/franklin.m/vardictintervals/chr9.bed",
                "/home/franklin.m/vardictintervals/chr10.bed",
                "/home/franklin.m/vardictintervals/chr11.bed",
                "/home/franklin.m/vardictintervals/chr12.bed",
                "/home/franklin.m/vardictintervals/chr13.bed",
                "/home/franklin.m/vardictintervals/chr14.bed",
                "/home/franklin.m/vardictintervals/chr15.bed",
                "/home/franklin.m/vardictintervals/chr16.bed",
                "/home/franklin.m/vardictintervals/chr17.bed",
                "/home/franklin.m/vardictintervals/chr18.bed",
                "/home/franklin.m/vardictintervals/chr19.bed",
                "/home/franklin.m/vardictintervals/chr20.bed",
                "/home/franklin.m/vardictintervals/chr21.bed",
                "/home/franklin.m/vardictintervals/chr22.bed",
                "/home/franklin.m/vardictintervals/chrX.bed",
                "/home/franklin.m/vardictintervals/chrY.bed",
                "/home/franklin.m/vardictintervals/chrM.bed"
            ],

            "gatkIntervals": [
                "/home/franklin.m/gatkintervals/1.bed",
                "/home/franklin.m/gatkintervals/2.bed",
                "/home/franklin.m/gatkintervals/3.bed",
                "/home/franklin.m/gatkintervals/4.bed",
                "/home/franklin.m/gatkintervals/5.bed",
                "/home/franklin.m/gatkintervals/6.bed",
                "/home/franklin.m/gatkintervals/7.bed",
                "/home/franklin.m/gatkintervals/8.bed",
                "/home/franklin.m/gatkintervals/9.bed",
                "/home/franklin.m/gatkintervals/10.bed",
                "/home/franklin.m/gatkintervals/11.bed",
                "/home/franklin.m/gatkintervals/12.bed",
                "/home/franklin.m/gatkintervals/13.bed",
                "/home/franklin.m/gatkintervals/14.bed",
                "/home/franklin.m/gatkintervals/15.bed",
                "/home/franklin.m/gatkintervals/16.bed",
                "/home/franklin.m/gatkintervals/17.bed",
                "/home/franklin.m/gatkintervals/18.bed",
                "/home/franklin.m/gatkintervals/19.bed",
                "/home/franklin.m/gatkintervals/20.bed",
                "/home/franklin.m/gatkintervals/21.bed",
                "/home/franklin.m/gatkintervals/22.bed",
                "/home/franklin.m/gatkintervals/X.bed",
                "/home/franklin.m/gatkintervals/Y.bed",
                "/home/franklin.m/gatkintervals/M.bed",
            ],
            "reference": "/home/franklin.m/reference/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta",
            "snps_dbsnp": "/home/franklin.m/reference/dbsnp_contigs_renamed/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
            "snps_1000gp": "/home/franklin.m/reference/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
            "known_indels": "/home/franklin.m/reference/known_indels_contigs_renamed/Homo_sapiens_assembly38.known_indels.vcf.gz",
            "mills_1000gp_indels": "/home/franklin.m/reference/mills_indels/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
        }
    }
}


if __name__ == "__main__":

    wf = WholeGenomeGermlineWorkflow()
    print(wf.generate_resources_file("cwl", hints={CaptureType.key(): CaptureType.THIRTYX}))

    # wf.report(tabulate_tablefmt="github")

    # hints = {CaptureType.key(): CAPTURE_TYPE}
    #
    # im = inputs_map[CAPTURE_TYPE][ENVIRONMENT]
    #
    # for inp in wf._inputs:
    #     if inp.id() in im:
    #         inp.input.value = im[inp.id()]
    #
    # wf.translate("wdl", to_disk=True, should_validate=True, merge_resources=True, hints=hints,
    #              with_resource_overrides=True, export_path="~/Desktop/{name}/{language}")
    #
    # # jr.fromjanis(wf, env="local", hints=hints, watch=False, validation_reqs=jr.ValidationRequirements(
    # #     truthVCF="/Users/franklinmichael/Desktop/variants/Germline/gold.vcf",
    # #     intervals="/Users/franklinmichael/Desktop/variants/Germline/BRCA1.bed",
    # #     reference="/Users/franklinmichael/reference/hg38/assembly_contigs_renamed/Homo_sapiens_assembly38.fasta",
    # #     fields=[
    # #         "variants_gatk",
    # #         "variants_vardict",
    # #         "variants_strelka",
    # #         "combinedVariants",
    # #     ],
    # ),)
