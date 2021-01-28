# Kids first pipelines

Pipelines in this folder were automatically converted from CWL into Janis.

Pipelines:

- https://github.com/kids-first/kf-somatic-workflow
- https://github.com/kids-first/kf-rnaseq-workflow
- https://github.com/kids-first/kf-alignment-workflow
- https://github.com/kids-first/kf-jointgenotyping-workflow

General notes:

- These pipelines were translated on 2021-01-29
- They seem to generally go with the `^.bai` and `^.crai` secondary file patterns (usually).
- No guarantee about these translations, especially their accuracy. 

Cleanup process:

- Find and replace all of the `<expr>{expr}</expr>` block with the appropriate Janis counterpart
- Standardise the secondary files in the pipeline
- Check and run for consistency with the original pipelines

## Somatic pipeline

This has a few more custom javascript functions in it that we can't parse. Please see the log below for more information.

- Trying to support IndexedBam and IndexedCram by constructing secondary files based on the extension
- Strange workflow IDS with slashes, custom set to (`brownm28/mb-controlfreec-troubleshoot/control-freec-11-6-sbg/0` -> `control_freec`)
- Custom expressions for determining memory values

```text
$ janisdk fromcwl -o /Users/franklinmichael/source/janis-pipelines/janis_pipelines/kidsfirst/ /Users/franklinmichael/source/kf-somatic-workflow/workflow/kfdrc-somatic-variant-workflow.cwl
 
[INFO]: Loading CWL file: /Users/franklinmichael/source/kf-somatic-workflow/workflow/kfdrc-somatic-variant-workflow.cwl
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_index ? 'echo tabix -p vcf' : 'tabix -p vcf'</expr>'
[WARN]: Won't translate the expression for input file:///Users/franklinmichael/source/kf-somatic-workflow/tools/bwa_index.cwl#bwa_index/input_fasta: $(self.basename)
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_alt && inputs.input_amb && inputs.input_ann && inputs.input_bwt && inputs.input_pac && inputs.input_sa ? 'echo bwa' : inputs.generate_bwa_indexes ? 'bwa' : 'echo bwa'</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_dict ? 'echo java -jar /gatk-package-4.1.7.0-local.jar' : 'java -jar /gatk-package-4.1.7.0-local.jar' </expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_index ? 'echo samtools faidx' : 'samtools faidx' </expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_sample.secondaryFiles[0]</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_sample.nameroot</expr>'
The tag for tool: '0' (fullID: file:///Users/franklinmichael/source/kf-somatic-workflow/tools/control-freec-11-6-sbg.cwl#brownm28/mb-controlfreec-troubleshoot/control-freec-11-6-sbg/0) was invalid, please choose another: control_freec
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_reads.nameroot</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_reads.nameroot</expr>'
[CRITICAL]: Mismatch of types when joining 'inputs.min_subclone_presence' to 'control_free_c.min_subclone_presence': Float -/→ Optional<Integer>
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.ram * 1000</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_tumor_bam.nameroot</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.bed.nameroot</expr>'
[CRITICAL]: Mismatch of types when joining 'lancet.lancet_vcf' to 'sort_merge_lancet_vcf.input_vcfs': Array<File> -/→ Array<Gzipped<VCF>>
[CRITICAL]: Mismatch of types when joining 'inputs.indexed_reference_fasta' to 'vep_annot_lancet.reference': GenericFileWithSecondaries [.fai, ^.dict] -/→ FastaFai
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.ram * 1000</expr>'
[CRITICAL]: Mismatch of types when joining 'inputs.input_normal_aligned' to 'manta.input_normal_cram': GenericFileWithSecondaries [${
  var dpath = self.location.replace(self.basename, "")
  if(self.nameext == '.bam'){
    return {"location": dpath+self.nameroot+".bai", "class": "File"}
  }
  else{
    return {"location": dpath+self.basename+".crai", "class": "File"}
  }
}
] -/→ Optional<CramPair>
2021-01-29T10:11:31 [CRITICAL]: Mismatch of types when joining 'inputs.input_tumor_aligned' to 'manta.input_tumor_cram': GenericFileWithSecondaries [${
  var dpath = self.location.replace(self.basename, "")
  if(self.nameext == '.bam'){
    return {"location": dpath+self.nameroot+".bai", "class": "File"}
  }
  else{
    return {"location": dpath+self.basename+".crai", "class": "File"}
  }
}
] -/→ Optional<CramPair>
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_normal_name) > sample_list.txt && echo $(inputs.input_tumor_name) >> sample_list.txt && bcftools reheader -s sample_list.txt $(inputs.input_vcf.path) > $(inputs.input_vcf.nameroot.replace(".vcf", ".reheadered.vcf.gz")) && tabix $(inputs.input_vcf.nameroot.replace(".vcf", ".reheadered.vcf.gz")</expr>'
[CRITICAL]: Mismatch of types when joining 'prepare_reference.indexed_fasta' to 'run_manta.indexed_reference_fasta': File -/→ GenericFileWithSecondaries [.fai, ^.dict]
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.max_memory * 1000</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_tumor_aligned.nameroot</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.interval_list.nameroot</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.max_memory * 1000</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.aligned_reads.nameroot</expr>'
[CRITICAL]: Mismatch of types when joining 'inputs.input_normal_aligned' to 'gatk_get_normal_pileup_summaries.aligned_reads': GenericFileWithSecondaries [${
  var dpath = self.location.replace(self.basename, "")
  if(self.nameext == '.bam'){
    return {"location": dpath+self.nameroot+".bai", "class": "File"}
  }
  else{
    return {"location": dpath+self.basename+".crai", "class": "File"}
  }
}
] -/→ CramPair
2021-01-29T10:11:31 [CRITICAL]: Mismatch of types when joining 'inputs.input_tumor_aligned' to 'gatk_get_tumor_pileup_summaries.aligned_reads': GenericFileWithSecondaries [${
  var dpath = self.location.replace(self.basename, "")
  if(self.nameext == '.bam'){
    return {"location": dpath+self.nameroot+".bai", "class": "File"}
  }
  else{
    return {"location": dpath+self.basename+".crai", "class": "File"}
  }
}
] -/→ CramPair
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.max_memory * 1000</expr>'
[CRITICAL]: Mismatch of types when joining 'inputs.indexed_reference_fasta' to 'vep_annot_mutect2.reference': GenericFileWithSecondaries [.fai, ^.dict] -/→ FastaFai
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.manta_small_indels && inputs.use_manta_small_indels ? '--indelCandidates ' + inputs.manta_small_indels.path : ''</expr>'
[CRITICAL]: Mismatch of types when joining 'inputs.indexed_reference_fasta' to 'vep_annot_strelka2.reference': GenericFileWithSecondaries [.fai, ^.dict] -/→ FastaFai
[CRITICAL]: Mismatch of types when joining 'prepare_reference.indexed_fasta' to 'run_strelka2.indexed_reference_fasta': File -/→ GenericFileWithSecondaries [.fai, ^.dict]
[CRITICAL]: Mismatch of types when joining 'run_manta.manta_small_indels' to 'run_strelka2.manta_small_indels': File -/→ Optional<Gzipped<VCF>>
[CRITICAL]: Mismatch of types when joining to output node ['run_theta2.n3_graph', 'run_theta2.n2_results', 'run_theta2.best_results'] to 'theta2_subclonal_results' (Optional<File> -/→ Optional<Array<File>>)
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.ram * 1000</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.bed.nameroot</expr>'
[CRITICAL]: Mismatch of types when joining 'inputs.indexed_reference_fasta' to 'vep_annot_vardict.reference': GenericFileWithSecondaries [.fai, ^.dict] -/→ FastaFai
[CRITICAL]: Mismatch of types when joining 'prepare_reference.indexed_fasta' to 'samtools_cram2bam_plus_calmd_normal.reference': File -/→ FastaFai
[CRITICAL]: Mismatch of types when joining 'prepare_reference.indexed_fasta' to 'samtools_cram2bam_plus_calmd_tumor.reference': File -/→ FastaFai
[CRITICAL]: Mismatch of types when joining 'inputs.wgs_calling_interval_list' to 'select_interval_list.wgs_input': File -/→ Optional<String>
[CRITICAL]: Mismatch of types when joining 'inputs.padded_capture_regions' to 'select_interval_list.wxs_input': File -/→ Optional<String>
[CRITICAL]: Mismatch of types when joining 'select_interval_list.outp' to 'gatk_intervallisttools.interval_list': String -/→ Optional<File>
[CRITICAL]: Mismatch of types when joining 'select_interval_list.outp' to 'python_vardict_interval_split.wgs_bed_file': String -/→ File
[CRITICAL]: Mismatch of types when joining 'prepare_reference.indexed_fasta' to 'run_cnvkit.reference': File -/→ FastaFai
[CRITICAL]: Mismatch of types when joining 'prepare_reference.indexed_fasta' to 'run_controlfreec.indexed_reference_fasta': File -/→ FastaFai
[CRITICAL]: Mismatch of types when joining 'gatk_intervallisttools.outp' to 'select_mutect_bed_interval.wgs_input': Optional<Array<File>> -/→ Optional<String>
[CRITICAL]: Mismatch of types when joining 'gatk_intervallisttools.outp' to 'select_mutect_bed_interval.wxs_input': Optional<Array<File>> -/→ Optional<String>
[CRITICAL]: Mismatch of types when joining 'python_vardict_interval_split.split_intervals_bed' to 'select_vardict_bed_interval.wgs_input': Array<File> -/→ Optional<String>
[CRITICAL]: Mismatch of types when joining 'gatk_intervallisttools.outp' to 'select_vardict_bed_interval.wxs_input': Optional<Array<File>> -/→ Optional<String>
[CRITICAL]: Mismatch of types when joining 'select_mutect_bed_interval.outp' to 'run_mutect2.bed_invtl_split': String -/→ Array<File>
[CRITICAL]: Mismatch of types when joining 'prepare_reference.indexed_fasta' to 'run_mutect2.indexed_reference_fasta': File -/→ GenericFileWithSecondaries [.fai, ^.dict]
[CRITICAL]: Mismatch of types when joining 'select_vardict_bed_interval.outp' to 'run_vardict.bed_invtl_split': String -/→ Array<File>
[CRITICAL]: Mismatch of types when joining 'prepare_reference.indexed_fasta' to 'run_vardict.indexed_reference_fasta': File -/→ GenericFileWithSecondaries [.fai, ^.dict]
[CRITICAL]: Mismatch of types when joining 'gatk_intervallisttools_exome_plus.outp' to 'select_lancet_bed_inteval.wgs_input': Optional<Array<File>> -/→ Optional<String>
[CRITICAL]: Mismatch of types when joining 'gatk_intervallisttools.outp' to 'select_lancet_bed_inteval.wxs_input': Optional<Array<File>> -/→ Optional<String>
[CRITICAL]: Mismatch of types when joining 'select_lancet_bed_inteval.outp' to 'run_lancet.bed_invtl_split': String -/→ Array<File>
[CRITICAL]: Mismatch of types when joining 'prepare_reference.indexed_fasta' to 'run_lancet.indexed_reference_fasta': File -/→ GenericFileWithSecondaries [.fai, ^.dict]
[CRITICAL]: Mismatch of types when joining 'choose_defaults.out_lancet_padding' to 'run_lancet.padding': Optional<Integer> -/→ Integer
[CRITICAL]: Mismatch of types when joining 'choose_defaults.out_lancet_window' to 'run_lancet.window': Optional<Integer> -/→ Integer
[INFO]: Loaded Workflow: kfdrc_somatic_variant_workflow
[WARN]: Janis does not recognise <expr>inputs.ram * 1000</expr> (<class 'str'>) as a valid value for memory, returning 4GB
[WARN]: Janis does not recognise ${
    if (inputs.max_threads) {
        return inputs.max_threads
    } else {
        return 8
    }
} (<class 'str'>) as a valid CPU value, returning 1
2021-01-29T10:11:34 [WARN]: Janis does not recognise ${
    if (inputs.total_memory) {
        return inputs.total_memory
    } else {
        return 15000
    }
} (<class 'str'>) as a valid value for memory, returning 4GB
[WARN]: Janis does not recognise <expr>inputs.max_memory * 1000</expr> (<class 'str'>) as a valid value for memory, returning 4GB
[WARN]: Janis does not recognise <expr>inputs.max_memory * 1000</expr> (<class 'str'>) as a valid value for memory, returning 4GB
[WARN]: Janis does not recognise <expr>inputs.max_memory * 1000</expr> (<class 'str'>) as a valid value for memory, returning 4GB
[WARN]: Janis does not recognise <expr>inputs.max_memory * 1000</expr> (<class 'str'>) as a valid value for memory, returning 4GB
[WARN]: Janis does not recognise <expr>inputs.ram * 1000</expr> (<class 'str'>) as a valid value for memory, returning 4GB
[WARN]: Janis does not recognise <expr>inputs.ram * 1000</expr> (<class 'str'>) as a valid value for memory, returning 4GB
```


