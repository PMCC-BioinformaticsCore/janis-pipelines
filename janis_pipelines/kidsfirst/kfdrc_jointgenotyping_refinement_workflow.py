from datetime import datetime
from typing import List, Optional, Dict, Any

from janis_core import *
from janis_bioinformatics.data_types.fasta import FastaFai
from janis_bioinformatics.data_types.vcf import VcfTabix, VcfIdx
from janis_core.types.common_data_types import (
    File,
    Array,
    String,
    Boolean,
    GenericFileWithSecondaries,
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
    container="pgc-images.sbgenomics.com/d3b-bixu/bwa:0.7.17-r1188",
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
Script_Dynamicallycombineintervals_V0_1_0 = CommandToolBuilder(
    tool="script_dynamicallycombineintervals",
    base_command=["python", "-c"],
    inputs=[
        ToolInput(
            tag="input_vcfs",
            input_type=Array(t=File()),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="interval", input_type=File(), doc=InputDocumentation(doc=None)),
    ],
    outputs=[
        ToolOutput(
            tag="out_intervals",
            output_type=Array(t=File()),
            selector=WildcardSelector(wildcard="out-*.intervals"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/python:2.7.13",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "def parse_interval(interval):\n    colon_split = interval.split(':')\n    chromosome = colon_split[0]\n    dash_split = colon_split[1].split('-')\n    start = int(dash_split[0])\n    end = int(dash_split[1])\n    return chromosome, start, end\ndef add_interval(chr, start, end, i):\n    fn = 'out-{:0>5d}.intervals'.format(i)\n    lw = chr + ':' + str(start) + '-' + str(end) + '\n'\n    with open(fn, 'w') as fo:\n        fo.writelines(lw)\n    return chr, start, end\ndef main():\n    interval = '{JANIS_CWL_TOKEN_2}'\n    num_of_original_intervals = sum(1 for line in open(interval))\n    num_gvcfs = {JANIS_CWL_TOKEN_1}\n    merge_count = int(num_of_original_intervals/num_gvcfs/2.5)\n    count = 0\n    i = 1\n    chain_count = merge_count\n    l_chr, l_start, l_end = '', 0, 0\n    with open(interval) as f:\n        for line in f.readlines():\n            # initialization\n            if count == 0:\n                w_chr, w_start, w_end = parse_interval(line)\n                count = 1\n                continue\n            # reached number to combine, so spit out and start over\n            if count == chain_count:\n                l_char, l_start, l_end = add_interval(w_chr, w_start, w_end, i)\n                w_chr, w_start, w_end = parse_interval(line)\n                count = 1\n                i += 1\n                continue\n            c_chr, c_start, c_end = parse_interval(line)\n            # if adjacent keep the chain going\n            if c_chr == w_chr and c_start == w_end + 1:\n                w_end = c_end\n                count += 1\n                continue\n            # not adjacent, end here and start a new chain\n            else:\n                l_char, l_start, l_end = add_interval(w_chr, w_start, w_end, i)\n                w_chr, w_start, w_end = parse_interval(line)\n                count = 1\n                i += 1\n        if l_char != w_chr or l_start != w_start or l_end != w_end:\n            add_interval(w_chr, w_start, w_end, i)\nif __name__ == '__main__':\n    main()",
                JANIS_CWL_TOKEN_1="<expr>inputs.input_vcfs.length</expr>",
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="interval", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=True,
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

Gatk_Import_Genotype_Filtergvcf_Merge_V0_1_0 = CommandToolBuilder(
    tool="gatk_import_genotype_filtergvcf_merge",
    base_command=[],
    inputs=[
        ToolInput(
            tag="dbsnp_vcf", input_type=VcfIdx(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="input_vcfs",
            input_type=Array(t=VcfTabix()),
            position=1,
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="interval", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="reference_fasta",
            input_type=GenericFileWithSecondaries(secondaries=["^.dict", ".fai"]),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="sites_only_vcf",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="sites_only.variant_filtered.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="variant_filtered_vcf",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="variant_filtered.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.0.12.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "/gatk --java-options '-Xms4g' GenomicsDBImport --genomicsdb-workspace-path genomicsdb --batch-size 50 -L {JANIS_CWL_TOKEN_1} --reader-threads 16 -ip 5",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="interval", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="&& tar -cf genomicsdb.tar genomicsdb",
            position=2,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value=StringFormatter(
                "&& /gatk --java-options '-Xmx8g -Xms4g' GenotypeGVCFs -R {JANIS_CWL_TOKEN_1} -O output.vcf.gz -D {JANIS_CWL_TOKEN_2} -G StandardAnnotation --only-output-calls-starting-in-intervals -new-qual -V gendb://genomicsdb -L {JANIS_CWL_TOKEN_3}",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="reference_fasta", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="dbsnp_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="interval", type_hint=File()
                ),
            ),
            position=3,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="&& /gatk --java-options '-Xmx3g -Xms3g' VariantFiltration --filter-expression 'ExcessHet > 54.69' --filter-name ExcessHet -O variant_filtered.vcf.gz -V output.vcf.gz",
            position=4,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="&& /gatk MakeSitesOnlyVcf -I variant_filtered.vcf.gz -O sites_only.variant_filtered.vcf.gz",
            position=5,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
    ],
    cpus=1,
    memory=8000,
)
Gatk_Gathervcfs_V0_1_0 = CommandToolBuilder(
    tool="gatk_gathervcfs",
    base_command=[],
    inputs=[
        ToolInput(
            tag="input_vcfs",
            input_type=Array(t=File()),
            position=1,
            doc=InputDocumentation(doc=None),
        )
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="sites_only.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.0.12.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="/gatk --java-options '-Xmx6g -Xms6g' GatherVcfsCloud --ignore-safety-checks --gather-type BLOCK --output sites_only.vcf.gz",
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
        ToolArgument(
            value="&& /gatk IndexFeatureFile -F sites_only.vcf.gz",
            position=2,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        ),
    ],
    cpus=5,
    memory=10000,
)
Gatk_Indelsvariantrecalibrator_V0_1_0 = CommandToolBuilder(
    tool="gatk_indelsvariantrecalibrator",
    base_command=[],
    inputs=[
        ToolInput(
            tag="axiomPoly_resource_vcf",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="dbsnp_resource_vcf",
            input_type=VcfIdx(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="mills_resource_vcf",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="sites_only_variant_filtered_vcf",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="recalibration",
            output_type=VcfIdx(),
            selector=WildcardSelector(wildcard="indels.recal"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="tranches",
            output_type=File(),
            selector=WildcardSelector(wildcard="indels.tranches"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.0.12.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "/gatk --java-options '-Xmx24g -Xms24g' VariantRecalibrator -V {JANIS_CWL_TOKEN_3} -O indels.recal --tranches-file indels.tranches --trust-all-polymorphic --mode INDEL --max-gaussians 4 -resource mills,known=false,training=true,truth=true,prior=12:{JANIS_CWL_TOKEN_1} -resource axiomPoly,known=false,training=true,truth=false,prior=10:{JANIS_CWL_TOKEN_4} -resource dbsnp,known=true,training=false,truth=false,prior=2:{JANIS_CWL_TOKEN_2} -tranche 100.0 -tranche 99.95 -tranche 99.9 -tranche 99.5 -tranche 99.0 -tranche 97.0 -tranche 96.0 -tranche 95.0 -tranche 94.0 -tranche 93.5 -tranche 93.0 -tranche 92.0 -tranche 91.0 -tranche 90.0 -an FS -an ReadPosRankSum -an MQRankSum -an QD -an SOR -an DP",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="mills_resource_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="dbsnp_resource_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="sites_only_variant_filtered_vcf", type_hint=File(),
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="axiomPoly_resource_vcf", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=1,
    memory=7000,
)
Gatk_Snpsvariantrecalibratorcreatemodel_V0_1_0 = CommandToolBuilder(
    tool="gatk_snpsvariantrecalibratorcreatemodel",
    base_command=["/bin/bash", "-c"],
    inputs=[
        ToolInput(
            tag="dbsnp_resource_vcf",
            input_type=VcfIdx(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="hapmap_resource_vcf",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="omni_resource_vcf",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="one_thousand_genomes_resource_vcf",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="sites_only_variant_filtered_vcf",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="model_report",
            output_type=File(),
            selector=WildcardSelector(wildcard="snps.model.report"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.0.12.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "set -eo pipefail\n/gatk --java-options '-Xmx60g -Xms15g' VariantRecalibrator -V {JANIS_CWL_TOKEN_3} -O snps.recal --tranches-file snps.tranches --trust-all-polymorphic --mode SNP --output-model snps.model.report --max-gaussians 6 -resource hapmap,known=false,training=true,truth=true,prior=15:{JANIS_CWL_TOKEN_2} -resource omni,known=false,training=true,truth=true,prior=12:{JANIS_CWL_TOKEN_1} -resource 1000G,known=false,training=true,truth=false,prior=10:{JANIS_CWL_TOKEN_4} -resource dbsnp,known=true,training=false,truth=false,prior=7:{JANIS_CWL_TOKEN_5} -tranche 100.0 -tranche 99.95 -tranche 99.9 -tranche 99.8 -tranche 99.6 -tranche 99.5 -tranche 99.4 -tranche 99.3 -tranche 99.0 -tranche 98.0 -tranche 97.0 -tranche 90.0 -an QD -an MQRankSum -an ReadPosRankSum -an FS -an MQ -an SOR -an DP || (echo 'Failed with max gaussians 6, trying 4' && /gatk --java-options '-Xmx60g -Xms15g' VariantRecalibrator -V {JANIS_CWL_TOKEN_3} -O snps.recal --tranches-file snps.tranches --trust-all-polymorphic --mode SNP --output-model snps.model.report --max-gaussians 4 -resource hapmap,known=false,training=true,truth=true,prior=15:{JANIS_CWL_TOKEN_2} -resource omni,known=false,training=true,truth=true,prior=12:{JANIS_CWL_TOKEN_1} -resource 1000G,known=false,training=true,truth=false,prior=10:{JANIS_CWL_TOKEN_4} -resource dbsnp,known=true,training=false,truth=false,prior=7:{JANIS_CWL_TOKEN_5} -tranche 100.0 -tranche 99.95 -tranche 99.9 -tranche 99.8 -tranche 99.6 -tranche 99.5 -tranche 99.4 -tranche 99.3 -tranche 99.0 -tranche 98.0 -tranche 97.0 -tranche 90.0 -an QD -an MQRankSum -an ReadPosRankSum -an FS -an MQ -an SOR -an DP)",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="omni_resource_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="hapmap_resource_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="sites_only_variant_filtered_vcf", type_hint=File(),
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="one_thousand_genomes_resource_vcf",
                    type_hint=File(),
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="dbsnp_resource_vcf", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=1,
    memory=7000,
)
Gatk_Snpsvariantrecalibratorscattered_V0_1_0 = CommandToolBuilder(
    tool="gatk_snpsvariantrecalibratorscattered",
    base_command=[],
    inputs=[
        ToolInput(
            tag="dbsnp_resource_vcf",
            input_type=VcfIdx(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="hapmap_resource_vcf",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="model_report", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="omni_resource_vcf",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="one_thousand_genomes_resource_vcf",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="sites_only_variant_filtered_vcf",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="recalibration",
            output_type=VcfIdx(),
            selector=WildcardSelector(wildcard="scatter.snps.recal"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="tranches",
            output_type=File(),
            selector=WildcardSelector(wildcard="scatter.snps.tranches"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.0.12.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "/gatk --java-options '-Xmx3g -Xms3g' VariantRecalibrator -V {JANIS_CWL_TOKEN_4} -O scatter.snps.recal --tranches-file scatter.snps.tranches --output-tranches-for-scatter --trust-all-polymorphic --mode SNP --input-model {JANIS_CWL_TOKEN_3} --max-gaussians 6 -resource hapmap,known=false,training=true,truth=true,prior=15:{JANIS_CWL_TOKEN_2} -resource omni,known=false,training=true,truth=true,prior=12:{JANIS_CWL_TOKEN_1} -resource 1000G,known=false,training=true,truth=false,prior=10:{JANIS_CWL_TOKEN_5} -resource dbsnp,known=true,training=false,truth=false,prior=7:{JANIS_CWL_TOKEN_6} -tranche 100.0 -tranche 99.95 -tranche 99.9 -tranche 99.8 -tranche 99.6 -tranche 99.5 -tranche 99.4 -tranche 99.3 -tranche 99.0 -tranche 98.0 -tranche 97.0 -tranche 90.0 -an QD -an MQRankSum -an ReadPosRankSum -an FS -an MQ -an SOR -an DP",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="omni_resource_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="hapmap_resource_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="model_report", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="sites_only_variant_filtered_vcf", type_hint=File(),
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="one_thousand_genomes_resource_vcf",
                    type_hint=File(),
                ),
                JANIS_CWL_TOKEN_6=InputSelector(
                    input_to_select="dbsnp_resource_vcf", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=1,
    memory=7000,
)
Gatk_Gathertranches_V0_1_0 = CommandToolBuilder(
    tool="gatk_gathertranches",
    base_command=[],
    inputs=[
        ToolInput(
            tag="tranches",
            input_type=Array(t=File()),
            position=1,
            doc=InputDocumentation(doc=None),
        )
    ],
    outputs=[
        ToolOutput(
            tag="outp",
            output_type=File(),
            selector=WildcardSelector(wildcard="snps.gathered.tranches"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.0.12.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value="/gatk --java-options '-Xmx6g -Xms6g' GatherTranches --output snps.gathered.tranches",
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=2,
    memory=7000,
)
Gatk_Applyrecalibration_V0_1_0 = CommandToolBuilder(
    tool="gatk_applyrecalibration",
    base_command=[],
    inputs=[
        ToolInput(
            tag="indels_recalibration",
            input_type=VcfIdx(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="indels_tranches", input_type=File(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="input_vcf", input_type=VcfTabix(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="snps_recalibration",
            input_type=VcfIdx(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="snps_tranches", input_type=File(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="recalibrated_vcf",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="scatter.filtered.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        )
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.0.12.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "/gatk --java-options '-Xmx5g -Xms5g' ApplyVQSR -O tmp.indel.recalibrated.vcf -V {JANIS_CWL_TOKEN_4} --recal-file {JANIS_CWL_TOKEN_2} --tranches-file {JANIS_CWL_TOKEN_3} -ts-filter-level 99.7 --create-output-bam-index true -mode INDEL\n/gatk --java-options '-Xmx5g -Xms5g' ApplyVQSR -O scatter.filtered.vcf.gz -V tmp.indel.recalibrated.vcf --recal-file {JANIS_CWL_TOKEN_1} --tranches-file {JANIS_CWL_TOKEN_5} -ts-filter-level 99.7 --create-output-bam-index true -mode SNP",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="snps_recalibration", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="indels_recalibration", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="indels_tranches", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="input_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_5=InputSelector(
                    input_to_select="snps_tranches", type_hint=File()
                ),
            ),
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=2,
    memory=7000,
)
Kfdrc_Peddy_Tool_V0_1_0 = CommandToolBuilder(
    tool="kfdrc_peddy_tool",
    base_command=["python"],
    inputs=[
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="ped", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="vqsr_vcf", input_type=VcfTabix(), doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="output_csv",
            output_type=Array(t=File()),
            selector=WildcardSelector(wildcard="*_check.csv"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="output_html",
            output_type=Array(t=File()),
            selector=WildcardSelector(wildcard="*.html"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="output_peddy",
            output_type=Array(t=File()),
            selector=WildcardSelector(wildcard="*.peddy.ped"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/peddy:latest",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "-m peddy -p 4 --sites hg38 --prefix {JANIS_CWL_TOKEN_2}.peddy --plot {JANIS_CWL_TOKEN_3} {JANIS_CWL_TOKEN_1}",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="ped", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="vqsr_vcf", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    memory=1000,
)
Picard_Collectgvcfcallingmetrics_V0_1_0 = CommandToolBuilder(
    tool="picard_collectgvcfcallingmetrics",
    base_command=[],
    inputs=[
        ToolInput(
            tag="dbsnp_vcf", input_type=VcfIdx(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="input_vcf", input_type=VcfTabix(), doc=InputDocumentation(doc=None),
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
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.0.12.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "/gatk --java-options '-Xmx6g -Xms6g' CollectVariantCallingMetrics -I {JANIS_CWL_TOKEN_2} -O {JANIS_CWL_TOKEN_4} --DBSNP {JANIS_CWL_TOKEN_1} -SD {JANIS_CWL_TOKEN_5} -TI {JANIS_CWL_TOKEN_3} --THREAD_COUNT 8",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="dbsnp_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="input_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="wgs_evaluation_interval_list", type_hint=File(),
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="output_basename", type_hint=File()
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
    cpus=8,
    memory=7000,
)
Kfdrc_Gatk_Calculategenotypeposteriors_V0_1_0 = CommandToolBuilder(
    tool="kfdrc_gatk_calculategenotypeposteriors",
    base_command=["/gatk"],
    inputs=[
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="ped", input_type=File(optional=True), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference_fasta",
            input_type=GenericFileWithSecondaries(secondaries=["^.dict", ".fai"]),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="snp_sites", input_type=VcfIdx(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="vqsr_vcf", input_type=VcfTabix(), doc=InputDocumentation(doc=None),
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
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.0.12.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "--java-options '-Xms8000m -XX:GCTimeLimit=50 -XX:GCHeapFreeLimit=10' CalculateGenotypePosteriors -R {JANIS_CWL_TOKEN_1} -O {JANIS_CWL_TOKEN_3}.postCGP.vcf.gz -V {JANIS_CWL_TOKEN_4} --supporting {JANIS_CWL_TOKEN_2} ${\n  var arg = '';\n  if (inputs.ped != null){\n    arg += ' --pedigree ' + inputs.ped.path;\n  }\n  return arg;\n}",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="reference_fasta", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="snp_sites", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="vqsr_vcf", type_hint=File()
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
Kfdrc_Gatk_Variantfiltration_V0_1_0 = CommandToolBuilder(
    tool="kfdrc_gatk_variantfiltration",
    base_command=["/gatk"],
    inputs=[
        ToolInput(
            tag="cgp_vcf", input_type=VcfTabix(), doc=InputDocumentation(doc=None)
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference_fasta",
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
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:4.0.12.0",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "--java-options '-Xms8000m -XX:GCTimeLimit=50 -XX:GCHeapFreeLimit=10' VariantFiltration -R {JANIS_CWL_TOKEN_1} -O {JANIS_CWL_TOKEN_3}.postCGP.Gfiltered.vcf.gz -V {JANIS_CWL_TOKEN_2} -G-filter 'GQ < 20.0' -G-filter-name lowGQ",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="reference_fasta", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="cgp_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
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
Kfdrc_Gatk_Variantannotator_V0_1_0 = CommandToolBuilder(
    tool="kfdrc_gatk_variantannotator",
    base_command=["java"],
    inputs=[
        ToolInput(
            tag="cgp_filtered_vcf",
            input_type=VcfTabix(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(tag="ped", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="reference_fasta",
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
    container="pgc-images.sbgenomics.com/d3b-bixu/gatk:3.8_ubuntu",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "-Xms8000m -XX:GCTimeLimit=50 -XX:GCHeapFreeLimit=10 -jar /GenomeAnalysisTK.jar -T VariantAnnotator -R {JANIS_CWL_TOKEN_2} -o {JANIS_CWL_TOKEN_4}.postCGP.Gfiltered.deNovos.vcf.gz -V {JANIS_CWL_TOKEN_3} -A PossibleDeNovo -ped {JANIS_CWL_TOKEN_1} --pedigreeValidationType STRICT",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="ped", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="reference_fasta", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="cgp_filtered_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
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
Kf_Vep_Annotate_V0_1_0 = CommandToolBuilder(
    tool="kf_vep_annotate",
    base_command=["tar", "-xzf"],
    inputs=[
        ToolInput(tag="cache", input_type=File(), doc=InputDocumentation(doc=None)),
        ToolInput(
            tag="input_vcf", input_type=VcfTabix(), doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="output_basename",
            input_type=String(),
            doc=InputDocumentation(doc=None),
        ),
        ToolInput(
            tag="reference_fasta",
            input_type=FastaFai(),
            doc=InputDocumentation(doc=None),
        ),
    ],
    outputs=[
        ToolOutput(
            tag="output_txt",
            output_type=File(),
            selector=WildcardSelector(wildcard="*_stats.txt"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="output_vcf",
            output_type=VcfTabix(),
            selector=WildcardSelector(wildcard="*.vcf.gz"),
            doc=OutputDocumentation(doc=None),
        ),
        ToolOutput(
            tag="warn_txt",
            output_type=File(optional=True),
            selector=WildcardSelector(wildcard="*_warnings.txt"),
            doc=OutputDocumentation(doc=None),
        ),
    ],
    container="pgc-images.sbgenomics.com/d3b-bixu/vep:r93",
    version="v0.1.0",
    arguments=[
        ToolArgument(
            value=StringFormatter(
                "{JANIS_CWL_TOKEN_4} && perl /ensembl-vep/vep --cache --dir_cache $PWD --cache_version 93 --vcf --symbol --canonical --variant_class --offline --hgvs --hgvsg --fork 14 --sift b --vcf_info_field ANN -i {JANIS_CWL_TOKEN_1} -o STDOUT --stats_file {JANIS_CWL_TOKEN_3}_stats.txt --stats_text --warning_file {JANIS_CWL_TOKEN_3}_warnings.txt --fasta {JANIS_CWL_TOKEN_2} | /ensembl-vep/htslib/bgzip -c > {JANIS_CWL_TOKEN_3}.CGP.filtered.deNovo.vep.vcf.gz && /ensembl-vep/htslib/tabix {JANIS_CWL_TOKEN_3}.CGP.filtered.deNovo.vep.vcf.gz",
                JANIS_CWL_TOKEN_1=InputSelector(
                    input_to_select="input_vcf", type_hint=File()
                ),
                JANIS_CWL_TOKEN_2=InputSelector(
                    input_to_select="reference_fasta", type_hint=File()
                ),
                JANIS_CWL_TOKEN_3=InputSelector(
                    input_to_select="output_basename", type_hint=File()
                ),
                JANIS_CWL_TOKEN_4=InputSelector(
                    input_to_select="cache", type_hint=File()
                ),
            ),
            position=1,
            doc=InputDocumentation(doc=None),
            shell_quote=False,
        )
    ],
    cpus=14,
    memory=24000,
)

Kfdrc_Jointgenotyping_Refinement_Workflow = WorkflowBuilder(
    identifier="kfdrc_jointgenotyping_refinement_workflow",
    friendly_name="Kids First DRC Joint Genotyping Workflow",
    doc="# Kids First DRC Joint Genotyping Workflow\nKids First Data Resource Center Joint Genotyping Workflow (cram-to-deNovoGVCF). Cohort sample variant calling and genotype refinement.\n\nUsing existing gVCFs, likely from GATK Haplotype Caller, we follow this workflow: [Germline short variant discovery (SNPs + Indels)](https://software.broadinstitute.org/gatk/best-practices/workflow?id=11145), to create family joint calling and joint trios (typically mother-father-child) variant calls. Peddy is run to raise any potential issues in family relation definitions and sex assignment.\n\nIf you would like to run this workflow using the cavatica public app, a basic primer on running public apps can be found [here](https://www.notion.so/d3b/Starting-From-Scratch-Running-Cavatica-af5ebb78c38a4f3190e32e67b4ce12bb).\nAlternatively, if you'd like to run it locally using `cwltool`, a basic primer on that can be found [here](https://www.notion.so/d3b/Starting-From-Scratch-Running-CWLtool-b8dbbde2dc7742e4aff290b0a878344d) and combined with app-specific info from the readme below.\nThis workflow is the current production workflow, equivalent to this [Cavatica public app](https://cavatica.sbgenomics.com/public/apps#cavatica/apps-publisher/kfdrc-jointgenotyping-refinement-workflow).\n\n![data service logo](https://github.com/d3b-center/d3b-research-workflows/raw/master/doc/kfdrc-logo-sm.png)\n\n### Runtime Estimates\n- Single 5 GB gVCF Input: 90 Minutes & $2.25\n- Trio of 6 GB gVCFs Input: 240 Minutes & $3.25 \n\n### Tips To Run:\n1. inputs vcf files are the gVCF files from GATK Haplotype Caller, need to have the index **.tbi** files copy to the same project too.\n1. ped file in the input shows the family relationship between samples, the format should be the same as in GATK website [link](https://gatkforums.broadinstitute.org/gatk/discussion/7696/pedigree-ped-files), the Individual ID, Paternal ID and Maternal ID must be the same as in the inputs vcf files header.\n1. Here we recommend to use GRCh38 as reference genome to do the analysis, positions in gVCF should be GRCh38 too.\n1. Reference locations:\n    - https://console.cloud.google.com/storage/browser/genomics-public-data/resources/broad/hg38/v0/\n    - kfdrc bucket: s3://kids-first-seq-data/broad-references/\n    - cavatica: https://cavatica.sbgenomics.com/u/yuankun/kf-reference/\n1. Suggested inputs:\n    -  Axiom_Exome_Plus.genotypes.all_populations.poly.hg38.vcf.gz\n    -  Homo_sapiens_assembly38.dbsnp138.vcf\n    -  hapmap_3.3.hg38.vcf.gz\n    -  Mills_and_1000G_gold_standard.indels.hg38.vcf.gz\n    -  1000G_omni2.5.hg38.vcf.gz\n    -  1000G_phase1.snps.high_confidence.hg38.vcf.gz\n    -  Homo_sapiens_assembly38.dict\n    -  Homo_sapiens_assembly38.fasta.fai\n    -  Homo_sapiens_assembly38.fasta\n    -  1000G_phase3_v4_20130502.sites.hg38.vcf\n    -  hg38.even.handcurated.20k.intervals\n    -  homo_sapiens_vep_93_GRCh38_convert_cache.tar.gz, from ftp://ftp.ensembl.org/pub/release-93/variation/indexed_vep_cache/ - variant effect predictor cache.\n    -  wgs_evaluation_regions.hg38.interval_list\n\n## Other Resources\n- dockerfiles: https://github.com/d3b-center/bixtools\n\n![pipeline flowchart](https://github.com/kids-first/kf-jointgenotyping-workflow/blob/master/docs/kfdrc-jointgenotyping-refinement-workflow.png?raw=true 'Joint Genotyping Workflow')\n",
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "axiomPoly_resource_tbi",
    File(optional=True),
    doc=InputDocumentation(
        doc="Axiom_Exome_Plus.genotypes.all_populations.poly.hg38.vcf.gz.tbi"
    ),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "axiomPoly_resource_vcf",
    File(),
    doc=InputDocumentation(
        doc="Axiom_Exome_Plus.genotypes.all_populations.poly.hg38.vcf.gz"
    ),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "dbsnp_idx",
    File(optional=True),
    doc=InputDocumentation(doc="Homo_sapiens_assembly38.dbsnp138.vcf.idx"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "dbsnp_vcf",
    File(),
    doc=InputDocumentation(doc="Homo_sapiens_assembly38.dbsnp138.vcf"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "hapmap_resource_tbi",
    File(optional=True),
    doc=InputDocumentation(doc="Hapmap genotype SNP input tbi"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "hapmap_resource_vcf",
    File(),
    doc=InputDocumentation(doc="Hapmap genotype SNP input vcf"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "input_vcfs",
    Array(t=File()),
    doc=InputDocumentation(doc="Input array of individual sample gVCF files"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "mills_resource_tbi",
    File(optional=True),
    doc=InputDocumentation(doc="Mills_and_1000G_gold_standard.indels.hg38.vcf.gz.tbi"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "mills_resource_vcf",
    File(),
    doc=InputDocumentation(doc="Mills_and_1000G_gold_standard.indels.hg38.vcf.gz"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "omni_resource_tbi",
    File(optional=True),
    doc=InputDocumentation(doc="1000G_omni2.5.hg38.vcf.gz.tbi"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "omni_resource_vcf",
    File(),
    doc=InputDocumentation(doc="1000G_omni2.5.hg38.vcf.gz"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "one_thousand_genomes_resource_tbi",
    File(optional=True),
    doc=InputDocumentation(
        doc="1000G_phase1.snps.high_confidence.hg38.vcf.gz.tbi, high confidence snps"
    ),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "one_thousand_genomes_resource_vcf",
    File(),
    doc=InputDocumentation(
        doc="1000G_phase1.snps.high_confidence.hg38.vcf.gz, high confidence snps"
    ),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "output_basename", String(),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "ped", File(), doc=InputDocumentation(doc="Ped file for the family relationship"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "reference_dict",
    File(optional=True),
    doc=InputDocumentation(doc="Homo_sapiens_assembly38.dict"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "reference_fai",
    File(optional=True),
    doc=InputDocumentation(doc="Homo_sapiens_assembly38.fasta.fai"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "reference_fasta",
    File(),
    doc=InputDocumentation(doc="Homo_sapiens_assembly38.fasta"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "snp_sites_idx",
    File(optional=True),
    doc=InputDocumentation(doc="1000G_phase3_v4_20130502.sites.hg38.vcf.idx"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "snp_sites_vcf",
    File(),
    doc=InputDocumentation(doc="1000G_phase3_v4_20130502.sites.hg38.vcf"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "unpadded_intervals_file",
    File(),
    doc=InputDocumentation(doc="hg38.even.handcurated.20k.intervals"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "vep_cache",
    File(),
    doc=InputDocumentation(doc="Variant effect predictor cache file"),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.input(
    "wgs_evaluation_interval_list",
    File(),
    doc=InputDocumentation(doc="wgs_evaluation_regions.hg38.interval_list"),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "dynamicallycombineintervals",
    Script_Dynamicallycombineintervals_V0_1_0(
        input_vcfs=Kfdrc_Jointgenotyping_Refinement_Workflow.input_vcfs,
        interval=Kfdrc_Jointgenotyping_Refinement_Workflow.unpadded_intervals_file,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "index_1k",
    Tabix_Index_V0_1_0(
        input_file=Kfdrc_Jointgenotyping_Refinement_Workflow.one_thousand_genomes_resource_vcf,
        input_index=Kfdrc_Jointgenotyping_Refinement_Workflow.one_thousand_genomes_resource_tbi,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "index_axiomPoly",
    Tabix_Index_V0_1_0(
        input_file=Kfdrc_Jointgenotyping_Refinement_Workflow.axiomPoly_resource_vcf,
        input_index=Kfdrc_Jointgenotyping_Refinement_Workflow.axiomPoly_resource_tbi,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "index_dbsnp",
    Gatk_Indexfeaturefile_V0_1_0(
        input_file=Kfdrc_Jointgenotyping_Refinement_Workflow.dbsnp_vcf,
        input_index=Kfdrc_Jointgenotyping_Refinement_Workflow.dbsnp_idx,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "index_hapmap",
    Tabix_Index_V0_1_0(
        input_file=Kfdrc_Jointgenotyping_Refinement_Workflow.hapmap_resource_vcf,
        input_index=Kfdrc_Jointgenotyping_Refinement_Workflow.hapmap_resource_tbi,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "index_mills",
    Tabix_Index_V0_1_0(
        input_file=Kfdrc_Jointgenotyping_Refinement_Workflow.mills_resource_vcf,
        input_index=Kfdrc_Jointgenotyping_Refinement_Workflow.mills_resource_tbi,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "index_omni",
    Tabix_Index_V0_1_0(
        input_file=Kfdrc_Jointgenotyping_Refinement_Workflow.omni_resource_vcf,
        input_index=Kfdrc_Jointgenotyping_Refinement_Workflow.omni_resource_tbi,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "index_snp",
    Gatk_Indexfeaturefile_V0_1_0(
        input_file=Kfdrc_Jointgenotyping_Refinement_Workflow.snp_sites_vcf,
        input_index=Kfdrc_Jointgenotyping_Refinement_Workflow.snp_sites_idx,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "prepare_reference",
    Kfdrc_Prepare_Reference(
        input_dict=Kfdrc_Jointgenotyping_Refinement_Workflow.reference_dict,
        input_fai=Kfdrc_Jointgenotyping_Refinement_Workflow.reference_fai,
        input_fasta=Kfdrc_Jointgenotyping_Refinement_Workflow.reference_fasta,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "gatk_import_genotype_filtergvcf_merge",
    Gatk_Import_Genotype_Filtergvcf_Merge_V0_1_0(
        dbsnp_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.index_dbsnp.outp,
        input_vcfs=Kfdrc_Jointgenotyping_Refinement_Workflow.input_vcfs,
        interval=Kfdrc_Jointgenotyping_Refinement_Workflow.dynamicallycombineintervals.out_intervals,
        reference_fasta=Kfdrc_Jointgenotyping_Refinement_Workflow.prepare_reference.indexed_fasta,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "gatk_gathervcfs",
    Gatk_Gathervcfs_V0_1_0(
        input_vcfs=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_import_genotype_filtergvcf_merge.sites_only_vcf,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "gatk_indelsvariantrecalibrator",
    Gatk_Indelsvariantrecalibrator_V0_1_0(
        axiomPoly_resource_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.index_axiomPoly.outp,
        dbsnp_resource_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.index_dbsnp.outp,
        mills_resource_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.index_mills.outp,
        sites_only_variant_filtered_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_gathervcfs.outp,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "gatk_snpsvariantrecalibratorcreatemodel",
    Gatk_Snpsvariantrecalibratorcreatemodel_V0_1_0(
        dbsnp_resource_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.index_dbsnp.outp,
        hapmap_resource_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.index_hapmap.outp,
        omni_resource_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.index_omni.outp,
        one_thousand_genomes_resource_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.index_1k.outp,
        sites_only_variant_filtered_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_gathervcfs.outp,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "gatk_snpsvariantrecalibratorscattered",
    Gatk_Snpsvariantrecalibratorscattered_V0_1_0(
        dbsnp_resource_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.index_dbsnp.outp,
        hapmap_resource_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.index_hapmap.outp,
        model_report=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_snpsvariantrecalibratorcreatemodel.model_report,
        omni_resource_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.index_omni.outp,
        one_thousand_genomes_resource_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.index_1k.outp,
        sites_only_variant_filtered_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_import_genotype_filtergvcf_merge.sites_only_vcf,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "gatk_gathertranches",
    Gatk_Gathertranches_V0_1_0(
        tranches=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_snpsvariantrecalibratorscattered.tranches,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "gatk_applyrecalibration",
    Gatk_Applyrecalibration_V0_1_0(
        indels_recalibration=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_indelsvariantrecalibrator.recalibration,
        indels_tranches=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_indelsvariantrecalibrator.tranches,
        input_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_import_genotype_filtergvcf_merge.variant_filtered_vcf,
        snps_recalibration=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_snpsvariantrecalibratorscattered.recalibration,
        snps_tranches=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_gathertranches.outp,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "gatk_gatherfinalvcf",
    Gatk_Gathervcfs_V0_1_0(
        input_vcfs=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_applyrecalibration.recalibrated_vcf,
        output_basename=Kfdrc_Jointgenotyping_Refinement_Workflow.output_basename,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "peddy",
    Kfdrc_Peddy_Tool_V0_1_0(
        output_basename=Kfdrc_Jointgenotyping_Refinement_Workflow.output_basename,
        ped=Kfdrc_Jointgenotyping_Refinement_Workflow.ped,
        vqsr_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_gatherfinalvcf.outp,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "picard_collectvariantcallingmetrics",
    Picard_Collectgvcfcallingmetrics_V0_1_0(
        dbsnp_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.index_dbsnp.outp,
        input_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_gatherfinalvcf.outp,
        output_basename=Kfdrc_Jointgenotyping_Refinement_Workflow.output_basename,
        reference_dict=Kfdrc_Jointgenotyping_Refinement_Workflow.prepare_reference.reference_dict,
        wgs_evaluation_interval_list=Kfdrc_Jointgenotyping_Refinement_Workflow.wgs_evaluation_interval_list,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "gatk_calculategenotypeposteriors",
    Kfdrc_Gatk_Calculategenotypeposteriors_V0_1_0(
        output_basename=Kfdrc_Jointgenotyping_Refinement_Workflow.output_basename,
        ped=Kfdrc_Jointgenotyping_Refinement_Workflow.ped,
        reference_fasta=Kfdrc_Jointgenotyping_Refinement_Workflow.prepare_reference.indexed_fasta,
        snp_sites=Kfdrc_Jointgenotyping_Refinement_Workflow.index_snp.outp,
        vqsr_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_gatherfinalvcf.outp,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "gatk_variantfiltration",
    Kfdrc_Gatk_Variantfiltration_V0_1_0(
        cgp_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_calculategenotypeposteriors.outp,
        output_basename=Kfdrc_Jointgenotyping_Refinement_Workflow.output_basename,
        reference_fasta=Kfdrc_Jointgenotyping_Refinement_Workflow.prepare_reference.indexed_fasta,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "gatk_variantannotator",
    Kfdrc_Gatk_Variantannotator_V0_1_0(
        cgp_filtered_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_variantfiltration.outp,
        output_basename=Kfdrc_Jointgenotyping_Refinement_Workflow.output_basename,
        ped=Kfdrc_Jointgenotyping_Refinement_Workflow.ped,
        reference_fasta=Kfdrc_Jointgenotyping_Refinement_Workflow.prepare_reference.indexed_fasta,
    ),
)


Kfdrc_Jointgenotyping_Refinement_Workflow.step(
    "vep_annotate",
    Kf_Vep_Annotate_V0_1_0(
        cache=Kfdrc_Jointgenotyping_Refinement_Workflow.vep_cache,
        input_vcf=Kfdrc_Jointgenotyping_Refinement_Workflow.gatk_variantannotator.outp,
        output_basename=Kfdrc_Jointgenotyping_Refinement_Workflow.output_basename,
        reference_fasta=Kfdrc_Jointgenotyping_Refinement_Workflow.prepare_reference.indexed_fasta,
    ),
)

Kfdrc_Jointgenotyping_Refinement_Workflow.output(
    "cgp_vep_annotated_vcf",
    source=Kfdrc_Jointgenotyping_Refinement_Workflow.vep_annotate.output_vcf,
    output_name=True,
)

Kfdrc_Jointgenotyping_Refinement_Workflow.output(
    "collectvariantcallingmetrics",
    source=Kfdrc_Jointgenotyping_Refinement_Workflow.picard_collectvariantcallingmetrics.outp,
    output_name=True,
)

Kfdrc_Jointgenotyping_Refinement_Workflow.output(
    "peddy_csv",
    source=Kfdrc_Jointgenotyping_Refinement_Workflow.peddy.output_csv,
    output_name=True,
)

Kfdrc_Jointgenotyping_Refinement_Workflow.output(
    "peddy_html",
    source=Kfdrc_Jointgenotyping_Refinement_Workflow.peddy.output_html,
    output_name=True,
)

Kfdrc_Jointgenotyping_Refinement_Workflow.output(
    "peddy_ped",
    source=Kfdrc_Jointgenotyping_Refinement_Workflow.peddy.output_peddy,
    output_name=True,
)

Kfdrc_Jointgenotyping_Refinement_Workflow.output(
    "vcf_summary_stats",
    source=Kfdrc_Jointgenotyping_Refinement_Workflow.vep_annotate.output_txt,
    output_name=True,
)

Kfdrc_Jointgenotyping_Refinement_Workflow.output(
    "vep_warn",
    source=Kfdrc_Jointgenotyping_Refinement_Workflow.vep_annotate.warn_txt,
    output_name=True,
)


if __name__ == "__main__":
    # or "cwl"
    Kfdrc_Jointgenotyping_Refinement_Workflow().translate("wdl")
