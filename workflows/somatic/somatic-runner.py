from janis import CaptureType
from .somaticpipeline import WholeGenomeSomaticWorkflow

ENVIRONMENT = "spartan"
CAPTURE_TYPE = CaptureType.THIRTYX

inputs_map = {
    CaptureType.THIRTYX: {
        "spartan": {
            "normalBam": "/data/cephfs/punim0755/cromwell-executions/WgSomatic/be8f0bb7-90c6-4e7a-a092-2895c226f704/"
            "call-normal/somatic_subpipeline/61cf831e-2768-4950-b43c-9a2e0f995fef/call-mergeAndMark/"
            "processbamfiles/aa2e30ef-5529-45e5-acbf-672809964cfb/call-markDuplicates/execution/"
            "generated-2b023da6-a469-11e9-af5b-acde48001122.bam",
            "tumorInputs": [
                "/data/cephfs/punim0755/cromwell-executions/WgSomatic/be8f0bb7-90c6-4e7a-a092-2895c226f704/"
                "call-tumor/somatic_subpipeline/4c371607-563e-46b9-ab84-9e284ff11ae5/call-alignAndSort/"
                "shard-0/alignsortedbam/56c8c977-ac04-49a3-b4dd-db3371565bd7/call-sortsam/execution/"
                "generated-2b01f512-a469-11e9-af5b-acde48001122.bam"
            ],
            "strelkaIntervals": "/data/cephfs/punim0755/wgs/inputs/strelkaintervals/hg38.bed.gz",
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
                "/data/cephfs/punim0755/wgs/inputs/vardictintervals/chrM.bed",
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
        }
    }
}


if __name__ == "__main__":
    w = WholeGenomeSomaticWorkflow()

    im = inputs_map[CAPTURE_TYPE][ENVIRONMENT]
    for inp in w._inputs:
        if inp.id() in im:
            inp.input.value = im[inp.id()]

    hints = {CaptureType.key(): CAPTURE_TYPE}
    #
    w.translate(
        "wdl",
        to_console=True,
        to_disk=True,
        should_validate=True,
        write_inputs_file=True,
    )
    w.generate_resources_table({CaptureType.key(): CAPTURE_TYPE}, to_disk=True)
    # w.generate_resources_file("wdl", hints)
    #
    if (
        str(
            input(f"Run at {ENVIRONMENT} (CaptureType: {CAPTURE_TYPE}) (Y/n)? ")
        ).lower()
        == "y"
    ):
        import shepherd

        tid = shepherd.fromjanis(
            w, env="spartan", hints=hints, watch=False
        )  # , inputs="wg-somatic-gcp-disk.json")
        print(tid)