## RNA Seq pipeline

- The expression tool `kf-rnaseq-workflow/tools/expression_parse_strand_param.cwl` will not translate correctly, some extra functionality might need to be added to Janis

```text
$ janisdk fromcwl -o /Users/franklinmichael/source/janis-pipelines/janis_pipelines/kidsfirst/ /Users/franklinmichael/source/kf-rnaseq-workflow/workflow/kfdrc-rnaseq-workflow.cwl

[INFO]: Loading CWL file: /Users/franklinmichael/source/kf-rnaseq-workflow/workflow/kfdrc-rnaseq-workflow.cwl
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>"*TRIMMED." + inputs.readFilesIn1</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.strand ? inputs.strand == "default" ? "" : "--"+inputs.strand : ""</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.reads2 ? inputs.reads1.path+" "+inputs.reads2.path : "--single -l "+inputs.avg_frag_len+" -s "+inputs.std_dev+" "+inputs.reads1</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.chimeric_sam_out.nameroot</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.chimeric_sam_out.nameroot</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.unsorted_bam.nameroot</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.genomeDir.nameroot.split('.'</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.readFilesIn2 ? inputs.readFilesIn2.path : ''</expr>'
[WARN]: Expression tools aren't well converted to Janis as they rely on unimplemented functionality: file:///Users/franklinmichael/source/kf-rnaseq-workflow/tools/expression_parse_strand_param.cwl#expression_strand_params
```


