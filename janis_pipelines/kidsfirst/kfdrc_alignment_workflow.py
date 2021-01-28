from datetime import datetime
from typing import List, Optional, Dict, Any

from janis_core import *
from janis_bioinformatics.data_types.cram import CramCrai
from janis_bioinformatics.data_types.fasta import FastaFai
from janis_bioinformatics.data_types.vcf import VcfTabix, VcfIdx
from janis_core.types.common_data_types import (
    String,
    File,
    Array,
    Int,
    Boolean,
    GenericFileWithSecondaries,
    Float,
)

Gatk_Indexfeaturefile_V0_1_0 = CommandToolBuilder(
    tool="gatk_indexfeaturefile",
    base_command=[],
    inputs=[
        ToolInput(
            tag="input_file",
            input_type=File(),
            position=2,
            prefix="-I",
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_index",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=VcfIdx(),
            selector=WildcardSelector(
                wildcard=BasenameOperator(
                    InputSelector(input_to_select="input_file", type_hint=File())
                )
            ),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.1.7.0R",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="<expr>inputs.input_index ? 'echo /gatk' : '/gatk'</expr>",
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="IndexFeatureFile ",
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
    ],
    doc="Creates an index for a feature file, e.g. VCF or BED file.",
)
Picard_Intervallisttools_V0_1_0 = CommandToolBuilder(
    tool="picard_intervallisttools",
    base_command=["java", "-Xmx2000m", "-jar", "/picard.jar"],
    inputs=[
        ToolInput(
            tag="interval_list", input_type=File(), doc=InputDocumentation(doc=None),
        )
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=Array(t=File()),
            selector=WildcardSelector(wildcard="temp*/*.interval_list"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/picard:2.18.2-dev",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "IntervalListTools SCATTER_COUNT=50 SUBDIVISION_MODE=BALANCING_WITHOUT_INTERVAL_SUBDIVISION_WITH_OVERFLOW UNIQUE=true SORT=true BREAK_BANDS_AT_MULTIPLES_OF=1000000 INPUT={JANIS_CWL_TOKEN_1} OUTPUT={JANIS_CWL_TOKEN_2}",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="interval_list", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2="<expr>runtime.outdir</expr>",
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    doc="This tool scatters a single interval list into many interval list files.\nThe following programs are run in this tool:\n  - picard IntervalListTools",
)
Verifybamid_Contamination_V0_1_0 = CommandToolBuilder(
    tool="verifybamid_contamination",
    base_command=["/bin/VerifyBamID"],
    inputs=[
        ToolInput(
            tag="contamination_sites_bed",
            input_type=File(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="contamination_sites_mu",
            input_type=File(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="contamination_sites_ud",
            input_type=File(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="ref_fasta", input_type=FastaFai(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="contamination",
            output_type=Float(),
            selector=WildcardSelector(wildcard="*.selfSM"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="outp",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.selfSM"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/verifybamid:1.0.2",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "--Verbose --NumPC 4 --Output {JANIS_CWL_TOKEN_4} --BamFile {JANIS_CWL_TOKEN_2} --Reference {JANIS_CWL_TOKEN_1} --UDPath {JANIS_CWL_TOKEN_6} --MeanPath {JANIS_CWL_TOKEN_3} --BedPath {JANIS_CWL_TOKEN_5} 1>/dev/null",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="ref_fasta", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="input_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="contamination_sites_mu", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="contamination_sites_bed", type_hint=File()
                ),
                JANIS_CWL_TOKEN_6=InputSelector(
                    input_to_select="contamination_sites_ud", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=4,
    memory=5000,
    doc="This tool verifies whether the reads in particular file match previously known genotypes for an individual\nand checks whether the reads are contaminated as a mixture of two samples.\nThe following programs are run in this tool:\n  - VerifyBamID",
)
Gatk_Haplotypecaller_V0_1_0 = CommandToolBuilder(
    tool="gatk_haplotypecaller",
    base_command=["/gatk-launch", "--javaOptions", "-Xms2000m"],
    inputs=[
        ToolInput(
            tag="contamination", input_type=Float(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="interval_list", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference",
            input_type=GenericFileWithSecondaries(secondaries=["^.dict", ".fai"]),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="*.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.beta.1-3.5",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "PrintReads -I {JANIS_CWL_TOKEN_3} --interval_padding 500 -L {JANIS_CWL_TOKEN_2} -O local.sharded.bam && java -XX:GCTimeLimit=50 -XX:GCHeapFreeLimit=10 -Xms8000m -jar /GenomeAnalysisTK.jar -T HaplotypeCaller -R {JANIS_CWL_TOKEN_5} -o {JANIS_CWL_TOKEN_1}.vcf.gz -I local.sharded.bam -L {JANIS_CWL_TOKEN_2} -ERC GVCF --max_alternate_alleles 3 -variant_index_parameter 128000 -variant_index_type LINEAR -contamination {JANIS_CWL_TOKEN_4} --read_filter OverclippedRead",
                JANIS_CWL_TOKEN_1="<expr>inputs.input_bam.nameroot</expr>",
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="interval_list", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="input_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="contamination", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=10000,
    doc="This tool calls germline SNPs and indels via local re-assembly of haplotypes.\nThe following programs are run in this tool:\n  - GATK PrintReads\n  - GATK HaplotypeCaller",
)
Picard_Mergevcfs_V0_1_0 = CommandToolBuilder(
    tool="picard_mergevcfs",
    base_command=["java", "-Xms2000m", "-jar", "/picard.jar", "MergeVcfs"],
    inputs=[
        ToolInput(
            tag="input_vcf",
            input_type=Array(t=VcfTabix()),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_vcf_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="*.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/picard:2.18.2-dev",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "OUTPUT={JANIS_CWL_TOKEN_1}.g.vcf.gz",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="output_vcf_basename", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=3000,
    doc="This tool merges many VCFs into a single VCF.\nThe following programs are run in this tool:\n  - picard MergeVcfs",
)
Gatk_Collectgvcfcallingmetrics_V0_1_0 = CommandToolBuilder(
    tool="gatk_collectgvcfcallingmetrics",
    base_command=[
        "java",
        "-Xms2000m",
        "-jar",
        "/picard.jar",
        "CollectVariantCallingMetrics",
    ],
    inputs=[
        ToolInput(
            tag="dbsnp_vcf", input_type=VcfIdx(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="final_gvcf_base_name",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_vcf", input_type=VcfTabix(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference_dict", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="wgs_evaluation_interval_list",
            input_type=File(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=Array(t=File()),
            selector=WildcardSelector(wildcard="*_metrics"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/picard:2.18.2-dev",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "INPUT={JANIS_CWL_TOKEN_1} OUTPUT={JANIS_CWL_TOKEN_2} DBSNP={JANIS_CWL_TOKEN_3} SEQUENCE_DICTIONARY={JANIS_CWL_TOKEN_5} TARGET_INTERVALS={JANIS_CWL_TOKEN_4} GVCF_INPUT=true THREAD_COUNT=16",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="input_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="final_gvcf_base_name", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="dbsnp_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="wgs_evaluation_interval_list", type_hint=File(),
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="reference_dict", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=16,
    memory=3000,
    doc="This tool collects summary and per-sample metrics about variant calls in a VCF file.\nThe following programs are run in this tool:\n  - picard CollectVariantCallingMetrics",
)
Fastq_Chomp_V0_1_0 = CommandToolBuilder(
    tool="fastq_chomp",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(
            tag="input_fastq", input_type=File(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="max_size",
            input_type=Int(),
            default=10000000000,
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=Array(t=File()),
            selector=WildcardSelector(wildcard="*.fq"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/bwa-bundle:dev",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "set -eo pipefail\n\nif [ {JANIS_CWL_TOKEN_1} -gt {JANIS_CWL_TOKEN_3} ]; then\n  zcat {JANIS_CWL_TOKEN_2} | split -dl 320000000 - reads-\n  ls reads-* | xargs -i mv {} {}.fq\nelse\n  echo 'FASTQ not large enough to split.'\nfi",
                JANIS_CWL_TOKEN_1=FileSizeOperator(
                    InputSelector(input_to_select="input_fastq", type_hint=File())
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="input_fastq", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="max_size", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=4,
    memory=8000,
    doc="This tool will chomp any fastq larger than the max size (10 gb by default) into 320000000 line chunks (80M reads). \nPrograms used in this tool:\n  - zcat | split\n  - ls | mv",
)
Bwa_Mem_Naive_V0_1_0 = CommandToolBuilder(
    tool="bwa_mem_naive",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(
            tag="interleaved",
            input_type=Boolean(),
            default=False,
            doc=InputDocumentation(doc=None, quality=InputQualityType.configuration),
        ),
        ToolInput(
            tag="mates",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="min_alignment_score",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="reads", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="ref",
            input_type=GenericFileWithSecondaries(
                secondaries=[
                    ".64.amb",
                    ".64.ann",
                    ".64.bwt",
                    ".64.pac",
                    ".64.sa",
                    "^.dict",
                    ".fai",
                ]
            ),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="rg",
            input_type=String(),
            position=1,
            shell_quote=True,
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.bam"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/bwa-kf-bundle:0.1.17",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "set -eo pipefail\nbwa mem -K 100000000 ${if (inputs.interleaved) {return '-p';} else {return ''}} -v 3 -t 36 ${if (inputs.min_alignment_score == null) { return '';} else {return '-T ' + inputs.min_alignment_score;}} -Y {JANIS_CWL_TOKEN_1} -R",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="ref", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="${return inputs.reads.path} ${if (inputs.mates != null) {return inputs.mates.path} else {return ''}} | /opt/samblaster/samblaster -i /dev/stdin -o /dev/stdout | /opt/sambamba_0.6.3/sambamba_v0.6.3 view -t 36 -f bam -l 0 -S /dev/stdin | /opt/sambamba_0.6.3/sambamba_v0.6.3 sort -t 36 --natural-sort -m 15GiB --tmpdir ./ -o ${if (inputs.reads != null) {return inputs.reads.nameroot} else {return ''}}.unsorted.bam -l 5 /dev/stdin",
            position=2,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
    ],
    cpus=36,
    memory=50000,
    doc="The program can handle the following classes of inputs:\n - single end reads (only reads File and rg string provided)\n - reads with mates (reads File, mates File, and rg string provided)\n - interleaved reads (reads File provided, rg string provided, and interleaved set to true)\nThis tool runs the following programs:\n - bwa mem | samblaster | sambamba view | sambamba sort",
)
Kfdrc_Process_Se_Set = WorkflowBuilder(identifier="kfdrc_process_se_set",)

Kfdrc_Process_Se_Set.input(
    "indexed_reference_fasta",
    GenericFileWithSecondaries(
        secondaries=[
            ".64.amb",
            ".64.ann",
            ".64.bwt",
            ".64.pac",
            ".64.sa",
            ".64.alt",
            "^.dict",
        ]
    ),
)

Kfdrc_Process_Se_Set.input(
    "input_se_reads", File(),
)

Kfdrc_Process_Se_Set.input(
    "input_se_rgs", String(),
)

Kfdrc_Process_Se_Set.input(
    "min_alignment_score", Int(optional=True),
)


Kfdrc_Process_Se_Set.step(
    "zcat_split_reads",
    Fastq_Chomp_V0_1_0(input_fastq=Kfdrc_Process_Se_Set.input_se_reads,),
)


Kfdrc_Process_Se_Set.step(
    "bwa_mem_split_se_reads",
    Bwa_Mem_Naive_V0_1_0(
        min_alignment_score=Kfdrc_Process_Se_Set.min_alignment_score,
        reads=Kfdrc_Process_Se_Set.zcat_split_reads.outp,
        ref=Kfdrc_Process_Se_Set.indexed_reference_fasta,
        rg=Kfdrc_Process_Se_Set.input_se_rgs,
    ),
)

Kfdrc_Process_Se_Set.output(
    "unsorted_bams",
    source=Kfdrc_Process_Se_Set.bwa_mem_split_se_reads.outp,
    output_name=True,
)

Kfdrc_Process_Pe_Set = WorkflowBuilder(identifier="kfdrc_process_pe_set",)

Kfdrc_Process_Pe_Set.input(
    "indexed_reference_fasta",
    GenericFileWithSecondaries(
        secondaries=[
            ".64.amb",
            ".64.ann",
            ".64.bwt",
            ".64.pac",
            ".64.sa",
            ".64.alt",
            "^.dict",
        ]
    ),
)

Kfdrc_Process_Pe_Set.input(
    "input_pe_mates", File(),
)

Kfdrc_Process_Pe_Set.input(
    "input_pe_reads", File(),
)

Kfdrc_Process_Pe_Set.input(
    "input_pe_rgs", String(),
)

Kfdrc_Process_Pe_Set.input(
    "min_alignment_score", Int(optional=True),
)


Kfdrc_Process_Pe_Set.step(
    "zcat_split_mates",
    Fastq_Chomp_V0_1_0(input_fastq=Kfdrc_Process_Pe_Set.input_pe_mates,),
)


Kfdrc_Process_Pe_Set.step(
    "zcat_split_reads",
    Fastq_Chomp_V0_1_0(input_fastq=Kfdrc_Process_Pe_Set.input_pe_reads,),
)


Kfdrc_Process_Pe_Set.step(
    "bwa_mem_split_pe_reads",
    Bwa_Mem_Naive_V0_1_0(
        mates=Kfdrc_Process_Pe_Set.zcat_split_mates.outp,
        min_alignment_score=Kfdrc_Process_Pe_Set.min_alignment_score,
        reads=Kfdrc_Process_Pe_Set.zcat_split_reads.outp,
        ref=Kfdrc_Process_Pe_Set.indexed_reference_fasta,
        rg=Kfdrc_Process_Pe_Set.input_pe_rgs,
    ),
)

Kfdrc_Process_Pe_Set.output(
    "unsorted_bams",
    source=Kfdrc_Process_Pe_Set.bwa_mem_split_pe_reads.outp,
    output_name=True,
)

Bamtofastq_Chomp_V0_1_0 = CommandToolBuilder(
    tool="bamtofastq_chomp",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(tag="input_bam", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="max_size",
            input_type=Int(),
            default=20000000000,
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=Array(t=File()),
            selector=WildcardSelector(wildcard="*.fq"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="rg_string",
            output_type=File(),
            selector=WildcardSelector(wildcard="rg.txt"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/bwa-bundle:dev",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "set -eo pipefail\n\nsamtools view -H {JANIS_CWL_TOKEN_1} | grep ^@RG > rg.txt\n\nif [ {JANIS_CWL_TOKEN_2} -gt {JANIS_CWL_TOKEN_3} ]; then\n  bamtofastq tryoq=1 filename={JANIS_CWL_TOKEN_1} | split -dl 680000000 - reads-\n  ls reads-* | xargs -i mv {} {}.fq\nelse\n  bamtofastq tryoq=1 filename={JANIS_CWL_TOKEN_1} > reads-00.fq\nfi",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="input_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=FileSizeOperator(
                    InputSelector(input_to_select="input_bam", type_hint=File())
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="max_size", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=1000,
    doc="If the input BAM is not provided the program will simply exit without failing.\nThis tool runs two programs:\n  - samtools view && biobambam2 bamtofastq\nThe program will first grab the RG header from the input BAM and put it in a file.\nThis RG header in the text file is later parsed into a string.\nNext it will convert the bam to fastq. If the file is over the max_size, it will\nchunk the output FASTQ into 680 million line FASTQs (85 million read pairs).",
)
Expression_Preparerg_V0_1_0 = CommandToolBuilder(
    tool="expression_preparerg",
    base_command=["nodejs", "expression.js"],
    inputs=[
        ToolInput(
            tag="rg", input_type=File(optional=True), doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="sample", input_type=String(), doc=InputDocumentation(doc=None)),
    ],
    outputs=[
        ToolOutput(
            tag="rg_str",
            output_type=String(),
            selector="JANIS (potentially unimplemented): j.ReadJsonOperator(j.Stdout)[out_id]",
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="ubuntu:latest",
    version="v0.1.0",
    arguments=[],
    files_to_create={
        "expression.js": "'use strict';\nvar inputs=$(inputs);\nvar runtime=$(runtime);\nvar ret = function(){ if (inputs.rg == null) {return {rg_str: null}}; var arr = inputs.rg.contents.split('\n')[0].split('\t'); for (var i=1; i<arr.length; i++){ if (arr[i].startsWith('SM')){ arr[i] = 'SM:' + inputs.sample; } } return {rg_str: arr.join('\\t')}; }();\nprocess.stdout.write(JSON.stringify(ret));"
    },
)
Samtools_Split_V0_1_0 = CommandToolBuilder(
    tool="samtools_split",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(tag="input_bam", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(tag="reference", input_type=File(), doc=InputDocumentation(doc=None)),
    ],
    outputs=[
        ToolOutput(
            tag="bam_files",
            output_type=Array(t=File()),
            selector=WildcardSelector(wildcard="*.bam"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/samtools:1.9",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "set -eo pipefail\nRG_NUM=`samtools view -H {JANIS_CWL_TOKEN_1} | grep -c ^@RG`\nif [ $RG_NUM != 1 ]; then\n  samtools split -f '%!.bam' -@ 36 --reference {JANIS_CWL_TOKEN_2} {JANIS_CWL_TOKEN_1}\nfi",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="input_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    doc="This tool splits the input bam input read group bams if it has more than one readgroup.\nPrograms run in this tool:\n  - samtools view | grep\n  - samtools split\nUsing samtools view and grep count the header lines starting with @RG. If that number is\nnot one, split the bam file into read group bams using samtools.",
)
Kfdrc_Rgbam_To_Realnbam = WorkflowBuilder(identifier="kfdrc_rgbam_to_realnbam",)

Kfdrc_Rgbam_To_Realnbam.input(
    "indexed_reference_fasta",
    GenericFileWithSecondaries(
        secondaries=[
            ".64.amb",
            ".64.ann",
            ".64.bwt",
            ".64.pac",
            ".64.sa",
            ".64.alt",
            "^.dict",
        ]
    ),
)

Kfdrc_Rgbam_To_Realnbam.input(
    "input_rgbam", File(),
)

Kfdrc_Rgbam_To_Realnbam.input(
    "min_alignment_score", Int(optional=True),
)

Kfdrc_Rgbam_To_Realnbam.input(
    "sample_name", String(),
)

Kfdrc_Rgbam_To_Realnbam.input(
    "bwa_mem_naive_bam_interleaved", Boolean(optional=True), default=True,
)


Kfdrc_Rgbam_To_Realnbam.step(
    "bamtofastq_chomp",
    Bamtofastq_Chomp_V0_1_0(input_bam=Kfdrc_Rgbam_To_Realnbam.input_rgbam,),
)


Kfdrc_Rgbam_To_Realnbam.step(
    "expression_updatergsample",
    Expression_Preparerg_V0_1_0(
        rg=Kfdrc_Rgbam_To_Realnbam.bamtofastq_chomp.rg_string,
        sample=Kfdrc_Rgbam_To_Realnbam.sample_name,
    ),
)


Kfdrc_Rgbam_To_Realnbam.step(
    "bwa_mem_naive_bam",
    Bwa_Mem_Naive_V0_1_0(
        interleaved=Kfdrc_Rgbam_To_Realnbam.bwa_mem_naive_bam_interleaved,
        min_alignment_score=Kfdrc_Rgbam_To_Realnbam.min_alignment_score,
        reads=Kfdrc_Rgbam_To_Realnbam.bamtofastq_chomp.outp,
        ref=Kfdrc_Rgbam_To_Realnbam.indexed_reference_fasta,
        rg=Kfdrc_Rgbam_To_Realnbam.expression_updatergsample.rg_str,
    ),
)

Kfdrc_Rgbam_To_Realnbam.output(
    "unsorted_bams",
    source=Kfdrc_Rgbam_To_Realnbam.bwa_mem_naive_bam.outp,
    output_name=True,
)

Kfdrc_Process_Bam = WorkflowBuilder(identifier="kfdrc_process_bam",)

Kfdrc_Process_Bam.input(
    "indexed_reference_fasta",
    GenericFileWithSecondaries(
        secondaries=[
            ".64.amb",
            ".64.ann",
            ".64.bwt",
            ".64.pac",
            ".64.sa",
            ".64.alt",
            "^.dict",
        ]
    ),
)

Kfdrc_Process_Bam.input(
    "input_bam", File(),
)

Kfdrc_Process_Bam.input(
    "min_alignment_score", Int(optional=True),
)

Kfdrc_Process_Bam.input(
    "sample_name", String(),
)


Kfdrc_Process_Bam.step(
    "samtools_split",
    Samtools_Split_V0_1_0(
        input_bam=Kfdrc_Process_Bam.input_bam,
        reference=Kfdrc_Process_Bam.indexed_reference_fasta,
    ),
)


Kfdrc_Process_Bam.step(
    "realign_split_bam",
    Kfdrc_Rgbam_To_Realnbam(
        indexed_reference_fasta=Kfdrc_Process_Bam.indexed_reference_fasta,
        input_rgbam=Kfdrc_Process_Bam.samtools_split.bam_files,
        min_alignment_score=Kfdrc_Process_Bam.min_alignment_score,
        sample_name=Kfdrc_Process_Bam.sample_name,
    ),
)

Kfdrc_Process_Bam.output(
    "unsorted_bams",
    source=Kfdrc_Process_Bam.realign_split_bam.unsorted_bams,
    output_name=True,
)

Gatekeeper_V0_1_0 = CommandToolBuilder(
    tool="gatekeeper",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(
            tag="run_agg_metrics",
            input_type=Boolean(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="run_bam_processing",
            input_type=Boolean(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="run_gvcf_processing",
            input_type=Boolean(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="run_hs_metrics",
            input_type=Boolean(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="run_pe_reads_processing",
            input_type=Boolean(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="run_se_reads_processing",
            input_type=Boolean(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="run_wgs_metrics",
            input_type=Boolean(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="scatter_agg_metrics",
            output_type=Array(t=Int()),
            selector="${ if (inputs.run_agg_metrics) {return [1]} else {return []} }",
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="scatter_bams",
            output_type=Array(t=Int()),
            selector="${ if (inputs.run_bam_processing) {return [1]} else {return []} }",
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="scatter_gvcf",
            output_type=Array(t=Int()),
            selector="${ if (inputs.run_gvcf_processing) {return [1]} else {return []} }",
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="scatter_hs_metrics",
            output_type=Array(t=Int()),
            selector="${ if (inputs.run_hs_metrics) {return [1]} else {return []} }",
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="scatter_pe_reads",
            output_type=Array(t=Int()),
            selector="${ if (inputs.run_pe_reads_processing) {return [1]} else {return []} }",
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="scatter_se_reads",
            output_type=Array(t=Int()),
            selector="${ if (inputs.run_se_reads_processing) {return [1]} else {return []} }",
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="scatter_wgs_metrics",
            output_type=Array(t=Int()),
            selector="${ if (inputs.run_wgs_metrics) {return [1]} else {return []} }",
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/ubuntu:18.04",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="set -eo pipefail\n${\n  if (inputs.run_bam_processing || inputs.run_pe_reads_processing ||  inputs.run_se_reads_processing) {\n    return 'echo Files Provided...Processing >&2 && exit 0'\n  } else {\n    return 'echo No BAMs or FASTQs provided, mission accomplished >&2 && exit 1'\n  }\n}",
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
)
Tabix_Index_V0_1_0 = CommandToolBuilder(
    tool="tabix_index",
    base_command=[],
    inputs=[
        ToolInput(
            tag="input_file",
            input_type=File(),
            position=1,
            shell_quote=False,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_index",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=VcfTabix(),
            selector=WildcardSelector(
                wildcard=BasenameOperator(
                    InputSelector(input_to_select="input_file", type_hint=File())
                )
            ),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/samtools:1.9",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="<expr>inputs.input_index ? 'echo tabix -p vcf' : 'tabix -p vcf'</expr>",
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    doc="This tool will run tabix conditionally dependent on whether an index is provided. The tool will output the input_file with the index, provided or created within, as a secondary file.",
)
Untar_Indexed_Reference_V0_1_0 = CommandToolBuilder(
    tool="untar_indexed_reference",
    base_command=["tar", "xf"],
    inputs=[
        ToolInput(
            tag="reference_tar",
            input_type=File(),
            position=1,
            doc=InputDocumentation(doc=None),
        )
    ],
    outputs=[
        ToolOutput(
            tag="alt",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.64.alt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="amb",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.64.amb"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="ann",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.64.ann"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="bwt",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.64.bwt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="dict",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.dict"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="fai",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.fai"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="fasta",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.fasta"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="pac",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.64.pac"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="sa",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.64.sa"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="ubuntu:latest",
    version="v0.1.0",
    arguments=[],
)
Bundle_Secondaryfiles_V0_1_0 = CommandToolBuilder(
    tool="bundle_secondaryfiles",
    base_command=["echo"],
    inputs=[
        ToolInput(
            tag="primary_file", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="secondary_files",
            input_type=Array(t=File()),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=GenericFileWithSecondaries(
                secondaries=["$(inputs.secondary_files)"]
            ),
            selector=WildcardSelector(
                wildcard=BasenameOperator(
                    InputSelector(input_to_select="primary_file", type_hint=File())
                )
            ),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="ubuntu:latest",
    version="v0.1.0",
    arguments=[],
    doc="This tool takes a primary file and list of secondary files as input and passes the primary_file as\nthe output with the secondary_files as secondaryFiles.",
)
Kfdrc_Process_Bamlist = WorkflowBuilder(identifier="kfdrc_process_bamlist",)

Kfdrc_Process_Bamlist.input(
    "conditional_run", Int(),
)

Kfdrc_Process_Bamlist.input(
    "indexed_reference_fasta",
    GenericFileWithSecondaries(
        secondaries=[
            ".64.amb",
            ".64.ann",
            ".64.bwt",
            ".64.pac",
            ".64.sa",
            "^.dict",
            ".fai",
        ]
    ),
)

Kfdrc_Process_Bamlist.input(
    "input_bam_list", Array(t=File()),
)

Kfdrc_Process_Bamlist.input(
    "min_alignment_score", Int(optional=True),
)

Kfdrc_Process_Bamlist.input(
    "sample_name", String(),
)


Kfdrc_Process_Bamlist.step(
    "process_bams",
    Kfdrc_Process_Bam(
        indexed_reference_fasta=Kfdrc_Process_Bamlist.indexed_reference_fasta,
        input_bam=Kfdrc_Process_Bamlist.input_bam_list,
        min_alignment_score=Kfdrc_Process_Bamlist.min_alignment_score,
        sample_name=Kfdrc_Process_Bamlist.sample_name,
    ),
)

Kfdrc_Process_Bamlist.output(
    "unsorted_bams",
    source=Kfdrc_Process_Bamlist.process_bams.unsorted_bams,
    output_name=True,
)

Kfdrc_Process_Pe_Readslist2 = WorkflowBuilder(identifier="kfdrc_process_pe_readslist2",)

Kfdrc_Process_Pe_Readslist2.input(
    "conditional_run", Int(),
)

Kfdrc_Process_Pe_Readslist2.input(
    "indexed_reference_fasta",
    GenericFileWithSecondaries(
        secondaries=[
            ".64.amb",
            ".64.ann",
            ".64.bwt",
            ".64.pac",
            ".64.sa",
            "^.dict",
            ".fai",
        ]
    ),
)

Kfdrc_Process_Pe_Readslist2.input(
    "input_pe_mates_list", Array(t=File()),
)

Kfdrc_Process_Pe_Readslist2.input(
    "input_pe_reads_list", Array(t=File()),
)

Kfdrc_Process_Pe_Readslist2.input(
    "input_pe_rgs_list", Array(t=String()),
)

Kfdrc_Process_Pe_Readslist2.input(
    "min_alignment_score", Int(optional=True),
)


Kfdrc_Process_Pe_Readslist2.step(
    "process_pe_set",
    Kfdrc_Process_Pe_Set(
        indexed_reference_fasta=Kfdrc_Process_Pe_Readslist2.indexed_reference_fasta,
        input_pe_mates=Kfdrc_Process_Pe_Readslist2.input_pe_mates_list,
        input_pe_reads=Kfdrc_Process_Pe_Readslist2.input_pe_reads_list,
        input_pe_rgs=Kfdrc_Process_Pe_Readslist2.input_pe_rgs_list,
        min_alignment_score=Kfdrc_Process_Pe_Readslist2.min_alignment_score,
    ),
)

Kfdrc_Process_Pe_Readslist2.output(
    "unsorted_bams",
    source=Kfdrc_Process_Pe_Readslist2.process_pe_set.unsorted_bams,
    output_name=True,
)

Kfdrc_Process_Se_Readslist2 = WorkflowBuilder(identifier="kfdrc_process_se_readslist2",)

Kfdrc_Process_Se_Readslist2.input(
    "conditional_run", Int(),
)

Kfdrc_Process_Se_Readslist2.input(
    "indexed_reference_fasta",
    GenericFileWithSecondaries(
        secondaries=[
            ".64.amb",
            ".64.ann",
            ".64.bwt",
            ".64.pac",
            ".64.sa",
            "^.dict",
            ".fai",
        ]
    ),
)

Kfdrc_Process_Se_Readslist2.input(
    "input_se_reads_list", Array(t=File()),
)

Kfdrc_Process_Se_Readslist2.input(
    "input_se_rgs_list", Array(t=String()),
)

Kfdrc_Process_Se_Readslist2.input(
    "min_alignment_score", Int(optional=True),
)


Kfdrc_Process_Se_Readslist2.step(
    "process_se_set",
    Kfdrc_Process_Se_Set(
        indexed_reference_fasta=Kfdrc_Process_Se_Readslist2.indexed_reference_fasta,
        input_se_reads=Kfdrc_Process_Se_Readslist2.input_se_reads_list,
        input_se_rgs=Kfdrc_Process_Se_Readslist2.input_se_rgs_list,
        min_alignment_score=Kfdrc_Process_Se_Readslist2.min_alignment_score,
    ),
)

Kfdrc_Process_Se_Readslist2.output(
    "unsorted_bams",
    source=Kfdrc_Process_Se_Readslist2.process_se_set.unsorted_bams,
    output_name=True,
)

Python_Createsequencegroups_V0_1_0 = CommandToolBuilder(
    tool="python_createsequencegroups",
    base_command=["python", "-c"],
    inputs=[
        ToolInput(tag="ref_dict", input_type=File(), doc=InputDocumentation(doc=None))
    ],
    outputs=[
        ToolOutput(
            tag="sequence_intervals",
            output_type=Array(t=File()),
            selector=WildcardSelector(wildcard="sequence_grouping_*.intervals"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="sequence_intervals_with_unmapped",
            output_type=Array(t=File()),
            selector=WildcardSelector(wildcard="*.intervals"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/python:2.7.13",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "def main():\n    with open('{JANIS_CWL_TOKEN_1}', 'r') as ref_dict_file:\n        sequence_tuple_list = []\n        longest_sequence = 0\n        for line in ref_dict_file:\n            if line.startswith('@SQ'):\n                line_split = line.split(chr(9))\n                sequence_tuple_list.append((line_split[1].split('SN:')[1], int(line_split[2].split('LN:')[1])))\n        longest_sequence = sorted(sequence_tuple_list, key=lambda x: x[1], reverse=True)[0][1]\n    hg38_protection_tag = ':1+'\n    tsv_string = sequence_tuple_list[0][0] + hg38_protection_tag\n    temp_size = sequence_tuple_list[0][1]\n    i = 0\n    for sequence_tuple in sequence_tuple_list[1:]:\n        if temp_size + sequence_tuple[1] <= longest_sequence:\n            temp_size += sequence_tuple[1]\n            tsv_string += chr(10) + sequence_tuple[0] + hg38_protection_tag\n        else:\n            i += 1\n            pad = '{:0>2d}'.format(i)\n            tsv_file_name = 'sequence_grouping_' + pad + '.intervals'\n            with open(tsv_file_name, 'w') as tsv_file:\n                tsv_file.write(tsv_string)\n                tsv_file.close()\n            tsv_string = sequence_tuple[0] + hg38_protection_tag\n            temp_size = sequence_tuple[1]\n    i += 1\n    pad = '{:0>2d}'.format(i)\n    tsv_file_name = 'sequence_grouping_' + pad + '.intervals'\n    with open(tsv_file_name, 'w') as tsv_file:\n        tsv_file.write(tsv_string)\n        tsv_file.close()\n\n    with open('unmapped.intervals', 'w') as tsv_file:\n        tsv_file.write('unmapped')\n        tsv_file.close()\n\nif __name__ == '__main__':\n    main()",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="ref_dict", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=True,
        )
    ],
    doc="Splits the reference dict file in a list of interval files. \nIntervals are determined by the longest SQ length in the dict.",
)
Sambamba_Merge_Anylist_V0_1_0 = CommandToolBuilder(
    tool="sambamba_merge_anylist",
    base_command=[],
    inputs=[
        ToolInput(
            tag="bams", input_type=Array(t=String()), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="base_file_name", input_type=String(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="merged_bam",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.bam"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="images.sbgenomics.com/bogdang/sambamba:0.6.3",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="${\n  var flatin = flatten(inputs.bams);\n  var arr = [];\n  for (var i=0; i<flatin.length; i++) {\n    arr = arr.concat(flatin[i].path);\n  }\n  if (arr.length > 1) {\n    return '/opt/sambamba_0.6.3/sambamba_v0.6.3 merge -t 36 ' + inputs.base_file_name + '.aligned.duplicates_marked.unsorted.bam ' + arr.join(' ');\n  } else {\n    return 'cp ' + arr.join(' ') + ' ' + inputs.base_file_name + '.aligned.duplicates_marked.unsorted.bam';\n  }\n}",
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=36,
    memory=2024,
    doc="Takes any list, flattens that list, then merges the items of the list.\nThis tool runs the following programs:\n  - sambamba merge && rm",
)
Sambamba_Sort_V0_1_0 = CommandToolBuilder(
    tool="sambamba_sort",
    base_command=[],
    inputs=[
        ToolInput(tag="bam", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="base_file_name", input_type=String(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="suffix",
            input_type=String(),
            default="aligned.duplicates_marked.sorted",
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="sorted_bam",
            output_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            selector=WildcardSelector(wildcard="*.bam"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="images.sbgenomics.com/bogdang/sambamba:0.6.3",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "/opt/sambamba_0.6.3/sambamba_v0.6.3 sort -t 36 -m 10G -o {JANIS_CWL_TOKEN_2}.{JANIS_CWL_TOKEN_1}.bam {JANIS_CWL_TOKEN_3}\nmv {JANIS_CWL_TOKEN_2}.{JANIS_CWL_TOKEN_1}.bam.bai {JANIS_CWL_TOKEN_2}.{JANIS_CWL_TOKEN_1}.bai",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="suffix", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="base_file_name", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="bam", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=36,
    memory=15000,
    doc="This tool sorts the input bam.\nPrograms used by this tool:\n  - sambamba sort\n  - mv",
)
Gatkv4_Baserecalibrator_V0_1_0 = CommandToolBuilder(
    tool="gatkv4_baserecalibrator",
    base_command=["/gatk", "BaseRecalibrator"],
    inputs=[
        ToolInput(
            tag="input_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="knownsites",
            input_type=Array(t=VcfTabix()),
            position=1,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference",
            input_type=GenericFileWithSecondaries(secondaries=["^.dict", ".fai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="sequence_interval",
            input_type=File(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.recal_data.csv"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.0.3.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "--java-options '-Xms4000m -XX:GCTimeLimit=50 -XX:GCHeapFreeLimit=10 -XX:+PrintFlagsFinal -XX:+PrintGCTimeStamps -XX:+PrintGCDateStamps -XX:+PrintGCDetails -Xloggc:gc_log.log' -R {JANIS_CWL_TOKEN_2} -I {JANIS_CWL_TOKEN_1} --use-original-qualities -O {JANIS_CWL_TOKEN_4}.recal_data.csv -L {JANIS_CWL_TOKEN_3}",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="input_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="sequence_interval", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4="<expr>inputs.input_bam.nameroot</expr>",
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=8000,
    doc="Perform baserecalibration on a BAM.\nPrograms run in this tool:\n  - GATK BaseRecalibrator",
)
Gatk_Gatherbqsrreports_V0_1_0 = CommandToolBuilder(
    tool="gatk_gatherbqsrreports",
    base_command=["/gatk", "GatherBQSRReports"],
    inputs=[
        ToolInput(
            tag="input_brsq_reports",
            input_type=Array(t=File()),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.csv"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.0.3.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "--java-options '-Xms3000m' -O {JANIS_CWL_TOKEN_1}.GatherBqsrReports.recal_data.csv",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=8000,
    doc="This tool gathers the BQSR reports.\nThe following programs are run in this tool:\n  - GATK GatherBQSRReports",
)
Gatk4_Applybqsr_V0_1_0 = CommandToolBuilder(
    tool="gatk4_applybqsr",
    base_command=["/gatk", "ApplyBQSR"],
    inputs=[
        ToolInput(
            tag="bqsr_report", input_type=File(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="input_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference",
            input_type=GenericFileWithSecondaries(secondaries=["^.dict", ".fai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="sequence_interval",
            input_type=File(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="recalibrated_bam",
            output_type=GenericFileWithSecondaries(secondaries=["^.bai", ".md5"]),
            selector=WildcardSelector(wildcard="*bam"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.0.3.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "--java-options '-Xms3000m -XX:+PrintFlagsFinal -XX:+PrintGCTimeStamps -XX:+PrintGCDateStamps -XX:+PrintGCDetails -Xloggc:gc_log.log -XX:GCTimeLimit=50 -XX:GCHeapFreeLimit=10' --create-output-bam-md5 --add-output-sam-program-record -R {JANIS_CWL_TOKEN_5} -I {JANIS_CWL_TOKEN_3} --use-original-qualities -O {JANIS_CWL_TOKEN_1}.aligned.duplicates_marked.recalibrated.bam -bqsr {JANIS_CWL_TOKEN_2} --static-quantized-quals 10 --static-quantized-quals 20 --static-quantized-quals 30 -L {JANIS_CWL_TOKEN_4}",
                JANIS_CWL_TOKEN_1="<expr>inputs.input_bam.nameroot</expr>",
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="bqsr_report", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="input_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="sequence_interval", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=4500,
    doc="This tool applies BQSR to the input bam.\nThe following programs are run in this tool:\n  - GATK ApplyBQSR",
)
Picard_Gatherbamfiles_V0_1_0 = CommandToolBuilder(
    tool="picard_gatherbamfiles",
    base_command=[],
    inputs=[
        ToolInput(
            tag="input_bam",
            input_type=Array(t=GenericFileWithSecondaries(secondaries=["^.bai"])),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_bam_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=GenericFileWithSecondaries(secondaries=["^.bai", ".md5"]),
            selector=WildcardSelector(wildcard="*.bam"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/picard:2.18.2-dev",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "rm_bams='${\n  var arr = [];\n  for (var i=0; i<inputs.input_bam.length; i++)\n      arr = arr.concat(inputs.input_bam[i].path)\n  return (arr.join(' '))\n}'\ninput_bams='${\n  var arr = [];\n  for (var i=0; i<inputs.input_bam.length; i++)\n      arr = arr.concat(inputs.input_bam[i].path)\n  return (arr.join(' INPUT='))\n}'\njava -Xms2000m -jar /picard.jar GatherBamFiles OUTPUT={JANIS_CWL_TOKEN_1}.bam INPUT=$input_bams CREATE_INDEX=true CREATE_MD5_FILE=true",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="output_bam_basename", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=8000,
    doc="This program gathers the input bam files into a single bam.\nThe following programs are run in this program:\n  - picard GatherBamFiles\n  - rm",
)
Picard_Qualityscoredistribution_Conditional_V0_1_0 = CommandToolBuilder(
    tool="picard_qualityscoredistribution_conditional",
    base_command=[
        "java",
        "-Xms5000m",
        "-jar",
        "/picard.jar",
        "QualityScoreDistribution",
    ],
    inputs=[
        ToolInput(
            tag="conditional_run", input_type=Int(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference", input_type=FastaFai(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="chart",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.qual_score_dist.pdf"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="metrics",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.qual_score_dist.txt"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/picard-r:latest-dev",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "INPUT={JANIS_CWL_TOKEN_1} REFERENCE_SEQUENCE={JANIS_CWL_TOKEN_2} OUTPUT={JANIS_CWL_TOKEN_3}.qual_score_dist.txt CHART_OUTPUT={JANIS_CWL_TOKEN_3}.qual_score_dist.pdf",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="input_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3="<expr>inputs.input_bam.nameroot</expr>",
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=12000,
    doc="This tool plots the quality score distribution found in an input WGS/WXS bam.\nThe following programs are run in this tool:\n  - picard QualityScoreDistribution\nThis tool is also made to be used conditionally with the conditional_run parameter.\nSimply pass an empty array to conditional_run and scatter on the input to skip.",
)
Samtools_Bam_To_Cram_V0_1_0 = CommandToolBuilder(
    tool="samtools_bam_to_cram",
    base_command=["samtools", "view"],
    inputs=[
        ToolInput(
            tag="input_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference", input_type=FastaFai(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=CramCrai(),
            selector=WildcardSelector(wildcard="*.cram"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/samtools:1.8-dev",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "-C -T {JANIS_CWL_TOKEN_2} -o {JANIS_CWL_TOKEN_1}.cram {JANIS_CWL_TOKEN_3} && samtools index {JANIS_CWL_TOKEN_1}.cram",
                JANIS_CWL_TOKEN_1="<expr>inputs.input_bam.nameroot</expr>",
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="input_bam", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=4000,
    doc="This tool converts the input BAM into a CRAM.\nThe following programs are run in this tool:\n  - samtools view\n  - samtools index",
)
Kfdrc_Bam_To_Gvcf = WorkflowBuilder(identifier="kfdrc_bam_to_gvcf",)

Kfdrc_Bam_To_Gvcf.input(
    "conditional_run", Int(),
)

Kfdrc_Bam_To_Gvcf.input(
    "contamination_sites_bed", File(),
)

Kfdrc_Bam_To_Gvcf.input(
    "contamination_sites_mu", File(),
)

Kfdrc_Bam_To_Gvcf.input(
    "contamination_sites_ud", File(),
)

Kfdrc_Bam_To_Gvcf.input(
    "dbsnp_idx", File(optional=True),
)

Kfdrc_Bam_To_Gvcf.input(
    "dbsnp_vcf", File(),
)

Kfdrc_Bam_To_Gvcf.input(
    "indexed_reference_fasta", File(),
)

Kfdrc_Bam_To_Gvcf.input(
    "input_bam", File(),
)

Kfdrc_Bam_To_Gvcf.input(
    "output_basename", String(),
)

Kfdrc_Bam_To_Gvcf.input(
    "reference_dict", File(),
)

Kfdrc_Bam_To_Gvcf.input(
    "wgs_calling_interval_list", File(),
)

Kfdrc_Bam_To_Gvcf.input(
    "wgs_evaluation_interval_list", File(),
)


Kfdrc_Bam_To_Gvcf.step(
    "index_dbsnp",
    Gatk_Indexfeaturefile_V0_1_0(
        input_file=Kfdrc_Bam_To_Gvcf.dbsnp_vcf, input_index=Kfdrc_Bam_To_Gvcf.dbsnp_idx,
    ),
)


Kfdrc_Bam_To_Gvcf.step(
    "picard_intervallisttools",
    Picard_Intervallisttools_V0_1_0(
        interval_list=Kfdrc_Bam_To_Gvcf.wgs_calling_interval_list,
    ),
)


Kfdrc_Bam_To_Gvcf.step(
    "verifybamid",
    Verifybamid_Contamination_V0_1_0(
        contamination_sites_bed=Kfdrc_Bam_To_Gvcf.contamination_sites_bed,
        contamination_sites_mu=Kfdrc_Bam_To_Gvcf.contamination_sites_mu,
        contamination_sites_ud=Kfdrc_Bam_To_Gvcf.contamination_sites_ud,
        input_bam=Kfdrc_Bam_To_Gvcf.input_bam,
        output_basename=Kfdrc_Bam_To_Gvcf.output_basename,
        ref_fasta=Kfdrc_Bam_To_Gvcf.indexed_reference_fasta,
    ),
)


Kfdrc_Bam_To_Gvcf.step(
    "gatk_haplotypecaller",
    Gatk_Haplotypecaller_V0_1_0(
        contamination=Kfdrc_Bam_To_Gvcf.verifybamid.contamination,
        input_bam=Kfdrc_Bam_To_Gvcf.input_bam,
        interval_list=Kfdrc_Bam_To_Gvcf.picard_intervallisttools.outp,
        reference=Kfdrc_Bam_To_Gvcf.indexed_reference_fasta,
    ),
)


Kfdrc_Bam_To_Gvcf.step(
    "picard_mergevcfs",
    Picard_Mergevcfs_V0_1_0(
        input_vcf=Kfdrc_Bam_To_Gvcf.gatk_haplotypecaller.outp,
        output_vcf_basename=Kfdrc_Bam_To_Gvcf.output_basename,
    ),
)


Kfdrc_Bam_To_Gvcf.step(
    "picard_collectgvcfcallingmetrics",
    Gatk_Collectgvcfcallingmetrics_V0_1_0(
        dbsnp_vcf=Kfdrc_Bam_To_Gvcf.index_dbsnp.outp,
        final_gvcf_base_name=Kfdrc_Bam_To_Gvcf.output_basename,
        input_vcf=Kfdrc_Bam_To_Gvcf.picard_mergevcfs.outp,
        reference_dict=Kfdrc_Bam_To_Gvcf.reference_dict,
        wgs_evaluation_interval_list=Kfdrc_Bam_To_Gvcf.wgs_evaluation_interval_list,
    ),
)

Kfdrc_Bam_To_Gvcf.output(
    "gvcf", source=Kfdrc_Bam_To_Gvcf.picard_mergevcfs.outp, output_name=True,
)

Kfdrc_Bam_To_Gvcf.output(
    "gvcf_calling_metrics",
    source=Kfdrc_Bam_To_Gvcf.picard_collectgvcfcallingmetrics.outp,
    output_name=True,
)

Kfdrc_Bam_To_Gvcf.output(
    "verifybamid_output", source=Kfdrc_Bam_To_Gvcf.verifybamid.outp, output_name=True,
)

Picard_Collectalignmentsummarymetrics_Conditional_V0_1_0 = CommandToolBuilder(
    tool="picard_collectalignmentsummarymetrics_conditional",
    base_command=[
        "java",
        "-Xms5000m",
        "-jar",
        "/picard.jar",
        "CollectAlignmentSummaryMetrics",
    ],
    inputs=[
        ToolInput(
            tag="conditional_run", input_type=Int(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference", input_type=FastaFai(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.alignmentsummary_metrics"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/picard-r:latest-dev",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "INPUT={JANIS_CWL_TOKEN_1} REFERENCE_SEQUENCE={JANIS_CWL_TOKEN_2} OUTPUT={JANIS_CWL_TOKEN_3}.alignmentsummary_metrics METRIC_ACCUMULATION_LEVEL='null' METRIC_ACCUMULATION_LEVEL='SAMPLE' METRIC_ACCUMULATION_LEVEL='LIBRARY'",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="input_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3="<expr>inputs.input_bam.nameroot</expr>",
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=12000,
    doc="This tool collects alignment summary metrics on an input WGS/WXS bam.\nThe following programs are run in this tool:\n  - picard CollectAlignmentSummaryMetrics \nThis tool is also made to be used conditionally with the conditional_run parameter.\nSimply pass an empty array to conditional_run and scatter on the input to skip.",
)
Picard_Collectgcbiasmetrics_V0_1_0 = CommandToolBuilder(
    tool="picard_collectgcbiasmetrics",
    base_command=["java", "-Xms5000m", "-jar", "/picard.jar", "CollectGcBiasMetrics",],
    inputs=[
        ToolInput(
            tag="conditional_run", input_type=Int(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference", input_type=FastaFai(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="chart",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.gc_bias_metrics.pdf"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="detail",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.gc_bias_metrics.txt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="summary",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.summary_metrics.txt"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/picard-r:latest-dev",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "INPUT={JANIS_CWL_TOKEN_1} REFERENCE_SEQUENCE={JANIS_CWL_TOKEN_2} OUTPUT={JANIS_CWL_TOKEN_3}.gc_bias_metrics.txt SUMMARY_OUTPUT={JANIS_CWL_TOKEN_3}.summary_metrics.txt CHART_OUTPUT={JANIS_CWL_TOKEN_3}.gc_bias_metrics.pdf METRIC_ACCUMULATION_LEVEL='null' METRIC_ACCUMULATION_LEVEL='SAMPLE' METRIC_ACCUMULATION_LEVEL='LIBRARY'",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="input_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3="<expr>inputs.input_bam.nameroot</expr>",
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=12000,
    doc="This tool collects gc bias metrics on an input WGS/WXS bam.\nThe following programs are run in this tool:\n  - picard CollectGcBiasMetrics\nThis tool is also made to be used conditionally with the conditional_run parameter.\nSimply pass an empty array to conditional_run and scatter on the input to skip.",
)
Picard_Collecthsmetrics_Conditional_V0_1_0 = CommandToolBuilder(
    tool="picard_collecthsmetrics_conditional",
    base_command=["java", "-Xms2000m", "-jar", "/picard.jar", "CollectHsMetrics"],
    inputs=[
        ToolInput(
            tag="bait_intervals", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="conditional_run", input_type=Int(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference", input_type=FastaFai(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="target_intervals", input_type=File(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.hs_metrics"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/picard:2.18.2-dev",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "INPUT={JANIS_CWL_TOKEN_2} REFERENCE_SEQUENCE={JANIS_CWL_TOKEN_4} BAIT_INTERVALS={JANIS_CWL_TOKEN_3} TARGET_INTERVALS={JANIS_CWL_TOKEN_5} OUTPUT={JANIS_CWL_TOKEN_1}.hs_metrics",
                JANIS_CWL_TOKEN_1="<expr>inputs.input_bam.nameroot</expr>",
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="input_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="bait_intervals", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="target_intervals", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=8000,
    doc="This tool collects hs metrics on an input WXS bam.\nThe following programs are run in this tool:\n  - picard CollectHsMetrics\nThis tool is also made to be used conditionally with the conditional_run parameter.\nSimply pass an empty array to conditional_run and scatter on the input to skip.",
)
Picard_Collectinsertsizemetrics_Conditional_V0_1_0 = CommandToolBuilder(
    tool="picard_collectinsertsizemetrics_conditional",
    base_command=[
        "java",
        "-Xms5000m",
        "-jar",
        "/picard.jar",
        "CollectInsertSizeMetrics",
    ],
    inputs=[
        ToolInput(
            tag="conditional_run", input_type=Int(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference", input_type=FastaFai(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="metrics",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.insert_size_metrics"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="plot",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.insert_size_Histogram.pdf"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/picard-r:latest-dev",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "INPUT={JANIS_CWL_TOKEN_1} REFERENCE_SEQUENCE={JANIS_CWL_TOKEN_2} OUTPUT={JANIS_CWL_TOKEN_3}.insert_size_metrics HISTOGRAM_FILE={JANIS_CWL_TOKEN_3}.insert_size_Histogram.pdf METRIC_ACCUMULATION_LEVEL='null' METRIC_ACCUMULATION_LEVEL='SAMPLE' METRIC_ACCUMULATION_LEVEL='LIBRARY'",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="input_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3="<expr>inputs.input_bam.nameroot</expr>",
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=12000,
    doc="This tool collects insert size metrics on an input WGS/WXS bam.\nThe following programs are run in this tool:\n  - picard CollectInsertSizeMetrics\nThis tool is also made to be used conditionally with the conditional_run parameter.\nSimply pass an empty array to conditional_run and scatter on the input to skip.",
)
Picard_Collectsequencingartifactmetrics_Conditional_V0_1_0 = CommandToolBuilder(
    tool="picard_collectsequencingartifactmetrics_conditional",
    base_command=[
        "java",
        "-Xms5000m",
        "-jar",
        "/picard.jar",
        "CollectSequencingArtifactMetrics",
    ],
    inputs=[
        ToolInput(
            tag="conditional_run", input_type=Int(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference", input_type=FastaFai(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="bait_bias_detail_metrics",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.bait_bias_detail_metrics"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="bait_bias_summary_metrics",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.bait_bias_summary_metrics"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="error_summary_metrics",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.error_summary_metrics"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="pre_adapter_detail_metrics",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.pre_adapter_detail_metrics"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="pre_adapter_summary_metrics",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.pre_adapter_summary_metrics"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/picard-r:latest-dev",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "INPUT={JANIS_CWL_TOKEN_1} REFERENCE_SEQUENCE={JANIS_CWL_TOKEN_2} OUTPUT={JANIS_CWL_TOKEN_3}.artifact_metrics",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="input_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3="<expr>inputs.input_bam.nameroot</expr>",
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=12000,
    doc="This tool collects sequencing artifact metrics on an input WGS/WXS bam.\nThe following programs are run in this tool:\n  - picard CollectSequencingArtifactMetrics\nThis tool is also made to be used conditionally with the conditional_run parameter.\nSimply pass an empty array to conditional_run and scatter on the input to skip.",
)
Picard_Collectwgsmetrics_Conditional_V0_1_0 = CommandToolBuilder(
    tool="picard_collectwgsmetrics_conditional",
    base_command=[
        "java",
        "-Xms2000m",
        "-Xmx6000m",
        "-XX:GCTimeLimit=50",
        "-XX:GCHeapFreeLimit=10",
        "-jar",
        "/picard.jar",
        "CollectWgsMetrics",
    ],
    inputs=[
        ToolInput(
            tag="conditional_run", input_type=Int(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="intervals", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="reference", input_type=FastaFai(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=File(),
            selector=WildcardSelector(
                wildcard=StringFormatter(
                    "{JANIS_CWL_TOKEN_1}.wgs_metrics",
                    JANIS_CWL_TOKEN_1="<expr>inputs.input_bam.nameroot</expr>",
                )
            ),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/picard:2.18.2-dev",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "INPUT={JANIS_CWL_TOKEN_2} VALIDATION_STRINGENCY=SILENT REFERENCE_SEQUENCE={JANIS_CWL_TOKEN_3} INCLUDE_BQ_HISTOGRAM=true INTERVALS={JANIS_CWL_TOKEN_1} OUTPUT={JANIS_CWL_TOKEN_4}.wgs_metrics USE_FAST_ALGORITHM=true READ_LENGTH=250",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="intervals", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="input_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4="<expr>inputs.input_bam.nameroot</expr>",
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=8000,
    doc="This tool collects wgs metrics on an input WGS bam.\nThe following programs are run in this tool:\n  - picard CollectWgsMetrics\nThis tool is also made to be used conditionally with the conditional_run parameter.\nSimply pass an empty array to conditional_run and scatter on the input to skip.",
)

Kfdrc_Alignment_Workflow = WorkflowBuilder(
    identifier="kfdrc_alignment_workflow",
    friendly_name="Kids First DRC Alignment and GATK HaplotypeCaller Workflow",
    doc="Kids First Data Resource Center Alignment and Haplotype Calling Workflow (bam/fastq-to-cram, gVCF optional). This pipeline follows\nBroad best practices outlined in [Data pre-processing for variant discovery.](https://software.broadinstitute.org/gatk/best-practices/workflow?id=11165)\nIt uses bam/fastq input and aligns/re-aligns to a bwa-indexed reference fasta, version hg38. Resultant bam is de-dupped and\nbase score recalibrated. Contamination is calculated and a gVCF is created optionally using GATK4 vbeta.1-3.5 HaplotypeCaller. Inputs from\nthis can be used later on for further analysis in joint trio genotyping and subsequent refinement and deNovo variant analysis. If you would like to run this workflow using the cavatica public app, a basic primer on running public apps can be found [here](https://www.notion.so/d3b/Starting-From-Scratch-Running-Cavatica-af5ebb78c38a4f3190e32e67b4ce12bb).\nAlternatively, if you'd like to run it locally using `cwltool`, a basic primer on that can be found [here](https://www.notion.so/d3b/Starting-From-Scratch-Running-CWLtool-b8dbbde2dc7742e4aff290b0a878344d) and combined with app-specific info from the readme below.\nThis workflow is the current production workflow, superseding this [public app](https://cavatica.sbgenomics.com/public/apps#kids-first-drc/kids-first-drc-alignment-workflow/kfdrc-alignment-bam2cram2gvcf/); however the outputs are considered equivalent.\n\n# Input Agnostic Alignment Workflow\nWorkflow for the alignment or realignment of input BAMs, PE reads, and/or SE reads; conditionally generate gVCF and metrics.\n\nThis workflow is a all-in-one workflow for handling any kind of reads inputs: BAM inputs, PE reads\nand mates inputs, SE reads inputs,  or any combination of these. The workflow will naively attempt\nto process these depending on what you tell it you have provided. The user informs the workflow of\nwhich inputs to process using three boolean inputs: `run_bam_processing`, `run_pe_reads_processing`,\nand `run_se_reads_processing`. Providing `true` values for these as well their corresponding inputs\nwill result in those inputs being processed.\n\nThe second half of the workflow deals with optional gVCF creation and metrics collection.\nThis workflow is capable of collecting the metrics using the following boolean flags: `run_hs_metrics`,\n`run_wgs_metrics`, and `run_agg_metrics`. To run these metrics, additional optional inputs must\nalso be provided: `wxs_bait_interval_list` and `wxs_target_interval_list` for HsMetrics,\n`wgs_coverage_interval_list` for WgsMetrics. To generate the gVCF, set `run_gvcf_processing` to\n`true` and provide the following optional files: `dbsnp_vcf`, `contamination_sites_bed`,\n`contamination_sites_mu`, `contamination_sites_ud`, `wgs_calling_interval_list`, and\n`wgs_evaluation_interval_list`.\n\n![data service logo](https://github.com/d3b-center/d3b-research-workflows/raw/master/doc/kfdrc-logo-sm.png)\n\n## Basic Info\n- dockerfiles: https://github.com/d3b-center/bixtools\n- tested with\n  - Seven Bridges Cavatica Platform: https://cavatica.sbgenomics.com/\n  - cwltool: https://github.com/common-workflow-language/cwltool/releases/tag/3.0.20200324120055\n\n## References:\n- https://console.cloud.google.com/storage/browser/broad-references/hg38/v0/\n- kfdrc bucket: s3://kids-first-seq-data/broad-references/\n- cavatica: https://cavatica.sbgenomics.com/u/yuankun/kf-reference/\n\n## Inputs:\n```yaml\n  # REQUIRED\n  reference_tar: { type: File, doc: 'Tar file containing a reference fasta and, optionally, its complete set of associated indexes (samtools, bwa, and picard)' }\n  biospecimen_name: { type: string, doc: 'String name of biospcimen' }\n  output_basename: { type: string, doc: 'String to use as the base for output filenames' }\n  knownsites: { type: 'File[]', doc: 'List of files containing known polymorphic sites used to exclude regions around known polymorphisms from analysis' }\n  knownsites_indexes: { type: 'File[]?', doc: 'Corresponding indexes for the knownsites. File position in list must match with its corresponding VCF's position in the knownsites file list. For example, if the first file in the knownsites list is 1000G_omni2.5.hg38.vcf.gz then the first item in this list must be 1000G_omni2.5.hg38.vcf.gz.tbi. Optional, but will save time/cost on indexing.' }\n  # REQUIRED for gVCF\n  dbsnp_vcf: { type: 'File?', doc: 'dbSNP vcf file' }\n  dbsnp_idx: { type: 'File?', doc: 'dbSNP vcf index file' }\n  contamination_sites_bed: { type: 'File?', doc: '.bed file for markers used in this analysis,format(chr\tpos-1\tpos\trefAllele\taltAllele)' }\n  contamination_sites_mu: { type: 'File?', doc: '.mu matrix file of genotype matrix' }\n  contamination_sites_ud: { type: 'File?', doc: '.UD matrix file from SVD result of genotype matrix' }\n  run_gvcf_processing: { type: boolean, doc: 'gVCF will be generated. Requires: dbsnp_vcf, contamination_sites_bed, contamination_sites_mu, contamination_sites_ud, wgs_calling_interval_list, wgs_evaluation_interval_list' }\n  # ADJUST TO FIT INPUT READS TYPE(S)\n  input_bam_list: { type: 'File[]?', doc: 'List of input BAM files' }\n  input_pe_reads_list: { type: 'File[]?', doc: 'List of input R1 paired end fastq reads' }\n  input_pe_mates_list: { type: 'File[]?', doc: 'List of input R2 paired end fastq reads' }\n  input_pe_rgs_list: { type: 'string[]?', doc: 'List of RG strings to use in PE processing' }\n  input_se_reads_list: { type: 'File[]?', doc: 'List of input single end fastq reads' }\n  input_se_rgs_list: { type: 'string[]?', doc: 'List of RG strings to use in SE processing' }\n  run_bam_processing: { type: boolean, doc: 'BAM processing will be run. Requires: input_bam_list' }\n  run_pe_reads_processing: { type: boolean, doc: 'PE reads processing will be run. Requires: input_pe_reads_list, input_pe_mates_list, input_pe_rgs_list' }\n  run_se_reads_processing: { type: boolean, doc: 'SE reads processing will be run. Requires: input_se_reads_list, input_se_rgs_list' }\n  # IF WGS or CREATE gVCF\n  wgs_calling_interval_list: { type: 'File?', doc: 'WGS interval list used to aid scattering Haplotype caller' }\n  wgs_coverage_interval_list: { type: 'File?', doc: 'An interval list file that contains the positions to restrict the wgs metrics assessment' }\n  wgs_evaluation_interval_list: { type: 'File?', doc: 'Target intervals to restrict gVCF metric analysis (for VariantCallingMetrics)' }\n  # IF WXS\n  wxs_bait_interval_list: { type: 'File?', doc: 'An interval list file that contains the locations of the WXS baits used (for HsMetrics)' }\n  wxs_target_interval_list: { type: 'File?', doc: 'An interval list file that contains the locations of the WXS targets (for HsMetrics)' }\n  # ADJUST TO GENERATE METRICS\n  run_hs_metrics: { type: boolean, doc: 'HsMetrics will be collected. Only recommended for WXS inputs. Requires: wxs_bait_interval_list, wxs_target_interval_list' }\n  run_wgs_metrics: { type: boolean, doc: 'WgsMetrics will be collected. Only recommended for WGS inputs. Requires: wgs_coverage_interval_list' }\n  run_agg_metrics: { type: boolean, doc: 'AlignmentSummaryMetrics, GcBiasMetrics, InsertSizeMetrics, QualityScoreDistribution, and SequencingArtifactMetrics will be collected. Recommended for both WXS and WGS inputs.' }\n  # ADVANCED\n  min_alignment_score: { type: 'int?', default: 30, doc: 'For BWA MEM, Don't output alignment with score lower than INT. This option only affects output.' }\n```\n\n### Detailed Input Information:\nThe pipeline is build to handle three distinct input types:\n1. BAMs\n1. PE Fastqs\n1. SE Fastqs\n\nAdditionally, the workflow supports these three in any combination. You can have PE Fastqs and BAMs,\nPE Fastqs and SE Fastqs, BAMS and PE Fastqs and SE Fastqs, etc. Each of these three classes will be\nprocsessed and aligned separately and the resulting BWA aligned bams will be merged into a final BAM\nbefore performing steps like BQSR and Metrics collection.\n\n#### BAM Inputs\nThe BAM processing portion of the pipeline is the simplest when it comes to inputs. You may provide\na single BAM or many BAMs. The input for BAMs is a file list. In Cavatica or other GUI interfaces,\nsimply select the files you wish to process. For command line interfaces such as cwltool, your input\nshould look like the following.\n```json\n{\n  ...,\n  'run_pe_reads_processing': false,\n  'run_se_reads_processing': false,\n  'run_bam_processing': true,\n  'input_bam_list': [\n    {\n      'class': 'File',\n      'location': '/path/to/bam1.bam'\n    },\n    {\n      'class': 'File',\n      'location': '/path/to/bam2.bam'\n    }\n  ],\n  ...\n}\n```\n\n#### SE Fastq Inputs\nSE fastq processing requires more input to build the jobs correctly. Rather than providing a single\nlist you must provide two lists: `input_se_reads_list` and `input_se_rgs_list`. The `input_se_reads_list`\nis where you put the files and the `input_se_rgs_list` is where you put your desired BAM @RG headers for\neach reads file. These two lists are must be ordered and of equal length. By ordered, that means the\nfirst item of the `input_se_rgs_list` will be used when aligning the first item of the `input_se_reads_list`.\nIMPORTANT NOTE: When you are entering the rg names, you need to use a second escape `\` to the tab values `\t`\nas seen below. When the string value is read in by a tool such as cwltool it will interpret a `\\t` input\nas `\t` and a `\t` as the literal `<tab>` value which is not a valid entry for bwa mem.\nIf you are using Cavatica GUI, however, no extra escape is necessary. The GUI will add an extra\nescape to any tab values you enter.\n\nIn Cavatica make sure to double check that everything is in the right order when you enter the inputs.\nIn command line interfaces such as cwltool, your input should look like the following.\n```json\n{\n  ...,\n  'run_pe_reads_processing': false,\n  'run_se_reads_processing': true,\n  'run_bam_processing': false,\n  'input_se_reads_list': [\n    {\n      'class': 'File',\n      'location': '/path/to/single1.fastq'\n    },\n    {\n      'class': 'File',\n      'location': '/path/to/single2.fastq'\n    }\n  ],\n  'inputs_se_rgs_list': [\n    '@RG\\tID:single1\\tLB:library_name\\tPL:ILLUMINA\\tSM:sample_name',\n    '@RG\\tID:single2\\tLB:library_name\\tPL:ILLUMINA\\tSM:sample_name'\n  ],\n  ...\n}\n```\nTake particular note of how the first item in the rgs list is the metadata for the first item in the fastq list.\n\n#### PE Fastq Inputs\nPE Fastq processing inputs is exactly like SE Fastq processing but requires you to provide the paired mates\nfiles for your input paired reads. Once again, when using Cavatica make sure your inputs are in the correct\norder. In command line interfaces such as cwltool, your input should look like the following.\n```json\n{\n  ...,\n  'run_pe_reads_processing': true,\n  'run_se_reads_processing': false,\n  'run_bam_processing': false,\n  'input_pe_reads_list': [\n    {\n      'class': 'File',\n      'location': '/path/to/sample1_R1.fastq'\n    },\n    {\n      'class': 'File',\n      'location': '/path/to/sample2_R1fastq'\n    },\n    {\n      'class': 'File',\n      'location': '/path/to/sample3_R1.fastq'\n    }\n  ],\n  'input_pe_mates_list': [\n    {\n      'class': 'File',\n      'location': '/path/to/sample1_R2.fastq'\n    },\n    {\n      'class': 'File',\n      'location': '/path/to/sample2_R2.fastq'\n    },\n    {\n      'class': 'File',\n      'location': '/path/to/sample3_R2.fastq'\n    }\n  ],\n  'inputs_pe_rgs_list': [\n    '@RG\\tID:sample1\\tLB:library_name\\tPL:ILLUMINA\tSM:sample_name',\n    '@RG\\tID:sample2\\tLB:library_name\\tPL:ILLUMINA\tSM:sample_name',\n    '@RG\\tID:sample3\\tLB:library_name\\tPL:ILLUMINA\tSM:sample_name'\n  ],\n  ...\n}\n```\n\n#### Multiple Input Types\nAs mentioned above, these three input types can be added in any combination. If you wanted to add\nall three your command line input would look like the following.\n```json\n{\n  ...,\n  'run_pe_reads_processing': true,\n  'run_se_reads_processing': true,\n  'run_bam_processing': true,\n  'input_bam_list': [\n    {\n      'class': 'File',\n      'location': '/path/to/bam1.bam'\n    },\n    {\n      'class': 'File',\n      'location': '/path/to/bam2.bam'\n    }\n  ],\n  'input_se_reads_list': [\n    {\n      'class': 'File',\n      'location': '/path/to/single1.fastq'\n    },\n    {\n      'class': 'File',\n      'location': '/path/to/single2.fastq'\n    }\n  ],\n  'inputs_se_rgs_list': [\n    '@RG\\tID:single1\\tLB:library_name\\tPL:ILLUMINA\\tSM:sample_name',\n    '@RG\\tID:single2\\tLB:library_name\\tPL:ILLUMINA\\tSM:sample_name'\n  ],\n  'input_pe_reads_list': [\n    {\n      'class': 'File',\n      'location': '/path/to/sample1_R1.fastq'\n    },\n    {\n      'class': 'File',\n      'location': '/path/to/sample2_R1fastq'\n    },\n    {\n      'class': 'File',\n      'location': '/path/to/sample3_R1.fastq'\n    }\n  ],\n  'input_pe_mates_list': [\n    {\n      'class': 'File',\n      'location': '/path/to/sample1_R2.fastq'\n    },\n    {\n      'class': 'File',\n      'location': '/path/to/sample2_R2.fastq'\n    },\n    {\n      'class': 'File',\n      'location': '/path/to/sample3_R2.fastq'\n    }\n  ],\n  'inputs_pe_rgs_list': [\n    '@RG\\tID:sample1\\tLB:library_name\\tPL:ILLUMINA\\tSM:sample_name',\n    '@RG\\tID:sample2\\tLB:library_name\\tPL:ILLUMINA\\tSM:sample_name',\n    '@RG\\tID:sample3\\tLB:library_name\\tPL:ILLUMINA\\tSM:sample_name'\n  ],\n  ...\n}\n```\n\n### Example Runtimes:\n1. 120 GB WGS BAM with AggMetrics, WgsMetrics, and gVCF creation: 14 hours & $35\n1. 120 GB WGS BAM only: 11 hours\n1. 4x40 GB WGS FASTQ files with AggMetrics, WgsMetrics, and gVCF creation: 23 hours & $72\n1. 4x40 GB WGS FASTQ files only: 18 hours\n1. 4x9 GB WXS FASTQ files with AggMetrics and gVCF creation: 4 hours & $9\n1. 4x9 GB WXS FASTQ files only: 3 hours\n\n### Caveats:\n1. Duplicates are flagged in a process that is connected to bwa mem. The implication of this design\n   decision is that duplicates are flagged only on the inputs of that are scattered into bwa.\n   Duplicates, therefore, are not being flagged at a library level and, for large BAM and FASTQ inputs,\n   duplicates are only being detected within a portion of the read group.\n\n### Tips for running:\n1. For the fastq input file lists (PE or SE), make sure the lists are properly ordered. The items in\n   the arrays are processed based on their position. These lists are dotproduct scattered. This means\n   that the first file in `input_pe_reads_list` is run with the first file in `input_pe_mates_list`\n   and the first string in `input_pe_rgs_list`. This also means these arrays must be the same\n   length or the workflow will fail.\n1. The input for the reference_tar must be a tar file containing the reference fasta along with its indexes.\n   The required indexes are `[.64.ann,.64.amb,.64.bwt,.64.pac,.64.sa,.dict,.fai]` and are generated by bwa, picard, and samtools.\n   Additionally, an `.64.alt` index is recommended.\n1. If you are making your own bwa indexes make sure to use the `-6` flag to obtain the `.64` version of the\n   indexes. Indexes that do not match this naming schema will cause a failure in certain runner ecosystems.\n1. Should you decide to create your own reference indexes and omit the ALT index file from the reference,\n   or if its naming structure mismatches the other indexes, then your alignments will be equivalent to the results you would\n   obtain if you run BWA-MEM with the -j option.\n1. The following is an example of a complete reference tar input:\n```\n~ tar tf Homo_sapiens_assembly38.tgz\nHomo_sapiens_assembly38.dict\nHomo_sapiens_assembly38.fasta\nHomo_sapiens_assembly38.fasta.64.alt\nHomo_sapiens_assembly38.fasta.64.amb\nHomo_sapiens_assembly38.fasta.64.ann\nHomo_sapiens_assembly38.fasta.64.bwt\nHomo_sapiens_assembly38.fasta.64.pac\nHomo_sapiens_assembly38.fasta.64.sa\nHomo_sapiens_assembly38.fasta.fai\n```\n1. For advanced usage, you can skip the knownsite indexing by providing the knownsites_indexes input.\n   This file list should contain the indexes for each of the files in your knownsites input. Please\n   note this list must be ordered in such a way where the position of the index file in the\n   knownsites_indexes list must correspond with the position of the VCF file in the knownsites list\n   that it indexes. In the example input below you can see that the 1000G_omni2.5.hg38.vcf.gz.tbi\n   file is the fourth item in the knownsites_indexes because the 1000G_omni2.5.hg38.vcf.gz file is the\n   fourth item in the knownsites list. Failure to order in this way will result in the pipeline\n   failing or generating erroneous files.\n1. Turning off gVCF creation and metrics collection for a minimal successful run.\n1. Suggested reference inputs (available from the [Broad Resource Bundle](https://console.cloud.google.com/storage/browser/genomics-public-data/resources/broad/hg38/v0)):\n```yaml\ncontamination_sites_bed: Homo_sapiens_assembly38.contam.bed\ncontamination_sites_mu: Homo_sapiens_assembly38.contam.mu\ncontamination_sites_ud: Homo_sapiens_assembly38.contam.UD\ndbsnp_vcf: Homo_sapiens_assembly38.dbsnp138.vcf\nreference_tar: Homo_sapiens_assembly38.tgz\nknownsites:\n  - Homo_sapiens_assembly38.known_indels.vcf.gz\n  - Mills_and_1000G_gold_standard.indels.hg38.vcf.gz\n  - 1000G_phase1.snps.high_confidence.hg38.vcf.gz\n  - 1000G_omni2.5.hg38.vcf.gz\nknownsites_indexes:\n  - Homo_sapiens_assembly38.known_indels.vcf.gz.tbi\n  - Mills_and_1000G_gold_standard.indels.hg38.vcf.gz.tbi\n  - 1000G_phase1.snps.high_confidence.hg38.vcf.gz.tbi\n  - 1000G_omni2.5.hg38.vcf.gz.tbi\n```\n",
)

Kfdrc_Alignment_Workflow.input(
    "biospecimen_name",
    String(),
    doc=InputDocumentation(doc="String name of biospcimen"),
)

Kfdrc_Alignment_Workflow.input(
    "contamination_sites_bed",
    File(optional=True),
    doc=InputDocumentation(
        doc=".bed file for markers used in this analysis,format(chr	pos-1	pos	refAllele	altAllele)"
    ),
)

Kfdrc_Alignment_Workflow.input(
    "contamination_sites_mu",
    File(optional=True),
    doc=InputDocumentation(doc=".mu matrix file of genotype matrix"),
)

Kfdrc_Alignment_Workflow.input(
    "contamination_sites_ud",
    File(optional=True),
    doc=InputDocumentation(doc=".UD matrix file from SVD result of genotype matrix"),
)

Kfdrc_Alignment_Workflow.input(
    "dbsnp_idx",
    File(optional=True),
    doc=InputDocumentation(doc="dbSNP vcf index file"),
)

Kfdrc_Alignment_Workflow.input(
    "dbsnp_vcf", File(optional=True), doc=InputDocumentation(doc="dbSNP vcf file"),
)

Kfdrc_Alignment_Workflow.input(
    "input_bam_list",
    Array(t=File(), optional=True),
    doc=InputDocumentation(doc="List of input BAM files"),
)

Kfdrc_Alignment_Workflow.input(
    "input_pe_mates_list",
    Array(t=File(), optional=True),
    doc=InputDocumentation(doc="List of input R2 paired end fastq reads"),
)

Kfdrc_Alignment_Workflow.input(
    "input_pe_reads_list",
    Array(t=File(), optional=True),
    doc=InputDocumentation(doc="List of input R1 paired end fastq reads"),
)

Kfdrc_Alignment_Workflow.input(
    "input_pe_rgs_list",
    Array(t=String(), optional=True),
    doc=InputDocumentation(doc="List of RG strings to use in PE processing"),
)

Kfdrc_Alignment_Workflow.input(
    "input_se_reads_list",
    Array(t=File(), optional=True),
    doc=InputDocumentation(doc="List of input singlie end fastq reads"),
)

Kfdrc_Alignment_Workflow.input(
    "input_se_rgs_list",
    Array(t=String(), optional=True),
    doc=InputDocumentation(doc="List of RG strings to use in SE processing"),
)

Kfdrc_Alignment_Workflow.input(
    "knownsites",
    Array(t=File()),
    doc=InputDocumentation(
        doc="List of files containing known polymorphic sites used to exclude regions around known polymorphisms from analysis"
    ),
)

Kfdrc_Alignment_Workflow.input(
    "knownsites_indexes",
    Array(t=File(), optional=True),
    doc=InputDocumentation(
        doc="Corresponding indexes for the knownsites. File position in list must match with its corresponding VCF's position in the knownsites file list. For example, if the first file in the knownsites list is 1000G_omni2.5.hg38.vcf.gz then the first item in this list must be 1000G_omni2.5.hg38.vcf.gz.tbi. Optional, but will save time/cost on indexing."
    ),
)

Kfdrc_Alignment_Workflow.input(
    "min_alignment_score",
    Int(optional=True),
    default=30,
    doc=InputDocumentation(
        doc="For BWA MEM, Don't output alignment with score lower than INT. This option only affects output."
    ),
)

Kfdrc_Alignment_Workflow.input(
    "output_basename",
    String(),
    doc=InputDocumentation(doc="String to use as the base for output filenames"),
)

Kfdrc_Alignment_Workflow.input(
    "reference_tar",
    File(),
    doc=InputDocumentation(
        doc="Tar file containing a reference fasta and, optionally, its complete set of associated indexes (samtools, bwa, and picard)"
    ),
)

Kfdrc_Alignment_Workflow.input(
    "run_agg_metrics",
    Boolean(),
    doc=InputDocumentation(
        doc="AlignmentSummaryMetrics, GcBiasMetrics, InsertSizeMetrics, QualityScoreDistribution, and SequencingArtifactMetrics will be collected. Recommended for both WXS and WGS inputs."
    ),
)

Kfdrc_Alignment_Workflow.input(
    "run_bam_processing",
    Boolean(),
    doc=InputDocumentation(doc="BAM processing will be run. Requires: input_bam_list"),
)

Kfdrc_Alignment_Workflow.input(
    "run_gvcf_processing",
    Boolean(),
    doc=InputDocumentation(
        doc="gVCF will be generated. Requires: dbsnp_vcf, contamination_sites_bed, contamination_sites_mu, contamination_sites_ud, wgs_calling_interval_list, wgs_evaluation_interval_list"
    ),
)

Kfdrc_Alignment_Workflow.input(
    "run_hs_metrics",
    Boolean(),
    doc=InputDocumentation(
        doc="HsMetrics will be collected. Only recommended for WXS inputs. Requires: wxs_bait_interval_list, wxs_target_interval_list"
    ),
)

Kfdrc_Alignment_Workflow.input(
    "run_pe_reads_processing",
    Boolean(),
    doc=InputDocumentation(
        doc="PE reads processing will be run. Requires: input_pe_reads_list, input_pe_mates_list, input_pe_rgs_list"
    ),
)

Kfdrc_Alignment_Workflow.input(
    "run_se_reads_processing",
    Boolean(),
    doc=InputDocumentation(
        doc="SE reads processing will be run. Requires: input_se_reads_list, input_se_rgs_list"
    ),
)

Kfdrc_Alignment_Workflow.input(
    "run_wgs_metrics",
    Boolean(),
    doc=InputDocumentation(
        doc="WgsMetrics will be collected. Only recommended for WGS inputs. Requires: wgs_coverage_interval_list"
    ),
)

Kfdrc_Alignment_Workflow.input(
    "wgs_calling_interval_list",
    File(optional=True),
    doc=InputDocumentation(
        doc="WGS interval list used to aid scattering Haplotype caller"
    ),
)

Kfdrc_Alignment_Workflow.input(
    "wgs_coverage_interval_list",
    File(optional=True),
    doc=InputDocumentation(
        doc="An interval list file that contains the positions to restrict the wgs metrics assessment"
    ),
)

Kfdrc_Alignment_Workflow.input(
    "wgs_evaluation_interval_list",
    File(optional=True),
    doc=InputDocumentation(
        doc="Target intervals to restrict gvcf metric analysis (for VariantCallingMetrics)"
    ),
)

Kfdrc_Alignment_Workflow.input(
    "wxs_bait_interval_list",
    File(optional=True),
    doc=InputDocumentation(
        doc="An interval list file that contains the locations of the WXS baits used (for HsMetrics)"
    ),
)

Kfdrc_Alignment_Workflow.input(
    "wxs_target_interval_list",
    File(optional=True),
    doc=InputDocumentation(
        doc="An interval list file that contains the locations of the WXS targets (for HsMetrics)"
    ),
)


Kfdrc_Alignment_Workflow.step(
    "gatekeeper",
    Gatekeeper_V0_1_0(
        run_agg_metrics=Kfdrc_Alignment_Workflow.run_agg_metrics,
        run_bam_processing=Kfdrc_Alignment_Workflow.run_bam_processing,
        run_gvcf_processing=Kfdrc_Alignment_Workflow.run_gvcf_processing,
        run_hs_metrics=Kfdrc_Alignment_Workflow.run_hs_metrics,
        run_pe_reads_processing=Kfdrc_Alignment_Workflow.run_pe_reads_processing,
        run_se_reads_processing=Kfdrc_Alignment_Workflow.run_se_reads_processing,
        run_wgs_metrics=Kfdrc_Alignment_Workflow.run_wgs_metrics,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "index_knownsites",
    Tabix_Index_V0_1_0(
        input_file=Kfdrc_Alignment_Workflow.knownsites,
        input_index=Kfdrc_Alignment_Workflow.knownsites_indexes,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "untar_reference",
    Untar_Indexed_Reference_V0_1_0(
        reference_tar=Kfdrc_Alignment_Workflow.reference_tar,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "bundle_secondaries",
    Bundle_Secondaryfiles_V0_1_0(
        primary_file=Kfdrc_Alignment_Workflow.untar_reference.fasta,
        secondary_files=[
            Kfdrc_Alignment_Workflow.untar_reference.fai,
            Kfdrc_Alignment_Workflow.untar_reference.dict,
            Kfdrc_Alignment_Workflow.untar_reference.alt,
            Kfdrc_Alignment_Workflow.untar_reference.amb,
            Kfdrc_Alignment_Workflow.untar_reference.ann,
            Kfdrc_Alignment_Workflow.untar_reference.bwt,
            Kfdrc_Alignment_Workflow.untar_reference.pac,
            Kfdrc_Alignment_Workflow.untar_reference.sa,
        ],
    ),
)


Kfdrc_Alignment_Workflow.step(
    "process_bams",
    Kfdrc_Process_Bamlist(
        conditional_run=Kfdrc_Alignment_Workflow.gatekeeper.scatter_bams,
        indexed_reference_fasta=Kfdrc_Alignment_Workflow.bundle_secondaries.outp,
        input_bam_list=Kfdrc_Alignment_Workflow.input_bam_list,
        min_alignment_score=Kfdrc_Alignment_Workflow.min_alignment_score,
        sample_name=Kfdrc_Alignment_Workflow.biospecimen_name,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "process_pe_reads",
    Kfdrc_Process_Pe_Readslist2(
        conditional_run=Kfdrc_Alignment_Workflow.gatekeeper.scatter_pe_reads,
        indexed_reference_fasta=Kfdrc_Alignment_Workflow.bundle_secondaries.outp,
        input_pe_mates_list=Kfdrc_Alignment_Workflow.input_pe_mates_list,
        input_pe_reads_list=Kfdrc_Alignment_Workflow.input_pe_reads_list,
        input_pe_rgs_list=Kfdrc_Alignment_Workflow.input_pe_rgs_list,
        min_alignment_score=Kfdrc_Alignment_Workflow.min_alignment_score,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "process_se_reads",
    Kfdrc_Process_Se_Readslist2(
        conditional_run=Kfdrc_Alignment_Workflow.gatekeeper.scatter_se_reads,
        indexed_reference_fasta=Kfdrc_Alignment_Workflow.bundle_secondaries.outp,
        input_se_reads_list=Kfdrc_Alignment_Workflow.input_se_reads_list,
        input_se_rgs_list=Kfdrc_Alignment_Workflow.input_se_rgs_list,
        min_alignment_score=Kfdrc_Alignment_Workflow.min_alignment_score,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "python_createsequencegroups",
    Python_Createsequencegroups_V0_1_0(
        ref_dict=Kfdrc_Alignment_Workflow.untar_reference.dict,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "sambamba_merge",
    Sambamba_Merge_Anylist_V0_1_0(
        bams=[
            Kfdrc_Alignment_Workflow.process_bams.unsorted_bams,
            Kfdrc_Alignment_Workflow.process_pe_reads.unsorted_bams,
            Kfdrc_Alignment_Workflow.process_se_reads.unsorted_bams,
        ],
        base_file_name=Kfdrc_Alignment_Workflow.output_basename,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "sambamba_sort",
    Sambamba_Sort_V0_1_0(
        bam=Kfdrc_Alignment_Workflow.sambamba_merge.merged_bam,
        base_file_name=Kfdrc_Alignment_Workflow.output_basename,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "gatk_baserecalibrator",
    Gatkv4_Baserecalibrator_V0_1_0(
        input_bam=Kfdrc_Alignment_Workflow.sambamba_sort.sorted_bam,
        knownsites=Kfdrc_Alignment_Workflow.index_knownsites.outp,
        reference=Kfdrc_Alignment_Workflow.bundle_secondaries.outp,
        sequence_interval=Kfdrc_Alignment_Workflow.python_createsequencegroups.sequence_intervals,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "gatk_gatherbqsrreports",
    Gatk_Gatherbqsrreports_V0_1_0(
        input_brsq_reports=Kfdrc_Alignment_Workflow.gatk_baserecalibrator.outp,
        output_basename=Kfdrc_Alignment_Workflow.output_basename,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "gatk_applybqsr",
    Gatk4_Applybqsr_V0_1_0(
        bqsr_report=Kfdrc_Alignment_Workflow.gatk_gatherbqsrreports.outp,
        input_bam=Kfdrc_Alignment_Workflow.sambamba_sort.sorted_bam,
        reference=Kfdrc_Alignment_Workflow.bundle_secondaries.outp,
        sequence_interval=Kfdrc_Alignment_Workflow.python_createsequencegroups.sequence_intervals_with_unmapped,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "picard_gatherbamfiles",
    Picard_Gatherbamfiles_V0_1_0(
        input_bam=Kfdrc_Alignment_Workflow.gatk_applybqsr.recalibrated_bam,
        output_bam_basename=Kfdrc_Alignment_Workflow.output_basename,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "picard_qualityscoredistribution",
    Picard_Qualityscoredistribution_Conditional_V0_1_0(
        conditional_run=Kfdrc_Alignment_Workflow.gatekeeper.scatter_agg_metrics,
        input_bam=Kfdrc_Alignment_Workflow.picard_gatherbamfiles.outp,
        reference=Kfdrc_Alignment_Workflow.bundle_secondaries.outp,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "samtools_bam_to_cram",
    Samtools_Bam_To_Cram_V0_1_0(
        input_bam=Kfdrc_Alignment_Workflow.picard_gatherbamfiles.outp,
        reference=Kfdrc_Alignment_Workflow.bundle_secondaries.outp,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "generate_gvcf",
    Kfdrc_Bam_To_Gvcf(
        conditional_run=Kfdrc_Alignment_Workflow.gatekeeper.scatter_gvcf,
        contamination_sites_bed=Kfdrc_Alignment_Workflow.contamination_sites_bed,
        contamination_sites_mu=Kfdrc_Alignment_Workflow.contamination_sites_mu,
        contamination_sites_ud=Kfdrc_Alignment_Workflow.contamination_sites_ud,
        dbsnp_idx=Kfdrc_Alignment_Workflow.dbsnp_idx,
        dbsnp_vcf=Kfdrc_Alignment_Workflow.dbsnp_vcf,
        indexed_reference_fasta=Kfdrc_Alignment_Workflow.bundle_secondaries.outp,
        input_bam=Kfdrc_Alignment_Workflow.picard_gatherbamfiles.outp,
        output_basename=Kfdrc_Alignment_Workflow.output_basename,
        reference_dict=Kfdrc_Alignment_Workflow.untar_reference.dict,
        wgs_calling_interval_list=Kfdrc_Alignment_Workflow.wgs_calling_interval_list,
        wgs_evaluation_interval_list=Kfdrc_Alignment_Workflow.wgs_evaluation_interval_list,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "picard_collectalignmentsummarymetrics",
    Picard_Collectalignmentsummarymetrics_Conditional_V0_1_0(
        conditional_run=Kfdrc_Alignment_Workflow.gatekeeper.scatter_agg_metrics,
        input_bam=Kfdrc_Alignment_Workflow.picard_gatherbamfiles.outp,
        reference=Kfdrc_Alignment_Workflow.bundle_secondaries.outp,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "picard_collectgcbiasmetrics",
    Picard_Collectgcbiasmetrics_V0_1_0(
        conditional_run=Kfdrc_Alignment_Workflow.gatekeeper.scatter_agg_metrics,
        input_bam=Kfdrc_Alignment_Workflow.picard_gatherbamfiles.outp,
        reference=Kfdrc_Alignment_Workflow.bundle_secondaries.outp,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "picard_collecthsmetrics",
    Picard_Collecthsmetrics_Conditional_V0_1_0(
        bait_intervals=Kfdrc_Alignment_Workflow.wxs_bait_interval_list,
        conditional_run=Kfdrc_Alignment_Workflow.gatekeeper.scatter_hs_metrics,
        input_bam=Kfdrc_Alignment_Workflow.picard_gatherbamfiles.outp,
        reference=Kfdrc_Alignment_Workflow.bundle_secondaries.outp,
        target_intervals=Kfdrc_Alignment_Workflow.wxs_target_interval_list,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "picard_collectinsertsizemetrics",
    Picard_Collectinsertsizemetrics_Conditional_V0_1_0(
        conditional_run=Kfdrc_Alignment_Workflow.gatekeeper.scatter_agg_metrics,
        input_bam=Kfdrc_Alignment_Workflow.picard_gatherbamfiles.outp,
        reference=Kfdrc_Alignment_Workflow.bundle_secondaries.outp,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "picard_collectsequencingartifactmetrics",
    Picard_Collectsequencingartifactmetrics_Conditional_V0_1_0(
        conditional_run=Kfdrc_Alignment_Workflow.gatekeeper.scatter_agg_metrics,
        input_bam=Kfdrc_Alignment_Workflow.picard_gatherbamfiles.outp,
        reference=Kfdrc_Alignment_Workflow.bundle_secondaries.outp,
    ),
)


Kfdrc_Alignment_Workflow.step(
    "picard_collectwgsmetrics",
    Picard_Collectwgsmetrics_Conditional_V0_1_0(
        conditional_run=Kfdrc_Alignment_Workflow.gatekeeper.scatter_wgs_metrics,
        input_bam=Kfdrc_Alignment_Workflow.picard_gatherbamfiles.outp,
        intervals=Kfdrc_Alignment_Workflow.wgs_coverage_interval_list,
        reference=Kfdrc_Alignment_Workflow.bundle_secondaries.outp,
    ),
)

Kfdrc_Alignment_Workflow.output(
    "alignment_metrics",
    source=Kfdrc_Alignment_Workflow.picard_collectalignmentsummarymetrics.outp,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "artifact_bait_bias_detail_metrics",
    source=Kfdrc_Alignment_Workflow.picard_collectsequencingartifactmetrics.bait_bias_detail_metrics,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "artifact_bait_bias_summary_metrics",
    source=Kfdrc_Alignment_Workflow.picard_collectsequencingartifactmetrics.bait_bias_summary_metrics,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "artifact_error_summary_metrics",
    source=Kfdrc_Alignment_Workflow.picard_collectsequencingartifactmetrics.error_summary_metrics,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "artifact_pre_adapter_detail_metrics",
    source=Kfdrc_Alignment_Workflow.picard_collectsequencingartifactmetrics.pre_adapter_detail_metrics,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "artifact_pre_adapter_summary_metrics",
    source=Kfdrc_Alignment_Workflow.picard_collectsequencingartifactmetrics.pre_adapter_summary_metrics,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "bqsr_report",
    source=Kfdrc_Alignment_Workflow.gatk_gatherbqsrreports.outp,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "cram", source=Kfdrc_Alignment_Workflow.samtools_bam_to_cram.outp, output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "gc_bias_chart",
    source=Kfdrc_Alignment_Workflow.picard_collectgcbiasmetrics.chart,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "gc_bias_detail",
    source=Kfdrc_Alignment_Workflow.picard_collectgcbiasmetrics.detail,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "gc_bias_summary",
    source=Kfdrc_Alignment_Workflow.picard_collectgcbiasmetrics.summary,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "gvcf", source=Kfdrc_Alignment_Workflow.generate_gvcf.gvcf, output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "gvcf_calling_metrics",
    source=Kfdrc_Alignment_Workflow.generate_gvcf.gvcf_calling_metrics,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "hs_metrics",
    source=Kfdrc_Alignment_Workflow.picard_collecthsmetrics.outp,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "insert_metrics",
    source=Kfdrc_Alignment_Workflow.picard_collectinsertsizemetrics.metrics,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "insert_plot",
    source=Kfdrc_Alignment_Workflow.picard_collectinsertsizemetrics.plot,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "qual_chart",
    source=Kfdrc_Alignment_Workflow.picard_qualityscoredistribution.chart,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "qual_metrics",
    source=Kfdrc_Alignment_Workflow.picard_qualityscoredistribution.metrics,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "verifybamid_output",
    source=Kfdrc_Alignment_Workflow.generate_gvcf.verifybamid_output,
    output_name=True,
)

Kfdrc_Alignment_Workflow.output(
    "wgs_metrics",
    source=Kfdrc_Alignment_Workflow.picard_collectwgsmetrics.outp,
    output_name=True,
)


if __name__ == "__main__":
    # or "cwl"
    Kfdrc_Alignment_Workflow().translate("wdl")
