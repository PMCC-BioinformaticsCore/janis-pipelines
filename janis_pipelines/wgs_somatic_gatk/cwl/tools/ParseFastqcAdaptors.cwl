#!/usr/bin/env cwl-runner
baseCommand:
- python
- ParseFastqcAdaptors-script.py
class: CommandLineTool
cwlVersion: v1.0
doc: ''
id: ParseFastqcAdaptors
inputs:
- id: fastqc_datafiles
  inputBinding:
    prefix: --fastqc_datafiles
  label: fastqc_datafiles
  type:
    items: File
    type: array
- doc: "Specifies a file which contains the list of adapter sequences which will\n\
    be explicity searched against the library. The file must contain sets of named\
    \ adapters in\nthe form name[tab]sequence. Lines prefixed with a hash will be\
    \ ignored."
  id: cutadapt_adaptors_lookup
  inputBinding:
    prefix: --cutadapt_adaptors_lookup
  label: cutadapt_adaptors_lookup
  type:
  - File
  - 'null'
label: ParseFastqcAdaptors
outputs:
- id: adaptor_sequences
  label: adaptor_sequences
  outputBinding:
    glob: python-capture.stdout
    loadContents: true
    outputEval: "${\nvar d = JSON.parse(self[0].contents)\nif (!d) return null;\n\
      var c = d[\"adaptor_sequences\"]\nreturn c\n}"
  type:
    items: string
    type: array
requirements:
  InitialWorkDirRequirement:
    listing:
    - entry: "\nimport argparse, json, sys\nfrom typing import Optional, List, Dict,\
        \ Any\ncli = argparse.ArgumentParser(\"Argument parser for Janis PythonTool\"\
        )\ncli.add_argument(\"--fastqc_datafiles\", nargs='+', type=str, required=True)\n\
        cli.add_argument(\"--cutadapt_adaptors_lookup\", type=str, help='Specifies\
        \ a file which contains the list of adapter sequences which will\\nbe explicity\
        \ searched against the library. The file must contain sets of named adapters\
        \ in\\nthe form name[tab]sequence. Lines prefixed with a hash will be ignored.')\n\
        \nArray = List\nFile = str\nString = str\nFilename = str\nInt = int\nFloat\
        \ = float\nDouble = float\nBoolean = str\nDirectory = str\nStdout = str\n\
        class PythonTool:\n    File = str\n    Directory = str\n\n\n\ndef code_block(\n\
        \    fastqc_datafiles: List[File], cutadapt_adaptors_lookup: Optional[File]\n\
        ):\n    \"\"\"\n\n    :param fastqc_datafiles:\n\n    :param cutadapt_adaptors_lookup:\
        \ Specifies a file which contains the list of adapter sequences which will\n\
        \        be explicity searched against the library. The file must contain\
        \ sets of named adapters in\n        the form name[tab]sequence. Lines prefixed\
        \ with a hash will be ignored.\n    :return:\n    \"\"\"\n    if not cutadapt_adaptors_lookup:\n\
        \        return {\"adaptor_sequences\": []}\n\n    import mmap, re, csv\n\
        \    from io import StringIO\n    from sys import stderr\n\n    def get_overrepresented_text(f):\n\
        \        \"\"\"\n        Get the table \"Overrepresented sequences\" within\
        \ the fastqc_data.txt\n        \"\"\"\n        adapt_section_query = (\n \
        \           br\"(?s)>>Overrepresented sequences\\t\\S+\\n(.*?)>>END_MODULE\"\
        \n        )\n        # fastqc_datafile could be fairly large, so we'll use\
        \ mmap, and then\n        with open(f) as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)\
        \ as fp:\n            overrepresented_sequences_match = re.search(adapt_section_query,\
        \ fp)\n            if overrepresented_sequences_match is None:\n         \
        \       raise Exception(\n                    f\"Couldn't find query ('{adapt_section_query.decode('utf8')}')\
        \ in {fastqc_datafiles}\"\n                )\n\n            return overrepresented_sequences_match.groups()[0].decode(\"\
        utf8\")\n\n    def parse_tsv_table(tbl: str, skip_headers):\n        \"\"\"\
        \n        Parse a TSV table from a string using csvreader\n        \"\"\"\n\
        \n        rd = csv.reader(StringIO(tbl), delimiter=\"\\t\", quotechar='\"\
        ')\n        ret = list(rd)\n        if len(ret) == 0:\n            return\
        \ ret\n        if skip_headers:\n            ret.pop(0)  # discard headers\n\
        \        return ret\n\n    def get_cutadapt_map():\n        \"\"\"\n     \
        \   Helper method to parse the file 'cutadapt_adaptors_lookup' with\n    \
        \    format: 'name[tab]sequence' into the dictionary: '{ sequence: name }'\n\
        \        \"\"\"\n        cutadapt_map = {}\n        with open(cutadapt_adaptors_lookup)\
        \ as fp:\n            for row in fp:\n                st = row.strip()\n \
        \               if not st or st.startswith(\"#\"):\n                    continue\n\
        \n                # In reality, the format is $name[\\t+]$seqence (more than\
        \ one tab)\n                # so we'll just split on a tab, and remove all\
        \ the empty elements.\n                split = [f for f in st.split(\"\\t\"\
        ) if bool(f) and len(f) > 0]\n\n                # Invalid format for line,\
        \ so skip it.\n                if len(split) != 2:\n                    print(\n\
        \                        f\"Skipping cutadapt line '{st}' as irregular elements\
        \ ({len(split)})\",\n                        file=stderr,\n              \
        \      )\n                    continue\n\n                # reverse the order\
        \ from name[tab]sequence to { sequence: tab }\n                cutadapt_map[split[1]]\
        \ = split[0]\n        return cutadapt_map\n\n    # Start doing the work\n\
        \    adaptor_ids = set()\n    for fastqcfile in fastqc_datafiles:\n      \
        \  text = get_overrepresented_text(fastqcfile)\n        adaptor_ids = adaptor_ids.union(\n\
        \            set(a[0] for a in parse_tsv_table(text, skip_headers=True))\n\
        \        )\n\n    adaptor_sequences = []\n\n    if adaptor_ids:\n        cutadapt_map\
        \ = get_cutadapt_map()\n        for aid in adaptor_ids:\n            if aid\
        \ in cutadapt_map:\n                print(\n                    f\"Identified\
        \ sequence '{aid}' as '{cutadapt_map.get(aid)}' in lookup\",\n           \
        \         file=stderr,\n                )\n                adaptor_sequences.append(aid)\n\
        \n            else:\n                print(\n                    f\"Couldn't\
        \ find a corresponding sequence for '{aid}' in lookup map\",\n           \
        \         file=stderr,\n                )\n\n    return {\"adaptor_sequences\"\
        : adaptor_sequences}\n\n\ntry:\n    args = cli.parse_args()\n    result =\
        \ code_block(fastqc_datafiles=args.fastqc_datafiles, cutadapt_adaptors_lookup=args.cutadapt_adaptors_lookup)\n\
        \    print(json.dumps(result))\nexcept e:\n    print(str(e), file=sys.stderr)\n\
        \    raise\n"
      entryname: ParseFastqcAdaptors-script.py
  InlineJavascriptRequirement: {}
stdout: python-capture.stdout