## Alignment workflow

- Secondary files are decided based on an input string ... eep


```
$ janisdk fromcwl -o /Users/franklinmichael/source/janis-pipelines/janis_pipelines/kidsfirst/ /Users/franklinmichael/source/kf-alignment-workflow/workflows/kfdrc_alignment_wf.cwl 
2021-01-29T10:20:16 [INFO]: Loading CWL file: /Users/franklinmichael/source/kf-alignment-workflow/workflows/kfdrc_alignment_wf.cwl
2021-01-29T10:20:17 [WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_bam.nameroot</expr>'
2021-01-29T10:20:17 [WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_bam.nameroot</expr>'
2021-01-29T10:20:17 [WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_bam.nameroot</expr>'
2021-01-29T10:20:17 [WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_index ? 'echo /gatk' : '/gatk'</expr>'
2021-01-29T10:20:17 [WARN]: Couldn't translate javascript token, will use the placeholder '<expr>runtime.outdir</expr>'
2021-01-29T10:20:17 [CRITICAL]: Mismatch of types when joining 'inputs.input_bam' to 'verifybamid.input_bam': File -/→ GenericFileWithSecondaries [^.bai]
2021-01-29T10:20:17 [CRITICAL]: Mismatch of types when joining 'inputs.indexed_reference_fasta' to 'verifybamid.ref_fasta': File -/→ FastaFai
2021-01-29T10:20:17 [CRITICAL]: Mismatch of types when joining 'inputs.input_bam' to 'gatk_haplotypecaller.input_bam': File -/→ GenericFileWithSecondaries [^.bai]
2021-01-29T10:20:17 [CRITICAL]: Mismatch of types when joining 'inputs.indexed_reference_fasta' to 'gatk_haplotypecaller.reference': File -/→ GenericFileWithSecondaries [^.dict, .fai]
2021-01-29T10:20:17 [WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_index ? 'echo tabix -p vcf' : 'tabix -p vcf'</expr>'
2021-01-29T10:20:17 [WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_bam.nameroot</expr>'
2021-01-29T10:20:17 [WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_bam.nameroot</expr>'
2021-01-29T10:20:17 [WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_bam.nameroot</expr>'
2021-01-29T10:20:17 [WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_bam.nameroot</expr>'
2021-01-29T10:20:17 [WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_bam.nameroot</expr>'
2021-01-29T10:20:17 [WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_bam.nameroot</expr>'
2021-01-29T10:20:17 [WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_bam.nameroot</expr>'
2021-01-29T10:20:17 [WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_bam.nameroot</expr>'
2021-01-29T10:20:17 [WARN]: Expression tools aren't well converted to Janis as they rely on unimplemented functionality: file:///Users/franklinmichael/source/kf-alignment-workflow/tools/expression_preparerg.cwl#expression_preparerg
2021-01-29T10:20:17 [WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_bam.nameroot</expr>'
2021-01-29T10:20:17 [CRITICAL]: Mismatch of types when joining 'process_bams.unsorted_bams' to 'sambamba_merge.bams': Array<Array<Array<Array<File>>>> -/→ Array<String>
2021-01-29T10:20:17 [CRITICAL]: Mismatch of types when joining 'process_pe_reads.unsorted_bams' to 'sambamba_merge.bams': Array<Array<Array<File>>> -/→ Array<String>
2021-01-29T10:20:17 [CRITICAL]: Mismatch of types when joining 'process_se_reads.unsorted_bams' to 'sambamba_merge.bams': Array<Array<Array<File>>> -/→ Array<String>
2021-01-29T10:20:17 [CRITICAL]: Mismatch of types when joining 'bundle_secondaries.outp' to 'picard_qualityscoredistribution.reference': GenericFileWithSecondaries [$(inputs.secondary_files)] -/→ FastaFai
2021-01-29T10:20:17 [CRITICAL]: Mismatch of types when joining 'bundle_secondaries.outp' to 'samtools_bam_to_cram.reference': GenericFileWithSecondaries [$(inputs.secondary_files)] -/→ FastaFai
2021-01-29T10:20:17 [CRITICAL]: Mismatch of types when joining 'bundle_secondaries.outp' to 'picard_collectalignmentsummarymetrics.reference': GenericFileWithSecondaries [$(inputs.secondary_files)] -/→ FastaFai
2021-01-29T10:20:17 [CRITICAL]: Mismatch of types when joining 'bundle_secondaries.outp' to 'picard_collectgcbiasmetrics.reference': GenericFileWithSecondaries [$(inputs.secondary_files)] -/→ FastaFai
2021-01-29T10:20:17 [CRITICAL]: Mismatch of types when joining 'bundle_secondaries.outp' to 'picard_collecthsmetrics.reference': GenericFileWithSecondaries [$(inputs.secondary_files)] -/→ FastaFai
2021-01-29T10:20:17 [CRITICAL]: Mismatch of types when joining 'bundle_secondaries.outp' to 'picard_collectinsertsizemetrics.reference': GenericFileWithSecondaries [$(inputs.secondary_files)] -/→ FastaFai
2021-01-29T10:20:17 [CRITICAL]: Mismatch of types when joining 'bundle_secondaries.outp' to 'picard_collectsequencingartifactmetrics.reference': GenericFileWithSecondaries [$(inputs.secondary_files)] -/→ FastaFai
2021-01-29T10:20:17 [CRITICAL]: Mismatch of types when joining 'bundle_secondaries.outp' to 'picard_collectwgsmetrics.reference': GenericFileWithSecondaries [$(inputs.secondary_files)] -/→ FastaFai
```

