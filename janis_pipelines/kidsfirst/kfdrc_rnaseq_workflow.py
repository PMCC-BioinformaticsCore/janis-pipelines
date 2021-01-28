from datetime import datetime
from typing import List, Optional, Dict, Any

from janis_core import *
from janis_core.types.common_data_types import File, String, Int

Format_Fusion_File_V0_1_0 = CommandToolBuilder(
    tool="format_fusion_file",
    base_command=["Rscript"],
    inputs=[
        ToolInput(
            tag="caller",
            input_type=String(),
            doc=InputDocumentation(doc=None, quality=InputQualityType.configuration),
        ),
        ToolInput(
            tag="input_caller_fusion_file",
            input_type=File(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="sample_name", input_type=String(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="formatted_fusion_tsv",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.tsv"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/annofuse:0.90.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "/rocker-build/formatFusionCalls.R --fusionfile {JANIS_CWL_TOKEN_2} --tumorid {JANIS_CWL_TOKEN_3} --caller {JANIS_CWL_TOKEN_1} --outputfile {JANIS_CWL_TOKEN_3}.{JANIS_CWL_TOKEN_1}_formatted.tsv",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="caller", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="input_caller_fusion_file", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="sample_name", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=4,
    memory=8000,
)
Fusion_Annotator_V0_1_0 = CommandToolBuilder(
    tool="fusion_annotator",
    base_command=["tar"],
    inputs=[
        ToolInput(
            tag="col_num",
            input_type=Int(optional=True),
            default=24,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="genome_tar", input_type=File(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="genome_untar_path",
            input_type=String(optional=True),
            default="GRCh38_v27_CTAT_lib_Feb092018/ctat_genome_lib_build_dir",
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_fusion_file",
            input_type=File(),
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
            tag="annotated_tsv",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.tsv"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/fusionanno:latest",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "-zxf {JANIS_CWL_TOKEN_3} && /opt/FusionAnnotator/FusionAnnotator --genome_lib_dir ./{JANIS_CWL_TOKEN_4} --annotate {JANIS_CWL_TOKEN_5} --fusion_name_col {JANIS_CWL_TOKEN_2} > {JANIS_CWL_TOKEN_1}.annotated.tsv",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="col_num", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="genome_tar", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="genome_untar_path", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="input_fusion_file", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=4,
    memory=8000,
)
Annofuse_V0_1_0 = CommandToolBuilder(
    tool="annoFuse",
    base_command=[],
    inputs=[
        ToolInput(
            tag="arriba_formatted_fusions",
            input_type=File(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="rsem_expr_file", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="sample_name", input_type=String(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="starfusion_formatted_fusions",
            input_type=File(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="filtered_fusions_tsv",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.tsv"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/annofuse:0.90.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "A_CT=`wc -l {JANIS_CWL_TOKEN_5} | cut -f 1 -d ' '`\nS_CT=`wc -l {JANIS_CWL_TOKEN_4} | cut -f 1 -d ' '`\nif [ $A_CT -eq 1 ] && [ $S_CT -eq 1 ]; then\n  echo 'Both inputs are empty, will skip processing as there no fusions.' >&2;\n  exit 0;\nfi\nRscript /rocker-build/annoFusePerSample.R --fusionfileArriba {JANIS_CWL_TOKEN_5} --fusionfileStarFusion {JANIS_CWL_TOKEN_4} --expressionFile {JANIS_CWL_TOKEN_2} --tumorID {JANIS_CWL_TOKEN_3} --outputfile {JANIS_CWL_TOKEN_1}.annoFuse_filter.tsv",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="rsem_expr_file", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="sample_name", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="starfusion_formatted_fusions", type_hint=File(),
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="arriba_formatted_fusions", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=4,
    memory=8000,
)
Bam2Fastq_V0_1_0 = CommandToolBuilder(
    tool="bam2fastq",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(
            tag="SampleID", input_type=String(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="input_reads_1", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_reads_2",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_type", input_type=String(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="runThreadN", input_type=Int(), doc=InputDocumentation(doc=None)),
    ],
    outputs=[
        ToolOutput(
            tag="fq1",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.converted_1.*"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="fq2",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.converted_2.*"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/samtools:1.9",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="set -eo pipefail\n${\n    if(inputs.input_type == 'PEBAM'){\n        var command = 'samtools sort -m 1G -n -O SAM -@ ' + inputs.runThreadN + ' ' + inputs.input_reads_1.path + ' | samtools fastq -c 2 -1 ' + inputs.SampleID + '.converted_1.fastq.gz -2 ' + inputs.SampleID + '.converted_2.fastq.gz -@ ' + inputs.runThreadN+ ' -'\n        return command\n    }\n    else if(inputs.input_type == 'SEBAM'){\n        var command = 'samtools sort -m 1G -n -O SAM -@ ' + inputs.runThreadN + ' ' + inputs.input_reads_1.path + ' | samtools fastq -c 2 -@ ' + inputs.runThreadN + ' - > ' + inputs.SampleID + '.converted_1.fastq && bgzip ' + inputs.SampleID + '.converted_1.fastq'\n        return command\n    }\n    else if(inputs.input_type == 'FASTQ' && inputs.input_reads_2 != null){\n        var extr1 = (inputs.input_reads_1.nameext == '.gz' ? '.fastq.gz' : inputs.input_reads_1.nameext)\n        var extr2 = (inputs.input_reads_2.nameext == '.gz' ? '.fastq.gz' : inputs.input_reads_2.nameext)\n        var command =  'cp ' + inputs.input_reads_1.path + ' ' + inputs.input_reads_1.nameroot + '.converted_1' + extr1 + ' && cp ' + inputs.input_reads_2.path + ' ' + inputs.input_reads_2.nameroot + '.converted_2' + extr2\n        return command\n    }\n    else if(inputs.input_type == 'FASTQ' && inputs.input_reads_2 == null){\n        var extr1 = (inputs.input_reads_1.nameext == '.gz' ? '.fastq.gz' : inputs.input_reads_1.nameext)\n        var command =  'cp ' + inputs.input_reads_1.path + ' ' + inputs.input_reads_1.nameroot + '.converted_1' + extr1\n        return command\n    }\n}",
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=36,
    memory=30000,
)
Cutadapter_V0_1_0 = CommandToolBuilder(
    tool="cutadapter",
    base_command=[],
    inputs=[
        ToolInput(
            tag="r1_adapter",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="r2_adapter",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="readFilesIn1", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="readFilesIn2",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="sample_name", input_type=String(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="cutadapt_stats",
            output_type=File(optional=True),
            selector=WildcardSelector(
                wildcard=StringFormatter(
                    "{JANIS_CWL_TOKEN_1}.cutadapt_results.txt",
                    JANIS_CWL_TOKEN_1=InputSelector(
                        input_to_select="sample_name", type_hint=File()
                    ),
                )
            ),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="trimmedReadsR1",
            output_type=File(),
            selector=WildcardSelector(
                wildcard=BasenameOperator(
                    "<expr>'*TRIMMED.' + inputs.readFilesIn1</expr>"
                )
            ),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="trimmedReadsR2",
            output_type=File(optional=True),
            selector=WildcardSelector(
                wildcard="${ if (inputs.readFilesIn2){ return '*TRIMMED.' + inputs.readFilesIn2.basename } else{ return 'placeholder' } }"
            ),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/cutadapt:latest",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="${\n  if (inputs.r1_adapter == null){\n    var cmd = 'cp ' + inputs.readFilesIn1.path + ' ./UNTRIMMED.' + inputs.readFilesIn1.basename\n    if (inputs.readFilesIn2 != null){\n      cmd += ';cp ' + inputs.readFilesIn2.path + ' ./UNTRIMMED.' + inputs.readFilesIn2.basename;\n  }\n  return cmd;\n  }\n  else{\n    var cmd = 'cutadapt -j 16 -m 20 --quality-base=33 -q 20 -a ' + inputs.r1_adapter;\n    if (inputs.r2_adapter && inputs.readFilesIn2){\n      cmd += ' -A ' + inputs.r2_adapter + ' -p TRIMMED.' + inputs.readFilesIn2.basename;\n    }\n    cmd += ' -o TRIMMED.' + inputs.readFilesIn1.basename + ' ' + inputs.readFilesIn1.path + ' ';\n    if (inputs.r2_adapter && inputs.readFilesIn2){\n      cmd += inputs.readFilesIn2.path\n    }\n    cmd += ' > ' + inputs.sample_name + '.cutadapt_results.txt';\n    return cmd;\n  }\n}",
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=16,
    memory=24000,
)
Star_Alignreads_V0_1_0 = CommandToolBuilder(
    tool="star_alignReads",
    base_command=[],
    inputs=[
        ToolInput(tag="genomeDir", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="outFileNamePrefix",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="outSAMattrRGline",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="readFilesIn1", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="readFilesIn2",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="runThreadN", input_type=Int(), doc=InputDocumentation(doc=None)),
    ],
    outputs=[
        ToolOutput(
            tag="chimeric_junctions",
            output_type=File(),
            selector=WildcardSelector(wildcard="*Chimeric.out.junction"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="chimeric_sam_out",
            output_type=File(),
            selector=WildcardSelector(wildcard="*Chimeric.out.sam"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="gene_counts",
            output_type=File(),
            selector=WildcardSelector(wildcard="*ReadsPerGene.out.tab.gz"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="genomic_bam_out",
            output_type=File(),
            selector=WildcardSelector(wildcard="*Aligned.out.bam"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="junctions_out",
            output_type=File(),
            selector=WildcardSelector(wildcard="*SJ.out.tab.gz"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="log_final_out",
            output_type=File(),
            selector=WildcardSelector(wildcard="*Log.final.out"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="log_out",
            output_type=File(),
            selector=WildcardSelector(wildcard="*Log.out"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="log_progress_out",
            output_type=File(),
            selector=WildcardSelector(wildcard="*Log.progress.out"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="transcriptome_bam_out",
            output_type=File(),
            selector=WildcardSelector(wildcard="*Aligned.toTranscriptome.out.bam"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/star:2.6.1d",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "tar -xzf {JANIS_CWL_TOKEN_7} && STAR --outSAMattrRGline {JANIS_CWL_TOKEN_6} --genomeDir ./{JANIS_CWL_TOKEN_2}[0])/ --readFilesIn {JANIS_CWL_TOKEN_1} {JANIS_CWL_TOKEN_3} --readFilesCommand zcat --runThreadN {JANIS_CWL_TOKEN_5} --twopassMode Basic --outFilterMultimapNmax 20 --alignSJoverhangMin 8 --alignSJDBoverhangMin 10 --alignSJstitchMismatchNmax 5 -1 5 5 --outFilterMismatchNmax 999 --outFilterMismatchNoverLmax 0.1 --alignIntronMax 100000 --chimSegmentReadGapMax 3 --chimOutJunctionFormat 1 --alignMatesGapMax 100000 --outFilterType BySJout --outFilterScoreMinOverLread 0.33 --outFilterMatchNminOverLread 0.33 --outReadsUnmapped None --limitSjdbInsertNsj 1200000 --outFileNamePrefix {JANIS_CWL_TOKEN_4}. --outSAMstrandField intronMotif --outFilterIntronMotifs None --alignSoftClipAtReferenceEnds Yes --quantMode TranscriptomeSAM GeneCounts --outSAMtype BAM Unsorted --outSAMunmapped Within --genomeLoad NoSharedMemory --chimSegmentMin 12 --chimJunctionOverhangMin 12 --chimOutType Junctions SeparateSAMold WithinBAM SoftClip --chimMainSegmentMultNmax 1 --outSAMattributes NH HI AS nM NM ch && gzip *ReadsPerGene.out.tab *SJ.out.tab",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="readFilesIn1", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2="<expr>inputs.genomeDir.nameroot.split('.'</expr>",
                JANIS_CWL_TOKEN_3="<expr>inputs.readFilesIn2 ? inputs.readFilesIn2.path : ''</expr>",
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="outFileNamePrefix", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="runThreadN", type_hint=File()
                ),
                JANIS_CWL_TOKEN_6=InputSelector(
                    input_to_select="outSAMattrRGline", type_hint=File()
                ),
                JANIS_CWL_TOKEN_7=InputSelector(
                    input_to_select="genomeDir", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=16,
    memory=60000,
)
Star_Fusion_V0_1_0 = CommandToolBuilder(
    tool="star_fusion",
    base_command=["tar"],
    inputs=[
        ToolInput(
            tag="Chimeric_junction",
            input_type=File(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="SampleID", input_type=String(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="genome_tar", input_type=File(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="genome_untar_path",
            input_type=String(optional=True),
            default="GRCh38_v27_CTAT_lib_Feb092018/ctat_genome_lib_build_dir",
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="abridged_coding",
            output_type=File(),
            selector=WildcardSelector(
                wildcard="*.fusion_predictions.abridged.coding_effect.tsv"
            ),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="chimeric_junction_compressed",
            output_type=File(),
            selector=WildcardSelector(
                wildcard=StringFormatter(
                    "{JANIS_CWL_TOKEN_1}.gz",
                    JANIS_CWL_TOKEN_1=BasenameOperator(
                        InputSelector(
                            input_to_select="Chimeric_junction", type_hint=File()
                        )
                    ),
                )
            ),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/star:fusion-1.5.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "-zxf {JANIS_CWL_TOKEN_1} && /usr/local/STAR-Fusion/STAR-Fusion --genome_lib_dir ./{JANIS_CWL_TOKEN_4} -J {JANIS_CWL_TOKEN_2} --output_dir STAR-Fusion_outdir --examine_coding_effect --CPU 16 && mv STAR-Fusion_outdir/star-fusion.fusion_predictions.abridged.coding_effect.tsv {JANIS_CWL_TOKEN_5}.STAR.fusion_predictions.abridged.coding_effect.tsv && gzip -c {JANIS_CWL_TOKEN_2} > {JANIS_CWL_TOKEN_3}.gz",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="genome_tar", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="Chimeric_junction", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=BasenameOperator(
                    InputSelector(input_to_select="Chimeric_junction", type_hint=File())
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="genome_untar_path", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="SampleID", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=16,
    memory=64000,
)
Expression_Strand_Params_V0_1_0 = CommandToolBuilder(
    tool="expression_strand_params",
    base_command=["nodejs", "expression.js"],
    inputs=[
        ToolInput(
            tag="wf_strand_param",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        )
    ],
    outputs=[
        ToolOutput(
            tag="arriba_std",
            output_type=String(),
            selector="j.ReadJsonOperator(j.Stdout)[out_id]",
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="kallisto_std",
            output_type=String(),
            selector="j.ReadJsonOperator(j.Stdout)[out_id]",
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="rnaseqc_std",
            output_type=String(),
            selector="j.ReadJsonOperator(j.Stdout)[out_id]",
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="rsem_std",
            output_type=String(),
            selector="j.ReadJsonOperator(j.Stdout)[out_id]",
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="ubuntu:latest",
    version="v0.1.0",
    arguments=[],
    files_to_create={
        "expression.js": "'use strict';\nvar inputs=$(inputs);\nvar runtime=$(runtime);\nvar ret = function(){ var strand = 'default'; if (inputs.wf_strand_param != null){ strand = inputs.wf_strand_param; } var parse_dict = { 'default': {'rsem_std': 'none', 'kallisto_std': 'default', 'rnaseqc_std': 'default', 'arriba_std': 'auto'}, 'rf-stranded': {'rsem_std': 'reverse', 'kallisto_std': 'rf-stranded', 'rnaseqc_std': 'rf', 'arriba_std': 'reverse'}, 'fr-stranded': {'rsem_std': 'forward', 'kallisto_std': 'fr-stranded', 'rnaseqc_std': 'fr', 'arriba_std': 'yes'} }; if (strand in parse_dict){ return parse_dict[strand];\n} else{ throw new Error(strand + ' is a not a valid strand param. Use one of default, rf-stranded, fr-stranded'); } }();\nprocess.stdout.write(JSON.stringify(ret));"
    },
)
Kallisto_V0_1_0 = CommandToolBuilder(
    tool="kallisto",
    base_command=[],
    inputs=[
        ToolInput(
            tag="SampleID", input_type=String(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="avg_frag_len",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="reads1", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="reads2",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="std_dev",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="strand",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="transcript_idx", input_type=File(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="abundance_out",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.abundance.tsv.gz"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="images.sbgenomics.com/uros_sipetic/kallisto:0.43.1",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "kallisto quant -i {JANIS_CWL_TOKEN_3} -o output -b 10 -t 8 {JANIS_CWL_TOKEN_1} {JANIS_CWL_TOKEN_2} && mv output/abundance.tsv {JANIS_CWL_TOKEN_4}.kallisto.abundance.tsv && gzip {JANIS_CWL_TOKEN_4}.kallisto.abundance.tsv",
                JANIS_CWL_TOKEN_1="<expr>inputs.strand ? inputs.strand == 'default' ? '' : '--'+inputs.strand : ''</expr>",
                JANIS_CWL_TOKEN_2="<expr>inputs.reads2 ? inputs.reads1.path+' '+inputs.reads2.path : '--single -l '+inputs.avg_frag_len+' -s '+inputs.std_dev+' '+inputs.reads1</expr>",
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="transcript_idx", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="SampleID", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=8,
    memory=10000,
)
Rsem_Calculate_Expression_V0_1_0 = CommandToolBuilder(
    tool="rsem_calculate_expression",
    base_command=["tar"],
    inputs=[
        ToolInput(tag="bam", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(tag="genomeDir", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="input_reads_2",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="outFileNamePrefix",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="strandedness",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="gene_out",
            output_type=File(),
            selector=WildcardSelector(wildcard="*genes.results.gz"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="isoform_out",
            output_type=File(),
            selector=WildcardSelector(wildcard="*isoforms.results.gz"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="images.sbgenomics.com/uros_sipetic/rsem:1.3.1",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "-zxf {JANIS_CWL_TOKEN_1} && ${\n  var cmd = 'rsem-calculate-expression --alignments --append-names --no-bam-output -p 16';\n  if (inputs.strandedness != null && inputs.strandedness != 'default'){\n    cmd += ' --strandedness ' + inputs.strandedness;\n  }\n  if (inputs.input_reads_2 != null){\n      cmd += ' --paired-end';\n  }\n  cmd += ' ' + inputs.bam.path + ' ./' + inputs.genomeDir.nameroot.split('.')[0] + '/' + inputs.genomeDir.nameroot.split('.')[0] + ' ' +  inputs.outFileNamePrefix + '.rsem';\n  return cmd\n} && gzip *results",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="genomeDir", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=16,
    memory=24000,
)
Samtools_Sort_V0_1_0 = CommandToolBuilder(
    tool="samtools_sort",
    base_command=["samtools"],
    inputs=[
        ToolInput(
            tag="chimeric_sam_out", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="unsorted_bam", input_type=File(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="chimeric_bam_out",
            output_type=File(),
            selector=WildcardSelector(
                wildcard=StringFormatter(
                    "{JANIS_CWL_TOKEN_1}.bam",
                    JANIS_CWL_TOKEN_1="<expr>inputs.chimeric_sam_out.nameroot</expr>",
                )
            ),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="sorted_bai",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.sorted.bai"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="sorted_bam",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.sorted.bam"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/samtools:1.9",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "sort {JANIS_CWL_TOKEN_3} -@ 16 -m 1G -O bam > {JANIS_CWL_TOKEN_2}.sorted.bam && samtools index -@ 16 {JANIS_CWL_TOKEN_2}.sorted.bam {JANIS_CWL_TOKEN_2}.sorted.bai && samtools view -bh -@ 16 {JANIS_CWL_TOKEN_4} -o {JANIS_CWL_TOKEN_1}.bam",
                JANIS_CWL_TOKEN_1="<expr>inputs.chimeric_sam_out.nameroot</expr>",
                JANIS_CWL_TOKEN_2="<expr>inputs.unsorted_bam.nameroot</expr>",
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="unsorted_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="chimeric_sam_out", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=16,
    memory=24000,
)
Arriba_Fusion_V0_1_0 = CommandToolBuilder(
    tool="arriba_fusion",
    base_command=["/arriba_v1.1.0/arriba"],
    inputs=[
        ToolInput(
            tag="arriba_strand_flag",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="chimeric_sam_out", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="genome_aligned_bai",
            input_type=File(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="genome_aligned_bam",
            input_type=File(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="gtf_anno", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="outFileNamePrefix",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference_fasta", input_type=File(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="arriba_fusions",
            output_type=File(),
            selector=WildcardSelector(
                wildcard=StringFormatter(
                    "{JANIS_CWL_TOKEN_1}.arriba.fusions.tsv",
                    JANIS_CWL_TOKEN_1=InputSelector(
                        input_to_select="outFileNamePrefix", type_hint=File()
                    ),
                )
            ),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="arriba_pdf",
            output_type=File(),
            selector=WildcardSelector(
                wildcard=StringFormatter(
                    "{JANIS_CWL_TOKEN_1}.arriba.fusions.pdf",
                    JANIS_CWL_TOKEN_1=InputSelector(
                        input_to_select="outFileNamePrefix", type_hint=File()
                    ),
                )
            ),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/arriba:1.1.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "-c {JANIS_CWL_TOKEN_2} -x {JANIS_CWL_TOKEN_4} -a {JANIS_CWL_TOKEN_5} -g {JANIS_CWL_TOKEN_1} -o {JANIS_CWL_TOKEN_3}.arriba.fusions.tsv -O {JANIS_CWL_TOKEN_3}.arriba.discarded_fusions.tsv -b /arriba_v1.1.0/database/blacklist_hg38_GRCh38_2018-11-04.tsv.gz -T -P ${\n  if(inputs.arriba_strand_flag == null){\n    return '-s auto';\n  }\n  else{\n    return '-s ' + inputs.arriba_strand_flag;\n  }\n} && /arriba_v1.1.0/draw_fusions.R --annotation={JANIS_CWL_TOKEN_1} --fusions={JANIS_CWL_TOKEN_3}.arriba.fusions.tsv --alignments={JANIS_CWL_TOKEN_4} --cytobands=/arriba_v1.1.0/database/cytobands_hg38_GRCh38_2018-02-23.tsv --proteinDomains=/arriba_v1.1.0/database/protein_domains_hg38_GRCh38_2018-03-06.gff3 --output={JANIS_CWL_TOKEN_3}.arriba.fusions.pdf",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="gtf_anno", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="chimeric_sam_out", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="outFileNamePrefix", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="genome_aligned_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="reference_fasta", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=8,
    memory=64000,
)
Rnaseqc_V0_1_0 = CommandToolBuilder(
    tool="rnaseqc",
    base_command=["rnaseqc"],
    inputs=[
        ToolInput(
            tag="Aligned_sorted_bam",
            input_type=File(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="collapsed_gtf", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_reads2",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="strand",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="Exon_count",
            output_type=File(),
            selector=WildcardSelector(wildcard="output/*.exon_reads.gct"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="Gene_TPM",
            output_type=File(),
            selector=WildcardSelector(wildcard="output/*.gene_tpm.gct"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="Gene_count",
            output_type=File(),
            selector=WildcardSelector(wildcard="output/*.gene_reads.gct"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="Metrics",
            output_type=File(),
            selector=WildcardSelector(wildcard="output/*.metrics.tsv"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="gcr.io/broad-cga-aarong-gtex/rnaseqc:latest",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "{JANIS_CWL_TOKEN_1} {JANIS_CWL_TOKEN_2} output/ ${\n  var cmd = '--legacy';\n  if (inputs.strand != null && inputs.strand != 'default'){\n    cmd += ' --stranded=' + inputs.strand;\n  }\n  if (inputs.input_reads2 == null) {\n    cmd += ' --unpaired';\n  }\n  return cmd;\n}",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="collapsed_gtf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="Aligned_sorted_bam", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=8,
    memory=10000,
)
Supplemental_Tar_Gz_V0_1_0 = CommandToolBuilder(
    tool="supplemental_tar_gz",
    base_command=["mkdir"],
    inputs=[
        ToolInput(
            tag="Exon_count", input_type=File(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(tag="Gene_TPM", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="Gene_count", input_type=File(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="outFileNamePrefix",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="RNASeQC_counts",
            output_type=File(),
            selector=WildcardSelector(
                wildcard=StringFormatter(
                    "{JANIS_CWL_TOKEN_1}.RNASeQC.counts.tar.gz",
                    JANIS_CWL_TOKEN_1=InputSelector(
                        input_to_select="outFileNamePrefix", type_hint=File()
                    ),
                )
            ),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/ubuntu:18.04",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "{JANIS_CWL_TOKEN_1}_RNASeQC_counts\ncp {JANIS_CWL_TOKEN_3} {JANIS_CWL_TOKEN_4} {JANIS_CWL_TOKEN_2} {JANIS_CWL_TOKEN_1}_RNASeQC_counts\ntar -czf {JANIS_CWL_TOKEN_1}.RNASeQC.counts.tar.gz {JANIS_CWL_TOKEN_1}_RNASeQC_counts",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="outFileNamePrefix", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="Exon_count", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="Gene_TPM", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="Gene_count", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=4,
    memory=1600,
)
Kfdrc_Annofuse_Wf = WorkflowBuilder(identifier="kfdrc_annofuse_wf",)

Kfdrc_Annofuse_Wf.input(
    "FusionGenome",
    File(),
    doc=InputDocumentation(doc="GRCh38_v27_CTAT_lib_Feb092018.plug-n-play.tar.gz"),
)

Kfdrc_Annofuse_Wf.input(
    "arriba_output_file",
    File(),
    doc=InputDocumentation(
        doc="Output from arriba, usually extension arriba.fusions.tsv"
    ),
)

Kfdrc_Annofuse_Wf.input(
    "col_num",
    Int(optional=True),
    doc=InputDocumentation(doc="column number in file of fusion name."),
)

Kfdrc_Annofuse_Wf.input(
    "genome_untar_path",
    String(optional=True),
    default="GRCh38_v27_CTAT_lib_Feb092018/ctat_genome_lib_build_dir",
    doc=InputDocumentation(
        doc="This is what the path will be when genome_tar is unpackaged"
    ),
)

Kfdrc_Annofuse_Wf.input(
    "output_basename",
    String(),
    doc=InputDocumentation(doc="String to use as basename for outputs"),
)

Kfdrc_Annofuse_Wf.input(
    "rsem_expr_file",
    File(),
    doc=InputDocumentation(doc="gzipped rsem gene expression file"),
)

Kfdrc_Annofuse_Wf.input(
    "sample_name",
    String(),
    doc=InputDocumentation(doc="Sample name used for file base name of all outputs"),
)

Kfdrc_Annofuse_Wf.input(
    "star_fusion_output_file",
    File(),
    doc=InputDocumentation(
        doc="Output from arriba, usually extension STAR.fusion_predictions.abridged.coding_effect.tsv"
    ),
)

Kfdrc_Annofuse_Wf.input(
    "format_arriba_output_caller", String(optional=True), default="arriba",
)

Kfdrc_Annofuse_Wf.input(
    "format_starfusion_output_caller", String(optional=True), default="starfusion",
)


Kfdrc_Annofuse_Wf.step(
    "format_arriba_output",
    Format_Fusion_File_V0_1_0(
        caller=Kfdrc_Annofuse_Wf.format_arriba_output_caller,
        input_caller_fusion_file=Kfdrc_Annofuse_Wf.arriba_output_file,
        sample_name=Kfdrc_Annofuse_Wf.sample_name,
    ),
)


Kfdrc_Annofuse_Wf.step(
    "format_starfusion_output",
    Format_Fusion_File_V0_1_0(
        caller=Kfdrc_Annofuse_Wf.format_starfusion_output_caller,
        input_caller_fusion_file=Kfdrc_Annofuse_Wf.star_fusion_output_file,
        sample_name=Kfdrc_Annofuse_Wf.sample_name,
    ),
)


Kfdrc_Annofuse_Wf.step(
    "annotate_arriba",
    Fusion_Annotator_V0_1_0(
        col_num=Kfdrc_Annofuse_Wf.col_num,
        genome_tar=Kfdrc_Annofuse_Wf.FusionGenome,
        genome_untar_path=Kfdrc_Annofuse_Wf.genome_untar_path,
        input_fusion_file=Kfdrc_Annofuse_Wf.format_arriba_output.formatted_fusion_tsv,
        output_basename=Kfdrc_Annofuse_Wf.output_basename,
    ),
)


Kfdrc_Annofuse_Wf.step(
    "annoFuse_filter",
    Annofuse_V0_1_0(
        arriba_formatted_fusions=Kfdrc_Annofuse_Wf.annotate_arriba.annotated_tsv,
        output_basename=Kfdrc_Annofuse_Wf.output_basename,
        rsem_expr_file=Kfdrc_Annofuse_Wf.rsem_expr_file,
        sample_name=Kfdrc_Annofuse_Wf.sample_name,
        starfusion_formatted_fusions=Kfdrc_Annofuse_Wf.format_starfusion_output.formatted_fusion_tsv,
    ),
)

Kfdrc_Annofuse_Wf.output(
    "annofuse_filtered_fusions_tsv",
    source=Kfdrc_Annofuse_Wf.annoFuse_filter.filtered_fusions_tsv,
    output_name=True,
)


Kfdrc_Rnaseq_Workflow = WorkflowBuilder(
    identifier="kfdrc_rnaseq_workflow",
    friendly_name="Kids First DRC RNAseq Workflow",
    doc="# Kids First RNA-Seq Workflow\n\nThis is the Kids First RNA-Seq pipeline, which includes fusion and expression detection.\n\n![data service logo](https://github.com/d3b-center/d3b-research-workflows/raw/master/doc/kfdrc-logo-sm.png)\n\n## Introduction\nThis pipeline utilizes cutadapt to trim adapters from the raw reads, if necessary, and passes the reads to STAR for alignment.\nThe alignment output is used by RSEM for gene expression abundance estimation.\nAdditionally, Kallisto is used for quantification, but uses pseudoalignments to estimate the gene abundance from the raw data.\nFusion calling is performed using Arriba and STAR-Fusion detection tools on the STAR alignment outputs.\nFiltering and prioritization of fusion calls is done by annoFuse.\nMetrics for the workflow are generated by RNA-SeQC.\n\nIf you would like to run this workflow using the cavatica public app, a basic primer on running public apps can be found [here](https://www.notion.so/d3b/Starting-From-Scratch-Running-Cavatica-af5ebb78c38a4f3190e32e67b4ce12bb).\nAlternatively, if you'd like to run it locally using `cwltool`, a basic primer on that can be found [here](https://www.notion.so/d3b/Starting-From-Scratch-Running-CWLtool-b8dbbde2dc7742e4aff290b0a878344d) and combined with app-specific info from the readme below.\nThis workflow is the current production workflow, equivalent to this [Cavatica public app](https://cavatica.sbgenomics.com/public/apps#cavatica/apps-publisher/kfdrc-rnaseq-workflow).\n\n### Cutadapt\n[Cutadapt v2.5](https://github.com/marcelm/cutadapt) Cut adapter sequences from raw reads if needed.\n### STAR\n[STAR v2.6.1d](https://doi.org/f4h523) RNA-Seq raw data alignment.\n### RSEM\n[RSEM v1.3.1](https://doi:10/cwg8n5) Calculation of gene expression.\n### Kallisto\n[Kallisto v0.43.1](https://doi:10.1038/nbt.3519) Raw data pseudoalignment to estimate gene abundance.\n### STAR-Fusion\n[STAR-Fusion v1.5.0](https://doi:10.1101/120295) Fusion detection for `STAR` chimeric reads.\n### Arriba\n[Arriba v1.1.0](https://github.com/suhrig/arriba/) Fusion caller that uses `STAR` aligned reads and chimeric reads output.\n### annoFuse\n[annoFuse 0.90.0](https://github.com/d3b-center/annoFuse/releases/tag/v0.90.0) Filter and prioritize fusion calls. For more information, please see the following [paper](https://www.biorxiv.org/content/10.1101/839738v3).\n### RNA-SeQC\n[RNA-SeQC v2.3.4](https://github.com/broadinstitute/rnaseqc) Generate metrics such as gene and transcript counts, sense/antisene mapping, mapping rates, etc\n\n## Usage\n\n### Runtime Estimates:\n- 8 GB single end FASTQ input: 66 Minutes & $2.00\n- 17 GB single end FASTQ input: 58 Minutes & $2.00\n\n### Inputs common:\n```yaml\ninputs:\n  sample_name: string\n  r1_adapter: {type: ['null', string]}\n  r2_adapter: {type: ['null', string]}\n  STAR_outSAMattrRGline: string\n  STARgenome: File\n  RSEMgenome: File\n  reference_fasta: File\n  gtf_anno: File\n  FusionGenome: File\n  runThread: int\n  RNAseQC_GTF: File\n  kallisto_idx: File\n  wf_strand_param: {type: [{type: enum, name: wf_strand_param, symbols: ['default', 'rf-stranded', 'fr-stranded']}], doc: 'use 'default' for unstranded/auto, 'rf-stranded' if read1 in the fastq read pairs is reverse complement to the transcript, 'fr-stranded' if read1 same sense as transcript'}\n  input_type: {type: [{type: enum, name: input_type, symbols: ['BAM', 'FASTQ']}], doc: 'Please select one option for input file type, BAM or FASTQ.'}\n```\n\n### Bam input-specific:\n```yaml\ninputs:\n  reads1: File\n```\n\n### PE Fastq input-specific:\n```yaml\ninputs:\n  reads1: File\n  reads2: File\n```\n\n### SE Fastq input-specific:\n```yaml\ninputs:\n  reads1: File\n```\n\n### Run:\n\n1) For fastq or bam input, run `kfdrc-rnaseq-wf` as this can accept both file types.\nFor PE fastq input, please enter the reads 1 file in `reads1` and the reads 2 file in `reads2`.\nFor SE fastq input, enter the single ends reads file in `reads1` and leave `reads2` empty as it is optional.\nFor bam input, please enter the reads file in `reads1` and leave `reads2` empty as it is optional.\n\n2) `r1_adapter` and `r2_adapter` are OPTIONAL.\nIf the input reads have already been trimmed, leave these as null and cutadapt step will simple pass on the fastq files to STAR.\nIf they do need trimming, supply the adapters and the cutadapt step will trim, and pass trimmed fastqs along.\n\n3) `wf_strand_param` is a workflow convenience param so that, if you input the following, the equivalent will propagate to the four tools that use that parameter:\n    - `default`: 'rsem_std': null, 'kallisto_std': null, 'rnaseqc_std': null, 'arriba_std': null. This means unstranded or auto in the case of arriba.\n    - `rf-stranded`: 'rsem_std': 0, 'kallisto_std': 'rf-stranded', 'rnaseqc_std': 'rf', 'arriba_std': 'reverse'.  This means if read1 in the input fastq/bam is reverse complement to the transcript that it maps to.\n    - `fr-stranded`: 'rsem_std': 1, 'kallisto_std': 'fr-stranded', 'rnaseqc_std': 'fr', 'arriba_std': 'yes'. This means if read1 in the input fastq/bam is the same sense (maps 5' to 3') to the transcript that it maps to.\n\n4) Suggested `STAR_outSAMattrRGline`, with **TABS SEPARATING THE TAGS**,  format is:\n\n    `ID:sample_name LB:aliquot_id   PL:platform SM:BSID` for example `ID:7316-242   LB:750189 PL:ILLUMINA SM:BS_W72364MN`\n5) Suggested inputs are:\n\n    - `FusionGenome`: [GRCh38_v27_CTAT_lib_Feb092018.plug-n-play.tar.gz](https://data.broadinstitute.org/Trinity/CTAT_RESOURCE_LIB/__genome_libs_StarFv1.3/GRCh38_v27_CTAT_lib_Feb092018.plug-n-play.tar.gz)\n    - `gtf_anno`: gencode.v27.primary_assembly.annotation.gtf, location: ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_27/gencode.v27.primary_assembly.annotation.gtf.gz, will need to unzip\n    - `RNAseQC_GTF`: gencode.v27.primary_assembly.RNAseQC.gtf, built using `gtf_anno` and following build instructions [here](https://github.com/broadinstitute/rnaseqc#usage)\n    - `RSEMgenome`: RSEM_GENCODE27.tar.gz, built using the `reference_fasta` and `gtf_anno`, following `GENCODE` instructions from [here](https://deweylab.github.io/RSEM/README.html), then creating a tar ball of the results.\n    - `STARgenome`: STAR_GENCODE27.tar.gz, created using the star_genomegenerate.cwl tool, using the `reference_fasta`, `gtf_anno`, and setting `sjdbOverhang` to 100\n    - `reference_fasta`: [GRCh38.primary_assembly.genome.fa](ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_27/GRCh38.primary_assembly.genome.fa.gz), will need to unzip\n    - `kallisto_idx`: gencode.v27.kallisto.index, built from gencode 27 trascript fasta: ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_27/gencode.v27.transcripts.fa.gz, following instructions from [here](https://pachterlab.github.io/kallisto/manual)\n\n### Outputs:\n```yaml\noutputs:\n  cutadapt_stats: {type: File, outputSource: cutadapt/cutadapt_stats} # only if adapter supplied\n  STAR_transcriptome_bam: {type: File, outputSource: star/transcriptome_bam_out}\n  STAR_sorted_genomic_bam: {type: File, outputSource: samtools_sort/sorted_bam}\n  STAR_sorted_genomic_bai: {type: File, outputSource: samtools_sort/sorted_bai}\n  STAR_chimeric_bam_out: {type: File, outputSource: samtools_sort/chimeric_bam_out}\n  STAR_chimeric_junctions: {type: File, outputSource: star_fusion/chimeric_junction_compressed}\n  STAR_gene_count: {type: File, outputSource: star/gene_counts}\n  STAR_junctions_out: {type: File, outputSource: star/junctions_out}\n  STAR_final_log: {type: File, outputSource: star/log_final_out}\n  STAR-Fusion_results: {type: File, outputSource: star_fusion/abridged_coding}\n  arriba_fusion_results: {type: File, outputSource: arriba_fusion/arriba_fusions}\n  arriba_fusion_viz: {type: File, outputSource: arriba_fusion/arriba_pdf}\n  RSEM_isoform: {type: File, outputSource: rsem/isoform_out}\n  RSEM_gene: {type: File, outputSource: rsem/gene_out}\n  RNASeQC_Metrics: {type: File, outputSource: rna_seqc/Metrics}\n  RNASeQC_counts: {type: File, outputSource: supplemental/RNASeQC_counts} # contains gene tpm, gene read, and exon counts\n  kallisto_Abundance: {type: File, outputSource: kallisto/abundance_out}\n  annofuse_filtered_fusions_tsv: { type: 'File?', outputSource: annoFuse_filter/filtered_fusions_tsv, doc: 'Filtered output of formatted and annotated Star Fusion and arriba results' }\n```\n",
)

Kfdrc_Rnaseq_Workflow.input(
    "FusionGenome",
    File(),
    doc=InputDocumentation(doc="GRCh38_v27_CTAT_lib_Feb092018.plug-n-play.tar.gz"),
)

Kfdrc_Rnaseq_Workflow.input(
    "RNAseQC_GTF",
    File(),
    doc=InputDocumentation(doc="gencode.v27.primary_assembly.RNAseQC.gtf"),
)

Kfdrc_Rnaseq_Workflow.input(
    "RSEMgenome", File(), doc=InputDocumentation(doc="RSEM_GENCODE27.tar.gz"),
)

Kfdrc_Rnaseq_Workflow.input(
    "STAR_outSAMattrRGline",
    String(),
    doc=InputDocumentation(
        doc="Suggested setting, with TABS SEPARATING THE TAGS, format is: ID:sample_name LB:aliquot_id PL:platform SM:BSID for example ID:7316-242 LB:750189 PL:ILLUMINA SM:BS_W72364MN"
    ),
)

Kfdrc_Rnaseq_Workflow.input(
    "STARgenome", File(), doc=InputDocumentation(doc="STAR_GENCODE27.tar.gz"),
)

Kfdrc_Rnaseq_Workflow.input(
    "annofuse_col_num",
    Int(optional=True),
    doc=InputDocumentation(doc="column number in file of fusion name."),
)

Kfdrc_Rnaseq_Workflow.input(
    "annofuse_genome_untar_path",
    String(optional=True),
    default="GRCh38_v27_CTAT_lib_Feb092018/ctat_genome_lib_build_dir",
    doc=InputDocumentation(
        doc="This is what the path will be when genome_tar is unpackaged"
    ),
)

Kfdrc_Rnaseq_Workflow.input(
    "gtf_anno",
    File(),
    doc=InputDocumentation(doc="gencode.v27.primary_assembly.annotation.gtf"),
)

Kfdrc_Rnaseq_Workflow.input(
    "input_type",
    String(),
    doc=InputDocumentation(
        doc="Please select one option for input file type, PEBAM (paired-end BAM), SEBAM (single-end BAM) or FASTQ."
    ),
)

Kfdrc_Rnaseq_Workflow.input(
    "kallisto_avg_frag_len",
    Int(optional=True),
    doc=InputDocumentation(
        doc="Optional input. Average fragment length for Kallisto only if single end input."
    ),
)

Kfdrc_Rnaseq_Workflow.input(
    "kallisto_idx", File(), doc=InputDocumentation(doc="gencode.v27.kallisto.index"),
)

Kfdrc_Rnaseq_Workflow.input(
    "kallisto_std_dev",
    Int(optional=True),
    doc=InputDocumentation(
        doc="Optional input. Standard Deviation of the average fragment length for Kallisto only needed if single end input."
    ),
)

Kfdrc_Rnaseq_Workflow.input(
    "output_basename",
    String(),
    doc=InputDocumentation(doc="String to use as basename for outputs"),
)

Kfdrc_Rnaseq_Workflow.input(
    "r1_adapter",
    String(optional=True),
    doc=InputDocumentation(
        doc="Optional input. If the input reads have already been trimmed, leave these as null. If they do need trimming, supply the adapters."
    ),
)

Kfdrc_Rnaseq_Workflow.input(
    "r2_adapter",
    String(optional=True),
    doc=InputDocumentation(
        doc="Optional input. If the input reads have already been trimmed, leave these as null. If they do need trimming, supply the adapters."
    ),
)

Kfdrc_Rnaseq_Workflow.input(
    "reads1",
    File(),
    doc=InputDocumentation(
        doc="For FASTQ input, please enter reads 1 here. For BAM input, please enter reads here."
    ),
)

Kfdrc_Rnaseq_Workflow.input(
    "reads2",
    File(optional=True),
    doc=InputDocumentation(
        doc="For FASTQ input, please enter reads 2 here. For BAM input, leave empty."
    ),
)

Kfdrc_Rnaseq_Workflow.input(
    "reference_fasta",
    File(),
    doc=InputDocumentation(doc="GRCh38.primary_assembly.genome.fa"),
)

Kfdrc_Rnaseq_Workflow.input(
    "runThread", Int(), doc=InputDocumentation(doc="Amount of threads for analysis."),
)

Kfdrc_Rnaseq_Workflow.input(
    "sample_name", String(), doc=InputDocumentation(doc="Sample ID of the input reads"),
)

Kfdrc_Rnaseq_Workflow.input(
    "wf_strand_param",
    String(),
    doc=InputDocumentation(
        doc="use 'default' for unstranded/auto, 'rf-stranded' if read1 in the fastq read pairs is reverse complement to the transcript, 'fr-stranded' if read1 same sense as transcript"
    ),
)


Kfdrc_Rnaseq_Workflow.step(
    "bam2fastq",
    Bam2Fastq_V0_1_0(
        SampleID=Kfdrc_Rnaseq_Workflow.output_basename,
        input_reads_1=Kfdrc_Rnaseq_Workflow.reads1,
        input_reads_2=Kfdrc_Rnaseq_Workflow.reads2,
        input_type=Kfdrc_Rnaseq_Workflow.input_type,
        runThreadN=Kfdrc_Rnaseq_Workflow.runThread,
    ),
)


Kfdrc_Rnaseq_Workflow.step(
    "cutadapt",
    Cutadapter_V0_1_0(
        r1_adapter=Kfdrc_Rnaseq_Workflow.r1_adapter,
        r2_adapter=Kfdrc_Rnaseq_Workflow.r2_adapter,
        readFilesIn1=Kfdrc_Rnaseq_Workflow.bam2fastq.fq1,
        readFilesIn2=Kfdrc_Rnaseq_Workflow.bam2fastq.fq2,
        sample_name=Kfdrc_Rnaseq_Workflow.output_basename,
    ),
)


Kfdrc_Rnaseq_Workflow.step(
    "star",
    Star_Alignreads_V0_1_0(
        genomeDir=Kfdrc_Rnaseq_Workflow.STARgenome,
        outFileNamePrefix=Kfdrc_Rnaseq_Workflow.output_basename,
        outSAMattrRGline=Kfdrc_Rnaseq_Workflow.STAR_outSAMattrRGline,
        readFilesIn1=Kfdrc_Rnaseq_Workflow.cutadapt.trimmedReadsR1,
        readFilesIn2=Kfdrc_Rnaseq_Workflow.cutadapt.trimmedReadsR2,
        runThreadN=Kfdrc_Rnaseq_Workflow.runThread,
    ),
)


Kfdrc_Rnaseq_Workflow.step(
    "star_fusion",
    Star_Fusion_V0_1_0(
        Chimeric_junction=Kfdrc_Rnaseq_Workflow.star.chimeric_junctions,
        SampleID=Kfdrc_Rnaseq_Workflow.output_basename,
        genome_tar=Kfdrc_Rnaseq_Workflow.FusionGenome,
    ),
)


Kfdrc_Rnaseq_Workflow.step(
    "strand_parse",
    Expression_Strand_Params_V0_1_0(
        wf_strand_param=Kfdrc_Rnaseq_Workflow.wf_strand_param,
    ),
)


Kfdrc_Rnaseq_Workflow.step(
    "kallisto",
    Kallisto_V0_1_0(
        SampleID=Kfdrc_Rnaseq_Workflow.output_basename,
        avg_frag_len=Kfdrc_Rnaseq_Workflow.kallisto_avg_frag_len,
        reads1=Kfdrc_Rnaseq_Workflow.cutadapt.trimmedReadsR1,
        reads2=Kfdrc_Rnaseq_Workflow.cutadapt.trimmedReadsR2,
        std_dev=Kfdrc_Rnaseq_Workflow.kallisto_std_dev,
        strand=Kfdrc_Rnaseq_Workflow.strand_parse.kallisto_std,
        transcript_idx=Kfdrc_Rnaseq_Workflow.kallisto_idx,
    ),
)


Kfdrc_Rnaseq_Workflow.step(
    "rsem",
    Rsem_Calculate_Expression_V0_1_0(
        bam=Kfdrc_Rnaseq_Workflow.star.transcriptome_bam_out,
        genomeDir=Kfdrc_Rnaseq_Workflow.RSEMgenome,
        input_reads_2=Kfdrc_Rnaseq_Workflow.cutadapt.trimmedReadsR2,
        outFileNamePrefix=Kfdrc_Rnaseq_Workflow.output_basename,
        strandedness=Kfdrc_Rnaseq_Workflow.strand_parse.rsem_std,
    ),
)


Kfdrc_Rnaseq_Workflow.step(
    "samtools_sort",
    Samtools_Sort_V0_1_0(
        chimeric_sam_out=Kfdrc_Rnaseq_Workflow.star.chimeric_sam_out,
        unsorted_bam=Kfdrc_Rnaseq_Workflow.star.genomic_bam_out,
    ),
)


Kfdrc_Rnaseq_Workflow.step(
    "arriba_fusion",
    Arriba_Fusion_V0_1_0(
        arriba_strand_flag=Kfdrc_Rnaseq_Workflow.strand_parse.arriba_std,
        chimeric_sam_out=Kfdrc_Rnaseq_Workflow.star.chimeric_sam_out,
        genome_aligned_bai=Kfdrc_Rnaseq_Workflow.samtools_sort.sorted_bai,
        genome_aligned_bam=Kfdrc_Rnaseq_Workflow.samtools_sort.sorted_bam,
        gtf_anno=Kfdrc_Rnaseq_Workflow.gtf_anno,
        outFileNamePrefix=Kfdrc_Rnaseq_Workflow.output_basename,
        reference_fasta=Kfdrc_Rnaseq_Workflow.reference_fasta,
    ),
)


Kfdrc_Rnaseq_Workflow.step(
    "rna_seqc",
    Rnaseqc_V0_1_0(
        Aligned_sorted_bam=Kfdrc_Rnaseq_Workflow.samtools_sort.sorted_bam,
        collapsed_gtf=Kfdrc_Rnaseq_Workflow.RNAseQC_GTF,
        input_reads2=Kfdrc_Rnaseq_Workflow.cutadapt.trimmedReadsR2,
        strand=Kfdrc_Rnaseq_Workflow.strand_parse.rnaseqc_std,
    ),
)


Kfdrc_Rnaseq_Workflow.step(
    "supplemental",
    Supplemental_Tar_Gz_V0_1_0(
        Exon_count=Kfdrc_Rnaseq_Workflow.rna_seqc.Exon_count,
        Gene_TPM=Kfdrc_Rnaseq_Workflow.rna_seqc.Gene_TPM,
        Gene_count=Kfdrc_Rnaseq_Workflow.rna_seqc.Gene_count,
        outFileNamePrefix=Kfdrc_Rnaseq_Workflow.output_basename,
    ),
)


Kfdrc_Rnaseq_Workflow.step(
    "annofuse",
    Kfdrc_Annofuse_Wf(
        FusionGenome=Kfdrc_Rnaseq_Workflow.FusionGenome,
        arriba_output_file=Kfdrc_Rnaseq_Workflow.arriba_fusion.arriba_fusions,
        col_num=Kfdrc_Rnaseq_Workflow.annofuse_col_num,
        genome_untar_path=Kfdrc_Rnaseq_Workflow.annofuse_genome_untar_path,
        output_basename=Kfdrc_Rnaseq_Workflow.output_basename,
        rsem_expr_file=Kfdrc_Rnaseq_Workflow.rsem.gene_out,
        sample_name=Kfdrc_Rnaseq_Workflow.sample_name,
        star_fusion_output_file=Kfdrc_Rnaseq_Workflow.star_fusion.abridged_coding,
    ),
)

Kfdrc_Rnaseq_Workflow.output(
    "RNASeQC_Metrics", source=Kfdrc_Rnaseq_Workflow.rna_seqc.Metrics, output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "RNASeQC_counts",
    source=Kfdrc_Rnaseq_Workflow.supplemental.RNASeQC_counts,
    output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "RSEM_gene", source=Kfdrc_Rnaseq_Workflow.rsem.gene_out, output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "RSEM_isoform", source=Kfdrc_Rnaseq_Workflow.rsem.isoform_out, output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "STAR_Fusion_results",
    source=Kfdrc_Rnaseq_Workflow.star_fusion.abridged_coding,
    output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "STAR_chimeric_bam_out",
    source=Kfdrc_Rnaseq_Workflow.samtools_sort.chimeric_bam_out,
    output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "STAR_chimeric_junctions",
    source=Kfdrc_Rnaseq_Workflow.star_fusion.chimeric_junction_compressed,
    output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "STAR_final_log", source=Kfdrc_Rnaseq_Workflow.star.log_final_out, output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "STAR_gene_count", source=Kfdrc_Rnaseq_Workflow.star.gene_counts, output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "STAR_junctions_out",
    source=Kfdrc_Rnaseq_Workflow.star.junctions_out,
    output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "STAR_sorted_genomic_bai",
    source=Kfdrc_Rnaseq_Workflow.samtools_sort.sorted_bai,
    output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "STAR_sorted_genomic_bam",
    source=Kfdrc_Rnaseq_Workflow.samtools_sort.sorted_bam,
    output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "STAR_transcriptome_bam",
    source=Kfdrc_Rnaseq_Workflow.star.transcriptome_bam_out,
    output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "annofuse_filtered_fusions_tsv",
    source=Kfdrc_Rnaseq_Workflow.annofuse.annofuse_filtered_fusions_tsv,
    output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "arriba_fusion_results",
    source=Kfdrc_Rnaseq_Workflow.arriba_fusion.arriba_fusions,
    output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "arriba_fusion_viz",
    source=Kfdrc_Rnaseq_Workflow.arriba_fusion.arriba_pdf,
    output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "cutadapt_stats",
    source=Kfdrc_Rnaseq_Workflow.cutadapt.cutadapt_stats,
    output_name=True,
)

Kfdrc_Rnaseq_Workflow.output(
    "kallisto_Abundance",
    source=Kfdrc_Rnaseq_Workflow.kallisto.abundance_out,
    output_name=True,
)


if __name__ == "__main__":
    # or "cwl"
    Kfdrc_Rnaseq_Workflow().translate("wdl")
