from datetime import datetime
from typing import List, Optional, Dict, Any

from janis_core import *
from janis_bioinformatics.data_types.cram import CramCrai
from janis_bioinformatics.data_types.fasta import FastaFai
from janis_bioinformatics.data_types.vcf import VcfTabix
from janis_core.types.common_data_types import (
    File,
    Float,
    Boolean,
    String,
    Array,
    Int,
    GenericFileWithSecondaries,
)

Lancet_V0_1_0 = CommandToolBuilder(
    tool="lancet",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(tag="bed", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="input_normal_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_tumor_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="padding", input_type=Int(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="ram",
            input_type=Int(optional=True),
            default=12,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference",
            input_type=GenericFileWithSecondaries(secondaries=["^.dict", ".fai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="window", input_type=Int(), doc=InputDocumentation(doc=None)),
    ],
    outputs=[
        ToolOutput(
            tag="lancet_vcf",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.vcf"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/lancet:1.0.7",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "set -eo pipefail\n/lancet-1.0.7/lancet --tumor {JANIS_CWL_TOKEN_5} --normal {JANIS_CWL_TOKEN_3} --ref {JANIS_CWL_TOKEN_4} --bed {JANIS_CWL_TOKEN_2} --num-threads 6 --window-size {JANIS_CWL_TOKEN_1} --padding {JANIS_CWL_TOKEN_6} --max-indel-len 50 > {JANIS_CWL_TOKEN_7}.{JANIS_CWL_TOKEN_8}.vcf || (echo 'active region filter failed, trying without' && /lancet-1.0.7/lancet --tumor {JANIS_CWL_TOKEN_5} --normal {JANIS_CWL_TOKEN_3} --ref {JANIS_CWL_TOKEN_4} --bed {JANIS_CWL_TOKEN_2} --num-threads 6 --window-size {JANIS_CWL_TOKEN_1} --active-region-off --padding {JANIS_CWL_TOKEN_6} --max-indel-len 50 > {JANIS_CWL_TOKEN_7}.{JANIS_CWL_TOKEN_8}.vcf)",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="window", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="bed", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="input_normal_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="input_tumor_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_6=InputSelector(
                    input_to_select="padding", type_hint=File()
                ),
                JANIS_CWL_TOKEN_7="<expr>inputs.input_tumor_bam.nameroot</expr>",
                JANIS_CWL_TOKEN_8="<expr>inputs.bed.nameroot</expr>",
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=6,
    memory="<expr>inputs.ram * 1000</expr>",
)
Gatk4_Mergevcfs_V0_1_0 = CommandToolBuilder(
    tool="gatk4_mergevcfs",
    base_command=["/gatk", "MergeVcfs"],
    inputs=[
        ToolInput(
            tag="input_vcfs",
            input_type=Array(t=VcfTabix()),
            position=1,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference_dict", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="silent_flag",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="tool_name",
            input_type=String(),
            doc=InputDocumentation(doc=None, quality=InputQualityType.configuration),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="merged_vcf",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="*.merged.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.1.1.0",
    version="v0.1.0",
    friendly_name="GATK Merge VCF",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "--java-options '-Xmx2000m' --TMP_DIR=./TMP --CREATE_INDEX=true --SEQUENCE_DICTIONARY={JANIS_CWL_TOKEN_1} ${\n  var cmd = '--OUTPUT=' + inputs.output_basename + '.' + inputs.tool_name + '.merged.vcf.gz '\n  if (typeof inputs.silent_flag !== 'undefined' && inputs.silent_flag == 1){\n    cmd += '--VALIDATION_STRINGENCY SILENT'\n  }\n  return cmd\n}",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="reference_dict", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=2,
    memory=4000,
    doc="Merge input vcfs",
)
Gatk4_Selectvariants_V0_1_0 = CommandToolBuilder(
    tool="gatk4_selectvariants",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(
            tag="input_vcf", input_type=VcfTabix(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="mode",
            input_type=String(optional=True),
            default="gatk",
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="tool_name",
            input_type=String(),
            doc=InputDocumentation(doc=None, quality=InputQualityType.configuration),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="pass_vcf",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="*.PASS.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.1.1.0",
    version="v0.1.0",
    friendly_name="GATK Select PASS",
    arguments=[
        ToolArgument(
            value="set -eo pipefail\n${\n  var run_mode = inputs.mode;\n  if (run_mode == 'grep' || run_mode == 'gatk'){\n    var in_vcf = inputs.input_vcf.path;\n    var out_vcf = inputs.output_basename + '.' + inputs.tool_name + '.PASS.vcf.gz';\n    var cmd = '/gatk SelectVariants --java-options '-Xmx8000m' -V ' + in_vcf +  ' -O ' + out_vcf + ' --exclude-filtered TRUE';\n    if (run_mode == 'grep'){\n      cmd = 'zcat ' + in_vcf + ' | grep -E '^#|PASS' | bgzip > ' + out_vcf + '; tabix ' + out_vcf;\n    }\n    return cmd;\n  }\n  else{\n    throw new Error(run_mode + ' is a not a valid mode.  Choices are gatk or grep.');\n  }\n}",
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=4,
    memory=8000,
)
Kfdrc_Vep_Somatic_Annotate_Maf_V0_1_0 = CommandToolBuilder(
    tool="kfdrc_vep_somatic_annotate_maf",
    base_command=["tar", "-xzf"],
    inputs=[
        ToolInput(tag="cache", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="cache_version",
            input_type=Int(optional=True),
            default=93,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_vcf", input_type=VcfTabix(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="normal_id", input_type=String(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="ref_build",
            input_type=String(optional=True),
            default="GRCh38",
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference", input_type=FastaFai(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="tool_name",
            input_type=String(),
            doc=InputDocumentation(doc=None, quality=InputQualityType.configuration),
        ),
        ToolInput(
            tag="tumor_id", input_type=String(), doc=InputDocumentation(doc=None)
        ),
    ],
    outputs=[
        ToolOutput(
            tag="output_maf",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.maf"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="output_tbi",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.vcf.gz.tbi"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="output_vcf",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="warn_txt",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.txt"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/vep:r93_v2",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "{JANIS_CWL_TOKEN_8} && gunzip -c {JANIS_CWL_TOKEN_5} > input_file.vcf && perl /vcf2maf/vcf2maf.pl --input-vcf input_file.vcf --output-maf {JANIS_CWL_TOKEN_9}.{JANIS_CWL_TOKEN_2}.vep.maf --filter-vcf 0 --vep-path /ensembl-vep/ --vep-data $PWD --vep-forks 16 --ncbi-build {JANIS_CWL_TOKEN_7} --cache-version {JANIS_CWL_TOKEN_6} --ref-fasta {JANIS_CWL_TOKEN_3} --tumor-id {JANIS_CWL_TOKEN_4} --normal-id {JANIS_CWL_TOKEN_1} && mv input_file.vep.vcf {JANIS_CWL_TOKEN_9}.{JANIS_CWL_TOKEN_2}.PASS.vep.vcf && /ensembl-vep/htslib/bgzip {JANIS_CWL_TOKEN_9}.{JANIS_CWL_TOKEN_2}.PASS.vep.vcf && /ensembl-vep/htslib/tabix {JANIS_CWL_TOKEN_9}.{JANIS_CWL_TOKEN_2}.PASS.vep.vcf.gz",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="normal_id", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="tool_name", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="tumor_id", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="input_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_6=InputSelector(
                    input_to_select="cache_version", type_hint=File()
                ),
                JANIS_CWL_TOKEN_7=InputSelector(
                    input_to_select="ref_build", type_hint=File()
                ),
                JANIS_CWL_TOKEN_8=InputSelector(
                    input_to_select="cache", type_hint=File()
                ),
                JANIS_CWL_TOKEN_9=InputSelector(
                    input_to_select="output_basename", type_hint=File()
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
Bcftools_Filter_Vcf_V0_1_0 = CommandToolBuilder(
    tool="bcftools_filter_vcf",
    base_command=[],
    inputs=[
        ToolInput(
            tag="exclude_expression",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="include_expression",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="input_vcf", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="output_basename",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="filtered_vcf",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="*.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/bvcftools:latest",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="${\n  var out_base = inputs.output_basename;\n  if (out_base == null){\n    out_base = inputs.input_vcf.nameroot + '.bcf_filtered'\n  }\n  var cmd = 'bcftools view ';\n  if (inputs.include_expression != null){\n      cmd += '--include '' + inputs.include_expression + '' ' + inputs.input_vcf.path;\n      if (inputs.exclude_expression != null){\n          cmd += ' | bcftools view --exclude '' + inputs.exclude_expression + '' -O z > ' + out_base + '.vcf.gz;';\n      } else {\n          cmd += ' -O z > ' + out_base + '.vcf.gz;';\n      }\n  } else if (inputs.include_expression == null && inputs.exclude_expression != null){\n      cmd += '--exclude '' + inputs.exclude_expression + '' ' + inputs.input_vcf.path + ' -O z > ' + out_base + '.vcf.gz;';\n  } else if (inputs.include_expression == null && inputs.exclude_expression == null){\n      cmd = 'cp ' + inputs.input_vcf.path + ' ./' + out_base + '.vcf.gz;';\n  }\n  cmd += 'tabix ' + out_base + '.vcf.gz;'\n  return cmd;\n}",
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=1,
    memory=1000,
    doc="More generic tool to take in an include expression and optionally an exclude expresssion to filter a vcf",
)
Cnvkit_Export_Theta2_V0_1_0 = CommandToolBuilder(
    tool="cnvkit_export_theta2",
    base_command=["cnvkit.py", "export", "theta"],
    inputs=[
        ToolInput(
            tag="normal_ID", input_type=String(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="paired_vcf", input_type=File(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="reference_cnn", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="tumor_ID", input_type=String(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(tag="tumor_cns", input_type=File(), doc=InputDocumentation(doc=None)),
    ],
    outputs=[
        ToolOutput(
            tag="call_interval_count",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.call.interval_count"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="call_normal_snp",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.call.normal.snp_formatted.txt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="call_tumor_snp",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.call.tumor.snp_formatted.txt"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="images.sbgenomics.com/milos_nikolic/cnvkit:0.9.3",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "-r {JANIS_CWL_TOKEN_3} -v {JANIS_CWL_TOKEN_1} -i {JANIS_CWL_TOKEN_4} -n {JANIS_CWL_TOKEN_5} {JANIS_CWL_TOKEN_2}",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="paired_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="tumor_cns", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="reference_cnn", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="tumor_ID", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="normal_ID", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=4,
    memory=16000,
)
Theta2_V0_1_0 = CommandToolBuilder(
    tool="theta2",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(
            tag="interval_count", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="min_frac",
            input_type=Float(optional=True),
            default=0.05,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="normal_snp", input_type=File(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="tumor_snp", input_type=File(), doc=InputDocumentation(doc=None)),
    ],
    outputs=[
        ToolOutput(
            tag="best_results",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.BEST.results"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="n2_graph",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.n2.graph.pdf"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="n2_results",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.n2.results"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="n2_withBounds",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.n2.withBounds"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="n3_graph",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.n3.graph.pdf"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="n3_results",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.n3.results"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="n3_withBounds",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.n3.withBounds"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/theta2:0.7",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "set -eo pipefail\n/THetA/bin/RunTHetA --TUMOR_FILE {JANIS_CWL_TOKEN_1} --NORMAL_FILE {JANIS_CWL_TOKEN_5} --OUTPUT_PREFIX {JANIS_CWL_TOKEN_3} --NUM_PROCESSES 8 --MIN_FRAC {JANIS_CWL_TOKEN_2} {JANIS_CWL_TOKEN_4} || (echo 'Theta2 failed, likely due to insufficient copy number variation to calculate purity, or due to an input error, skipping >&2'; exit 0;)",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="tumor_snp", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="min_frac", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="interval_count", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="normal_snp", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=8,
    memory=32000,
)
Cnvkit_Import_Theta2_V0_1_0 = CommandToolBuilder(
    tool="cnvkit_import_theta2",
    base_command=[],
    inputs=[
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="theta2_best_results",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="theta2_n2_results",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="tumor_cns", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="tumor_sample_name",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="theta2_adjusted_cns",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.theta2.total.cns"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="theta2_adjusted_seg",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.theta2.total.seg"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="theta2_subclone_cns",
            output_type=Array(t=File(), optional=True),
            selector=WildcardSelector(wildcard="*.theta2.subclone*.cns"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="theta2_subclone_seg",
            output_type=Array(t=File(), optional=True),
            selector=WildcardSelector(wildcard="*.theta2.subclone*.seg"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="images.sbgenomics.com/milos_nikolic/cnvkit:0.9.3",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "${\n  if (inputs.theta2_n2_results == null){\n    return 'echo Theta 2 input is null, skipping purity adjustment >&2; exit 0;'\n  }\n  else{\n    return 'echo running Theta 2;';\n  }\n}\ncnvkit.py import-theta {JANIS_CWL_TOKEN_1} ${if (inputs.theta2_n2_results != null) {return inputs.theta2_n2_results.path;}} -d ./\nmv ${return inputs.output_basename}.call-1.cns ${return inputs.output_basename}.theta2.total.cns\nln -s ${return inputs.output_basename}.theta2.total.cns ${return inputs.tumor_sample_name}.cns\ncnvkit.py export seg ${return inputs.tumor_sample_name}.cns -o ${return inputs.output_basename}.theta2.total.seg\nrm ${return inputs.tumor_sample_name}.cns\ncnvkit.py import-theta {JANIS_CWL_TOKEN_1} ${if (inputs.theta2_best_results != null) {return inputs.theta2_best_results.path;}} -d ./\nmv ${return inputs.output_basename}.call-1.cns ${return inputs.output_basename}.theta2.subclone1.cns\nln -s ${return inputs.output_basename}.theta2.subclone1.cns ${return inputs.tumor_sample_name}.cns\ncnvkit.py export seg ${return inputs.tumor_sample_name}.cns -o ${return inputs.output_basename}.theta2.subclone1.seg\nrm ${return inputs.tumor_sample_name}.cns\nSC2=${return inputs.output_basename}.call-2.cns;\nif [ -f '$SC2' ]; then\n    mv ${return inputs.output_basename}.call-2.cns ${return inputs.output_basename}.theta2.subclone2.cns;\n    ln -s ${return inputs.output_basename}.theta2.subclone2.cns ${return inputs.tumor_sample_name}.cns;\n    cnvkit.py export seg ${return inputs.tumor_sample_name}.cns -o ${return inputs.output_basename}.theta2.subclone2.seg;\n    rm ${return inputs.tumor_sample_name}.cns;\nelse\n  echo 'second subclone file not found. Skipping!' >&2;\nfi",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="tumor_cns", type_hint=File()
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
Vardictjava_V0_1_0 = CommandToolBuilder(
    tool="vardictjava",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(tag="bed", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="cpus",
            input_type=Int(optional=True),
            default=9,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_normal_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_normal_name",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_tumor_bam",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_tumor_name",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="min_vaf",
            input_type=Float(optional=True),
            default=0.05,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="padding",
            input_type=Int(optional=True),
            default=150,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="ram",
            input_type=Int(optional=True),
            default=18,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference",
            input_type=GenericFileWithSecondaries(secondaries=["^.dict", ".fai"]),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="vardict_vcf",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="*.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/vardict:1.7.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "set -eo pipefail; ${\n  var ram = Math.floor(inputs.ram/1.074 - 1);\n  var exp_cmd = 'export VAR_DICT_OPTS=''-Xms768m' '-Xmx' + ram + 'g'';';\n  return exp_cmd;\n} /VarDict-1.7.0/bin/VarDict -G {JANIS_CWL_TOKEN_8} -f {JANIS_CWL_TOKEN_3} -th {JANIS_CWL_TOKEN_1} --nosv -N {JANIS_CWL_TOKEN_11} -b '{JANIS_CWL_TOKEN_9}|{JANIS_CWL_TOKEN_6}' -z -c 1 -S 2 -E 3 -g 4 -F 0x700 -Q 10 -V 0.01 -x {JANIS_CWL_TOKEN_10} {JANIS_CWL_TOKEN_4} > vardict_results.txt && cat vardict_results.txt | /VarDict-1.7.0/bin/testsomatic.R > vardict_r_test_results.txt && cat vardict_r_test_results.txt | /VarDict-1.7.0/bin/var2vcf_paired.pl -N '{JANIS_CWL_TOKEN_5}|{JANIS_CWL_TOKEN_2}' -f {JANIS_CWL_TOKEN_3} -M -m 4.25 > {JANIS_CWL_TOKEN_11}.result.vcf && cat {JANIS_CWL_TOKEN_11}.result.vcf | perl -e 'while(<>){if ($_ =~ /^#/){print $_;} else{@a = split /\t/,$_; if($a[3] =~ /[KMRYSWBVHDXkmryswbvhdx]/){$a[3] = 'N';} if($a[4] =~ /[KMRYSWBVHDXkmryswbvhdx]/){$a[4] = 'N';} if($a[3] ne $a[4]){print join('\t', @a);}}}' > {JANIS_CWL_TOKEN_11}.canonical_base_only.{JANIS_CWL_TOKEN_7}.vcf && bgzip  {JANIS_CWL_TOKEN_11}.canonical_base_only.{JANIS_CWL_TOKEN_7}.vcf && tabix  {JANIS_CWL_TOKEN_11}.canonical_base_only.{JANIS_CWL_TOKEN_7}.vcf.gz",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="cpus", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="input_normal_name", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="min_vaf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="bed", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="input_tumor_name", type_hint=File()
                ),
                JANIS_CWL_TOKEN_6=InputSelector(
                    input_to_select="input_normal_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_7="<expr>inputs.bed.nameroot</expr>",
                JANIS_CWL_TOKEN_8=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_9=InputSelector(
                    input_to_select="input_tumor_bam", type_hint=File()
                ),
                JANIS_CWL_TOKEN_10=InputSelector(
                    input_to_select="padding", type_hint=File()
                ),
                JANIS_CWL_TOKEN_11=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=InputSelector(input_to_select="cpus", type_hint=File()),
    memory="<expr>inputs.ram * 1000</expr>",
)
Bcbio_Vardict_Fp_Somatic_Filter_V0_1_0 = CommandToolBuilder(
    tool="bcbio_vardict_fp_somatic_filter",
    base_command=["python"],
    inputs=[
        ToolInput(tag="input_vcf", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="filtered_vcf",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="*.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/bcbio_vardict_filter",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "/bcbio_vardict_filter.py {JANIS_CWL_TOKEN_1} | grep -E '^#|STATUS=StrongSomatic' > {JANIS_CWL_TOKEN_2}.bcbio_vardict_fp_somatic_filter.vcf\nbgzip {JANIS_CWL_TOKEN_2}.bcbio_vardict_fp_somatic_filter.vcf && tabix {JANIS_CWL_TOKEN_2}.bcbio_vardict_fp_somatic_filter.vcf.gz",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="input_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=4,
    memory=8000,
)
Gatk4_Getpileupsummary_V0_1_0 = CommandToolBuilder(
    tool="gatk4_getpileupsummary",
    base_command=["/gatk", "GetPileupSummaries"],
    inputs=[
        ToolInput(
            tag="aligned_reads",
            input_type=CramCrai(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="exac_common_vcf",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="interval_list", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="max_memory",
            input_type=Int(optional=True),
            default=2,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="reference", input_type=File(), doc=InputDocumentation(doc=None)),
    ],
    outputs=[
        ToolOutput(
            tag="pileup_table",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.pileupsummary.table"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.1.1.0",
    version="v0.1.0",
    friendly_name="GATK Pileup",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "--java-options '-Xmx${return Math.floor(inputs.max_memory*1000/1.074-1)}m' -I {JANIS_CWL_TOKEN_4} -V {JANIS_CWL_TOKEN_3} -L {JANIS_CWL_TOKEN_1} -R {JANIS_CWL_TOKEN_5} -O {JANIS_CWL_TOKEN_2}.pileupsummary.table",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="interval_list", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2="<expr>inputs.aligned_reads.nameroot</expr>",
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="exac_common_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="aligned_reads", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=2,
    memory="<expr>inputs.max_memory * 1000</expr>",
)
Gatk4_Learn_Oritentation_Bias_V0_1_0 = CommandToolBuilder(
    tool="gatk4_learn_oritentation_bias",
    base_command=["/gatk", "LearnReadOrientationModel"],
    inputs=[
        ToolInput(
            tag="input_tgz",
            input_type=Array(t=File()),
            position=1,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="max_memory",
            input_type=Int(optional=True),
            default=4,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="tool_name",
            input_type=String(),
            doc=InputDocumentation(doc=None, quality=InputQualityType.configuration),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="f1r2_bias",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.f1r2_bias.tar.gz"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.1.1.0",
    version="v0.1.0",
    friendly_name="GATK Learn Bias",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "--java-options '-Xmx${return Math.floor(inputs.max_memory*1000/1.074-1)}m' -O {JANIS_CWL_TOKEN_1}.{JANIS_CWL_TOKEN_2}.f1r2_bias.tar.gz ",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="tool_name", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=2,
    memory="<expr>inputs.max_memory * 1000</expr>",
)
Gatk4_Mergepileup_V0_1_0 = CommandToolBuilder(
    tool="gatk4_mergepileup",
    base_command=["/gatk", "GatherPileupSummaries"],
    inputs=[
        ToolInput(
            tag="input_tables",
            input_type=Array(t=File()),
            position=1,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference_dict", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="tool_name",
            input_type=String(),
            doc=InputDocumentation(doc=None, quality=InputQualityType.configuration),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="merged_table",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.merged.pileup.table"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.1.1.0",
    version="v0.1.0",
    friendly_name="GATK Merge Pileups",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "--java-options '-Xmx3000m' --sequence-dictionary {JANIS_CWL_TOKEN_1} -O {JANIS_CWL_TOKEN_2}.{JANIS_CWL_TOKEN_3}.merged.pileup.table ",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="reference_dict", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="tool_name", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=2,
    memory=4000,
)
Gatk4_Calulcate_Contamination_V0_1_0 = CommandToolBuilder(
    tool="gatk4_calulcate_contamination",
    base_command=["/gatk", "CalculateContamination"],
    inputs=[
        ToolInput(
            tag="normal_pileup", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="tumor_pileup", input_type=File(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="contamination_table",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.contamination.table"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="segmentation_table",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.segmentation.table"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.1.1.0",
    version="v0.1.0",
    friendly_name="GATK Calculate Contamination",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "--java-options '-Xmx4000m' -I {JANIS_CWL_TOKEN_3} --matched-normal {JANIS_CWL_TOKEN_1} -O {JANIS_CWL_TOKEN_2}.contamination.table --tumor-segmentation {JANIS_CWL_TOKEN_2}.segmentation.table",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="normal_pileup", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="tumor_pileup", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=2,
    memory=4000,
)
Gatk4_Mutect2_V0_1_0 = CommandToolBuilder(
    tool="gatk4_Mutect2",
    base_command=["/gatk", "Mutect2"],
    inputs=[
        ToolInput(
            tag="af_only_gnomad_vcf",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="exome_flag",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_normal_aligned",
            input_type=GenericFileWithSecondaries(
                secondaries=[
                    "${\n  var dpath = self.location.replace(self.basename, '')\n  if(self.nameext == '.bam'){\n    return {'location': dpath+self.nameroot+'.bai', 'class': 'File'}\n  }\n  else{\n    return {'location': dpath+self.basename+'.crai', 'class': 'File'}\n  }\n}\n"
                ]
            ),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_normal_name",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_tumor_aligned",
            input_type=GenericFileWithSecondaries(
                secondaries=[
                    "${\n  var dpath = self.location.replace(self.basename, '')\n  if(self.nameext == '.bam'){\n    return {'location': dpath+self.nameroot+'.bai', 'class': 'File'}\n  }\n  else{\n    return {'location': dpath+self.basename+'.crai', 'class': 'File'}\n  }\n}\n"
                ]
            ),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_tumor_name",
            input_type=String(),
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
            tag="f1r2_counts",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.f1r2_counts.tar.gz"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="mutect2_vcf",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="*.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="mutect_stats",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.stats"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.1.1.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "--java-options '-Xmx6000m' -R {JANIS_CWL_TOKEN_7} -I {JANIS_CWL_TOKEN_4} -I {JANIS_CWL_TOKEN_6} -tumor {JANIS_CWL_TOKEN_9} -normal {JANIS_CWL_TOKEN_2} --disable-read-filter MateOnSameContigOrNoMappedMateReadFilter -L {JANIS_CWL_TOKEN_1} --germline-resource {JANIS_CWL_TOKEN_3} --f1r2-tar-gz {JANIS_CWL_TOKEN_5}.{JANIS_CWL_TOKEN_8}.f1r2_counts.tar.gz ${\n  var arg = '-O ' + inputs.input_tumor_aligned.nameroot + '.' + inputs.interval_list.nameroot + '.Mutect2.vcf.gz'\n  if (inputs.exome_flag == 'Y'){\n    arg += ' --disable-adaptive-pruning'\n  }\n  return arg\n}",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="interval_list", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="input_normal_name", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="af_only_gnomad_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="input_tumor_aligned", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5="<expr>inputs.input_tumor_aligned.nameroot</expr>",
                JANIS_CWL_TOKEN_6=InputSelector(
                    input_to_select="input_normal_aligned", type_hint=File()
                ),
                JANIS_CWL_TOKEN_7=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_8="<expr>inputs.interval_list.nameroot</expr>",
                JANIS_CWL_TOKEN_9=InputSelector(
                    input_to_select="input_tumor_name", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=3,
    memory=6000,
)
Mutect2_Support = WorkflowBuilder(identifier="mutect2_support",)

Mutect2_Support.input(
    "exac_common_vcf", VcfTabix(),
)

Mutect2_Support.input(
    "f1r2_counts",
    Array(t=File()),
    doc=InputDocumentation(doc="orientation counts from mutect2 outputs"),
)

Mutect2_Support.input(
    "getpileup_memory", Int(optional=True),
)

Mutect2_Support.input(
    "indexed_reference_fasta",
    GenericFileWithSecondaries(secondaries=[".fai", "^.dict"]),
)

Mutect2_Support.input(
    "input_normal_aligned",
    GenericFileWithSecondaries(
        secondaries=[
            "${\n  var dpath = self.location.replace(self.basename, '')\n  if(self.nameext == '.bam'){\n    return {'location': dpath+self.nameroot+'.bai', 'class': 'File'}\n  }\n  else{\n    return {'location': dpath+self.basename+'.crai', 'class': 'File'}\n  }\n}\n"
        ]
    ),
    doc=InputDocumentation(doc="normal BAM or CRAM"),
)

Mutect2_Support.input(
    "input_tumor_aligned",
    GenericFileWithSecondaries(
        secondaries=[
            "${\n  var dpath = self.location.replace(self.basename, '')\n  if(self.nameext == '.bam'){\n    return {'location': dpath+self.nameroot+'.bai', 'class': 'File'}\n  }\n  else{\n    return {'location': dpath+self.basename+'.crai', 'class': 'File'}\n  }\n}\n"
        ]
    ),
    doc=InputDocumentation(doc="tumor BAM or CRAM"),
)

Mutect2_Support.input(
    "learnorientation_memory", Int(optional=True),
)

Mutect2_Support.input(
    "output_basename", String(),
)

Mutect2_Support.input(
    "reference_dict", File(),
)

Mutect2_Support.input(
    "wgs_calling_interval_list", Array(t=File()),
)

Mutect2_Support.input(
    "gatk_learn_orientation_bias_tool_name", String(optional=True), default="mutect2",
)

Mutect2_Support.input(
    "gatk_gather_normal_pileup_summaries_tool_name",
    String(optional=True),
    default="mutect2",
)

Mutect2_Support.input(
    "gatk_gather_tumor_pileup_summaries_tool_name",
    String(optional=True),
    default="mutect2",
)


Mutect2_Support.step(
    "gatk_get_normal_pileup_summaries",
    Gatk4_Getpileupsummary_V0_1_0(
        aligned_reads=Mutect2_Support.input_normal_aligned,
        exac_common_vcf=Mutect2_Support.exac_common_vcf,
        interval_list=Mutect2_Support.wgs_calling_interval_list,
        max_memory=Mutect2_Support.getpileup_memory,
        reference=Mutect2_Support.indexed_reference_fasta,
    ),
)


Mutect2_Support.step(
    "gatk_get_tumor_pileup_summaries",
    Gatk4_Getpileupsummary_V0_1_0(
        aligned_reads=Mutect2_Support.input_tumor_aligned,
        exac_common_vcf=Mutect2_Support.exac_common_vcf,
        interval_list=Mutect2_Support.wgs_calling_interval_list,
        max_memory=Mutect2_Support.getpileup_memory,
        reference=Mutect2_Support.indexed_reference_fasta,
    ),
)


Mutect2_Support.step(
    "gatk_learn_orientation_bias",
    Gatk4_Learn_Oritentation_Bias_V0_1_0(
        input_tgz=Mutect2_Support.f1r2_counts,
        max_memory=Mutect2_Support.learnorientation_memory,
        output_basename=Mutect2_Support.output_basename,
        tool_name=Mutect2_Support.gatk_learn_orientation_bias_tool_name,
    ),
)


Mutect2_Support.step(
    "gatk_gather_normal_pileup_summaries",
    Gatk4_Mergepileup_V0_1_0(
        input_tables=Mutect2_Support.gatk_get_normal_pileup_summaries.pileup_table,
        output_basename=Mutect2_Support.output_basename,
        reference_dict=Mutect2_Support.reference_dict,
        tool_name=Mutect2_Support.gatk_gather_normal_pileup_summaries_tool_name,
    ),
)


Mutect2_Support.step(
    "gatk_gather_tumor_pileup_summaries",
    Gatk4_Mergepileup_V0_1_0(
        input_tables=Mutect2_Support.gatk_get_tumor_pileup_summaries.pileup_table,
        output_basename=Mutect2_Support.output_basename,
        reference_dict=Mutect2_Support.reference_dict,
        tool_name=Mutect2_Support.gatk_gather_tumor_pileup_summaries_tool_name,
    ),
)


Mutect2_Support.step(
    "gatk_calculate_contamination",
    Gatk4_Calulcate_Contamination_V0_1_0(
        normal_pileup=Mutect2_Support.gatk_gather_normal_pileup_summaries.merged_table,
        output_basename=Mutect2_Support.output_basename,
        tumor_pileup=Mutect2_Support.gatk_gather_tumor_pileup_summaries.merged_table,
    ),
)

Mutect2_Support.output(
    "contamination_table",
    source=Mutect2_Support.gatk_calculate_contamination.contamination_table,
    output_name=True,
)

Mutect2_Support.output(
    "f1r2_bias",
    source=Mutect2_Support.gatk_learn_orientation_bias.f1r2_bias,
    output_name=True,
)

Mutect2_Support.output(
    "segmentation_table",
    source=Mutect2_Support.gatk_calculate_contamination.segmentation_table,
    output_name=True,
)

Gatk4_Filtermutect2Calls_V0_1_0 = CommandToolBuilder(
    tool="gatk4_filtermutect2calls",
    base_command=["/gatk", "FilterMutectCalls"],
    inputs=[
        ToolInput(
            tag="contamination_table",
            input_type=File(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="max_memory",
            input_type=Int(optional=True),
            default=4,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="mutect_stats", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="mutect_vcf", input_type=VcfTabix(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="ob_priors", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="reference", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="segmentation_table",
            input_type=File(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="filtered_vcf",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="*.mutect2_filtered.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="stats_table",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.mutect2_filtered.txt"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.1.1.0",
    version="v0.1.0",
    friendly_name="GATK Filter Mutect2",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "--java-options '-Xmx${return Math.floor(inputs.max_memory*1000/1.074-1)}m' -V {JANIS_CWL_TOKEN_3} -O {JANIS_CWL_TOKEN_6}.mutect2_filtered.vcf.gz -R {JANIS_CWL_TOKEN_4} --contamination-table {JANIS_CWL_TOKEN_2} --tumor-segmentation {JANIS_CWL_TOKEN_1} --ob-priors {JANIS_CWL_TOKEN_5} --filtering-stats {JANIS_CWL_TOKEN_6}.mutect2_filtered.txt --stats {JANIS_CWL_TOKEN_7}",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="segmentation_table", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="contamination_table", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="mutect_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="ob_priors", type_hint=File()
                ),
                JANIS_CWL_TOKEN_6=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
                JANIS_CWL_TOKEN_7=InputSelector(
                    input_to_select="mutect_stats", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=2,
    memory="<expr>inputs.max_memory * 1000</expr>",
)
Controlfreec_Mini_Pileup_V0_1_0 = CommandToolBuilder(
    tool="controlfreec_mini_pileup",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(
            tag="input_reads",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference", input_type=FastaFai(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="snp_vcf",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="threads",
            input_type=Int(optional=True),
            default=16,
            doc=InputDocumentation(doc=None, quality=InputQualityType.configuration),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="pileup",
            output_type=File(optional=True),
            selector=WildcardSelector(
                wildcard=StringFormatter(
                    "{JANIS_CWL_TOKEN_1}.miniPileup",
                    JANIS_CWL_TOKEN_1="<expr>inputs.input_reads.nameroot</expr>",
                )
            ),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="images.sbgenomics.com/vojislav_varjacic/control-freec-11-6:v1",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "set -eo pipefail\n${\n  if (inputs.snp_vcf == null){\n    return 'echo No vcf provided, skipping >&2 && exit 0;'\n  }\n  else{\n    return 'echo Creating pileup >&2;';\n  }\n}\nzcat ${if (inputs.snp_vcf != null) {return inputs.snp_vcf.path}} | grep -v '#' | awk {'printf ('%s\t%s\t%s\t%s\t%s\n', $1,$2-1,$2,$4,$5)'} > snps.bed\n/opt/sambamba_0.5.9/sambamba_v0.5.9 mpileup -t {JANIS_CWL_TOKEN_4} -o {JANIS_CWL_TOKEN_3}.miniPileup {JANIS_CWL_TOKEN_2} --samtools -f {JANIS_CWL_TOKEN_1} -d 8000 -Q 0 -q 1 -l snps.bed",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="input_reads", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3="<expr>inputs.input_reads.nameroot</expr>",
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="threads", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=InputSelector(input_to_select="threads", type_hint=File()),
    memory=10000,
)
Control_Freec_V0_1_0 = CommandToolBuilder(
    tool="control_freec",
    base_command=[],
    inputs=[
        ToolInput(
            tag="GC_content_profile",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="bed_graph_output",
            input_type=Boolean(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="break_point_threshold",
            input_type=Float(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="break_point_type",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="capture_regions",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="chr_len", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="coeff_var",
            input_type=Float(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="contamination",
            input_type=Float(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="contamination_adjustment",
            input_type=Boolean(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="degree",
            input_type=Float(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="force_GC_content_normalization",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="gem_mappability_file",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="intercept",
            input_type=Float(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="mate_copynumber_file_control",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="mate_copynumber_file_sample",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="mate_file_control",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="mate_file_sample",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="mate_orientation_control",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="mate_orientation_sample",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="max_expected_GC",
            input_type=Float(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="max_threads",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="min_CNA_length",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="min_expected_GC",
            input_type=Float(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="min_map_per_w",
            input_type=Float(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="min_subclone_presence",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="mini_pileup_control",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="mini_pileup_sample",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="minimal_coverage_per_position",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="minimal_quality_per_position",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="noisy_data",
            input_type=Boolean(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="ploidy", input_type=Array(t=Int()), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="print_NA",
            input_type=Boolean(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="read_cnt_threshold",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="reference", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="sex",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="shift_in_quality",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="snp_file",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="step", input_type=Int(optional=True), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="telocentromeric",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="total_memory",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="unique_match",
            input_type=Boolean(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="window",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="GC_profile",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="GC_profile.targetedRegions.cnp"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="cnvs",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*_CNVs"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="cnvs_pvalue",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.p.value.txt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="config_script",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="config.txt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="control_cpn",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*_control.cpn"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="control_pileup",
            output_type=File(optional=True),
            selector=WildcardSelector(
                wildcard="${\n    if (inputs.mate_file_control) {\n\n        return inputs.mate_file_control.path.split('/').pop() + '_minipileup.pileup'\n\n    }\n}"
            ),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="info_txt",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*_info.txt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="pngs",
            output_type=Array(t=File(), optional=True),
            selector=WildcardSelector(wildcard="*png"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="ratio",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*_ratio.txt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="ratio_BedGraph",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.BedGraph"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="sample_BAF",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*_BAF.txt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="sample_cpn",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*_sample.cpn"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="sample_pileup",
            output_type=File(optional=True),
            selector=WildcardSelector(
                wildcard="${\n    if (inputs.mate_file_sample) {\n\n        return inputs.mate_file_sample.path.split('/').pop() + '_minipileup.pileup'\n    }\n}"
            ),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="images.sbgenomics.com/vojislav_varjacic/control-freec-11-6:v1",
    version="v0.1.0",
    friendly_name="Control-FREEC 11.6",
    arguments=[
        ToolArgument(
            value="${\n    // script for splitting the genome fasta into chromosomes\n    return 'python split_fasta.py ' + inputs.reference.path\n\n}",
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="&&", position=1, doc=InputDocumentation(doc=None), shell_quote=False,
        ),
        ToolArgument(
            value="/opt/controlfreec/FREEC/src/freec",
            prefix="",
            position=2,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="-conf",
            position=3,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="config.txt",
            position=4,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="&&", position=5, doc=InputDocumentation(doc=None), shell_quote=False,
        ),
        ToolArgument(
            value="${\n\n\n\n\n    if (inputs.mate_file_sample) {\n        filepath = inputs.mate_file_sample.path\n        filename = filepath.split('/').pop()\n    } else {\n        filepath = inputs.mate_copynumber_file_sample.path\n        filename = filepath.split('/').pop()\n    }\n\n    CNVs = filename + '_CNVs'\n    ratio = filename + '_ratio' + '.txt'\n\n\n    return 'cat assess_significance.R | R --slave --args ' + CNVs + ' ' + ratio\n}",
            position=6,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="&&", position=7, doc=InputDocumentation(doc=None), shell_quote=False,
        ),
        ToolArgument(
            value="line=$(cat *info.txt | grep Output_Ploidy | sed -E 's/.+([0-9]+)/\\1/')",
            position=8,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="&&", position=9, doc=InputDocumentation(doc=None), shell_quote=False,
        ),
        ToolArgument(
            value="cat makeGraph.R | R --slave --args",
            position=10,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="$line",
            position=11,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="${\n    if (inputs.mate_file_sample) {\n        filepath = inputs.mate_file_sample.path\n        filename = filepath.split('/').pop()\n    } else {\n        filepath = inputs.mate_copynumber_file_sample.path\n        filename = filepath.split('/').pop()\n    }\n\n    ratio = filename + '_ratio' + '.txt'\n\n    return ratio\n}",
            position=12,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="${\n\n    if (inputs.snp_file) {\n\n        sufix = '_BAF'\n        sufix_ext = '.txt'\n\n        if (inputs.mate_file_sample) {\n            filepath = inputs.mate_file_sample.path\n            filename = filepath.split('/').pop()\n        } else {\n            filepath = inputs.mate_copynumber_file_sample.path\n            filename = filepath.split('/').pop()\n        }\n\n\n        new_filename = filename + sufix + sufix_ext\n\n        return new_filename\n    }\n}",
            position=13,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="${ //conversion of file names\n\n    if (inputs.mate_file_control) {\n        if (inputs.mate_file_control.path.split('.').pop() != 'pileup') {\n            com = ''\n            com += '&& mv sample.pileup '\n\n        }\n    }\n\n\n}",
            position=114,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
    ],
    cpus="${\n    if (inputs.max_threads) {\n        return inputs.max_threads\n    } else {\n        return 8\n    }\n}",
    memory="${\n    if (inputs.total_memory) {\n        return inputs.total_memory\n    } else {\n        return 15000\n    }\n}",
    files_to_create={
        "config.txt": "${\n\n    // The function returns the concatenated line for config file\n    function makeline(content, p1, p2) {\n        if (p2 != null) {\n            if (p2.path != null) {\n                p2 = p2.path\n            }\n            content = content.concat(p1)\n            content = content.concat(' = ')\n            content = content.concat(p2)\n            content = content.concat('\n')\n        }\n        return content\n\n    }\n\n    // General section\n    content = '[general]\n\n'\n    content = makeline(content, 'BedGraphOutput', inputs.bed_graph_output)\n    content = content.concat('bedtools = /opt/bedtools2/bin/bedtools\n')\n    content = makeline(content, 'chrLenFile', inputs.chr_len)\n    content = makeline(content, 'breakPointThreshold', inputs.break_point_threshold)\n    content = makeline(content, 'breakPointType', inputs.break_point_type)\n    content = makeline(content, 'chrFiles', '.')\n    content = makeline(content, 'coefficientOfVariation', inputs.coeff_var)\n\n    if (inputs.capture_regions) {\n        content = content.concat('window = 0\n')\n    } else {\n        content = makeline(content, 'window', inputs.window)\n    }\n\n    content = makeline(content, 'contamination', inputs.contamination)\n    content = makeline(content, 'contaminationAdjustment', inputs.contamination_adjustment)\n    content = makeline(content, 'degree', inputs.degree)\n    content = makeline(content, 'forceGCcontentNormalization', inputs.force_GC_content_normalization)\n    content = makeline(content, 'GCcontentProfile', inputs.GC_content_profile)\n    content = makeline(content, 'gemMappabilityFile', inputs.gem_mappability_file)\n    content = makeline(content, 'intercept', inputs.intercept)\n    content = makeline(content, 'minCNAlength', inputs.min_CNA_length)\n    content = makeline(content, 'minMappabilityPerWindow', inputs.min_map_per_w)\n    content = makeline(content, 'minExpectedGC', inputs.min_expected_GC)\n    content = makeline(content, 'maxExpectedGC', inputs.max_expected_GC)\n    content = makeline(content, 'minimalSubclonePresence', inputs.min_subclone_presence)\n    if (inputs.max_threads) {\n        content = makeline(content, 'maxThreads', inputs.max_threads)\n        content = makeline(content, 'SambambaThreads', inputs.max_threads)\n    } else {\n        content = content.concat('maxThreads = 8\n')\n        content = content.concat('SambambaThreads = 8\n')\n    }\n    content = makeline(content, 'noisyData', inputs.noisy_data)\n    content = makeline(content, 'ploidy', inputs.ploidy.toString())\n    content = makeline(content, 'printNA', inputs.print_NA)\n    content = makeline(content, 'readCountThreshold', inputs.read_cnt_threshold)\n    content = content.concat('sambamba = /opt/sambamba_0.5.9/sambamba_v0.5.9\n')\n\n    content = content.concat('samtools = /opt/samtools-1.3.1/samtools\n')\n    content = makeline(content, 'sex', inputs.sex)\n    content = makeline(content, 'step', inputs.step)\n    content = makeline(content, 'telocentromeric', inputs.telocentromeric)\n    content = makeline(content, 'uniqueMatch', inputs.unique_match)\n\n\n    // Sample section\n\n    content = content.concat('\n[sample]\n\n')\n    content = makeline(content, 'mateFile', inputs.mate_file_sample)\n    content = makeline(content, 'mateCopyNumberFile', inputs.mate_copynumber_file_sample)\n    content = makeline(content, 'miniPileup', inputs.mini_pileup_sample)\n    if (inputs.mate_file_sample) {\n        if (inputs.mate_file_sample.path.split('.').pop() == 'gz') {\n            content = makeline(content, 'inputFormat', inputs.mate_file_sample.path.split('.').slice(-2, -1)[0])\n        } else {\n            content = makeline(content, 'inputFormat', inputs.mate_file_sample.path.split('.').pop())\n        }\n        content = makeline(content, 'mateOrientation', inputs.mate_orientation_sample)\n    }\n\n\n    // Control section\n\n    content = content.concat('\n[control]\n\n')\n    content = makeline(content, 'mateFile', inputs.mate_file_control)\n    content = makeline(content, 'mateCopyNumberFile', inputs.mate_copynumber_file_control)\n    content = makeline(content, 'miniPileup', inputs.mini_pileup_control)\n    if (inputs.mate_file_control) {\n        content = makeline(content, 'inputFormat', inputs.mate_file_control.path.split('.').pop())\n        content = makeline(content, 'mateOrientation', inputs.mate_orientation_sample)\n    }\n\n\n\n\n    // BAF section\n\n    content = content.concat('\n[BAF]\n\n')\n    content = makeline(content, 'minimalCoveragePerPosition', inputs.minimal_coverage_per_position)\n    content = makeline(content, 'minimalQualityPerPosition', inputs.minimal_quality_per_position)\n    content = makeline(content, 'shiftInQuality', inputs.shift_in_quality)\n    if (inputs.snp_file) {\n        content = makeline(content, 'SNPfile', inputs.snp_file)\n        if (inputs.mate_file_sample) {\n            if ((inputs.mate_file_sample.path.split('.').pop().toUpperCase() != 'PILEUP') &&\n                (inputs.mate_file_sample.path.split('.').slice(-2, -1)[0].toUpperCase() != 'PILEUP')) {\n                content = makeline(content, 'makePileup', inputs.snp_file)\n                content = makeline(content, 'fastaFile', inputs.reference)\n            }\n        }\n    }\n\n    // Target section\n\n    content = content.concat('\n[target]\n\n')\n    content = makeline(content, 'captureRegions', inputs.capture_regions)\n\n    return content\n}",
        "split_fasta.py": "import sys\n\nwith open(sys.argv[1], 'r') as f:\n    fasta = f.readlines()\n\nref_lines = {}\nfor i in range(0, len(fasta)):\n    if fasta[i][0] == '>':\n        chrom = fasta[i].split()[0].split('>')[1]\n        print('Reading chromosome: ' + chrom)\n        ref_lines[chrom] = [fasta[i]]\n    else:\n        ref_lines[chrom].append(fasta[i])\n\nfor chromosome, lines in ref_lines.items():\n    print('Creating ' + chromosome + '.fasta')\n    with open(chromosome + '.fasta', 'w') as chr_fasta:\n        for line in lines:\n            chr_fasta.write(line)",
        "assess_significance.R": "#!/usr/bin/env Rscript\n\nlibrary(rtracklayer)\n\nargs <- commandArgs()\n\ndataTable <-read.table(args[5], header=TRUE);\nratio<-data.frame(dataTable)\n\ndataTable <- read.table(args[4], header=FALSE)\ncnvs<- data.frame(dataTable) \n\nratio$Ratio[which(ratio$Ratio==-1)]=NA\n\ncnvs.bed=GRanges(cnvs[,1],IRanges(cnvs[,2],cnvs[,3]))  \nratio.bed=GRanges(ratio$Chromosome,IRanges(ratio$Start,ratio$Start),score=ratio$Ratio)\n\noverlaps <- subsetByOverlaps(ratio.bed,cnvs.bed)\nnormals <- setdiff(ratio.bed,cnvs.bed)\nnormals <- subsetByOverlaps(ratio.bed,normals)\n\n#mu <- mean(score(normals),na.rm=TRUE)\n#sigma<- sd(score(normals),na.rm=TRUE)\n\n#hist(score(normals),n=500,xlim=c(0,2))\n#hist(log(score(normals)),n=500,xlim=c(-1,1))\n\n#shapiro.test(score(normals)[which(!is.na(score(normals)))][5001:10000])\n#qqnorm (score(normals)[which(!is.na(score(normals)))],ylim=(c(0,10)))\n#qqline(score(normals)[which(!is.na(score(normals)))], col = 2)\n\n#shapiro.test(log(score(normals))[which(!is.na(score(normals)))][5001:10000])\n#qqnorm (log(score(normals))[which(!is.na(score(normals)))],ylim=(c(-6,10)))\n#qqline(log(score(normals))[which(!is.na(score(normals)))], col = 2)\n\nnumberOfCol=length(cnvs)\n\nfor (i in c(1:length(cnvs[,1]))) {\n  values <- score(subsetByOverlaps(ratio.bed,cnvs.bed[i]))\n  #wilcox.test(values,mu=mu)\n  W <- function(values,normals){resultw <- try(wilcox.test(values,score(normals)), silent = TRUE)\n	if(class(resultw)=='try-error') return(list('statistic'=NA,'parameter'=NA,'p.value'=NA,'null.value'=NA,'alternative'=NA,'method'=NA,'data.name'=NA)) else resultw}\n  KS <- function(values,normals){resultks <- try(ks.test(values,score(normals)), silent = TRUE)\n	if(class(resultks)=='try-error') return(list('statistic'=NA,'p.value'=NA,'alternative'=NA,'method'=NA,'data.name'=NA)) else resultks}\n  #resultks <- try(KS <- ks.test(values,score(normals)), silent = TRUE)\n  #	if(class(resultks)=='try-error') NA) else resultks\n  cnvs[i,numberOfCol+1]=W(values,normals)$p.value\n  cnvs[i,numberOfCol+2]=KS(values,normals)$p.value\n  }\n\nif (numberOfCol==5) {\n  names(cnvs)=c('chr','start','end','copy number','status','WilcoxonRankSumTestPvalue','KolmogorovSmirnovPvalue')  \n}\nif (numberOfCol==7) {\n  names(cnvs)=c('chr','start','end','copy number','status','genotype','uncertainty','WilcoxonRankSumTestPvalue','KolmogorovSmirnovPvalue')  \n}\nif (numberOfCol==9) {\n  names(cnvs)=c('chr','start','end','copy number','status','genotype','uncertainty','somatic/germline','precentageOfGermline','WilcoxonRankSumTestPvalue','KolmogorovSmirnovPvalue')  \n}\nwrite.table(cnvs, file=paste(args[4],'.p.value.txt',sep=''),sep='\t',quote=F,row.names=F)",
        "makeGraph.R": "#!/usr/bin/env Rscript\n\nargs <- commandArgs()\n\ndataTable <-read.table(args[5], header=TRUE);\n\nratio<-data.frame(dataTable)\nploidy <- type.convert(args[4])\n\n\npng(filename = paste(args[5],'.log2.png',sep = ''), width = 1180, height = 1180,\n    units = 'px', pointsize = 20, bg = 'white', res = NA)\nplot(1:10)\nop <- par(mfrow = c(5,5))\n\nfor (i in c(1:22,'X','Y')) {\n	tt <- which(ratio$Chromosome==i)\n	if (length(tt)>0) {\n	 plot(ratio$Start[tt],log2(ratio$Ratio[tt]),xlab = paste ('position, chr',i),ylab = 'normalized copy number profile (log2)',pch = '.',col = colors()[88])\n	 tt <- which(ratio$Chromosome==i  & ratio$CopyNumber>ploidy )\n	 points(ratio$Start[tt],log2(ratio$Ratio[tt]),pch = '.',col = colors()[136])\n	\n	\n	tt <- which(ratio$Chromosome==i  & ratio$CopyNumber<ploidy & ratio$CopyNumber!= -1)\n	 points(ratio$Start[tt],log2(ratio$Ratio[tt]),pch = '.',col = colors()[461])\n	 tt <- which(ratio$Chromosome==i)\n	 \n	 #UNCOMMENT HERE TO SEE THE PREDICTED COPY NUMBER LEVEL:\n	 #points(ratio$Start[tt],log2(ratio$CopyNumber[tt]/ploidy), pch = '.', col = colors()[24],cex=4)\n	 \n	}\n	tt <- which(ratio$Chromosome==i)\n	\n	#UNCOMMENT HERE TO SEE THE EVALUATED MEDIAN LEVEL PER SEGMENT:\n	points(ratio$Start[tt],log2(ratio$MedianRatio[tt]), pch = '.', col = colors()[463],cex=4)\n	\n}\n\ndev.off()\n\n\npng(filename = paste(args[5],'.png',sep = ''), width = 1180, height = 1180,\n    units = 'px', pointsize = 20, bg = 'white', res = NA)\nplot(1:10)\nop <- par(mfrow = c(5,5))\n\nmaxLevelToPlot <- 3\nfor (i in c(1:length(ratio$Ratio))) {\n	if (ratio$Ratio[i]>maxLevelToPlot) {\n		ratio$Ratio[i]=maxLevelToPlot;\n	}\n}\n\n\nfor (i in c(1:22,'X','Y')) {\n	tt <- which(ratio$Chromosome==i)\n	if (length(tt)>0) {\n	 plot(ratio$Start[tt],ratio$Ratio[tt]*ploidy,ylim = c(0,maxLevelToPlot*ploidy),xlab = paste ('position, chr',i),ylab = 'normalized copy number profile',pch = '.',col = colors()[88])\n	 tt <- which(ratio$Chromosome==i  & ratio$CopyNumber>ploidy )\n	 points(ratio$Start[tt],ratio$Ratio[tt]*ploidy,pch = '.',col = colors()[136])\n	\n	tt <- which(ratio$Chromosome==i  & ratio$Ratio==maxLevelToPlot & ratio$CopyNumber>ploidy)	\n	points(ratio$Start[tt],ratio$Ratio[tt]*ploidy,pch = '.',col = colors()[136],cex=4)\n	 \n	tt <- which(ratio$Chromosome==i  & ratio$CopyNumber<ploidy & ratio$CopyNumber!= -1)\n	 points(ratio$Start[tt],ratio$Ratio[tt]*ploidy,pch = '.',col = colors()[461])\n	 tt <- which(ratio$Chromosome==i)\n	 \n	 #UNCOMMENT HERE TO SEE THE PREDICTED COPY NUMBER LEVEL:\n	 #points(ratio$Start[tt],ratio$CopyNumber[tt], pch = '.', col = colors()[24],cex=4)\n	 \n	}\n	tt <- which(ratio$Chromosome==i)\n	\n	#UNCOMMENT HERE TO SEE THE EVALUATED MEDIAN LEVEL PER SEGMENT:\n	points(ratio$Start[tt],ratio$MedianRatio[tt]*ploidy, pch = '.', col = colors()[463],cex=4)\n	\n}\n\ndev.off()\n\n\n\n\nif (length(args)>5) {\n	dataTable <-read.table(args[6], header=TRUE);\n	BAF<-data.frame(dataTable)\n\n	png(filename = paste(args[6],'.png',sep = ''), width = 1180, height = 1180,\n	    units = 'px', pointsize = 20, bg = 'white', res = NA)\n	plot(1:10)\n	op <- par(mfrow = c(5,5))\n\n	for (i in c(1:22,'X','Y')) {\n	    tt <- which(BAF$Chromosome==i)\n	    if (length(tt)>0){\n		lBAF <-BAF[tt,]\n		plot(lBAF$Position,lBAF$BAF,ylim = c(-0.1,1.1),xlab = paste ('position, chr',i),ylab = 'BAF',pch = '.',col = colors()[1])\n\n		tt <- which(lBAF$A==0.5)		\n		points(lBAF$Position[tt],lBAF$BAF[tt],pch = '.',col = colors()[92])\n		tt <- which(lBAF$A!=0.5 & lBAF$A>=0)\n		points(lBAF$Position[tt],lBAF$BAF[tt],pch = '.',col = colors()[62])\n		tt <- 1\n		pres <- 1\n\n		if (length(lBAF$A)>4) {\n			for (j in c(2:(length(lBAF$A)-pres-1))) {\n				if (lBAF$A[j]==lBAF$A[j+pres]) {	\n					tt[length(tt)+1] <- j \n				}\n			}\n			points(lBAF$Position[tt],lBAF$A[tt],pch = '.',col = colors()[24],cex=4)\n			points(lBAF$Position[tt],lBAF$B[tt],pch = '.',col = colors()[24],cex=4)	\n		}\n\n		tt <- 1\n		pres <- 1\n		if (length(lBAF$FittedA)>4) {\n			for (j in c(2:(length(lBAF$FittedA)-pres-1))) {\n				if (lBAF$FittedA[j]==lBAF$FittedA[j+pres]) {	\n					tt[length(tt)+1] <- j \n				}\n			}\n			points(lBAF$Position[tt],lBAF$FittedA[tt],pch = '.',col = colors()[463],cex=4)\n			points(lBAF$Position[tt],lBAF$FittedB[tt],pch = '.',col = colors()[463],cex=4)	\n		}\n\n	   }\n\n	}\n	dev.off()\n\n}",
    },
    doc="Control-FREEC analyzes copy-number variants and allelic imbalances in exome and whole-genome DNA sequencing.\n\nThis tool automatically computes, normalizes and segments copy number and beta allele frequency (BAF) profiles, then calls copy number alterations and LOH. [1]\n\n*A list of **all inputs and parameters** with corresponding descriptions can be found at the bottom of the page.*\n### Common Use Cases\n\n* The **chrLenFile** input is required and can be found in Public Reference Files as **Homo\_sapiens\_assembly38.fasta.sizes**, **ucsc.hg19.fasta.sizes** and **human\_g1k\_v37\_decoy.fasta.sizes**.\n\n* The **ploidy** parameter is required. In case of doubt, different values can be set and Control-FREEC will select the one that explains the most observed CNVs.\n\n* Normal and control sample can be provided through two possible inputs:\n     * **mateFile**, a file with mapped reads\n     * **mateCopyNumberFile**, a raw copy number file created for both normal and control sample, provided through **mateFile** in a first run, and can be reused in the future runs for more efficient computation.\n\n\n\n* **A control (matched normal) sample is optional for whole genome sequencing data but mandatory for whole exome or targeted sequencing data.**\n\n* Similar to **mateCopyNumberFile**, a **Mini pileup Sample** and **Mini pileup Control** files can be created in the first run, if the **Known SNPs** file is provided. Consequently, by providing these files as inputs in future tasks, execution time will decrease significantly.\n\n* If a **mateFile** is specified, the **mateOrientation** parameter must be set.\n\n* In order to create a **BAF profile**, one of the following options must be implemented:\n    * **mateFile** + **Known SNPs** \n    * **mateCopyNumberFile** + **mateFile** + **KnownSNPs**\n    * **mateCopyNumberFile** + **miniPileup** + **KnownSNPs**\n\n### Changes Introduced by Seven Bridges\n\n* Based on the input parameters, a config file is created in order to properly run Control-FREEC.\n\n### Common Issues and Important Notes\n\n* **A control (matched normal) sample is optional for whole genome sequencing data but mandatory for whole exome or targeted sequencing data.**\n\n* A **gemMappabilityFile** can be used only in the mode without a control sample.\n\n* If a **mateFile** is specified, the **mateOrientation** parameter must be set.\n\n* Currently, there is an issue with creating a **BAF sample file** with the b37 notation. The genotypes for CNV regions are, however, created.\n\n\n### Performance Benchmarking\n\nThe instance set for this tool is the AWS c4.2xlarge instance with 8 vCPUs, 15 GiB of RAM and 1 TB of EBS (disk space).\n|     BAM size in GB    | Type |  Instance  | Duration | Cost ($) |\n|:--------------------:|:----:|:----------:|:--------:|:--------:|\n|         2x12 (Normal-Tumor)         |  WES | c4.2xlarge |  1h 52m  |    0.8   |\n|   100 (Tumor-only)   |  WGS | c4.2xlarge |  17h 43m |     7    |\n| 2x100 (Normal-Tumor) |  WGS | c4.2xlarge |   1d 8h  |    13    |\n|   100 (Tumor-only)   |  WGS | c4.8xlarge |  6h 30m |     10    |\n| 2x100 (Normal-Tumor) |  WGS | c4.8xlarge |   11h  |    18    |\n\nAn instance with more resources can be obtained by providing inputs for **Maximum threads** and **Total memory [MB]**.\n\n*Cost can be significantly reduced by using **spot instances**. Visit the [Knowledge Center](https://docs.sevenbridges.com/docs/about-spot-instances) for more details.*  \n\n###References\n[1] [Control-FREEC: Prediction of copy number alterations and loss of heterozygosity using deep-sequencing data](http://boevalab.com/FREEC/tutorial.html#install)",
)
Ubuntu_Ratio2Seg_V0_1_0 = CommandToolBuilder(
    tool="ubuntu_ratio2seg",
    base_command=["python", "-c"],
    inputs=[
        ToolInput(
            tag="ctrlfreec_ratio", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference_fai", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="sample_name", input_type=String(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="ctrlfreec_ratio2seg",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.seg"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/python:2.7.13",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "\nimport math\n\nfai = open('{JANIS_CWL_TOKEN_2}')\nh = {}\nfor line in fai:\n    f = line.split('\t')\n    if f == 'chrM':\n        break\n    f[0] = f[0].replace('chr','')\n    h[f[0]] = f[1]\nfai.close()\n\nsmp = '{JANIS_CWL_TOKEN_1}'\n\nratio_file = open('{JANIS_CWL_TOKEN_3}')\nout = open('{JANIS_CWL_TOKEN_4}.controlfreec.seg', 'w')\nout.write('ID\tchrom\tloc.start\tloc.end\tnum.mark\tseg.mean\n') \nhead = next(ratio_file)\ncount = 0\nfor line in ratio_file:\n    data = line.rstrip('\n').split('\t')\n    (chrom, pos, ratio, meanRatio) = (data[0], data[1], data[2], data[3])\n    if float(meanRatio) == -1:\n        continue\n    count += 1\n    if count == 1:\n        start = pos\n        seg_ratio = meanRatio\n        on_chr = chrom\n    else:\n        if chrom != on_chr:\n            out.write('\t'.join((smp, 'chr' + on_chr, start, h[on_chr], str(count))) + '\t')\n            if float(seg_ratio) != 0:\n                out.write(str(math.log(float(seg_ratio), 2)) + '\n')\n            else:\n                out.write(str(math.log(float(seg_ratio) + 1, 2)) + '\n')\n            start = pos\n            seg_ratio = meanRatio\n            on_chr = chrom\n            count = 1\n        elif meanRatio != seg_ratio:\n            out.write('\t'.join((smp, 'chr' + chrom, start, str(int(pos)-1), str(count))) + '\t')\n            if float(seg_ratio) != 0:\n                out.write(str(math.log(float(seg_ratio), 2)) + '\n')\n            else:\n                out.write(str(math.log(float(seg_ratio) + 1, 2)) + '\n')\n            start = pos\n            seg_ratio = meanRatio\n            count = 1\nratio_file.close()\nout.close()\n",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="sample_name", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="reference_fai", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="ctrlfreec_ratio", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=True,
        )
    ],
    cpus=1,
    memory=1000,
)
Ubuntu_Rename_Cf_Outputs_V0_1_0 = CommandToolBuilder(
    tool="ubuntu_rename_cf_outputs",
    base_command=[],
    inputs=[
        ToolInput(
            tag="input_files",
            input_type=Array(t=File()),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_pngs",
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
            tag="ctrlfreec_baf",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.BAF.txt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="ctrlfreec_bam_ratio",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.ratio.txt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="ctrlfreec_cnvs",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.CNVs"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="ctrlfreec_config",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.config.txt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="ctrlfreec_info",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.info.txt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="ctrlfreec_normal_cpn",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.control.cpn"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="ctrlfreec_pngs",
            output_type=Array(t=File()),
            selector=WildcardSelector(wildcard="*.png"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="ctrlfreec_pval",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.CNVs.p.value.txt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="ctrlfreec_tumor_cpn",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.sample.cpn"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/ubuntu:18.04",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="${\n    var cmd = '';\n    for (var i=0; i < inputs.input_files.length; i++){\n      if (inputs.input_files[i] != null){\n        var basename = inputs.input_files[i].basename;\n        var fname = basename.replace('bam_', '');\n        var parts = fname.split('.');\n        parts.shift();\n        var check = fname.substr(fname.length - 10);\n        if (check == 'config.txt') {\n            cmd += 'cp ' + inputs.input_files[i].path + ' ' + inputs.output_basename + '.controlfreec.config.txt;';\n        } else {\n        fname = inputs.output_basename + '.controlfreec.' + parts.join('.');\n        cmd += ' cp ' + inputs.input_files[i].path + ' ' + fname + ';';\n        }\n      }\n      else{\n        cmd += 'echo A null file was detected, skipping >&2;'\n      }\n    }\n  for (var j=0; j < inputs.input_pngs.length; j++){\n      var nameroot = inputs.input_pngs[j].nameroot;\n      var fname = nameroot.replace('bam_', '');\n      fname = fname.replace('.txt', '');\n      var parts = fname.split('.');\n      parts.shift();\n      fname = inputs.output_basename + '.controlfreec.' + parts.join('.') + '.png';\n      cmd += ' cp ' + inputs.input_pngs[j].path + ' ' + fname + ';';\n      }\n    return cmd;\n}",
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=2,
    memory=1000,
    doc="Rename contrfreeec outputs",
)
Cnvkit_Batch_V0_1_0 = CommandToolBuilder(
    tool="cnvkit_batch",
    base_command=None,
    inputs=[
        ToolInput(
            tag="annotation_file",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="b_allele_vcf",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="capture_regions",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="cnvkit_cnn",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_control",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_sample",
            input_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference",
            input_type=FastaFai(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="sex", input_type=String(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="threads",
            input_type=Int(optional=True),
            default=16,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="tumor_sample_name",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="wgs_mode",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="output_calls",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.call.cns"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="output_cnn",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*_reference.cnn"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="output_cnr",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.cnr"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="output_diagram",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.diagram.pdf"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="output_gainloss",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.gainloss.txt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="output_metrics",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.metrics.txt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="output_scatter",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.scatter.pdf"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="output_seg",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.seg"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="images.sbgenomics.com/milos_nikolic/cnvkit:0.9.3",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "ln -s {JANIS_CWL_TOKEN_3} .; ln -s {JANIS_CWL_TOKEN_4} ./{JANIS_CWL_TOKEN_1}.bai\n${ \n    var cmd = '';\n    if (inputs.input_control != null) {\n        cmd = 'ln -s ' + inputs.input_control.path + ' .; ln -s ' + inputs.input_control.secondaryFiles[0].path + ' ./' + inputs.input_control.basename + '.bai'\n    }\n    return cmd;\n}\ncnvkit.py batch -p {JANIS_CWL_TOKEN_2} ${\n    var cmd = '';\n    if (inputs.wgs_mode == 'Y') {\n        cmd = ' -m wgs ';\n    }\n    return cmd;\n} {JANIS_CWL_TOKEN_3} ${\n    var cmd = '';\n    if (inputs.capture_regions != null) {\n        cmd = '--targets ' + inputs.capture_regions.path;\n    }\n    return cmd;\n} ${\n  if (inputs.cnv_kit_cnn == null){\n    var arg = '--output-reference ' + inputs.output_basename + '_cnvkit_reference.cnn --fasta ' + inputs.reference.path + ' --annotate ' + inputs.annotation_file.path;\n    if (inputs.input_control != null) {\n        arg += ' --normal ' + inputs.input_control.path;\n    }\n  }\n  else{\n    var arg = '--reference ' + inputs.cnv_kit_cnn.path;\n    var msex = ['m','y','male','Male']\n    if (msex.indexOf(inputs.sex) >= 0){\n      arg += ' --male-reference';\n    }\n  }\n  return arg;\n} --diagram  --scatter\ncnvkit.py call {JANIS_CWL_TOKEN_6}.cns ${\n  var arg = '';\n  if (inputs.b_allele_vcf != null){\n    arg = '--vcf ' + inputs.b_allele_vcf.path;\n  }\n  return arg;\n} ${\n  var arg = '--sample-sex ' + inputs.sex;\n  var msex = ['m','y','male','Male']\n  if (msex.indexOf(inputs.sex) >= 0){\n    arg += ' --male-reference';\n  }\n  return arg;\n} -o {JANIS_CWL_TOKEN_7}.call.cns\n      \nln -s {JANIS_CWL_TOKEN_7}.call.cns {JANIS_CWL_TOKEN_5}.cns\ncnvkit.py export seg {JANIS_CWL_TOKEN_5}.cns -o {JANIS_CWL_TOKEN_7}.call.seg\nrm {JANIS_CWL_TOKEN_5}.cns\ncnvkit.py metrics {JANIS_CWL_TOKEN_6}.cnr -s {JANIS_CWL_TOKEN_6}.cns -o {JANIS_CWL_TOKEN_7}.metrics.txt\ncnvkit.py gainloss {JANIS_CWL_TOKEN_6}.cnr -o {JANIS_CWL_TOKEN_7}.gainloss.txt\nmv {JANIS_CWL_TOKEN_6}.cnr {JANIS_CWL_TOKEN_7}.cnr\nmv {JANIS_CWL_TOKEN_6}-diagram.pdf {JANIS_CWL_TOKEN_7}.diagram.pdf\nmv {JANIS_CWL_TOKEN_6}-scatter.pdf {JANIS_CWL_TOKEN_7}.scatter.pdf",
                JANIS_CWL_TOKEN_1=BasenameOperator(
                    InputSelector(input_to_select="input_sample", type_hint=File())
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="threads", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="input_sample", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4="<expr>inputs.input_sample.secondaryFiles[0]</expr>",
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="tumor_sample_name", type_hint=File()
                ),
                JANIS_CWL_TOKEN_6="<expr>inputs.input_sample.nameroot</expr>",
                JANIS_CWL_TOKEN_7=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=InputSelector(input_to_select="threads", type_hint=File()),
    memory=32000,
)
Strelka2_V0_1_0 = CommandToolBuilder(
    tool="strelka2",
    base_command=[
        "/strelka-2.9.3.centos6_x86_64/bin/configureStrelkaSomaticWorkflow.py"
    ],
    inputs=[
        ToolInput(
            tag="cores",
            input_type=Int(optional=True),
            default=18,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="exome_flag",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="hg38_strelka_bed",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_normal_aligned",
            input_type=GenericFileWithSecondaries(
                secondaries=[
                    "${\n  var dpath = self.location.replace(self.basename, '')\n  if(self.nameext == '.bam'){\n    return {'location': dpath+self.nameroot+'.bai', 'class': 'File'}\n  }\n  else{\n    return {'location': dpath+self.basename+'.crai', 'class': 'File'}\n  }\n}\n"
                ]
            ),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_tumor_aligned",
            input_type=GenericFileWithSecondaries(
                secondaries=[
                    "${\n  var dpath = self.location.replace(self.basename, '')\n  if(self.nameext == '.bam'){\n    return {'location': dpath+self.nameroot+'.bai', 'class': 'File'}\n  }\n  else{\n    return {'location': dpath+self.basename+'.crai', 'class': 'File'}\n  }\n}\n"
                ]
            ),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="manta_small_indels",
            input_type=VcfTabix(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference",
            input_type=GenericFileWithSecondaries(secondaries=["^.dict", ".fai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="use_manta_small_indels",
            input_type=Boolean(optional=True),
            default=False,
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="output_indel",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="results/variants/*.indels.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="output_snv",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="results/variants/*.snvs.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/strelka",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "--normalBam {JANIS_CWL_TOKEN_3} --tumorBam {JANIS_CWL_TOKEN_1} --ref {JANIS_CWL_TOKEN_5} --callRegions {JANIS_CWL_TOKEN_2} {JANIS_CWL_TOKEN_4} ${\n  var arg = '--runDir=./';\n  if (inputs.exome_flag == 'Y'){\n    arg += ' --exome'\n  }\n  return arg\n} && ./runWorkflow.py -m local -j {JANIS_CWL_TOKEN_6}",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="input_tumor_aligned", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="hg38_strelka_bed", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="input_normal_aligned", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4="<expr>inputs.manta_small_indels && inputs.use_manta_small_indels ? '--indelCandidates ' + inputs.manta_small_indels.path : ''</expr>",
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="reference", type_hint=File()
                ),
                JANIS_CWL_TOKEN_6=InputSelector(
                    input_to_select="cores", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=InputSelector(input_to_select="cores", type_hint=File()),
    memory=10000,
)
Bcftools_Reheader_Vcf_V0_1_0 = CommandToolBuilder(
    tool="bcftools_reheader_vcf",
    base_command=["echo"],
    inputs=[
        ToolInput(
            tag="input_normal_name",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_tumor_name",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="input_vcf", input_type=File(), doc=InputDocumentation(doc=None)),
    ],
    outputs=[
        ToolOutput(
            tag="reheadered_vcf",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="*.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/bvcftools:latest",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="<expr>inputs.input_normal_name) > sample_list.txt && echo $(inputs.input_tumor_name) >> sample_list.txt && bcftools reheader -s sample_list.txt $(inputs.input_vcf.path) > $(inputs.input_vcf.nameroot.replace('.vcf', '.reheadered.vcf.gz')) && tabix $(inputs.input_vcf.nameroot.replace('.vcf', '.reheadered.vcf.gz')</expr>",
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=1,
    memory=1000,
)
Kfdrc_Manta_Sv_V0_1_0 = CommandToolBuilder(
    tool="kfdrc_manta_sv",
    base_command=["/manta-1.4.0.centos6_x86_64/bin/configManta.py"],
    inputs=[
        ToolInput(
            tag="cores",
            input_type=Int(optional=True),
            default=18,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="hg38_strelka_bed",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_normal_cram",
            input_type=CramCrai(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_tumor_cram",
            input_type=CramCrai(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="ram",
            input_type=Int(optional=True),
            default=10,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference",
            input_type=GenericFileWithSecondaries(secondaries=["^.dict", ".fai"]),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="output_sv",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="*SV.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="small_indels",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="*SmallIndels.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/manta:1.4.0",
    version="v0.1.0",
    friendly_name="Manta sv caller",
    arguments=[
        ToolArgument(
            value="${\n  var std = ' --ref ' + inputs.reference.path + ' --callRegions ' + inputs.hg38_strelka_bed.path + ' --runDir=./ && ./runWorkflow.py -m local -j ' + inputs.cores + ' ';\n  var mv = ' && mv results/variants/';\n  if (typeof inputs.input_tumor_cram === 'undefined' || inputs.input_tumor_cram === null){\n    var mv_cmd = mv + 'diploidSV.vcf.gz ' +  inputs.output_basename + '.manta.diploidSV.vcf.gz' + mv + 'diploidSV.vcf.gz.tbi ' + inputs.output_basename + '.manta.diploidSV.vcf.gz.tbi' + mv + 'candidateSmallIndels.vcf.gz ' + inputs.output_basename + '.manta.candidateSmallIndels.vcf.gz' + mv + 'candidateSmallIndels.vcf.gz.tbi ' + inputs.output_basename + '.manta.candidateSmallIndels.vcf.gz.tbi';\n    return '--bam '.concat(inputs.input_normal_cram.path, std, mv_cmd);\n  }\n  else if (typeof inputs.input_normal_cram === 'undefined' || inputs.input_normal_cram === null){\n    var mv_cmd = mv + 'tumorSV.vcf.gz ' + inputs.output_basename + '.manta.tumorSV.vcf.gz' + mv + 'tumorSV.vcf.gz.tbi ' + inputs.output_basename + '.manta.tumorSV.vcf.gz.tbi' + mv + 'candidateSmallIndels.vcf.gz ' + inputs.output_basename + '.manta.candidateSmallIndels.vcf.gz' + mv + 'candidateSmallIndels.vcf.gz.tbi ' + inputs.output_basename + '.manta.candidateSmallIndels.vcf.gz.tbi';\n    return '--tumorBam ' + inputs.input_tumor_cram.path + std + mv_cmd;\n  }\n  else{\n    var mv_cmd = mv + 'somaticSV.vcf.gz ' + inputs.output_basename + '.manta.somaticSV.vcf.gz' + mv + 'somaticSV.vcf.gz.tbi ' + inputs.output_basename + '.manta.somaticSV.vcf.gz.tbi' + mv + 'candidateSmallIndels.vcf.gz ' + inputs.output_basename + '.manta.candidateSmallIndels.vcf.gz' + mv + 'candidateSmallIndels.vcf.gz.tbi ' + inputs.output_basename + '.manta.candidateSmallIndels.vcf.gz.tbi';\n    return '--tumorBam ' + inputs.input_tumor_cram.path + ' --normalBam ' + inputs.input_normal_cram.path + std + mv_cmd;\n  }\n}",
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=InputSelector(input_to_select="cores", type_hint=File()),
    memory="<expr>inputs.ram * 1000</expr>",
    doc="Calls structural variants.  Tool designed to pick correct run mode based on if tumor, normal, or both crams are given",
)
Bwa_Index_V0_1_0 = CommandToolBuilder(
    tool="bwa_index",
    base_command=[],
    inputs=[
        ToolInput(
            tag="generate_bwa_indexes",
            input_type=Boolean(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_alt",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_amb",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_ann",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_bwt",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_fasta",
            input_type=File(),
            position=2,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_pac",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_sa",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
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
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.64.amb"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="ann",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.64.ann"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="bwt",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.64.bwt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="pac",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.64.pac"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="sa",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.64.sa"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/bwa:0.7.17-dev",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="<expr>inputs.input_alt && inputs.input_amb && inputs.input_ann && inputs.input_bwt && inputs.input_pac && inputs.input_sa ? 'echo bwa' : inputs.generate_bwa_indexes ? 'bwa' : 'echo bwa'</expr>",
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="index -6 -a bwtsw ",
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
    ],
    doc="This tool conditionally generates the bwa 64 indexes for an input fasta file using bwa index.\nThe tool will generate the indexes only of generate_bwa_indexes is set to true AND any of the alt,\namb, ann, bwt, pac, or sa files is missing.\nThe tool returns the six indexes as its output.",
)
Picard_Createsequencedictionary_V0_1_0 = CommandToolBuilder(
    tool="picard_createsequencedictionary",
    base_command=[],
    inputs=[
        ToolInput(
            tag="input_dict",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_fasta",
            input_type=File(),
            position=2,
            prefix="-R",
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="dict",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.dict"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.1.7.0R",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="<expr>inputs.input_dict ? 'echo java -jar /gatk-package-4.1.7.0-local.jar' : 'java -jar /gatk-package-4.1.7.0-local.jar' </expr>",
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="CreateSequenceDictionary",
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
    ],
    doc="This tool conditionally creats a sequence dictionary from an input fasta using Picard CreateSequenceDictionary.\nThe tool will only generate the index if an the input_dict is not passed.\nThe tool returnts the dict as its only output.",
)
Samtools_Faidx_V0_1_0 = CommandToolBuilder(
    tool="samtools_faidx",
    base_command=[],
    inputs=[
        ToolInput(
            tag="input_fasta",
            input_type=File(),
            position=1,
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
            tag="fai",
            output_type=File(),
            selector=WildcardSelector(wildcard="*.fai"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/samtools:1.9",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="<expr>inputs.input_index ? 'echo samtools faidx' : 'samtools faidx' </expr>",
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    doc="This tool takes an input fasta and optionally a input index for the input fasta.\nIf the index is not provided this tool will generate one.\nFinally the tool will return the input reference file with the index (generated or provided) as a secondaryFile.",
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
                secondaries=[
                    "${var arr = []; for (i = 0; i < inputs.secondary_files.length; i++) { if (inputs.secondary_files[i]) { arr.push(inputs.secondary_files[i].basename) } }; return arr}"
                ]
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
Mode_Defaults_V0_1_0 = CommandToolBuilder(
    tool="mode_defaults",
    base_command="echo",
    inputs=[
        ToolInput(
            tag="cnvkit_wgs_mode",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="exome_flag",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="i_flag",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_mode", input_type=String(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="lancet_padding",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="lancet_window",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="vardict_padding",
            input_type=Int(optional=True),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="out_cnvkit_wgs_mode",
            output_type=String(optional=True),
            selector="${\n  if (inputs.cnvkit_wgs_mode) { return inputs.cnvkit_wgs_mode }\n  else if (inputs.input_mode == 'WGS') { return 'Y' }\n  else if (inputs.input_mode == 'WXS') { return 'N' }\n}",
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="out_exome_flag",
            output_type=String(optional=True),
            selector="${\n  if (inputs.exome_flag) { return inputs.exome_flag }\n  else if (inputs.input_mode == 'WGS') { return 'N' }\n  else if (inputs.input_mode == 'WXS') { return 'Y' }\n}",
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="out_i_flag",
            output_type=String(optional=True),
            selector="${\n  if (inputs.i_flag) { return inputs.i_flag }\n  else if (inputs.input_mode == 'WGS') { return 'N' }\n  else if (inputs.input_mode == 'WXS') { return null }\n}",
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="out_lancet_padding",
            output_type=Int(optional=True),
            selector="${\n  if (inputs.lancet_padding) { return inputs.lancet_padding }\n  else if (inputs.input_mode == 'WGS') { return 300 }\n  else if (inputs.input_mode == 'WXS') { return 0 }\n}",
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="out_lancet_window",
            output_type=Int(optional=True),
            selector="${\n  if (inputs.lancet_window) { return inputs.lancet_window }\n  else if (inputs.input_mode == 'WGS') { return 600 }\n  else if (inputs.input_mode == 'WXS') { return 600 }\n}",
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="out_vardict_padding",
            output_type=Int(optional=True),
            selector="${\n  if (inputs.vardict_padding) { return inputs.vardict_padding }\n  else if (inputs.input_mode == 'WGS') { return 150 }\n  else if (inputs.input_mode == 'WXS') { return 0 }\n}",
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="ubuntu:latest",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "Selecting {JANIS_CWL_TOKEN_1} default values",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="input_mode", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
        )
    ],
    doc="Selects the appropriate defaults based on given the mode",
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
Kfdrc_Prepare_Reference = WorkflowBuilder(identifier="kfdrc_prepare_reference",)

Kfdrc_Prepare_Reference.input(
    "generate_bwa_indexes", Boolean(optional=True),
)

Kfdrc_Prepare_Reference.input(
    "input_alt", File(optional=True),
)

Kfdrc_Prepare_Reference.input(
    "input_amb", File(optional=True),
)

Kfdrc_Prepare_Reference.input(
    "input_ann", File(optional=True),
)

Kfdrc_Prepare_Reference.input(
    "input_bwt", File(optional=True),
)

Kfdrc_Prepare_Reference.input(
    "input_dict", File(optional=True),
)

Kfdrc_Prepare_Reference.input(
    "input_fai", File(optional=True),
)

Kfdrc_Prepare_Reference.input(
    "input_fasta", File(),
)

Kfdrc_Prepare_Reference.input(
    "input_pac", File(optional=True),
)

Kfdrc_Prepare_Reference.input(
    "input_sa", File(optional=True),
)


Kfdrc_Prepare_Reference.step(
    "bwa_index",
    Bwa_Index_V0_1_0(
        generate_bwa_indexes=Kfdrc_Prepare_Reference.generate_bwa_indexes,
        input_alt=Kfdrc_Prepare_Reference.input_alt,
        input_amb=Kfdrc_Prepare_Reference.input_amb,
        input_ann=Kfdrc_Prepare_Reference.input_ann,
        input_bwt=Kfdrc_Prepare_Reference.input_bwt,
        input_fasta=Kfdrc_Prepare_Reference.input_fasta,
        input_pac=Kfdrc_Prepare_Reference.input_pac,
        input_sa=Kfdrc_Prepare_Reference.input_sa,
    ),
)


Kfdrc_Prepare_Reference.step(
    "picard_create_sequence_dictionary",
    Picard_Createsequencedictionary_V0_1_0(
        input_dict=Kfdrc_Prepare_Reference.input_dict,
        input_fasta=Kfdrc_Prepare_Reference.input_fasta,
    ),
)


Kfdrc_Prepare_Reference.step(
    "samtools_faidx",
    Samtools_Faidx_V0_1_0(
        input_fasta=Kfdrc_Prepare_Reference.input_fasta,
        input_index=Kfdrc_Prepare_Reference.input_fai,
    ),
)


Kfdrc_Prepare_Reference.step(
    "bundle_secondaries",
    Bundle_Secondaryfiles_V0_1_0(
        primary_file=Kfdrc_Prepare_Reference.input_fasta,
        secondary_files=[
            Kfdrc_Prepare_Reference.samtools_faidx.fai,
            Kfdrc_Prepare_Reference.picard_create_sequence_dictionary.dict,
            Kfdrc_Prepare_Reference.bwa_index.alt,
            Kfdrc_Prepare_Reference.bwa_index.amb,
            Kfdrc_Prepare_Reference.bwa_index.ann,
            Kfdrc_Prepare_Reference.bwa_index.bwt,
            Kfdrc_Prepare_Reference.bwa_index.pac,
            Kfdrc_Prepare_Reference.bwa_index.sa,
        ],
    ),
)

Kfdrc_Prepare_Reference.output(
    "indexed_fasta",
    source=Kfdrc_Prepare_Reference.bundle_secondaries.outp,
    output_name=True,
)

Kfdrc_Prepare_Reference.output(
    "reference_dict",
    source=Kfdrc_Prepare_Reference.picard_create_sequence_dictionary.dict,
    output_name=True,
)

Kfdrc_Manta_Sub_Wf = WorkflowBuilder(identifier="kfdrc_manta_sub_wf",)

Kfdrc_Manta_Sub_Wf.input(
    "hg38_strelka_bed", VcfTabix(),
)

Kfdrc_Manta_Sub_Wf.input(
    "indexed_reference_fasta",
    GenericFileWithSecondaries(secondaries=[".fai", "^.dict"]),
)

Kfdrc_Manta_Sub_Wf.input(
    "input_normal_aligned",
    GenericFileWithSecondaries(
        secondaries=[
            "${\n  var dpath = self.location.replace(self.basename, '')\n  if(self.nameext == '.bam'){\n    return {'location': dpath+self.nameroot+'.bai', 'class': 'File'}\n  }\n  else{\n    return {'location': dpath+self.basename+'.crai', 'class': 'File'}\n  }\n}\n"
        ]
    ),
    doc=InputDocumentation(doc="normal BAM or CRAM"),
)

Kfdrc_Manta_Sub_Wf.input(
    "input_normal_name", String(),
)

Kfdrc_Manta_Sub_Wf.input(
    "input_tumor_aligned",
    GenericFileWithSecondaries(
        secondaries=[
            "${\n  var dpath = self.location.replace(self.basename, '')\n  if(self.nameext == '.bam'){\n    return {'location': dpath+self.nameroot+'.bai', 'class': 'File'}\n  }\n  else{\n    return {'location': dpath+self.basename+'.crai', 'class': 'File'}\n  }\n}\n"
        ]
    ),
    doc=InputDocumentation(doc="tumor BAM or CRAM"),
)

Kfdrc_Manta_Sub_Wf.input(
    "input_tumor_name", String(),
)

Kfdrc_Manta_Sub_Wf.input(
    "manta_cores", Int(optional=True),
)

Kfdrc_Manta_Sub_Wf.input(
    "manta_memory", Int(optional=True),
)

Kfdrc_Manta_Sub_Wf.input(
    "output_basename", String(),
)

Kfdrc_Manta_Sub_Wf.input(
    "reference_dict", File(),
)

Kfdrc_Manta_Sub_Wf.input(
    "select_vars_mode",
    String(optional=True),
    default="gatk",
    doc=InputDocumentation(
        doc="Choose 'gatk' for SelectVariants tool, or 'grep' for grep expression"
    ),
)

Kfdrc_Manta_Sub_Wf.input(
    "vep_cache", File(),
)

Kfdrc_Manta_Sub_Wf.input(
    "gatk_selectvariants_manta_tool_name", String(optional=True), default="manta",
)


Kfdrc_Manta_Sub_Wf.step(
    "manta",
    Kfdrc_Manta_Sv_V0_1_0(
        cores=Kfdrc_Manta_Sub_Wf.manta_cores,
        hg38_strelka_bed=Kfdrc_Manta_Sub_Wf.hg38_strelka_bed,
        input_normal_cram=Kfdrc_Manta_Sub_Wf.input_normal_aligned,
        input_tumor_cram=Kfdrc_Manta_Sub_Wf.input_tumor_aligned,
        output_basename=Kfdrc_Manta_Sub_Wf.output_basename,
        ram=Kfdrc_Manta_Sub_Wf.manta_memory,
        reference=Kfdrc_Manta_Sub_Wf.indexed_reference_fasta,
    ),
)


Kfdrc_Manta_Sub_Wf.step(
    "rename_manta_samples",
    Bcftools_Reheader_Vcf_V0_1_0(
        input_normal_name=Kfdrc_Manta_Sub_Wf.input_normal_name,
        input_tumor_name=Kfdrc_Manta_Sub_Wf.input_tumor_name,
        input_vcf=Kfdrc_Manta_Sub_Wf.manta.output_sv,
    ),
)


Kfdrc_Manta_Sub_Wf.step(
    "gatk_selectvariants_manta",
    Gatk4_Selectvariants_V0_1_0(
        input_vcf=Kfdrc_Manta_Sub_Wf.rename_manta_samples.reheadered_vcf,
        mode=Kfdrc_Manta_Sub_Wf.select_vars_mode,
        output_basename=Kfdrc_Manta_Sub_Wf.output_basename,
        tool_name=Kfdrc_Manta_Sub_Wf.gatk_selectvariants_manta_tool_name,
    ),
)

Kfdrc_Manta_Sub_Wf.output(
    "manta_pass_vcf",
    source=Kfdrc_Manta_Sub_Wf.gatk_selectvariants_manta.pass_vcf,
    output_name=True,
)

Kfdrc_Manta_Sub_Wf.output(
    "manta_prepass_vcf",
    source=Kfdrc_Manta_Sub_Wf.rename_manta_samples.reheadered_vcf,
    output_name=True,
)

Kfdrc_Manta_Sub_Wf.output(
    "manta_small_indels",
    source=Kfdrc_Manta_Sub_Wf.manta.small_indels,
    output_name=True,
)

Kfdrc_Strelka2_Sub_Wf = WorkflowBuilder(identifier="kfdrc_strelka2_sub_wf",)

Kfdrc_Strelka2_Sub_Wf.input(
    "exome_flag",
    String(optional=True),
    doc=InputDocumentation(doc="set to 'Y' for exome mode"),
)

Kfdrc_Strelka2_Sub_Wf.input(
    "hg38_strelka_bed", VcfTabix(),
)

Kfdrc_Strelka2_Sub_Wf.input(
    "indexed_reference_fasta",
    GenericFileWithSecondaries(secondaries=[".fai", "^.dict"]),
)

Kfdrc_Strelka2_Sub_Wf.input(
    "input_normal_aligned",
    GenericFileWithSecondaries(
        secondaries=[
            "${\n  var dpath = self.location.replace(self.basename, '')\n  if(self.nameext == '.bam'){\n    return {'location': dpath+self.nameroot+'.bai', 'class': 'File'}\n  }\n  else{\n    return {'location': dpath+self.basename+'.crai', 'class': 'File'}\n  }\n}\n"
        ]
    ),
    doc=InputDocumentation(doc="normal BAM or CRAM"),
)

Kfdrc_Strelka2_Sub_Wf.input(
    "input_normal_name", String(),
)

Kfdrc_Strelka2_Sub_Wf.input(
    "input_tumor_aligned",
    GenericFileWithSecondaries(
        secondaries=[
            "${\n  var dpath = self.location.replace(self.basename, '')\n  if(self.nameext == '.bam'){\n    return {'location': dpath+self.nameroot+'.bai', 'class': 'File'}\n  }\n  else{\n    return {'location': dpath+self.basename+'.crai', 'class': 'File'}\n  }\n}\n"
        ]
    ),
    doc=InputDocumentation(doc="tumor BAM or CRAM"),
)

Kfdrc_Strelka2_Sub_Wf.input(
    "input_tumor_name", String(),
)

Kfdrc_Strelka2_Sub_Wf.input(
    "manta_small_indels", VcfTabix(optional=True),
)

Kfdrc_Strelka2_Sub_Wf.input(
    "output_basename", String(),
)

Kfdrc_Strelka2_Sub_Wf.input(
    "reference_dict", File(),
)

Kfdrc_Strelka2_Sub_Wf.input(
    "select_vars_mode",
    String(optional=True),
    default="gatk",
    doc=InputDocumentation(
        doc="Choose 'gatk' for SelectVariants tool, or 'grep' for grep expression"
    ),
)

Kfdrc_Strelka2_Sub_Wf.input(
    "use_manta_small_indels", Boolean(optional=True), default=False,
)

Kfdrc_Strelka2_Sub_Wf.input(
    "vep_cache", File(),
)

Kfdrc_Strelka2_Sub_Wf.input(
    "vep_ref_build",
    String(optional=True),
    default="GRCh38",
    doc=InputDocumentation(doc="Genome ref build used, should line up with cache."),
)

Kfdrc_Strelka2_Sub_Wf.input(
    "merge_strelka2_vcf_tool_name", String(optional=True), default="strelka2",
)

Kfdrc_Strelka2_Sub_Wf.input(
    "gatk_selectvariants_strelka2_tool_name", String(optional=True), default="strelka2",
)

Kfdrc_Strelka2_Sub_Wf.input(
    "vep_annot_strelka2_tool_name", String(optional=True), default="strelka2_somatic",
)


Kfdrc_Strelka2_Sub_Wf.step(
    "strelka2",
    Strelka2_V0_1_0(
        exome_flag=Kfdrc_Strelka2_Sub_Wf.exome_flag,
        hg38_strelka_bed=Kfdrc_Strelka2_Sub_Wf.hg38_strelka_bed,
        input_normal_aligned=Kfdrc_Strelka2_Sub_Wf.input_normal_aligned,
        input_tumor_aligned=Kfdrc_Strelka2_Sub_Wf.input_tumor_aligned,
        manta_small_indels=Kfdrc_Strelka2_Sub_Wf.manta_small_indels,
        reference=Kfdrc_Strelka2_Sub_Wf.indexed_reference_fasta,
        use_manta_small_indels=Kfdrc_Strelka2_Sub_Wf.use_manta_small_indels,
    ),
)


Kfdrc_Strelka2_Sub_Wf.step(
    "merge_strelka2_vcf",
    Gatk4_Mergevcfs_V0_1_0(
        input_vcfs=[
            Kfdrc_Strelka2_Sub_Wf.strelka2.output_snv,
            Kfdrc_Strelka2_Sub_Wf.strelka2.output_indel,
        ],
        output_basename=Kfdrc_Strelka2_Sub_Wf.output_basename,
        reference_dict=Kfdrc_Strelka2_Sub_Wf.reference_dict,
        tool_name=Kfdrc_Strelka2_Sub_Wf.merge_strelka2_vcf_tool_name,
    ),
)


Kfdrc_Strelka2_Sub_Wf.step(
    "rename_strelka_samples",
    Bcftools_Reheader_Vcf_V0_1_0(
        input_normal_name=Kfdrc_Strelka2_Sub_Wf.input_normal_name,
        input_tumor_name=Kfdrc_Strelka2_Sub_Wf.input_tumor_name,
        input_vcf=Kfdrc_Strelka2_Sub_Wf.merge_strelka2_vcf.merged_vcf,
    ),
)


Kfdrc_Strelka2_Sub_Wf.step(
    "gatk_selectvariants_strelka2",
    Gatk4_Selectvariants_V0_1_0(
        input_vcf=Kfdrc_Strelka2_Sub_Wf.rename_strelka_samples.reheadered_vcf,
        mode=Kfdrc_Strelka2_Sub_Wf.select_vars_mode,
        output_basename=Kfdrc_Strelka2_Sub_Wf.output_basename,
        tool_name=Kfdrc_Strelka2_Sub_Wf.gatk_selectvariants_strelka2_tool_name,
    ),
)


Kfdrc_Strelka2_Sub_Wf.step(
    "vep_annot_strelka2",
    Kfdrc_Vep_Somatic_Annotate_Maf_V0_1_0(
        cache=Kfdrc_Strelka2_Sub_Wf.vep_cache,
        input_vcf=Kfdrc_Strelka2_Sub_Wf.gatk_selectvariants_strelka2.pass_vcf,
        normal_id=Kfdrc_Strelka2_Sub_Wf.input_normal_name,
        output_basename=Kfdrc_Strelka2_Sub_Wf.output_basename,
        ref_build=Kfdrc_Strelka2_Sub_Wf.vep_ref_build,
        reference=Kfdrc_Strelka2_Sub_Wf.indexed_reference_fasta,
        tool_name=Kfdrc_Strelka2_Sub_Wf.vep_annot_strelka2_tool_name,
        tumor_id=Kfdrc_Strelka2_Sub_Wf.input_tumor_name,
    ),
)

Kfdrc_Strelka2_Sub_Wf.output(
    "strelka2_prepass_vcf",
    source=Kfdrc_Strelka2_Sub_Wf.rename_strelka_samples.reheadered_vcf,
    output_name=True,
)

Kfdrc_Strelka2_Sub_Wf.output(
    "strelka2_vep_maf",
    source=Kfdrc_Strelka2_Sub_Wf.vep_annot_strelka2.output_maf,
    output_name=True,
)

Kfdrc_Strelka2_Sub_Wf.output(
    "strelka2_vep_tbi",
    source=Kfdrc_Strelka2_Sub_Wf.vep_annot_strelka2.output_tbi,
    output_name=True,
)

Kfdrc_Strelka2_Sub_Wf.output(
    "strelka2_vep_vcf",
    source=Kfdrc_Strelka2_Sub_Wf.vep_annot_strelka2.output_vcf,
    output_name=True,
)

Samtools_Cram2Bam_Plus_Calmd_V0_1_0 = CommandToolBuilder(
    tool="samtools_cram2bam_plus_calmd",
    base_command=["/bin/bash -c"],
    inputs=[
        ToolInput(
            tag="input_reads", input_type=File(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="reference", input_type=FastaFai(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="threads",
            input_type=Int(optional=True),
            default=16,
            doc=InputDocumentation(doc=None, quality=InputQualityType.configuration),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="bam_file",
            output_type=GenericFileWithSecondaries(secondaries=["^.bai"]),
            selector=WildcardSelector(wildcard="*.bam"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/samtools:1.9",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="set -eo pipefail\n${\n  var bam_name = inputs.input_reads.nameroot + '.bam';\n  var cmd = 'samtools view -@ ' + inputs.threads + ' -h -T ' + inputs.reference.path + ' ' + inputs.input_reads.path\n  + ' | samtools calmd -@ ' + inputs.threads + ' -b --reference ' + inputs.reference.path + ' - > ' + bam_name + ';';\n  if(inputs.input_reads.basename == bam_name){\n    cmd = '>&2 echo input reads already have bam extension, indexing and passing through; cp ' + inputs.input_reads.path\n    + ' ' + bam_name + ';'\n  }\n  cmd += 'samtools index -@ ' + inputs.threads + ' ' + bam_name + ' ' + inputs.input_reads.nameroot + '.bai;'\n  return cmd;\n}",
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=InputSelector(input_to_select="threads", type_hint=File()),
    memory=12000,
)
Mode_Selector_V0_1_0 = CommandToolBuilder(
    tool="mode_selector",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(
            tag="input_mode", input_type=String(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="wgs_input",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="wxs_input",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=String(),
            selector="${\n  if (inputs.input_mode == 'WGS') { return inputs.wgs_input }\n  else if (inputs.input_mode == 'WXS') { return inputs.wxs_input }\n}",
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/ubuntu:18.04",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="set -eo pipefail\n${\n    var cmd = ' >&2 echo Choosing inputs based on mode;';\n    if (inputs.input_mode == 'WGS' && inputs.wgs_input == null){\n      return 'echo WGS run requires wgs_input >&2 && exit 1;'\n    }\n    else if (inputs.input_mode == 'WXS' && inputs.wxs_input == null){\n      return 'echo WXS run requires wxs_input >&2 && exit 1;'\n    }\n    return cmd;\n}\n ",
            doc=InputDocumentation(doc=None),
        )
    ],
    doc="Selects the appropriate input to serve as the output given the mode",
)
Bedtools_Intersect_V0_1_0 = CommandToolBuilder(
    tool="bedtools_intersect",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(
            tag="flag",
            input_type=String(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_bed_file", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_vcf",
            input_type=VcfTabix(optional=True),
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
            tag="intersected_vcf",
            output_type=VcfTabix(optional=True),
            selector=WildcardSelector(wildcard="*.bed_intersect.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/vcfutils:latest",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="set -eo pipefail\n${\n    var cmd = ' >&2 echo checking if skip intersect flag given;';\n    var out_vcf = inputs.output_basename + '.bed_intersect.vcf';\n    if (inputs.input_vcf == null){\n      return 'echo No vcf provided, skipping >&2 && exit 0;'\n    }\n    if (inputs.flag != 'N'){\n      cmd += 'bedtools intersect -a ' + inputs.input_vcf.path + ' -b ' + inputs.input_bed_file.path + ' -header -wa > ' + out_vcf + ' && ';\n      cmd +=  'bgzip ' + out_vcf + ' && tabix ' + out_vcf + '.gz;';\n    }else{\n      cmd += ' >&2 echo Value N given, passing through vcf; cp ' + inputs.input_vcf.path + ' ' + out_vcf + '.gz;'\n      cmd += 'tabix ' + out_vcf + '.gz;'\n    }\n    return cmd;\n}",
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=4,
    memory=8000,
    doc="Intersect VCF with bedtools intersect, i.e. for WXS filter germline on unpadded intervals to ensure accurate CNV calls",
)
Kfdrc_Gatk_Variantfiltration_V0_1_0 = CommandToolBuilder(
    tool="kfdrc_gatk_variantfiltration",
    base_command=[],
    inputs=[
        ToolInput(
            tag="input_vcf",
            input_type=VcfTabix(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference_fasta", input_type=File(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="filtered_pass_vcf",
            output_type=VcfTabix(optional=True),
            selector=WildcardSelector(wildcard="*.gatk.hardfiltered.PASS.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="filtered_vcf",
            output_type=VcfTabix(optional=True),
            selector=WildcardSelector(wildcard="*.gatk.hardfiltered.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.1.1.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "${\n  if (inputs.input_vcf == null){\n    return 'echo No vcf provided, skipping >&2 && exit 0;';\n  }\n  else{\n    return 'echo Filtering vcf >&2 && ';\n  }\n} /gatk --java-options '-Xmx7000m' SelectVariants --exclude-filtered TRUE -select-type SNP ${\n  if (inputs.input_vcf != null){\n    return '-V ' + inputs.input_vcf.path;\n  }\n} -O snp_pass.vcf.gz\n/gatk VariantFiltration --java-options '-Xmx7000m' --filter-name GATK_QD --filter-expression 'QD < 2.0' --filter-name GATK_FS --filter-expression 'FS > 60.0' --filter-name GATK_MQ --filter-expression 'MQ < 40.0' --filter-name GATK_MQRankSum --filter-expression 'MQRankSum < -12.5' --filter-name GATK_ReadPosRankSum --filter-expression 'ReadPosRankSum < -8.0' --filter-name KFDRC_DP10 --filter-expression 'DP < 10' -V snp_pass.vcf.gz -O {JANIS_CWL_TOKEN_1}.gatk.hardfiltered.vcf.gz\n/gatk SelectVariants --exclude-filtered TRUE -V {JANIS_CWL_TOKEN_1}.gatk.hardfiltered.vcf.gz -O {JANIS_CWL_TOKEN_1}.gatk.hardfiltered.PASS.vcf.gz",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=2,
    memory=8000,
)
Gatk4_Intervallist2Bed_V0_1_0 = CommandToolBuilder(
    tool="gatk4_intervallist2bed",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(
            tag="bands",
            input_type=Int(),
            doc=InputDocumentation(doc=None, quality=InputQualityType.configuration),
        ),
        ToolInput(
            tag="break_by_chr",
            input_type=String(optional=True),
            default="N",
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="exome_flag",
            input_type=String(optional=True),
            default="N",
            doc=InputDocumentation(doc=None, quality=InputQualityType.configuration),
        ),
        ToolInput(
            tag="interval_list",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference_dict",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="scatter_ct",
            input_type=Int(),
            doc=InputDocumentation(doc=None, quality=InputQualityType.configuration),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=Array(t=File(), optional=True),
            selector=WildcardSelector(wildcard="*.bed"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.1.1.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="set -eo pipefail\n${\n  if (inputs.interval_list == null) {\n    return 'echo No interval list exiting without input >&2 && exit 0;';\n  }\n  else {\n    var cmd = '';\n    if (inputs.interval_list.nameext == '.interval_list'){\n      cmd = 'LIST=' + inputs.interval_list.path + ';';\n    }\n    else{\n      cmd = '/gatk BedToIntervalList -I ' + inputs.interval_list.path + ' -O ' + inputs.interval_list.nameroot \n      + '.interval_list -SD ' + inputs.reference_dict.path + '; LIST=' + inputs.interval_list.nameroot \n      + '.interval_list;';\n\n    }\n    if (inputs.exome_flag == 'Y'){\n        cmd += 'BANDS=0;';\n      }\n      \n    else{\n      cmd += 'BANDS=' + inputs.bands + ';';\n    }\n    return cmd;\n  }\n}\n${\n  if (inputs.break_by_chr == 'N'){\n    var cmd = '/gatk IntervalListTools --java-options '-Xmx2000m' --SCATTER_COUNT=' + inputs.scatter_ct + ' --SUBDIVISION_MODE=BALANCING_WITHOUT_INTERVAL_SUBDIVISION_WITH_OVERFLOW --UNIQUE=true --SORT=true --BREAK_BANDS_AT_MULTIPLES_OF=$BANDS --INPUT=$LIST --OUTPUT=.;'\n    cmd += 'CT=`find . -name 'temp_0*' | wc -l`;';\n    cmd += 'seq -f '%04g' $CT | xargs -I N -P 4 /gatk IntervalListToBed --java-options -Xmx100m -I temp_N_of_$CT/scattered.interval_list -O temp_N_of_$CT/scattered.interval_list.N.bed;';\n    cmd += 'mv temp_0*/*.bed .;';\n  }\n  else{\n    cmd = 'mkdir intvl_by_chr;'\n    cmd += '/gatk IntervalListTools --java-options '-Xmx2000m' --SCATTER_COUNT=' + inputs.scatter_ct + ' --SUBDIVISION_MODE=BALANCING_WITHOUT_INTERVAL_SUBDIVISION_WITH_OVERFLOW --UNIQUE=true --SORT=true --BREAK_BANDS_AT_MULTIPLES_OF=$BANDS --INPUT=$LIST --OUTPUT=intvl_by_chr/scattered.interval_list;';\n    cmd += '/gatk IntervalListToBed --java-options -Xmx100m -I intvl_by_chr/scattered.interval_list -O intvl_by_chr/scattered.interval_list.bed;'\n    cmd += 'cut -f 1 intvl_by_chr/scattered.interval_list.bed | uniq | xargs -ICM sh -c 'grep -P 'CM\\t' intvl_by_chr/scattered.interval_list.bed > CM_intervals.bed';';\n  }\n  return cmd;\n}",
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=2000,
)
Python_Vardict_Interval_Split_V0_1_0 = CommandToolBuilder(
    tool="python_vardict_interval_split",
    base_command=["python", "-c"],
    inputs=[
        ToolInput(
            tag="bp_target",
            input_type=Int(optional=True),
            default=60000000,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="intvl_target_size",
            input_type=Int(optional=True),
            default=20000,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="wgs_bed_file", input_type=File(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="split_intervals_bed",
            output_type=Array(t=File()),
            selector=WildcardSelector(wildcard="*.bed"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/python:2.7.13",
    version="v0.1.0",
    friendly_name="Create intervals for VarDict",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "def main():\n    import sys\n    bp_target = {JANIS_CWL_TOKEN_3}\n    intvl_target_size = {JANIS_CWL_TOKEN_1}\n    bed_file = open('{JANIS_CWL_TOKEN_2}')\n\n    i=0\n    intvl_set = {}\n    cur_size = 0\n    for cur_intvl in bed_file:\n        f = 0\n        if i not in intvl_set:\n            intvl_set[i] = []\n        # chr(9) is ASCII code for tab; chr(10) is ASCII code for newline\n        data = cur_intvl.rstrip(chr(10)).split(chr(9))\n        (chrom, start, end) = (data[0], data[1], data[2])\n        intvl_size = int(end) - int(start)\n        if intvl_size >= bp_target:\n            if len(intvl_set[i]) != 0:\n                i += 1\n                intvl_set[i] = []\n                f = 1\n        elif cur_size + intvl_size > bp_target:\n            if len(intvl_set[i]) != 0:\n                i += 1\n                intvl_set[i] = []\n                cur_size = intvl_size\n        else:\n            cur_size += intvl_size\n        intvl_set[i].append([chrom, start, end])\n        if f == 1:\n            i += 1\n            cur_size = 0\n    bed_file.close()\n\n    for set_i, invtl_list in sorted(intvl_set.items()):\n        set_size = 0\n        out = open('set_' + str(set_i) + '.bed', 'w')\n        for intervals in invtl_list:\n            (chrom, start, end) = (intervals[0], intervals[1], intervals[2])\n            intvl_size = int(end) - int(start)\n            set_size += intvl_size\n            for j in range(int(start), int(end), intvl_target_size):\n                new_end = j + intvl_target_size\n                if new_end > int(end):\n                    new_end = end\n                out.write(chrom + chr(9) + str(j) + chr(9) + str(new_end) + chr(10))\n        sys.stderr.write('Set ' + str(set_i) + ' size:' + chr(9) + str(set_size) + chr(10))\n        out.close()\n\nif __name__ == '__main__':\n    main()",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="intvl_target_size", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="wgs_bed_file", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="bp_target", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=True,
        )
    ],
    doc="This tool takes in an interval list with the WGS coords split by N regions. It splits the bed files into bed files with a max total number of base bairs, unless the regions is already larger, it stays in it's own file. Then within the split lists, intervals are split the specified chunks for easier processing by vardict.  This method prevents FP calls caused by regions with valid ACGT bases from being split between interval lists.  For example, for hg38 canonical chromosomes, using bp_target=60000000 and intvl_target_size=20000 will yield about 55 bed files, each with about 60M bp worth of coverage (unless the interval was already larger, it will be in it's own list), split into 20kb chunks.",
)
Kfdrc_Cnvkit_Sub_Wf = WorkflowBuilder(identifier="kfdrc_cnvkit_sub_wf",)

Kfdrc_Cnvkit_Sub_Wf.input(
    "annotation_file", File(), doc=InputDocumentation(doc="refFlat.txt file"),
)

Kfdrc_Cnvkit_Sub_Wf.input(
    "b_allele_vcf",
    File(optional=True),
    doc=InputDocumentation(doc="b allele germline vcf, if available"),
)

Kfdrc_Cnvkit_Sub_Wf.input(
    "capture_regions",
    File(optional=True),
    doc=InputDocumentation(doc="target regions for WES"),
)

Kfdrc_Cnvkit_Sub_Wf.input(
    "cnvkit_cnn_input",
    File(optional=True),
    doc=InputDocumentation(doc="If running using an existing .cnn, supply here"),
)

Kfdrc_Cnvkit_Sub_Wf.input(
    "input_normal_aligned", GenericFileWithSecondaries(secondaries=["^.bai"]),
)

Kfdrc_Cnvkit_Sub_Wf.input(
    "input_tumor_aligned", GenericFileWithSecondaries(secondaries=["^.bai"]),
)

Kfdrc_Cnvkit_Sub_Wf.input(
    "normal_sample_name", String(), doc=InputDocumentation(doc="For theta2 input"),
)

Kfdrc_Cnvkit_Sub_Wf.input(
    "output_basename", String(),
)

Kfdrc_Cnvkit_Sub_Wf.input(
    "reference", FastaFai(),
)

Kfdrc_Cnvkit_Sub_Wf.input(
    "sex",
    String(),
    doc=InputDocumentation(
        doc="Set sample sex.  CNVkit isn't always great at guessing it"
    ),
)

Kfdrc_Cnvkit_Sub_Wf.input(
    "threads", Int(optional=True), default=16,
)

Kfdrc_Cnvkit_Sub_Wf.input(
    "tumor_sample_name",
    String(),
    doc=InputDocumentation(doc="For seg file output and theta2 input"),
)

Kfdrc_Cnvkit_Sub_Wf.input(
    "wgs_mode",
    String(optional=True),
    doc=InputDocumentation(doc="for WGS mode, input Y. leave blank for hybrid mode"),
)


Kfdrc_Cnvkit_Sub_Wf.step(
    "cnvkit",
    Cnvkit_Batch_V0_1_0(
        annotation_file=Kfdrc_Cnvkit_Sub_Wf.annotation_file,
        b_allele_vcf=Kfdrc_Cnvkit_Sub_Wf.b_allele_vcf,
        capture_regions=Kfdrc_Cnvkit_Sub_Wf.capture_regions,
        cnvkit_cnn=Kfdrc_Cnvkit_Sub_Wf.cnvkit_cnn_input,
        input_control=Kfdrc_Cnvkit_Sub_Wf.input_normal_aligned,
        input_sample=Kfdrc_Cnvkit_Sub_Wf.input_tumor_aligned,
        output_basename=Kfdrc_Cnvkit_Sub_Wf.output_basename,
        reference=Kfdrc_Cnvkit_Sub_Wf.reference,
        sex=Kfdrc_Cnvkit_Sub_Wf.sex,
        threads=Kfdrc_Cnvkit_Sub_Wf.threads,
        tumor_sample_name=Kfdrc_Cnvkit_Sub_Wf.tumor_sample_name,
        wgs_mode=Kfdrc_Cnvkit_Sub_Wf.wgs_mode,
    ),
)

Kfdrc_Cnvkit_Sub_Wf.output(
    "cnvkit_calls", source=Kfdrc_Cnvkit_Sub_Wf.cnvkit.output_calls, output_name=True,
)

Kfdrc_Cnvkit_Sub_Wf.output(
    "cnvkit_cnn_output", source=Kfdrc_Cnvkit_Sub_Wf.cnvkit.output_cnn, output_name=True,
)

Kfdrc_Cnvkit_Sub_Wf.output(
    "cnvkit_cnr", source=Kfdrc_Cnvkit_Sub_Wf.cnvkit.output_cnr, output_name=True,
)

Kfdrc_Cnvkit_Sub_Wf.output(
    "cnvkit_gainloss",
    source=Kfdrc_Cnvkit_Sub_Wf.cnvkit.output_gainloss,
    output_name=True,
)

Kfdrc_Cnvkit_Sub_Wf.output(
    "cnvkit_metrics",
    source=Kfdrc_Cnvkit_Sub_Wf.cnvkit.output_metrics,
    output_name=True,
)

Kfdrc_Cnvkit_Sub_Wf.output(
    "cnvkit_seg", source=Kfdrc_Cnvkit_Sub_Wf.cnvkit.output_seg, output_name=True,
)

Kfdrc_Controlfreec_Sub_Wf = WorkflowBuilder(identifier="kfdrc_controlfreec_sub_wf",)

Kfdrc_Controlfreec_Sub_Wf.input(
    "b_allele",
    File(optional=True),
    doc=InputDocumentation(
        doc="germline calls, needed for BAF.  VarDict input recommended.  Tool will prefilter for germline and pass if expression given"
    ),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "capture_regions",
    File(optional=True),
    doc=InputDocumentation(doc="If not WGS, provide "),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "cfree_sex",
    String(optional=True),
    doc=InputDocumentation(doc="If known, XX for female, XY for male"),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "chr_len",
    File(),
    doc=InputDocumentation(
        doc="TSV with chromsome names and lengths. Limit to chromosome you actually want analyzed"
    ),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "coeff_var",
    Float(optional=True),
    default=0.05,
    doc=InputDocumentation(
        doc="Coefficient of variantion to set window size.  Default 0.05 recommended"
    ),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "contamination_adjustment",
    Boolean(optional=True),
    doc=InputDocumentation(
        doc="TRUE or FALSE to have ControlFreec estimate normal contam"
    ),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "gem_mappability_file",
    File(optional=True),
    doc=InputDocumentation(
        doc="GEM mappability file to make read count adjustments with"
    ),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "indexed_reference_fasta", FastaFai(),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "input_normal_aligned", GenericFileWithSecondaries(secondaries=["^.bai"]),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "input_tumor_aligned", GenericFileWithSecondaries(secondaries=["^.bai"]),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "input_tumor_name",
    String(),
    doc=InputDocumentation(doc="Sample name to put into the converted seg file"),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "mate_copynumber_file_control",
    File(optional=True),
    doc=InputDocumentation(
        doc="Normal cpn file from previous run. If used, will override bam use"
    ),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "mate_copynumber_file_sample",
    File(optional=True),
    doc=InputDocumentation(
        doc="Tumor cpn file from previous run. If used, will override bam use"
    ),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "mate_orientation_control",
    String(optional=True),
    default="FR",
    doc=InputDocumentation(
        doc="0 (for single ends), RF (Illumina mate-pairs), FR (Illumina paired-ends), FF (SOLiD mate-pairs)"
    ),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "mate_orientation_sample",
    String(optional=True),
    default="FR",
    doc=InputDocumentation(
        doc="0 (for single ends), RF (Illumina mate-pairs), FR (Illumina paired-ends), FF (SOLiD mate-pairs)"
    ),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "min_subclone_presence",
    Float(optional=True),
    doc=InputDocumentation(
        doc="Use if you want to detect sublones. Recommend 0.2 for WGS, 0.3 for WXS"
    ),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "output_basename", String(),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "ploidy",
    Array(t=Int()),
    doc=InputDocumentation(doc="Array of ploidy possibilities for ControlFreeC to try"),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "reference_fai",
    File(),
    doc=InputDocumentation(doc="fasta index file for seg file conversion"),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "threads",
    Int(),
    doc=InputDocumentation(
        doc="Number of threads to run controlfreec.  Going above 16 is not recommended, there is no apparent added value"
    ),
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "controlfreec_normal_mini_pileup_threads", Int(optional=True), default=16,
)

Kfdrc_Controlfreec_Sub_Wf.input(
    "controlfreec_tumor_mini_pileup_threads", Int(optional=True), default=16,
)


Kfdrc_Controlfreec_Sub_Wf.step(
    "controlfreec_normal_mini_pileup",
    Controlfreec_Mini_Pileup_V0_1_0(
        input_reads=Kfdrc_Controlfreec_Sub_Wf.input_normal_aligned,
        reference=Kfdrc_Controlfreec_Sub_Wf.indexed_reference_fasta,
        snp_vcf=Kfdrc_Controlfreec_Sub_Wf.b_allele,
        threads=Kfdrc_Controlfreec_Sub_Wf.controlfreec_normal_mini_pileup_threads,
    ),
)


Kfdrc_Controlfreec_Sub_Wf.step(
    "controlfreec_tumor_mini_pileup",
    Controlfreec_Mini_Pileup_V0_1_0(
        input_reads=Kfdrc_Controlfreec_Sub_Wf.input_tumor_aligned,
        reference=Kfdrc_Controlfreec_Sub_Wf.indexed_reference_fasta,
        snp_vcf=Kfdrc_Controlfreec_Sub_Wf.b_allele,
        threads=Kfdrc_Controlfreec_Sub_Wf.controlfreec_tumor_mini_pileup_threads,
    ),
)


Kfdrc_Controlfreec_Sub_Wf.step(
    "control_free_c",
    Control_Freec_V0_1_0(
        capture_regions=Kfdrc_Controlfreec_Sub_Wf.capture_regions,
        chr_len=Kfdrc_Controlfreec_Sub_Wf.chr_len,
        coeff_var=Kfdrc_Controlfreec_Sub_Wf.coeff_var,
        contamination_adjustment=Kfdrc_Controlfreec_Sub_Wf.contamination_adjustment,
        gem_mappability_file=Kfdrc_Controlfreec_Sub_Wf.gem_mappability_file,
        mate_copynumber_file_control=Kfdrc_Controlfreec_Sub_Wf.mate_copynumber_file_control,
        mate_copynumber_file_sample=Kfdrc_Controlfreec_Sub_Wf.mate_copynumber_file_sample,
        mate_file_control=Kfdrc_Controlfreec_Sub_Wf.input_normal_aligned,
        mate_file_sample=Kfdrc_Controlfreec_Sub_Wf.input_tumor_aligned,
        mate_orientation_control=Kfdrc_Controlfreec_Sub_Wf.mate_orientation_control,
        mate_orientation_sample=Kfdrc_Controlfreec_Sub_Wf.mate_orientation_sample,
        max_threads=Kfdrc_Controlfreec_Sub_Wf.threads,
        min_subclone_presence=Kfdrc_Controlfreec_Sub_Wf.min_subclone_presence,
        mini_pileup_control=Kfdrc_Controlfreec_Sub_Wf.controlfreec_normal_mini_pileup.pileup,
        mini_pileup_sample=Kfdrc_Controlfreec_Sub_Wf.controlfreec_tumor_mini_pileup.pileup,
        ploidy=Kfdrc_Controlfreec_Sub_Wf.ploidy,
        reference=Kfdrc_Controlfreec_Sub_Wf.indexed_reference_fasta,
        sex=Kfdrc_Controlfreec_Sub_Wf.cfree_sex,
        snp_file=Kfdrc_Controlfreec_Sub_Wf.b_allele,
    ),
)


Kfdrc_Controlfreec_Sub_Wf.step(
    "convert_ratio_to_seg",
    Ubuntu_Ratio2Seg_V0_1_0(
        ctrlfreec_ratio=Kfdrc_Controlfreec_Sub_Wf.control_free_c.ratio,
        output_basename=Kfdrc_Controlfreec_Sub_Wf.output_basename,
        reference_fai=Kfdrc_Controlfreec_Sub_Wf.reference_fai,
        sample_name=Kfdrc_Controlfreec_Sub_Wf.input_tumor_name,
    ),
)


Kfdrc_Controlfreec_Sub_Wf.step(
    "rename_outputs",
    Ubuntu_Rename_Cf_Outputs_V0_1_0(
        input_files=[
            Kfdrc_Controlfreec_Sub_Wf.control_free_c.cnvs,
            Kfdrc_Controlfreec_Sub_Wf.control_free_c.cnvs_pvalue,
            Kfdrc_Controlfreec_Sub_Wf.control_free_c.config_script,
            Kfdrc_Controlfreec_Sub_Wf.control_free_c.ratio,
            Kfdrc_Controlfreec_Sub_Wf.control_free_c.sample_BAF,
            Kfdrc_Controlfreec_Sub_Wf.control_free_c.info_txt,
        ],
        input_pngs=Kfdrc_Controlfreec_Sub_Wf.control_free_c.pngs,
        output_basename=Kfdrc_Controlfreec_Sub_Wf.output_basename,
    ),
)

Kfdrc_Controlfreec_Sub_Wf.output(
    "ctrlfreec_baf",
    source=Kfdrc_Controlfreec_Sub_Wf.rename_outputs.ctrlfreec_baf,
    output_name=True,
)

Kfdrc_Controlfreec_Sub_Wf.output(
    "ctrlfreec_bam_ratio",
    source=Kfdrc_Controlfreec_Sub_Wf.rename_outputs.ctrlfreec_bam_ratio,
    output_name=True,
)

Kfdrc_Controlfreec_Sub_Wf.output(
    "ctrlfreec_bam_seg",
    source=Kfdrc_Controlfreec_Sub_Wf.convert_ratio_to_seg.ctrlfreec_ratio2seg,
    output_name=True,
)

Kfdrc_Controlfreec_Sub_Wf.output(
    "ctrlfreec_cnvs",
    source=Kfdrc_Controlfreec_Sub_Wf.rename_outputs.ctrlfreec_cnvs,
    output_name=True,
)

Kfdrc_Controlfreec_Sub_Wf.output(
    "ctrlfreec_config",
    source=Kfdrc_Controlfreec_Sub_Wf.rename_outputs.ctrlfreec_config,
    output_name=True,
)

Kfdrc_Controlfreec_Sub_Wf.output(
    "ctrlfreec_info",
    source=Kfdrc_Controlfreec_Sub_Wf.rename_outputs.ctrlfreec_info,
    output_name=True,
)

Kfdrc_Controlfreec_Sub_Wf.output(
    "ctrlfreec_pngs",
    source=Kfdrc_Controlfreec_Sub_Wf.rename_outputs.ctrlfreec_pngs,
    output_name=True,
)

Kfdrc_Controlfreec_Sub_Wf.output(
    "ctrlfreec_pval",
    source=Kfdrc_Controlfreec_Sub_Wf.rename_outputs.ctrlfreec_pval,
    output_name=True,
)

Kfdrc_Mutect2_Sub_Wf = WorkflowBuilder(identifier="kfdrc_mutect2_sub_wf",)

Kfdrc_Mutect2_Sub_Wf.input(
    "af_only_gnomad_vcf", VcfTabix(),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "bed_invtl_split",
    Array(t=File()),
    doc=InputDocumentation(
        doc="Bed file intervals passed on from and outside pre-processing step"
    ),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "exac_common_vcf", VcfTabix(),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "exome_flag",
    String(optional=True),
    doc=InputDocumentation(doc="set to 'Y' for exome mode"),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "filtermutectcalls_memory", Int(optional=True),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "getpileup_memory", Int(optional=True),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "indexed_reference_fasta",
    GenericFileWithSecondaries(secondaries=[".fai", "^.dict"]),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "input_normal_aligned",
    GenericFileWithSecondaries(
        secondaries=[
            "${\n  var dpath = self.location.replace(self.basename, '')\n  if(self.nameext == '.bam'){\n    return {'location': dpath+self.nameroot+'.bai', 'class': 'File'}\n  }\n  else{\n    return {'location': dpath+self.basename+'.crai', 'class': 'File'}\n  }\n}\n"
        ]
    ),
    doc=InputDocumentation(doc="normal BAM or CRAM"),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "input_normal_name", String(),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "input_tumor_aligned",
    GenericFileWithSecondaries(
        secondaries=[
            "${\n  var dpath = self.location.replace(self.basename, '')\n  if(self.nameext == '.bam'){\n    return {'location': dpath+self.nameroot+'.bai', 'class': 'File'}\n  }\n  else{\n    return {'location': dpath+self.basename+'.crai', 'class': 'File'}\n  }\n}\n"
        ]
    ),
    doc=InputDocumentation(doc="tumor BAM or CRAM"),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "input_tumor_name", String(),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "learnorientation_memory", Int(optional=True),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "output_basename", String(),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "reference_dict", File(),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "select_vars_mode",
    String(optional=True),
    default="gatk",
    doc=InputDocumentation(
        doc="Choose 'gatk' for SelectVariants tool, or 'grep' for grep expression"
    ),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "vep_cache", File(),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "vep_ref_build",
    String(optional=True),
    default="GRCh38",
    doc=InputDocumentation(doc="Genome ref build used, should line up with cache."),
)

Kfdrc_Mutect2_Sub_Wf.input(
    "merge_mutect2_vcf_tool_name", String(optional=True), default="mutect2",
)

Kfdrc_Mutect2_Sub_Wf.input(
    "gatk_selectvariants_tool_name", String(optional=True), default="mutect2",
)

Kfdrc_Mutect2_Sub_Wf.input(
    "vep_annot_mutect2_tool_name", String(optional=True), default="mutect2_somatic",
)


Kfdrc_Mutect2_Sub_Wf.step(
    "mutect2",
    Gatk4_Mutect2_V0_1_0(
        af_only_gnomad_vcf=Kfdrc_Mutect2_Sub_Wf.af_only_gnomad_vcf,
        exome_flag=Kfdrc_Mutect2_Sub_Wf.exome_flag,
        input_normal_aligned=Kfdrc_Mutect2_Sub_Wf.input_normal_aligned,
        input_normal_name=Kfdrc_Mutect2_Sub_Wf.input_normal_name,
        input_tumor_aligned=Kfdrc_Mutect2_Sub_Wf.input_tumor_aligned,
        input_tumor_name=Kfdrc_Mutect2_Sub_Wf.input_tumor_name,
        interval_list=Kfdrc_Mutect2_Sub_Wf.bed_invtl_split,
        reference=Kfdrc_Mutect2_Sub_Wf.indexed_reference_fasta,
    ),
)


Kfdrc_Mutect2_Sub_Wf.step(
    "mutect2_filter_support",
    Mutect2_Support(
        exac_common_vcf=Kfdrc_Mutect2_Sub_Wf.exac_common_vcf,
        f1r2_counts=Kfdrc_Mutect2_Sub_Wf.mutect2.f1r2_counts,
        getpileup_memory=Kfdrc_Mutect2_Sub_Wf.getpileup_memory,
        indexed_reference_fasta=Kfdrc_Mutect2_Sub_Wf.indexed_reference_fasta,
        input_normal_aligned=Kfdrc_Mutect2_Sub_Wf.input_normal_aligned,
        input_tumor_aligned=Kfdrc_Mutect2_Sub_Wf.input_tumor_aligned,
        learnorientation_memory=Kfdrc_Mutect2_Sub_Wf.learnorientation_memory,
        output_basename=Kfdrc_Mutect2_Sub_Wf.output_basename,
        reference_dict=Kfdrc_Mutect2_Sub_Wf.reference_dict,
        wgs_calling_interval_list=Kfdrc_Mutect2_Sub_Wf.bed_invtl_split,
    ),
)


Kfdrc_Mutect2_Sub_Wf.step(
    "merge_mutect2_stats",
    Gatk4_Mergepileup_V0_1_0(
        input_stats=Kfdrc_Mutect2_Sub_Wf.mutect2.mutect_stats,
        output_basename=Kfdrc_Mutect2_Sub_Wf.output_basename,
    ),
)


Kfdrc_Mutect2_Sub_Wf.step(
    "merge_mutect2_vcf",
    Gatk4_Mergevcfs_V0_1_0(
        input_vcfs=Kfdrc_Mutect2_Sub_Wf.mutect2.mutect2_vcf,
        output_basename=Kfdrc_Mutect2_Sub_Wf.output_basename,
        reference_dict=Kfdrc_Mutect2_Sub_Wf.reference_dict,
        tool_name=Kfdrc_Mutect2_Sub_Wf.merge_mutect2_vcf_tool_name,
    ),
)


Kfdrc_Mutect2_Sub_Wf.step(
    "filter_mutect2_vcf",
    Gatk4_Filtermutect2Calls_V0_1_0(
        contamination_table=Kfdrc_Mutect2_Sub_Wf.mutect2_filter_support.contamination_table,
        max_memory=Kfdrc_Mutect2_Sub_Wf.filtermutectcalls_memory,
        mutect_stats=Kfdrc_Mutect2_Sub_Wf.merge_mutect2_stats.merged_stats,
        mutect_vcf=Kfdrc_Mutect2_Sub_Wf.merge_mutect2_vcf.merged_vcf,
        ob_priors=Kfdrc_Mutect2_Sub_Wf.mutect2_filter_support.f1r2_bias,
        output_basename=Kfdrc_Mutect2_Sub_Wf.output_basename,
        reference=Kfdrc_Mutect2_Sub_Wf.indexed_reference_fasta,
        segmentation_table=Kfdrc_Mutect2_Sub_Wf.mutect2_filter_support.segmentation_table,
    ),
)


Kfdrc_Mutect2_Sub_Wf.step(
    "gatk_selectvariants",
    Gatk4_Selectvariants_V0_1_0(
        input_vcf=Kfdrc_Mutect2_Sub_Wf.filter_mutect2_vcf.filtered_vcf,
        mode=Kfdrc_Mutect2_Sub_Wf.select_vars_mode,
        output_basename=Kfdrc_Mutect2_Sub_Wf.output_basename,
        tool_name=Kfdrc_Mutect2_Sub_Wf.gatk_selectvariants_tool_name,
    ),
)


Kfdrc_Mutect2_Sub_Wf.step(
    "vep_annot_mutect2",
    Kfdrc_Vep_Somatic_Annotate_Maf_V0_1_0(
        cache=Kfdrc_Mutect2_Sub_Wf.vep_cache,
        input_vcf=Kfdrc_Mutect2_Sub_Wf.gatk_selectvariants.pass_vcf,
        normal_id=Kfdrc_Mutect2_Sub_Wf.input_normal_name,
        output_basename=Kfdrc_Mutect2_Sub_Wf.output_basename,
        ref_build=Kfdrc_Mutect2_Sub_Wf.vep_ref_build,
        reference=Kfdrc_Mutect2_Sub_Wf.indexed_reference_fasta,
        tool_name=Kfdrc_Mutect2_Sub_Wf.vep_annot_mutect2_tool_name,
        tumor_id=Kfdrc_Mutect2_Sub_Wf.input_tumor_name,
    ),
)

Kfdrc_Mutect2_Sub_Wf.output(
    "mutect2_filtered_stats",
    source=Kfdrc_Mutect2_Sub_Wf.filter_mutect2_vcf.stats_table,
    output_name=True,
)

Kfdrc_Mutect2_Sub_Wf.output(
    "mutect2_filtered_vcf",
    source=Kfdrc_Mutect2_Sub_Wf.filter_mutect2_vcf.filtered_vcf,
    output_name=True,
)

Kfdrc_Mutect2_Sub_Wf.output(
    "mutect2_vep_maf",
    source=Kfdrc_Mutect2_Sub_Wf.vep_annot_mutect2.output_maf,
    output_name=True,
)

Kfdrc_Mutect2_Sub_Wf.output(
    "mutect2_vep_tbi",
    source=Kfdrc_Mutect2_Sub_Wf.vep_annot_mutect2.output_tbi,
    output_name=True,
)

Kfdrc_Mutect2_Sub_Wf.output(
    "mutect2_vep_vcf",
    source=Kfdrc_Mutect2_Sub_Wf.vep_annot_mutect2.output_vcf,
    output_name=True,
)

Kfdrc_Vardict_1_7_Sub_Wf = WorkflowBuilder(identifier="kfdrc_vardict_1_7_sub_wf",)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "bed_invtl_split",
    Array(t=File()),
    doc=InputDocumentation(
        doc="Bed file intervals passed on from and outside pre-processing step"
    ),
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "cpus", Int(optional=True), default=9,
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "indexed_reference_fasta",
    GenericFileWithSecondaries(secondaries=[".fai", "^.dict"]),
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "input_normal_aligned", GenericFileWithSecondaries(secondaries=["^.bai"]),
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "input_normal_name", String(),
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "input_tumor_aligned", GenericFileWithSecondaries(secondaries=["^.bai"]),
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "input_tumor_name", String(),
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "min_vaf",
    Float(optional=True),
    default=0.05,
    doc=InputDocumentation(
        doc="Min variant allele frequency for vardict to consider.  Recommend 0.05"
    ),
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "output_basename", String(),
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "padding",
    Int(optional=True),
    default=150,
    doc=InputDocumentation(
        doc="Padding to add to input intervals, recommened 0 if intervals already padded, 150 if not"
    ),
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "ram", Int(optional=True), default=18, doc=InputDocumentation(doc="In GB"),
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "reference_dict", File(),
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "select_vars_mode",
    String(optional=True),
    default="gatk",
    doc=InputDocumentation(
        doc="Choose 'gatk' for SelectVariants tool, or 'grep' for grep expression"
    ),
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "vep_cache", File(),
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "vep_ref_build",
    String(optional=True),
    default="GRCh38",
    doc=InputDocumentation(doc="Genome ref build used, should line up with cache."),
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "sort_merge_vardict_vcf_tool_name", String(optional=True), default="vardict",
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "gatk_selectvariants_vardict_tool_name", String(optional=True), default="vardict",
)

Kfdrc_Vardict_1_7_Sub_Wf.input(
    "vep_annot_vardict_tool_name", String(optional=True), default="vardict_somatic",
)


Kfdrc_Vardict_1_7_Sub_Wf.step(
    "vardict",
    Vardictjava_V0_1_0(
        bed=Kfdrc_Vardict_1_7_Sub_Wf.bed_invtl_split,
        cpus=Kfdrc_Vardict_1_7_Sub_Wf.cpus,
        input_normal_bam=Kfdrc_Vardict_1_7_Sub_Wf.input_normal_aligned,
        input_normal_name=Kfdrc_Vardict_1_7_Sub_Wf.input_normal_name,
        input_tumor_bam=Kfdrc_Vardict_1_7_Sub_Wf.input_tumor_aligned,
        input_tumor_name=Kfdrc_Vardict_1_7_Sub_Wf.input_tumor_name,
        min_vaf=Kfdrc_Vardict_1_7_Sub_Wf.min_vaf,
        output_basename=Kfdrc_Vardict_1_7_Sub_Wf.output_basename,
        padding=Kfdrc_Vardict_1_7_Sub_Wf.padding,
        ram=Kfdrc_Vardict_1_7_Sub_Wf.ram,
        reference=Kfdrc_Vardict_1_7_Sub_Wf.indexed_reference_fasta,
    ),
)


Kfdrc_Vardict_1_7_Sub_Wf.step(
    "sort_merge_vardict_vcf",
    Gatk4_Mergevcfs_V0_1_0(
        input_vcfs=Kfdrc_Vardict_1_7_Sub_Wf.vardict.vardict_vcf,
        output_basename=Kfdrc_Vardict_1_7_Sub_Wf.output_basename,
        reference_dict=Kfdrc_Vardict_1_7_Sub_Wf.reference_dict,
        tool_name=Kfdrc_Vardict_1_7_Sub_Wf.sort_merge_vardict_vcf_tool_name,
    ),
)


Kfdrc_Vardict_1_7_Sub_Wf.step(
    "bcbio_filter_fp_somatic",
    Bcbio_Vardict_Fp_Somatic_Filter_V0_1_0(
        input_vcf=Kfdrc_Vardict_1_7_Sub_Wf.sort_merge_vardict_vcf.merged_vcf,
        output_basename=Kfdrc_Vardict_1_7_Sub_Wf.output_basename,
    ),
)


Kfdrc_Vardict_1_7_Sub_Wf.step(
    "gatk_selectvariants_vardict",
    Gatk4_Selectvariants_V0_1_0(
        input_vcf=Kfdrc_Vardict_1_7_Sub_Wf.bcbio_filter_fp_somatic.filtered_vcf,
        mode=Kfdrc_Vardict_1_7_Sub_Wf.select_vars_mode,
        output_basename=Kfdrc_Vardict_1_7_Sub_Wf.output_basename,
        tool_name=Kfdrc_Vardict_1_7_Sub_Wf.gatk_selectvariants_vardict_tool_name,
    ),
)


Kfdrc_Vardict_1_7_Sub_Wf.step(
    "vep_annot_vardict",
    Kfdrc_Vep_Somatic_Annotate_Maf_V0_1_0(
        cache=Kfdrc_Vardict_1_7_Sub_Wf.vep_cache,
        input_vcf=Kfdrc_Vardict_1_7_Sub_Wf.gatk_selectvariants_vardict.pass_vcf,
        normal_id=Kfdrc_Vardict_1_7_Sub_Wf.input_normal_name,
        output_basename=Kfdrc_Vardict_1_7_Sub_Wf.output_basename,
        ref_build=Kfdrc_Vardict_1_7_Sub_Wf.vep_ref_build,
        reference=Kfdrc_Vardict_1_7_Sub_Wf.indexed_reference_fasta,
        tool_name=Kfdrc_Vardict_1_7_Sub_Wf.vep_annot_vardict_tool_name,
        tumor_id=Kfdrc_Vardict_1_7_Sub_Wf.input_tumor_name,
    ),
)

Kfdrc_Vardict_1_7_Sub_Wf.output(
    "vardict_prepass_vcf",
    source=Kfdrc_Vardict_1_7_Sub_Wf.sort_merge_vardict_vcf.merged_vcf,
    output_name=True,
)

Kfdrc_Vardict_1_7_Sub_Wf.output(
    "vardict_vep_somatic_only_maf",
    source=Kfdrc_Vardict_1_7_Sub_Wf.vep_annot_vardict.output_maf,
    output_name=True,
)

Kfdrc_Vardict_1_7_Sub_Wf.output(
    "vardict_vep_somatic_only_tbi",
    source=Kfdrc_Vardict_1_7_Sub_Wf.vep_annot_vardict.output_tbi,
    output_name=True,
)

Kfdrc_Vardict_1_7_Sub_Wf.output(
    "vardict_vep_somatic_only_vcf",
    source=Kfdrc_Vardict_1_7_Sub_Wf.vep_annot_vardict.output_vcf,
    output_name=True,
)

Preprocess_Lancet_Intervals_V0_1_0 = CommandToolBuilder(
    tool="preprocess_lancet_intervals",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(
            tag="mutect2_vcf",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="ref_bed",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="strelka2_vcf",
            input_type=File(optional=True),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="run_bed",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*.lancet_intvervals.bed"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/bedops:2.4.36",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="set -eo pipefail\n${\n  var flag = 0\n  var cmd = '';\n  var bed = []\n  if(inputs.ref_bed == null) {\n    return 'echo No ref bed provided providing empty output >&2 && exit 0;'\n  }\n  else {\n    if(inputs.strelka2_vcf != null){\n        flag = 1;\n        cmd += 'gunzip -c ' + inputs.strelka2_vcf.path + ' > ' + inputs.strelka2_vcf.basename + ';';\n        cmd += 'vcf2bed --insertions < ' + inputs.strelka2_vcf.basename + ' | cut -f 1-3 > strelka2.insertions.bed;';\n        bed.push('strelka2.insertions.bed');\n        cmd += 'vcf2bed --deletions < ' + inputs.strelka2_vcf.basename + ' | cut -f 1-3 > strelka2.deletions.bed;';\n        bed.push('strelka2.deletions.bed');\n        cmd += 'vcf2bed --snvs < ' + inputs.strelka2_vcf.basename + ' | cut -f 1-3 > strelka2.snvs.bed;';\n        bed.push('strelka2.snvs.bed');\n    }\n    if(inputs.mutect2_vcf != null){\n        flag = 1;\n        cmd += 'gunzip -c ' + inputs.mutect2_vcf.path + ' > ' + inputs.mutect2_vcf.basename + ';';\n        cmd += 'vcf2bed --insertions < ' + inputs.mutect2_vcf.basename +  ' | cut -f 1-3 > mutect2.insertions.bed;';\n        bed.push('mutect2.insertions.bed');\n        cmd += 'vcf2bed --deletions < ' + inputs.mutect2_vcf.basename + ' | cut -f 1-3 > mutect2.deletions.bed;';\n        bed.push('mutect2.deletions.bed');\n        cmd += 'vcf2bed --snvs < ' + inputs.mutect2_vcf.basename +  ' | cut -f 1-3 > mutect2.snvs.bed;';\n        bed.push('mutect2.snvs.bed');\n    }\n    if(flag == 0){\n        cmd += 'echo 'No input vcfs found to convert.  Returning ref bed'; cp ' + inputs.ref_bed.path + ' ' + inputs.output_basename + '.lancet_intvervals.bed;';\n    }\n    else{\n        cmd += 'cat ' + bed.join(' ') + ' ' + inputs.ref_bed.path + ' | bedtools sort | bedtools merge > ' + inputs.output_basename + '.lancet_intvervals.bed;';\n    }\n    return cmd;\n  }\n}",
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=4,
    memory=8000,
)
Kfdrc_Cnvkit_Batch_Wf = WorkflowBuilder(identifier="kfdrc_cnvkit_batch_wf",)

Kfdrc_Cnvkit_Batch_Wf.input(
    "combined_exclude_expression",
    String(optional=True),
    doc=InputDocumentation(
        doc="Filter expression if vcf has non-PASS combined calls, use as-needed"
    ),
)

Kfdrc_Cnvkit_Batch_Wf.input(
    "combined_include_expression",
    String(optional=True),
    doc=InputDocumentation(
        doc="Filter expression if vcf has non-PASS combined calls, use as-needed"
    ),
)

Kfdrc_Cnvkit_Batch_Wf.input(
    "min_theta2_frac",
    Float(optional=True),
    default=0.01,
    doc=InputDocumentation(
        doc="Minimum fraction of genome with copy umber alterations.  Default is 0.05, recommend 0.01"
    ),
)

Kfdrc_Cnvkit_Batch_Wf.input(
    "normal_sample_name", String(),
)

Kfdrc_Cnvkit_Batch_Wf.input(
    "output_basename", String(),
)

Kfdrc_Cnvkit_Batch_Wf.input(
    "paired_vcf",
    File(),
    doc=InputDocumentation(
        doc="Combined somatic and germline call file. VarDict input recommended."
    ),
)

Kfdrc_Cnvkit_Batch_Wf.input(
    "reference_cnn", File(), doc=InputDocumentation(doc="CNVkit output cnn file"),
)

Kfdrc_Cnvkit_Batch_Wf.input(
    "tumor_cns", File(), doc=InputDocumentation(doc="CNVkit output cns file"),
)

Kfdrc_Cnvkit_Batch_Wf.input(
    "tumor_sample_name", String(),
)


Kfdrc_Cnvkit_Batch_Wf.step(
    "bcftools_filter_combined_vcf",
    Bcftools_Filter_Vcf_V0_1_0(
        exclude_expression=Kfdrc_Cnvkit_Batch_Wf.combined_exclude_expression,
        include_expression=Kfdrc_Cnvkit_Batch_Wf.combined_include_expression,
        input_vcf=Kfdrc_Cnvkit_Batch_Wf.paired_vcf,
        output_basename=Kfdrc_Cnvkit_Batch_Wf.output_basename,
    ),
)


Kfdrc_Cnvkit_Batch_Wf.step(
    "cnvkit_export_theta2",
    Cnvkit_Export_Theta2_V0_1_0(
        normal_ID=Kfdrc_Cnvkit_Batch_Wf.normal_sample_name,
        paired_vcf=Kfdrc_Cnvkit_Batch_Wf.bcftools_filter_combined_vcf.filtered_vcf,
        reference_cnn=Kfdrc_Cnvkit_Batch_Wf.reference_cnn,
        tumor_ID=Kfdrc_Cnvkit_Batch_Wf.tumor_sample_name,
        tumor_cns=Kfdrc_Cnvkit_Batch_Wf.tumor_cns,
    ),
)


Kfdrc_Cnvkit_Batch_Wf.step(
    "run_theta2",
    Theta2_V0_1_0(
        interval_count=Kfdrc_Cnvkit_Batch_Wf.cnvkit_export_theta2.call_interval_count,
        min_frac=Kfdrc_Cnvkit_Batch_Wf.min_theta2_frac,
        normal_snp=Kfdrc_Cnvkit_Batch_Wf.cnvkit_export_theta2.call_normal_snp,
        output_basename=Kfdrc_Cnvkit_Batch_Wf.output_basename,
        tumor_snp=Kfdrc_Cnvkit_Batch_Wf.cnvkit_export_theta2.call_tumor_snp,
    ),
)


Kfdrc_Cnvkit_Batch_Wf.step(
    "cnvkit_import_theta2",
    Cnvkit_Import_Theta2_V0_1_0(
        output_basename=Kfdrc_Cnvkit_Batch_Wf.output_basename,
        theta2_best_results=Kfdrc_Cnvkit_Batch_Wf.run_theta2.best_results,
        theta2_n2_results=Kfdrc_Cnvkit_Batch_Wf.run_theta2.n2_results,
        tumor_cns=Kfdrc_Cnvkit_Batch_Wf.tumor_cns,
        tumor_sample_name=Kfdrc_Cnvkit_Batch_Wf.tumor_sample_name,
    ),
)

Kfdrc_Cnvkit_Batch_Wf.output(
    "theta2_adjusted_cns",
    source=Kfdrc_Cnvkit_Batch_Wf.cnvkit_import_theta2.theta2_adjusted_cns,
    output_name=True,
)

Kfdrc_Cnvkit_Batch_Wf.output(
    "theta2_adjusted_seg",
    source=Kfdrc_Cnvkit_Batch_Wf.cnvkit_import_theta2.theta2_adjusted_seg,
    output_name=True,
)

Kfdrc_Cnvkit_Batch_Wf.output(
    "theta2_subclonal_cns",
    source=Kfdrc_Cnvkit_Batch_Wf.cnvkit_import_theta2.theta2_subclone_cns,
    output_name=True,
)

Kfdrc_Cnvkit_Batch_Wf.output(
    "theta2_subclonal_results",
    source=[
        Kfdrc_Cnvkit_Batch_Wf.run_theta2.n3_graph,
        Kfdrc_Cnvkit_Batch_Wf.run_theta2.n2_results,
        Kfdrc_Cnvkit_Batch_Wf.run_theta2.best_results,
    ],
    output_name=True,
)

Kfdrc_Cnvkit_Batch_Wf.output(
    "theta2_subclone_seg",
    source=Kfdrc_Cnvkit_Batch_Wf.cnvkit_import_theta2.theta2_subclone_seg,
    output_name=True,
)

Kfdrc_Lancet_Sub_Wf = WorkflowBuilder(
    identifier="kfdrc_lancet_sub_wf", doc="Lancet sub workflow, meant to be wrapped",
)

Kfdrc_Lancet_Sub_Wf.input(
    "bed_invtl_split",
    Array(t=File()),
    doc=InputDocumentation(
        doc="Bed file intervals passed on from and outside pre-processing step"
    ),
)

Kfdrc_Lancet_Sub_Wf.input(
    "indexed_reference_fasta",
    GenericFileWithSecondaries(secondaries=[".fai", "^.dict"]),
)

Kfdrc_Lancet_Sub_Wf.input(
    "input_normal_aligned", GenericFileWithSecondaries(secondaries=["^.bai"]),
)

Kfdrc_Lancet_Sub_Wf.input(
    "input_normal_name", String(),
)

Kfdrc_Lancet_Sub_Wf.input(
    "input_tumor_aligned", GenericFileWithSecondaries(secondaries=["^.bai"]),
)

Kfdrc_Lancet_Sub_Wf.input(
    "input_tumor_name", String(),
)

Kfdrc_Lancet_Sub_Wf.input(
    "output_basename", String(),
)

Kfdrc_Lancet_Sub_Wf.input(
    "padding",
    Int(),
    doc=InputDocumentation(
        doc="If WGS (less likely), default 25, if exome+, recommend half window size"
    ),
)

Kfdrc_Lancet_Sub_Wf.input(
    "ram",
    Int(optional=True),
    default=12,
    doc=InputDocumentation(
        doc="Adjust in rare circumstances in which 12 GB is not enough."
    ),
)

Kfdrc_Lancet_Sub_Wf.input(
    "reference_dict", File(),
)

Kfdrc_Lancet_Sub_Wf.input(
    "select_vars_mode",
    String(optional=True),
    default="gatk",
    doc=InputDocumentation(
        doc="Choose 'gatk' for SelectVariants tool, or 'grep' for grep expression"
    ),
)

Kfdrc_Lancet_Sub_Wf.input(
    "vep_cache", File(),
)

Kfdrc_Lancet_Sub_Wf.input(
    "vep_ref_build",
    String(optional=True),
    default="GRCh38",
    doc=InputDocumentation(doc="Genome ref build used, should line up with cache."),
)

Kfdrc_Lancet_Sub_Wf.input(
    "window",
    Int(),
    doc=InputDocumentation(
        doc="window size for lancet.  default is 600, recommend 500 for WGS, 600 for exome+"
    ),
)

Kfdrc_Lancet_Sub_Wf.input(
    "sort_merge_lancet_vcf_tool_name", String(optional=True), default="lancet",
)

Kfdrc_Lancet_Sub_Wf.input(
    "gatk_selectvariants_lancet_tool_name", String(optional=True), default="lancet",
)

Kfdrc_Lancet_Sub_Wf.input(
    "vep_annot_lancet_tool_name", String(optional=True), default="lancet_somatic",
)


Kfdrc_Lancet_Sub_Wf.step(
    "lancet",
    Lancet_V0_1_0(
        bed=Kfdrc_Lancet_Sub_Wf.bed_invtl_split,
        input_normal_bam=Kfdrc_Lancet_Sub_Wf.input_normal_aligned,
        input_tumor_bam=Kfdrc_Lancet_Sub_Wf.input_tumor_aligned,
        output_basename=Kfdrc_Lancet_Sub_Wf.output_basename,
        padding=Kfdrc_Lancet_Sub_Wf.padding,
        ram=Kfdrc_Lancet_Sub_Wf.ram,
        reference=Kfdrc_Lancet_Sub_Wf.indexed_reference_fasta,
        window=Kfdrc_Lancet_Sub_Wf.window,
    ),
)


Kfdrc_Lancet_Sub_Wf.step(
    "sort_merge_lancet_vcf",
    Gatk4_Mergevcfs_V0_1_0(
        input_vcfs=Kfdrc_Lancet_Sub_Wf.lancet.lancet_vcf,
        output_basename=Kfdrc_Lancet_Sub_Wf.output_basename,
        reference_dict=Kfdrc_Lancet_Sub_Wf.reference_dict,
        tool_name=Kfdrc_Lancet_Sub_Wf.sort_merge_lancet_vcf_tool_name,
    ),
)


Kfdrc_Lancet_Sub_Wf.step(
    "gatk_selectvariants_lancet",
    Gatk4_Selectvariants_V0_1_0(
        input_vcf=Kfdrc_Lancet_Sub_Wf.sort_merge_lancet_vcf.merged_vcf,
        mode=Kfdrc_Lancet_Sub_Wf.select_vars_mode,
        output_basename=Kfdrc_Lancet_Sub_Wf.output_basename,
        tool_name=Kfdrc_Lancet_Sub_Wf.gatk_selectvariants_lancet_tool_name,
    ),
)


Kfdrc_Lancet_Sub_Wf.step(
    "vep_annot_lancet",
    Kfdrc_Vep_Somatic_Annotate_Maf_V0_1_0(
        cache=Kfdrc_Lancet_Sub_Wf.vep_cache,
        input_vcf=Kfdrc_Lancet_Sub_Wf.gatk_selectvariants_lancet.pass_vcf,
        normal_id=Kfdrc_Lancet_Sub_Wf.input_normal_name,
        output_basename=Kfdrc_Lancet_Sub_Wf.output_basename,
        ref_build=Kfdrc_Lancet_Sub_Wf.vep_ref_build,
        reference=Kfdrc_Lancet_Sub_Wf.indexed_reference_fasta,
        tool_name=Kfdrc_Lancet_Sub_Wf.vep_annot_lancet_tool_name,
        tumor_id=Kfdrc_Lancet_Sub_Wf.input_tumor_name,
    ),
)

Kfdrc_Lancet_Sub_Wf.output(
    "lancet_prepass_vcf",
    source=Kfdrc_Lancet_Sub_Wf.sort_merge_lancet_vcf.merged_vcf,
    output_name=True,
)

Kfdrc_Lancet_Sub_Wf.output(
    "lancet_vep_maf",
    source=Kfdrc_Lancet_Sub_Wf.vep_annot_lancet.output_maf,
    output_name=True,
)

Kfdrc_Lancet_Sub_Wf.output(
    "lancet_vep_tbi",
    source=Kfdrc_Lancet_Sub_Wf.vep_annot_lancet.output_tbi,
    output_name=True,
)

Kfdrc_Lancet_Sub_Wf.output(
    "lancet_vep_vcf",
    source=Kfdrc_Lancet_Sub_Wf.vep_annot_lancet.output_vcf,
    output_name=True,
)


Kfdrc_Somatic_Variant_Workflow = WorkflowBuilder(
    identifier="kfdrc_somatic_variant_workflow",
    friendly_name="Kids First DRC Somatic Variant Workflow",
    doc="# Kids First DRC Somatic Variant Workflow\n\nThis repository contains the Kids First Data Resource Center (DRC) Somatic Variant Workflow, which includes somatic variant (SNV), copy number variation (CNV), and structural variant (SV) calls.\nThis workflow takes aligned cram input and performs somatic variant calling using Strelka2, Mutect2, Lancet, and VarDict Java, CNV estimation using ControlFreeC and CNVkit, and SV calls using Manta.\nSomatic variant and SV call results are annotated using Variant Effect Predictor, with the Memorial Sloane Kettering Cancer Center (MSKCC) vcf2maf wrapper.\n\nIf you would like to run this workflow using the cavatica public app, a basic primer on running public apps can be found [here](https://www.notion.so/d3b/Starting-From-Scratch-Running-Cavatica-af5ebb78c38a4f3190e32e67b4ce12bb).\nAlternatively, if you'd like to run it locally using `cwltool`, a basic primer on that can be found [here](https://www.notion.so/d3b/Starting-From-Scratch-Running-CWLtool-b8dbbde2dc7742e4aff290b0a878344d) and combined with app-specific info from the readme below.\nThis workflow is the current production workflow, equivalent to this [Cavatica public app](https://cavatica.sbgenomics.com/public/apps#cavatica/apps-publisher/kfdrc-somatic-variant-workflow)\n\n![data service logo](https://github.com/d3b-center/d3b-research-workflows/raw/master/doc/kfdrc-logo-sm.png)\n\n## Running WGS or WXS\n\nThe [combinded workflow](https://github.com/kids-first/kf-somatic-workflow/blob/master/workflow/kfdrc-somatic-variant-workflow.cwl) is designed to be able to process either WGS or WXS inputs.\nThis functionality comes from usage of the `wgs_or_wxs` input enum. Depending on what is provided for this input, the tool will\nset the appropriate default values and check that the user has provided the correct inputs. For example, if the user sets the\ninput to WGS the lancet_padding value will be defaulted to 300; alternatively, if the user sets the input to WXS the lancet_padding\nvalue will be defaulted to 0. In either case, the user can override the defaults simply by providing their own value for lancet_padding\nin the inputs.\n\nThe `wgs_or_wxs` flag also controls which inputs are used for certain steps. For example, the bed_interval input for Lancet comes\nfrom different sources in the WGS and WXS pipelines. In the WGS pipeline separate processing is done ahead of time to generate\na new interval file. A tool in the workflow will take in the presumptive inputs for WGS and WXS modes. If the mode is WGS, then\nthe pipeline will pass on the file provided as the wgs_input and vice versa. If the wgs_input is missing and the mode is WGS, then\nthe pipeline will fail.\n\n### WGS-only Fields\n\nThere are two WGS only fields `wgs_calling_interval_list` and `lancet_calling_interval_bed`. If these are not provided in a WGS run,\nthe pipeline will fail.\n\n### WXS-only Fields\n\nThere are two WXS only fields `padded_capture_regions` and `unpadded_capture_regions`. If these are not provided in a WXS run,\nthe pipeline will fail.\n\n### Standalone Somatic Workflows\nEach tool used in the [combined workflow](https://github.com/kids-first/kf-somatic-workflow/blob/master/workflow/kfdrc-somatic-variant-workflow.cwl) can be run on its own. While the combined workflow calls all types of variant, each standalone caller only specializes in one class of variant.\n\n| Workflow                                                                                                                                            | CNV | SNV | SV |\n|-----------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|----|\n| [kfdrc-somatic-variant-workflow.cwl](https://github.com/kids-first/kf-somatic-workflow/blob/master/workflow/kfdrc-somatic-variant-workflow.cwl)     |  x  |  x  |  x |\n| [kfdrc_production_cnvkit_wf.cwl](https://github.com/kids-first/kf-somatic-workflow/blob/master/workflow/kfdrc_production_cnvkit_wf.cwl)             |  x  |     |    |\n| [kfdrc_production_controlfreec_wf.cwl](https://github.com/kids-first/kf-somatic-workflow/blob/master/workflow/kfdrc_production_controlfreec_wf.cwl) |  x  |     |    |\n| [kfdrc_production_lancet_wf.cwl](https://github.com/kids-first/kf-somatic-workflow/blob/master/workflow/kfdrc_production_lancet_wf.cwl)             |     |  x  |    |\n| [kfdrc_production_manta_wf.cwl](https://github.com/kids-first/kf-somatic-workflow/blob/master/workflow/kfdrc_production_manta_wf.cwl)               |     |     |  x |\n| [kfdrc_production_mutect2_wf.cwl](https://github.com/kids-first/kf-somatic-workflow/blob/master/workflow/kfdrc_production_mutect2_wf.cwl)           |     |  x  |    |\n| [kfdrc_production_strekla2_wf.cwl](https://github.com/kids-first/kf-somatic-workflow/blob/master/workflow/kfdrc_production_strekla2_wf.cwl)         |     |  x  |    |\n| [kfdrc_production_theta2_wf.cwl](https://github.com/kids-first/kf-somatic-workflow/blob/master/workflow/kfdrc_production_theta2_wf.cwl)             |     |     |  x |\n| [kfdrc_production_vardict_wf.cwl](https://github.com/kids-first/kf-somatic-workflow/blob/master/workflow/kfdrc_production_vardict_wf.cwl)           |     |  x  |    |\n\n#### SNV Callers\n\n- [Strelka2](https://github.com/Illumina/strelka) `v2.9.3` calls single nucleotide variants (SNV) and insertions/deletions (INDEL).\n- [Mutect2](https://gatk.broadinstitute.org/hc/en-us/articles/360036730411-Mutect2) `v4.1.1.0` from the Broad institute calls SNV, multi-nucleotide variants (MNV, basically equal length substitutions with length > 1) and INDEL.\n- [Lancet](https://github.com/nygenome/lancet) `v1.0.7` from the New York Genome Center (NYGC) calls SNV, MNV, and INDEL.\n- [VarDict Java](https://github.com/AstraZeneca-NGS/VarDictJava) `v1.7.0` from AstraZeneca calls SNV, MNV, INDEL and more.\n\nEach caller has a different approach to variant calling, and together one can glean confident results. Strelka2 is run with default settings, similarly Mutect2 following Broad Best Practices, as of this [workflow](https://github.com/broadinstitute/gatk/blob/4.1.1.0/scripts/mutect2_wdl/mutect2.wdl). Lancet is run in what I'd call an 'Exome+' mode, based on the NYGC methods described [here](https://www.biorxiv.org/content/biorxiv/early/2019/04/30/623702.full.pdf). In short, regions from GENCODE gtf with feature annotations `exon`, `UTR`, and start/stop `codon` are used as intervals, as well as regions flanking hits from `strelka2` and `mutect2`. Lastly, VarDict Java run params follow the protocol that the [Blue Collar Bioinformatics](https://bcbio-nextgen.readthedocs.io/en/latest/index.html) uses, with the exception of using a min variant allele frequency (VAF) of 0.05 instead of 0.1, which we find to be relevant for rare cancer variant discovery. We also employ their false positive filtering methods.\nFurthermore, each tool's results, in variant call format (vcf), are filtered on the `PASS` flag, with VarDict Java results additionally filtered for the flag `StrongSomatic`. Their results also include germline hits and other categories by default.\nThe pre-`PASS` filtered results can still be obtained from the workflow in the event the user wishes to keep some calls that failed `PASS` criteria.\n\n#### CNV Estimators\n\n- [ControlFreeC](https://github.com/BoevaLab/FREEC) `v11.6` is used for CNV estimation.\nThe tool portion of the workflow is a port from the [Seven Bridges Genomics](https://www.sevenbridges.com/) team, with a slight tweak in image outputs.\nAlso, the workflow wrapper limits what inputs and outputs are used based on our judgement of utility.\nOutputs include raw ratio calls, copy number calls with p values assigned, b allele frequency data, as well as copy number and b allele frequency plots.\n- [CNVkit](https://cnvkit.readthedocs.io/en/stable/) `v2.9.3` is a CNV second tool we currently use.\n- [THeTa2](https://github.com/raphael-group/THetA) is used to inform and adjust copy number calls from CNVkit with purity estimations.\n\nFor ControlFreeC and CNVkit, we take advantage of b allele frequency (from the gVCF created by our [alignment and haplotypecaller workflows](https://github.com/kids-first/kf-alignment-workflow)) integration for copy number genotype estimation and increased CNV accuracy.\n\n#### SV Callers\n\n- [Manta](https://github.com/Illumina/manta) `v1.4.0` is used to call SVs. Output is also in vcf format, with calls filtered on `PASS`.\nDefault settings are used at run time.\n\n#### Variant Annotation\n\n- [Variant Effect Predictor](https://useast.ensembl.org/info/docs/tools/vep/index.html) `release 93`, wrapped by [vcf2maf](https://github.com/mskcc/vcf2maf) `v1.6.17` is used to annotate somatic variant and SV calls.\n\nBoth the annotated vcf and maf file are made available.\n\n### Tips to Run:\n\n1. For input cram files, be sure to have indexed them beforehand as well.\n\n1. For ControlFreeC, it is highly recommended that you supply a vcf file with germline calls, GATK Haplotype caller recommended.\nPlease also make sure the index for this file is available.\nAlso, a range of input ploidy possibilities for the inputs are needed. You can simply use `2`, or put in a range, as an array, like 2, 3, 4.\nFor mate orientation, you will need to specify, the drop down and tool doc explains your options.\n\n1. As a cavatica app, default references for hg38 are already pre-populated, as well as some default settings - i.e., number of threads, coefficient of variation input for ControlFreec, and `PASS` filter tool mode.\n\n1. What is `select_vars_mode` you ask? On occasion, using GATK's `SelectVariants` tool will fail, so a simple `grep` mode on `PASS` can be used instead.\nRelated, `bcftools_filter_vcf` is built in as a convenience in case your b allele frequency file has not been filtered on `PASS`.\nYou can use the `include_expression` `Filter='PASS'` to achieve this.\n\n1. Suggested reference inputs are:\n\n    - `reference_fasta`: [Homo_sapiens_assembly38.fasta](https://console.cloud.google.com/storage/browser/genomics-public-data/resources/broad/hg38/v0?pli=1) - need a valid google account, this is a link to the resource bundle from Broad GATK\n    - `reference_dict`: [Homo_sapiens_assembly38.dict](https://console.cloud.google.com/storage/browser/genomics-public-data/resources/broad/hg38/v0?pli=1) - need a valid google account, this is a link to the resource bundle from Broad GATK\n    - `annotation_file`: [refFlat_HG38.txt](http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/refFlat.txt.gz) gunzip this file from UCSC.  Needed for gene annotation in `CNVkit`\n    - `wgs_calling_interval_list`: [wgs_calling_regions.hg38.interval_list](https://console.cloud.google.com/storage/browser/genomics-public-data/resources/broad/hg38/v0?pli=1) - need a valid google account, this is a link to the resource bundle from Broad GATK.*To create our 'wgs_canonical_calling_regions.hg38.interval_list', edit this file* by leaving only entries related to chr 1-22, X,Y, and M.M may need to be added.\n    - `lancet_calling_interval_bed`: `GRCh38.gencode.v31.CDS.merged.bed`.  As decribed at the beginning, for WGS, it's highly recommended to use CDS bed, and supplement with region calls from strelka2 & mutect2. Our reference was obtained from GENCODE, [release 31](https://www.gencodegenes.org/human/release_31.html) using this gtf file [gencode.v31.primary_assembly.annotation.gtf.gz](ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_31/gencode.v31.primary_assembly.annotation.gtf.gz) and parsing features for `UTR`, `start codon`, `stop codon`, and `exon`, then using bedtools sort and merge after converting coordinates into bed format.\n    - `af_only_gnomad_vcf`: [af-only-gnomad.hg38.vcf.gz](https://console.cloud.google.com/storage/browser/-gatk-best-practices/somatic-hg38) - need a valid google account, this is a link to the best practices google bucket from Broad GATK.\n    - `exac_common_vcf`: [small_exac_common_3.hg38.vcf.gz](https://console.cloud.google.com/storage/browser/gatk-best-practices/somatic-hg38) - need a valid google account, this is a link to the best practices google bucket from Broad GATK.\n    - `hg38_strelka_bed`: [hg38_strelka.bed.gz'](https://github.com/Illumina/strelka/blob/v2.9.x/docs/userGuide/README.md#extended-use-cases) - this link here has the bed-formatted text needed to copy to create this file. You will need to bgzip this file.\n     - `vep_cache`: `homo_sapiens_vep_93_GRCh38.tar.gz` from ftp://ftp.ensembl.org/pub/release-93/variation/indexed_vep_cache/ - variant effect predictor cache.\n     Current production workflow uses this version, and is compatible with the release used in the vcf2maf tool.\n     - `threads`: 16\n     - `chr_len`: hs38_chr.len, this a tsv file with chromosomes and their lengths. Should be limited to canonical chromosomes\n      The first column must be chromosomes, optionally the second can be an alternate format of chromosomes.\n      Last column must be chromosome length.\n      Using the `hg38_strelka_bed`, and removing chrM can be a good source for this.\n    - `coeff_var`: 0.05\n    - `contamination_adjustment`: FALSE\n\n1. Output files (Note, all vcf files that don't have an explicit index output have index files output as as secondary file.  In other words, they will be captured at the end of the workflow):\n\n    - Simple variant callers\n        - Strelka2:\n            - `strelka2_vep_vcf`: Variant effect predictor annotated vcf, filtered on `PASS`, somatic snv and indel call results from strelka2\n            - `strelka2_vep_tbi`: Index file of above bgzipped vcf\n            - `strelka2_prepass_vcf`: Somatic snv and indel call results with all `FILTER` categories for strelka2. Use this file if you believe important variants are being left out when using the algorithm's `PASS` filter.\n            - `strelka2_vep_maf`: Mutation annotation file (maf) format of `strelka2_vep_vcf`\n        - Mutect2:\n            - `mutect2_vep_vcf`: Variant effect predictor annotated vcf, filtered on `PASS`, somatic snv and indel call results from mutect2\n            - `mutect2_vep_tbi`: Index file of above bgzipped vcf\n            - `mutect2_prepass_vcf`: Somatic snv and indel call results with all `FILTER` categories for mutect2. Use this file if you believe important variants are being left out when using the algorithm's `PASS` filter.\n            - `mutect2_vep_maf`: maf of format of `mutect2_vep_vcf`\n        - VardictJava\n            - `vardict_vep_somatic_only_vcf`: Variant effect predictor annotated vcf, filtered on `PASS` and `StrongSomatic` call results from VardictJava\n            - `vardict_vep_somatic_only_tbi`: Index file of above bgzipped vcf\n            - `vardict_vep_somatic_only_maf`: maf format of `vardict_vep_somatic_only_vcf`\n            - `vardict_prepass_vcf`: All call results with all `FILTER` categories for VardictJava. Use this file if you believe important variants are being left out when using the algorithm's `PASS` filter and our `StrongSomatic` subset.\n        - Lancet\n            - `lancet_vep_vcf`: Variant effect predictor annotated vcf, filtered on `PASS`, somatic snv and indel call results from lancet\n            - `lancet_vep_tbi`: Index file of above bgzipped vcf\n            - `lancet_vep_maf`: maf format of `lancet_vep_vcf`\n            - `lancet_prepass_vcf`: Somatic snv and indel call results with all `FILTER` categories for lancet. Use this file if you believe important variants are being left out when using the algorithm's `PASS` filter.\n    - Structural variant callers\n        - Manta\n            - `manta_vep_vcf`: Variant effect predictor annotated vcf, filtered on `PASS`, sv call results from manta\n            - `manta_vep_tbi`: Index file of above bgzipped vcf\n            - `manta_prepass_vcf`: SV results with all `FILTER` categories for manta. Use this file if you believe important variants are being left out when using the algorithm's `PASS` filter.\n            - `manta_vep_maf`: maf of format of `manta_vep_vcf`\n    - Copy number variation callers\n        - ControlFREEC\n            - `ctrlfreec_pval`: CNV calls with copy number and p value confidence, a qualtitative 'gain, loss, neutral' assignment, and genotype with uncertainty assigned from ControlFreeC.  See author manual for more details.\n            - `ctrlfreec_config`: Config file used to run ControlFreeC.  Has some useful information on what parameters were used to run the tool.\n            - `ctrlfreec_pngs`: Plots of b allele frequency (baf) log2 ratio and ratio of tumor/normal copy number coverage.  Pink line in the middle of ratio plots is the median ratio.\n            - `ctrlfreec_bam_ratio`: Bam ratio text file.  Contain ratio, median ratio (used to inform `ctrlfreec_pval`), cnv estimates, baf estimate, and genotype estimate.\n            - `ctrlfreec_bam_seg`: In-house generated seg file based on ratio file.  Provided asa a convenience for compatibility with tools that require inputs in legacy microarray format.\n            - `ctrlfreec_baf`: baf estimations.\n            - `ctrlfreec_info`: Contains useful run time information, like ploidy used for analysis, and window size\n        - CNVkit\n            - `cnvkit_cnr`: Copy number ratio\n            - `cnvkit_cnn_output`: Normal/control sample copy number\n            - `cnvkit_calls`: Tumor/sample copy number\n            - `cnvkit_metrics`: Basic seg count and call stats\n            - `cnvkit_gainloss`: Per-gene log2 ratio\n            - `cnvkit_seg`: Classic microarray-style seg file\n            - `theta2_calls`: Purity-adjusted CNVkit copy number calls based on theta2 results\n            - `theta2_seg`: Purity-adjusted CNVkit seg file based on theta results\n            - `theta2_subclonal_results`: Theta2 Subclone purity results\n            - `theta2_subclonal_cns`: Theta2 sublone cns\n            - `theta2_subclone_seg`: Theta subclone seg file\n\n1. Docker images - the workflow tools will automatically pull them, but as a convenience are listed below:\n    - `Strelka2`: pgc-images.sbgenomics.com/d3b-bixu/strelka\n    - `Mutect2` and all `GATK` tools: pgc-images.sbgenomics.com/d3b-bixu/gatk:4.1.1.0\n    - `Lancet`: pgc-images.sbgenomics.com/d3b-bixu/lancet:1.0.7\n    - `VarDict Java`: pgc-images.sbgenomics.com/d3b-bixu/vardict:1.7.0\n    - `ControlFreeC`: images.sbgenomics.com/vojislav_varjacic/control-freec-11-6:v1\n    - `CNVkit`: images.sbgenomics.com/milos_nikolic/cnvkit:0.9.3\n    - `THetA2`: pgc-images.sbgenomics.com/d3b-bixu/theta2:0.7\n    - `samtools`: pgc-images.sbgenomics.com/d3b-bixu/samtools:1.9\n    - `Variant Effect Predictor`: pgc-images.sbgenomics.com/d3b-bixu/vep:r93_v2\n    - `Manta`: pgc-images.sbgenomics.com/d3b-bixu/manta:1.4.0\n    - `bcftools` and `vcftools`: pgc-images.sbgenomics.com/d3b-bixu/bvcftools:latest\n\n1. For highly complex samples, some tools have shown themselves to require memory allocation adjustments:\n   Manta, GATK LearnReadOrientationModel, GATK GetPileupSummaries, GATK FilterMutectCalls and Vardict.\n   Optional inputs exist to expand the memory allocation for these jobs: manta_memory, learnorientation_memory,\n   getpileup_memory, filtermutectcalls_memory, and vardict_ram, respectively.\n   For the java tools (Vardict and GATK), these values represent limits on the memory that can\n   be used for the respective jobs. Tasks will go to these values and not exceed it. They may succeed or fail,\n   but they will not exceed the limit established. The memory allocations for these is hardcapped. The memory\n   allocation option for Manta, conversely, is a soft cap. The memory requested will be allocated for the job\n   on a particular machine but once the task is running on the machine it may exceed that requested value. For example,\n   if Manta's memory allocation is set to 10 GB it will have 10 GB allocated to it at task creation, but, if the\n   task ends up running on a machine with more memory available, the task may use it. Setting a value here for Manta\n   will not prevent Manta from taking more than that value. The memory usage in Manta is limited by the machine hardware.\n   As such the option for Manta memory allocation is described as soft cap. For more information on Manta resource\n   usage see their [documentation](https://github.com/Illumina/manta/blob/master/docs/userGuide/README.md#runtime-hardware-requirements).\n\n## Other Resources\n- tool images: https://hub.docker.com/r/kfdrc/\n- dockerfiles: https://github.com/d3b-center/bixtools\n\n![pipeline flowchart](./docs/kfdrc-somatic-variant-workflow.png)\n",
)

Kfdrc_Somatic_Variant_Workflow.input(
    "b_allele",
    File(optional=True),
    doc=InputDocumentation(
        doc="germline calls, needed for BAF.  GATK HC VQSR input recommended.  Tool will prefilter for germline and pass if expression given"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "b_allele_index",
    File(optional=True),
    doc=InputDocumentation(doc="Tabix index for b_allele"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "cfree_chr_len", File(), doc=InputDocumentation(doc="file with chromosome lengths"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "cfree_coeff_var",
    Float(optional=True),
    default=0.05,
    doc=InputDocumentation(
        doc="Coefficient of variation to set window size.  Default 0.05 recommended"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "cfree_contamination_adjustment",
    Boolean(optional=True),
    doc=InputDocumentation(
        doc="TRUE or FALSE to have ControlFreec estimate normal contam"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "cfree_mate_orientation_control",
    String(optional=True),
    default="FR",
    doc=InputDocumentation(
        doc="0 (for single ends), RF (Illumina mate-pairs), FR (Illumina paired-ends), FF (SOLiD mate-pairs)"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "cfree_mate_orientation_sample",
    String(optional=True),
    default="FR",
    doc=InputDocumentation(
        doc="0 (for single ends), RF (Illumina mate-pairs), FR (Illumina paired-ends), FF (SOLiD mate-pairs)"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "cfree_ploidy",
    Array(t=Int()),
    doc=InputDocumentation(doc="Array of ploidy possibilities for ControlFreeC to try"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "cfree_sex",
    String(optional=True),
    doc=InputDocumentation(doc="If known, XX for female, XY for male"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "cfree_threads",
    Int(optional=True),
    default=16,
    doc=InputDocumentation(
        doc="For ControlFreeC. Recommend 16 max, as I/O gets saturated after that losing any advantage"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "cnvkit_annotation_file", File(), doc=InputDocumentation(doc="refFlat.txt file"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "cnvkit_sex",
    String(optional=True),
    doc=InputDocumentation(doc="If known, choices are m,y,male,Male,f,x,female,Female"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "cnvkit_wgs_mode",
    String(optional=True),
    doc=InputDocumentation(
        doc="for WGS mode, input Y. leave blank for WXS/hybrid mode"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "combined_exclude_expression",
    String(optional=True),
    doc=InputDocumentation(
        doc="Theta2 Purity value: Filter expression if vcf has non-PASS combined calls, use as-needed"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "combined_include_expression",
    String(optional=True),
    doc=InputDocumentation(
        doc="Theta2 Purity value: Filter expression if vcf has non-PASS combined calls, use as-needed, i.e. for VarDict: FILTER='PASS' && (INFO/STATUS='Germline' | INFO/STATUS='StrongSomatic')"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "exome_flag",
    String(optional=True),
    doc=InputDocumentation(
        doc="Whether to run in exome mode for callers. Y for WXS, N for WGS"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "filtermutectcalls_memory",
    Int(optional=True),
    doc=InputDocumentation(
        doc="GB of memory to allocate to GATK FilterMutectCalls; defaults to 4 (hard-capped)"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "getpileup_memory",
    Int(optional=True),
    doc=InputDocumentation(
        doc="GB of memory to allocate to GATK GetPileupSummaries; defaults to 2 (hard-capped)"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "hg38_strelka_bed",
    File(),
    doc=InputDocumentation(
        doc="Bgzipped interval bed file. Recommned padding 100bp for WXS; Recommend canonical chromosomes for WGS"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "hg38_strelka_tbi",
    File(optional=True),
    doc=InputDocumentation(doc="Tabix index for hg38_strelka_bed"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "i_flag",
    String(optional=True),
    doc=InputDocumentation(
        doc="Flag to intersect germline calls on padded regions. Use N if you want to skip this or have a WGS run"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "input_normal_aligned",
    GenericFileWithSecondaries(
        secondaries=[
            "${\n  var dpath = self.location.replace(self.basename, '')\n  if(self.nameext == '.bam'){\n    return {'location': dpath+self.nameroot+'.bai', 'class': 'File'}\n  }\n  else{\n    return {'location': dpath+self.basename+'.crai', 'class': 'File'}\n  }\n}\n"
        ]
    ),
    doc=InputDocumentation(doc="normal BAM or CRAM"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "input_normal_name", String(),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "input_tumor_aligned",
    GenericFileWithSecondaries(
        secondaries=[
            "${\n  var dpath = self.location.replace(self.basename, '')\n  if(self.nameext == '.bam'){\n    return {'location': dpath+self.nameroot+'.bai', 'class': 'File'}\n  }\n  else{\n    return {'location': dpath+self.basename+'.crai', 'class': 'File'}\n  }\n}\n"
        ]
    ),
    doc=InputDocumentation(doc="tumor BAM or CRAM"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "input_tumor_name", String(),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "lancet_calling_interval_bed",
    File(optional=True),
    doc=InputDocumentation(
        doc="For WGS, highly recommended to use CDS bed, and supplement with region calls from strelka2 & mutect2.  Can still give calling list as bed if true WGS calling desired instead of exome+"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "lancet_padding",
    Int(optional=True),
    doc=InputDocumentation(
        doc="Recommend 0 if interval file padded already, half window size if not. Recommended: 0 for WXS; 300 for WGS"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "lancet_ram",
    Int(optional=True),
    default=12,
    doc=InputDocumentation(
        doc="Adjust in rare circumstances in which 12 GB is not enough"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "lancet_window",
    Int(optional=True),
    doc=InputDocumentation(
        doc="Window size for lancet.  Recommend 500 for WGS; 600 for exome+"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "learnorientation_memory",
    Int(optional=True),
    doc=InputDocumentation(
        doc="GB of memory to allocate to GATK LearnReadOrientationModel; defaults to 4 (hard-capped)"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "manta_cores",
    Int(optional=True),
    doc=InputDocumentation(doc="Number of cores to allocate to Manta; defaults to 18"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "manta_memory",
    Int(optional=True),
    doc=InputDocumentation(
        doc="GB of memory to allocate to Manta; defaults to 10 (soft-capped)"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "min_theta2_frac",
    Float(optional=True),
    default=0.01,
    doc=InputDocumentation(
        doc="Minimum fraction of genome with copy umber alterations.  Default is 0.05, recommend 0.01"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "mutect2_af_only_gnomad_tbi",
    File(optional=True),
    doc=InputDocumentation(doc="Tabix index for mutect2_af_only_gnomad_vcf"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "mutect2_af_only_gnomad_vcf", File(),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "mutect2_exac_common_tbi",
    File(optional=True),
    doc=InputDocumentation(doc="Tabix index for mutect2_exac_common_vcf"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "mutect2_exac_common_vcf", File(),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "output_basename",
    String(),
    doc=InputDocumentation(doc="String value to use as basename for outputs"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "padded_capture_regions",
    File(optional=True),
    doc=InputDocumentation(doc="Recommend 100bp pad, for somatic variant"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "reference_dict", File(optional=True),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "reference_fai", File(optional=True),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "reference_fasta", File(),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "select_vars_mode",
    String(optional=True),
    default="gatk",
    doc=InputDocumentation(
        doc="Choose 'gatk' for SelectVariants tool, or 'grep' for grep expression"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "unpadded_capture_regions",
    File(optional=True),
    doc=InputDocumentation(doc="Capture regions with NO padding for cnv calling"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "use_manta_small_indels",
    Boolean(optional=True),
    default=False,
    doc=InputDocumentation(
        doc="Should the program use the small indels output from Manta in Strelka2 calling?"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "vardict_cpus",
    Int(optional=True),
    default=9,
    doc=InputDocumentation(doc="Number of CPUs for Vardict to use"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "vardict_min_vaf",
    Float(optional=True),
    default=0.05,
    doc=InputDocumentation(
        doc="Min variant allele frequency for vardict to consider. Recommend 0.05"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "vardict_padding",
    Int(optional=True),
    doc=InputDocumentation(
        doc="Padding to add to input intervals, recommend 0 if intervals already padded such as in WXS, 150 if not such as in WGS"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "vardict_ram",
    Int(optional=True),
    default=18,
    doc=InputDocumentation(doc="GB of RAM to allocate to Vardict (hard-capped)"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "vep_cache",
    File(),
    doc=InputDocumentation(doc="tar gzipped cache from ensembl/local converted cache"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "vep_ref_build",
    String(optional=True),
    default="GRCh38",
    doc=InputDocumentation(doc="Genome ref build used, should line up with cache"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "wgs_calling_interval_list",
    File(optional=True),
    doc=InputDocumentation(
        doc="GATK intervals list-style, or bed file.  Recommend canocical chromosomes with N regions removed"
    ),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "wgs_or_wxs",
    String(),
    doc=InputDocumentation(doc="Select if this run is WGS or WXS"),
)

Kfdrc_Somatic_Variant_Workflow.input(
    "samtools_cram2bam_plus_calmd_normal_threads", Int(optional=True), default=16,
)

Kfdrc_Somatic_Variant_Workflow.input(
    "samtools_cram2bam_plus_calmd_tumor_threads", Int(optional=True), default=16,
)

Kfdrc_Somatic_Variant_Workflow.input(
    "gatk_intervallisttools_bands", Int(optional=True), default=80000000,
)

Kfdrc_Somatic_Variant_Workflow.input(
    "gatk_intervallisttools_scatter_ct", Int(optional=True), default=50,
)

Kfdrc_Somatic_Variant_Workflow.input(
    "gatk_intervallisttools_exome_plus_bands", Int(optional=True), default=80000000,
)

Kfdrc_Somatic_Variant_Workflow.input(
    "gatk_intervallisttools_exome_plus_exome_flag", String(optional=True), default="Y",
)

Kfdrc_Somatic_Variant_Workflow.input(
    "gatk_intervallisttools_exome_plus_scatter_ct", Int(optional=True), default=50,
)


Kfdrc_Somatic_Variant_Workflow.step(
    "choose_defaults",
    Mode_Defaults_V0_1_0(
        cnvkit_wgs_mode=Kfdrc_Somatic_Variant_Workflow.cnvkit_wgs_mode,
        exome_flag=Kfdrc_Somatic_Variant_Workflow.exome_flag,
        i_flag=Kfdrc_Somatic_Variant_Workflow.i_flag,
        input_mode=Kfdrc_Somatic_Variant_Workflow.wgs_or_wxs,
        lancet_padding=Kfdrc_Somatic_Variant_Workflow.lancet_padding,
        lancet_window=Kfdrc_Somatic_Variant_Workflow.lancet_window,
        vardict_padding=Kfdrc_Somatic_Variant_Workflow.vardict_padding,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "index_b_allele",
    Tabix_Index_V0_1_0(
        input_file=Kfdrc_Somatic_Variant_Workflow.b_allele,
        input_index=Kfdrc_Somatic_Variant_Workflow.b_allele_index,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "index_mutect_exac",
    Tabix_Index_V0_1_0(
        input_file=Kfdrc_Somatic_Variant_Workflow.mutect2_exac_common_vcf,
        input_index=Kfdrc_Somatic_Variant_Workflow.mutect2_exac_common_tbi,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "index_mutect_gnomad",
    Tabix_Index_V0_1_0(
        input_file=Kfdrc_Somatic_Variant_Workflow.mutect2_af_only_gnomad_vcf,
        input_index=Kfdrc_Somatic_Variant_Workflow.mutect2_af_only_gnomad_tbi,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "index_strelka_bed",
    Tabix_Index_V0_1_0(
        input_file=Kfdrc_Somatic_Variant_Workflow.hg38_strelka_bed,
        input_index=Kfdrc_Somatic_Variant_Workflow.hg38_strelka_tbi,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "prepare_reference",
    Kfdrc_Prepare_Reference(
        input_dict=Kfdrc_Somatic_Variant_Workflow.reference_dict,
        input_fai=Kfdrc_Somatic_Variant_Workflow.reference_fai,
        input_fasta=Kfdrc_Somatic_Variant_Workflow.reference_fasta,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "run_manta",
    Kfdrc_Manta_Sub_Wf(
        hg38_strelka_bed=Kfdrc_Somatic_Variant_Workflow.index_strelka_bed.outp,
        indexed_reference_fasta=Kfdrc_Somatic_Variant_Workflow.prepare_reference.indexed_fasta,
        input_normal_aligned=Kfdrc_Somatic_Variant_Workflow.input_normal_aligned,
        input_normal_name=Kfdrc_Somatic_Variant_Workflow.input_normal_name,
        input_tumor_aligned=Kfdrc_Somatic_Variant_Workflow.input_tumor_aligned,
        input_tumor_name=Kfdrc_Somatic_Variant_Workflow.input_tumor_name,
        manta_cores=Kfdrc_Somatic_Variant_Workflow.manta_cores,
        manta_memory=Kfdrc_Somatic_Variant_Workflow.manta_memory,
        output_basename=Kfdrc_Somatic_Variant_Workflow.output_basename,
        reference_dict=Kfdrc_Somatic_Variant_Workflow.prepare_reference.reference_dict,
        select_vars_mode=Kfdrc_Somatic_Variant_Workflow.select_vars_mode,
        vep_cache=Kfdrc_Somatic_Variant_Workflow.vep_cache,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "run_strelka2",
    Kfdrc_Strelka2_Sub_Wf(
        exome_flag=Kfdrc_Somatic_Variant_Workflow.choose_defaults.out_exome_flag,
        hg38_strelka_bed=Kfdrc_Somatic_Variant_Workflow.index_strelka_bed.outp,
        indexed_reference_fasta=Kfdrc_Somatic_Variant_Workflow.prepare_reference.indexed_fasta,
        input_normal_aligned=Kfdrc_Somatic_Variant_Workflow.input_normal_aligned,
        input_normal_name=Kfdrc_Somatic_Variant_Workflow.input_normal_name,
        input_tumor_aligned=Kfdrc_Somatic_Variant_Workflow.input_tumor_aligned,
        input_tumor_name=Kfdrc_Somatic_Variant_Workflow.input_tumor_name,
        manta_small_indels=Kfdrc_Somatic_Variant_Workflow.run_manta.manta_small_indels,
        output_basename=Kfdrc_Somatic_Variant_Workflow.output_basename,
        reference_dict=Kfdrc_Somatic_Variant_Workflow.prepare_reference.reference_dict,
        select_vars_mode=Kfdrc_Somatic_Variant_Workflow.select_vars_mode,
        use_manta_small_indels=Kfdrc_Somatic_Variant_Workflow.use_manta_small_indels,
        vep_cache=Kfdrc_Somatic_Variant_Workflow.vep_cache,
        vep_ref_build=Kfdrc_Somatic_Variant_Workflow.vep_ref_build,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "samtools_cram2bam_plus_calmd_normal",
    Samtools_Cram2Bam_Plus_Calmd_V0_1_0(
        input_reads=Kfdrc_Somatic_Variant_Workflow.input_normal_aligned,
        reference=Kfdrc_Somatic_Variant_Workflow.prepare_reference.indexed_fasta,
        threads=Kfdrc_Somatic_Variant_Workflow.samtools_cram2bam_plus_calmd_normal_threads,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "samtools_cram2bam_plus_calmd_tumor",
    Samtools_Cram2Bam_Plus_Calmd_V0_1_0(
        input_reads=Kfdrc_Somatic_Variant_Workflow.input_tumor_aligned,
        reference=Kfdrc_Somatic_Variant_Workflow.prepare_reference.indexed_fasta,
        threads=Kfdrc_Somatic_Variant_Workflow.samtools_cram2bam_plus_calmd_tumor_threads,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "select_interval_list",
    Mode_Selector_V0_1_0(
        input_mode=Kfdrc_Somatic_Variant_Workflow.wgs_or_wxs,
        wgs_input=Kfdrc_Somatic_Variant_Workflow.wgs_calling_interval_list,
        wxs_input=Kfdrc_Somatic_Variant_Workflow.padded_capture_regions,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "bedtools_intersect_germline",
    Bedtools_Intersect_V0_1_0(
        flag=Kfdrc_Somatic_Variant_Workflow.choose_defaults.out_i_flag,
        input_bed_file=Kfdrc_Somatic_Variant_Workflow.unpadded_capture_regions,
        input_vcf=Kfdrc_Somatic_Variant_Workflow.index_b_allele.outp,
        output_basename=Kfdrc_Somatic_Variant_Workflow.output_basename,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "gatk_filter_germline",
    Kfdrc_Gatk_Variantfiltration_V0_1_0(
        input_vcf=Kfdrc_Somatic_Variant_Workflow.bedtools_intersect_germline.intersected_vcf,
        output_basename=Kfdrc_Somatic_Variant_Workflow.output_basename,
        reference_fasta=Kfdrc_Somatic_Variant_Workflow.prepare_reference.indexed_fasta,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "gatk_intervallisttools",
    Gatk4_Intervallist2Bed_V0_1_0(
        bands=Kfdrc_Somatic_Variant_Workflow.gatk_intervallisttools_bands,
        exome_flag=Kfdrc_Somatic_Variant_Workflow.choose_defaults.out_exome_flag,
        interval_list=Kfdrc_Somatic_Variant_Workflow.select_interval_list.outp,
        reference_dict=Kfdrc_Somatic_Variant_Workflow.prepare_reference.reference_dict,
        scatter_ct=Kfdrc_Somatic_Variant_Workflow.gatk_intervallisttools_scatter_ct,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "python_vardict_interval_split",
    Python_Vardict_Interval_Split_V0_1_0(
        wgs_bed_file=Kfdrc_Somatic_Variant_Workflow.select_interval_list.outp,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "run_cnvkit",
    Kfdrc_Cnvkit_Sub_Wf(
        annotation_file=Kfdrc_Somatic_Variant_Workflow.cnvkit_annotation_file,
        b_allele_vcf=Kfdrc_Somatic_Variant_Workflow.gatk_filter_germline.filtered_pass_vcf,
        capture_regions=Kfdrc_Somatic_Variant_Workflow.unpadded_capture_regions,
        input_normal_aligned=Kfdrc_Somatic_Variant_Workflow.samtools_cram2bam_plus_calmd_normal.bam_file,
        input_tumor_aligned=Kfdrc_Somatic_Variant_Workflow.samtools_cram2bam_plus_calmd_tumor.bam_file,
        normal_sample_name=Kfdrc_Somatic_Variant_Workflow.input_normal_name,
        output_basename=Kfdrc_Somatic_Variant_Workflow.output_basename,
        reference=Kfdrc_Somatic_Variant_Workflow.prepare_reference.indexed_fasta,
        sex=Kfdrc_Somatic_Variant_Workflow.cnvkit_sex,
        tumor_sample_name=Kfdrc_Somatic_Variant_Workflow.input_tumor_name,
        wgs_mode=Kfdrc_Somatic_Variant_Workflow.choose_defaults.out_cnvkit_wgs_mode,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "run_controlfreec",
    Kfdrc_Controlfreec_Sub_Wf(
        b_allele=Kfdrc_Somatic_Variant_Workflow.gatk_filter_germline.filtered_pass_vcf,
        capture_regions=Kfdrc_Somatic_Variant_Workflow.unpadded_capture_regions,
        cfree_sex=Kfdrc_Somatic_Variant_Workflow.cfree_sex,
        chr_len=Kfdrc_Somatic_Variant_Workflow.cfree_chr_len,
        coeff_var=Kfdrc_Somatic_Variant_Workflow.cfree_coeff_var,
        contamination_adjustment=Kfdrc_Somatic_Variant_Workflow.cfree_contamination_adjustment,
        indexed_reference_fasta=Kfdrc_Somatic_Variant_Workflow.prepare_reference.indexed_fasta,
        input_normal_aligned=Kfdrc_Somatic_Variant_Workflow.samtools_cram2bam_plus_calmd_normal.bam_file,
        input_tumor_aligned=Kfdrc_Somatic_Variant_Workflow.samtools_cram2bam_plus_calmd_tumor.bam_file,
        input_tumor_name=Kfdrc_Somatic_Variant_Workflow.input_tumor_name,
        mate_orientation_control=Kfdrc_Somatic_Variant_Workflow.cfree_mate_orientation_control,
        mate_orientation_sample=Kfdrc_Somatic_Variant_Workflow.cfree_mate_orientation_sample,
        output_basename=Kfdrc_Somatic_Variant_Workflow.output_basename,
        ploidy=Kfdrc_Somatic_Variant_Workflow.cfree_ploidy,
        reference_fai=Kfdrc_Somatic_Variant_Workflow.reference_fai,
        threads=Kfdrc_Somatic_Variant_Workflow.cfree_threads,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "select_mutect_bed_interval",
    Mode_Selector_V0_1_0(
        input_mode=Kfdrc_Somatic_Variant_Workflow.wgs_or_wxs,
        wgs_input=Kfdrc_Somatic_Variant_Workflow.gatk_intervallisttools.outp,
        wxs_input=Kfdrc_Somatic_Variant_Workflow.gatk_intervallisttools.outp,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "select_vardict_bed_interval",
    Mode_Selector_V0_1_0(
        input_mode=Kfdrc_Somatic_Variant_Workflow.wgs_or_wxs,
        wgs_input=Kfdrc_Somatic_Variant_Workflow.python_vardict_interval_split.split_intervals_bed,
        wxs_input=Kfdrc_Somatic_Variant_Workflow.gatk_intervallisttools.outp,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "run_mutect2",
    Kfdrc_Mutect2_Sub_Wf(
        af_only_gnomad_vcf=Kfdrc_Somatic_Variant_Workflow.index_mutect_gnomad.outp,
        bed_invtl_split=[
            Kfdrc_Somatic_Variant_Workflow.select_mutect_bed_interval.outp
        ],
        exac_common_vcf=Kfdrc_Somatic_Variant_Workflow.index_mutect_exac.outp,
        exome_flag=Kfdrc_Somatic_Variant_Workflow.choose_defaults.out_exome_flag,
        filtermutectcalls_memory=Kfdrc_Somatic_Variant_Workflow.filtermutectcalls_memory,
        getpileup_memory=Kfdrc_Somatic_Variant_Workflow.getpileup_memory,
        indexed_reference_fasta=Kfdrc_Somatic_Variant_Workflow.prepare_reference.indexed_fasta,
        input_normal_aligned=Kfdrc_Somatic_Variant_Workflow.input_normal_aligned,
        input_normal_name=Kfdrc_Somatic_Variant_Workflow.input_normal_name,
        input_tumor_aligned=Kfdrc_Somatic_Variant_Workflow.input_tumor_aligned,
        input_tumor_name=Kfdrc_Somatic_Variant_Workflow.input_tumor_name,
        learnorientation_memory=Kfdrc_Somatic_Variant_Workflow.learnorientation_memory,
        output_basename=Kfdrc_Somatic_Variant_Workflow.output_basename,
        reference_dict=Kfdrc_Somatic_Variant_Workflow.prepare_reference.reference_dict,
        select_vars_mode=Kfdrc_Somatic_Variant_Workflow.select_vars_mode,
        vep_cache=Kfdrc_Somatic_Variant_Workflow.vep_cache,
        vep_ref_build=Kfdrc_Somatic_Variant_Workflow.vep_ref_build,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "run_vardict",
    Kfdrc_Vardict_1_7_Sub_Wf(
        bed_invtl_split=[
            Kfdrc_Somatic_Variant_Workflow.select_vardict_bed_interval.outp
        ],
        cpus=Kfdrc_Somatic_Variant_Workflow.vardict_cpus,
        indexed_reference_fasta=Kfdrc_Somatic_Variant_Workflow.prepare_reference.indexed_fasta,
        input_normal_aligned=Kfdrc_Somatic_Variant_Workflow.samtools_cram2bam_plus_calmd_normal.bam_file,
        input_normal_name=Kfdrc_Somatic_Variant_Workflow.input_normal_name,
        input_tumor_aligned=Kfdrc_Somatic_Variant_Workflow.samtools_cram2bam_plus_calmd_tumor.bam_file,
        input_tumor_name=Kfdrc_Somatic_Variant_Workflow.input_tumor_name,
        min_vaf=Kfdrc_Somatic_Variant_Workflow.vardict_min_vaf,
        output_basename=Kfdrc_Somatic_Variant_Workflow.output_basename,
        padding=Kfdrc_Somatic_Variant_Workflow.choose_defaults.out_vardict_padding,
        ram=Kfdrc_Somatic_Variant_Workflow.vardict_ram,
        reference_dict=Kfdrc_Somatic_Variant_Workflow.prepare_reference.reference_dict,
        select_vars_mode=Kfdrc_Somatic_Variant_Workflow.select_vars_mode,
        vep_cache=Kfdrc_Somatic_Variant_Workflow.vep_cache,
        vep_ref_build=Kfdrc_Somatic_Variant_Workflow.vep_ref_build,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "bedops_gen_lancet_intervals",
    Preprocess_Lancet_Intervals_V0_1_0(
        mutect2_vcf=Kfdrc_Somatic_Variant_Workflow.run_mutect2.mutect2_vep_vcf,
        output_basename=Kfdrc_Somatic_Variant_Workflow.output_basename,
        ref_bed=Kfdrc_Somatic_Variant_Workflow.lancet_calling_interval_bed,
        strelka2_vcf=Kfdrc_Somatic_Variant_Workflow.run_strelka2.strelka2_vep_vcf,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "gatk_intervallisttools_exome_plus",
    Gatk4_Intervallist2Bed_V0_1_0(
        bands=Kfdrc_Somatic_Variant_Workflow.gatk_intervallisttools_exome_plus_bands,
        exome_flag=Kfdrc_Somatic_Variant_Workflow.gatk_intervallisttools_exome_plus_exome_flag,
        interval_list=Kfdrc_Somatic_Variant_Workflow.bedops_gen_lancet_intervals.run_bed,
        reference_dict=Kfdrc_Somatic_Variant_Workflow.prepare_reference.reference_dict,
        scatter_ct=Kfdrc_Somatic_Variant_Workflow.gatk_intervallisttools_exome_plus_scatter_ct,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "run_theta2_purity",
    Kfdrc_Cnvkit_Batch_Wf(
        combined_exclude_expression=Kfdrc_Somatic_Variant_Workflow.combined_exclude_expression,
        combined_include_expression=Kfdrc_Somatic_Variant_Workflow.combined_include_expression,
        min_theta2_frac=Kfdrc_Somatic_Variant_Workflow.min_theta2_frac,
        normal_sample_name=Kfdrc_Somatic_Variant_Workflow.input_normal_name,
        output_basename=Kfdrc_Somatic_Variant_Workflow.output_basename,
        paired_vcf=Kfdrc_Somatic_Variant_Workflow.run_vardict.vardict_prepass_vcf,
        reference_cnn=Kfdrc_Somatic_Variant_Workflow.run_cnvkit.cnvkit_cnn_output,
        tumor_cns=Kfdrc_Somatic_Variant_Workflow.run_cnvkit.cnvkit_calls,
        tumor_sample_name=Kfdrc_Somatic_Variant_Workflow.input_tumor_name,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "select_lancet_bed_inteval",
    Mode_Selector_V0_1_0(
        input_mode=Kfdrc_Somatic_Variant_Workflow.wgs_or_wxs,
        wgs_input=Kfdrc_Somatic_Variant_Workflow.gatk_intervallisttools_exome_plus.outp,
        wxs_input=Kfdrc_Somatic_Variant_Workflow.gatk_intervallisttools.outp,
    ),
)


Kfdrc_Somatic_Variant_Workflow.step(
    "run_lancet",
    Kfdrc_Lancet_Sub_Wf(
        bed_invtl_split=[Kfdrc_Somatic_Variant_Workflow.select_lancet_bed_inteval.outp],
        indexed_reference_fasta=Kfdrc_Somatic_Variant_Workflow.prepare_reference.indexed_fasta,
        input_normal_aligned=Kfdrc_Somatic_Variant_Workflow.samtools_cram2bam_plus_calmd_normal.bam_file,
        input_normal_name=Kfdrc_Somatic_Variant_Workflow.input_normal_name,
        input_tumor_aligned=Kfdrc_Somatic_Variant_Workflow.samtools_cram2bam_plus_calmd_tumor.bam_file,
        input_tumor_name=Kfdrc_Somatic_Variant_Workflow.input_tumor_name,
        output_basename=Kfdrc_Somatic_Variant_Workflow.output_basename,
        padding=Kfdrc_Somatic_Variant_Workflow.choose_defaults.out_lancet_padding,
        ram=Kfdrc_Somatic_Variant_Workflow.lancet_ram,
        reference_dict=Kfdrc_Somatic_Variant_Workflow.prepare_reference.reference_dict,
        select_vars_mode=Kfdrc_Somatic_Variant_Workflow.select_vars_mode,
        vep_cache=Kfdrc_Somatic_Variant_Workflow.vep_cache,
        vep_ref_build=Kfdrc_Somatic_Variant_Workflow.vep_ref_build,
        window=Kfdrc_Somatic_Variant_Workflow.choose_defaults.out_lancet_window,
    ),
)

Kfdrc_Somatic_Variant_Workflow.output(
    "cnvkit_calls",
    source=Kfdrc_Somatic_Variant_Workflow.run_cnvkit.cnvkit_calls,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "cnvkit_cnn_output",
    source=Kfdrc_Somatic_Variant_Workflow.run_cnvkit.cnvkit_cnn_output,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "cnvkit_cnr",
    source=Kfdrc_Somatic_Variant_Workflow.run_cnvkit.cnvkit_cnr,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "cnvkit_gainloss",
    source=Kfdrc_Somatic_Variant_Workflow.run_cnvkit.cnvkit_gainloss,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "cnvkit_metrics",
    source=Kfdrc_Somatic_Variant_Workflow.run_cnvkit.cnvkit_metrics,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "cnvkit_seg",
    source=Kfdrc_Somatic_Variant_Workflow.run_cnvkit.cnvkit_seg,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "ctrlfreec_baf",
    source=Kfdrc_Somatic_Variant_Workflow.run_controlfreec.ctrlfreec_baf,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "ctrlfreec_bam_ratio",
    source=Kfdrc_Somatic_Variant_Workflow.run_controlfreec.ctrlfreec_bam_ratio,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "ctrlfreec_bam_seg",
    source=Kfdrc_Somatic_Variant_Workflow.run_controlfreec.ctrlfreec_bam_seg,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "ctrlfreec_config",
    source=Kfdrc_Somatic_Variant_Workflow.run_controlfreec.ctrlfreec_config,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "ctrlfreec_info",
    source=Kfdrc_Somatic_Variant_Workflow.run_controlfreec.ctrlfreec_info,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "ctrlfreec_pngs",
    source=Kfdrc_Somatic_Variant_Workflow.run_controlfreec.ctrlfreec_pngs,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "ctrlfreec_pval",
    source=Kfdrc_Somatic_Variant_Workflow.run_controlfreec.ctrlfreec_pval,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "lancet_prepass_vcf",
    source=Kfdrc_Somatic_Variant_Workflow.run_lancet.lancet_prepass_vcf,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "lancet_vep_maf",
    source=Kfdrc_Somatic_Variant_Workflow.run_lancet.lancet_vep_maf,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "lancet_vep_tbi",
    source=Kfdrc_Somatic_Variant_Workflow.run_lancet.lancet_vep_tbi,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "lancet_vep_vcf",
    source=Kfdrc_Somatic_Variant_Workflow.run_lancet.lancet_vep_vcf,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "manta_pass_vcf",
    source=Kfdrc_Somatic_Variant_Workflow.run_manta.manta_pass_vcf,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "manta_prepass_vcf",
    source=Kfdrc_Somatic_Variant_Workflow.run_manta.manta_prepass_vcf,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "mutect2_prepass_vcf",
    source=Kfdrc_Somatic_Variant_Workflow.run_mutect2.mutect2_filtered_vcf,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "mutect2_vep_maf",
    source=Kfdrc_Somatic_Variant_Workflow.run_mutect2.mutect2_vep_maf,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "mutect2_vep_tbi",
    source=Kfdrc_Somatic_Variant_Workflow.run_mutect2.mutect2_vep_tbi,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "mutect2_vep_vcf",
    source=Kfdrc_Somatic_Variant_Workflow.run_mutect2.mutect2_vep_vcf,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "strelka2_prepass_vcf",
    source=Kfdrc_Somatic_Variant_Workflow.run_strelka2.strelka2_prepass_vcf,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "strelka2_vep_maf",
    source=Kfdrc_Somatic_Variant_Workflow.run_strelka2.strelka2_vep_maf,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "strelka2_vep_tbi",
    source=Kfdrc_Somatic_Variant_Workflow.run_strelka2.strelka2_vep_tbi,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "strelka2_vep_vcf",
    source=Kfdrc_Somatic_Variant_Workflow.run_strelka2.strelka2_vep_vcf,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "theta2_calls",
    source=Kfdrc_Somatic_Variant_Workflow.run_theta2_purity.theta2_adjusted_cns,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "theta2_seg",
    source=Kfdrc_Somatic_Variant_Workflow.run_theta2_purity.theta2_adjusted_seg,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "theta2_subclonal_cns",
    source=Kfdrc_Somatic_Variant_Workflow.run_theta2_purity.theta2_subclonal_cns,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "theta2_subclonal_results",
    source=Kfdrc_Somatic_Variant_Workflow.run_theta2_purity.theta2_subclonal_results,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "theta2_subclone_seg",
    source=Kfdrc_Somatic_Variant_Workflow.run_theta2_purity.theta2_subclone_seg,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "vardict_prepass_vcf",
    source=Kfdrc_Somatic_Variant_Workflow.run_vardict.vardict_prepass_vcf,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "vardict_vep_somatic_only_maf",
    source=Kfdrc_Somatic_Variant_Workflow.run_vardict.vardict_vep_somatic_only_maf,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "vardict_vep_somatic_only_tbi",
    source=Kfdrc_Somatic_Variant_Workflow.run_vardict.vardict_vep_somatic_only_tbi,
    output_name=True,
)

Kfdrc_Somatic_Variant_Workflow.output(
    "vardict_vep_somatic_only_vcf",
    source=Kfdrc_Somatic_Variant_Workflow.run_vardict.vardict_vep_somatic_only_vcf,
    output_name=True,
)


if __name__ == "__main__":
    # or "cwl"
    Kfdrc_Somatic_Variant_Workflow().translate("wdl")