## Joint genotyping pipeline

```text
$ janisdk fromcwl -o /Users/franklinmichael/source/janis-pipelines/janis_pipelines/kidsfirst/ /Users/franklinmichael/source/kf-jointgenotyping-workflow/workflow/kfdrc-jointgenotyping-refinement-workflow.cwl 

[INFO]: Loading CWL file: /Users/franklinmichael/source/kf-jointgenotyping-workflow/workflow/kfdrc-jointgenotyping-refinement-workflow.cwl
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_vcfs.length</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.output_basename + '.vcf.gz'</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.output_basename + '.vcf.gz'</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.output_basename + '.vcf.gz'</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_index ? 'echo tabix -p vcf' : 'tabix -p vcf'</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_index ? 'echo /gatk' : '/gatk'</expr>'
[WARN]: Won't translate the expression for input file:///Users/franklinmichael/source/kf-jointgenotyping-workflow/tools/bwa_index.cwl#bwa_index/input_fasta: $(self.basename)
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_alt && inputs.input_amb && inputs.input_ann && inputs.input_bwt && inputs.input_pac && inputs.input_sa ? 'echo bwa' : inputs.generate_bwa_indexes ? 'bwa' : 'echo bwa'</expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_dict ? 'echo java -jar /gatk-package-4.1.7.0-local.jar' : 'java -jar /gatk-package-4.1.7.0-local.jar' </expr>'
[WARN]: Couldn't translate javascript token, will use the placeholder '<expr>inputs.input_index ? 'echo samtools faidx' : 'samtools faidx' </expr>'
[CRITICAL]: Mismatch of types when joining 'inputs.input_vcfs' to 'gatk_import_genotype_filtergvcf_merge.input_vcfs': Array<File> -/→ Array<Gzipped<VCF>>
[CRITICAL]: Mismatch of types when joining 'prepare_reference.indexed_fasta' to 'gatk_import_genotype_filtergvcf_merge.reference_fasta': File -/→ GenericFileWithSecondaries [^.dict, .fai]
[CRITICAL]: Mismatch of types when joining 'prepare_reference.indexed_fasta' to 'gatk_calculategenotypeposteriors.reference_fasta': File -/→ GenericFileWithSecondaries [^.dict, .fai]
[CRITICAL]: Mismatch of types when joining 'prepare_reference.indexed_fasta' to 'gatk_variantfiltration.reference_fasta': File -/→ GenericFileWithSecondaries [^.dict, .fai]
[CRITICAL]: Mismatch of types when joining 'prepare_reference.indexed_fasta' to 'gatk_variantannotator.reference_fasta': File -/→ GenericFileWithSecondaries [^.dict, .fai]
[CRITICAL]: Mismatch of types when joining 'prepare_reference.indexed_fasta' to 'vep_annotate.reference_fasta': File -/→ FastaFai
[INFO]: Loaded Workflow: kfdrc_jointgenotyping_refinement_workflow
[INFO]: Exporting tool files to '/Users/franklinmichael/source/janis-pipelines/janis_pipelines/kidsfirst/'
```