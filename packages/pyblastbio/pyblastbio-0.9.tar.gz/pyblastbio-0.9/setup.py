# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyblast', 'pyblast.blast', 'pyblast.utils']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.73,<2.0',
 'fire>=0.3,<0.4',
 'loggable-jdv>=0.1.4,<0.2.0',
 'networkx>=2.4,<3.0',
 'termcolor>=1.1,<2.0']

extras_require = \
{'testing': ['tox>=3.13,<4.0', 'tox-conda>=0.2.0,<0.3.0']}

entry_points = \
{'console_scripts': ['pyblast = pyblast:cli.main']}

setup_kwargs = {
    'name': 'pyblastbio',
    'version': '0.9',
    'description': '',
    'long_description': '![](https://github.com/jvrana/pyblast/workflows/Python%package/badge.svg)\n[![Coverage Status](https://coveralls.io/repos/github/jvrana/pyblast/badge.svg?branch=master)](https://coveralls.io/github/jvrana/pyblast?branch=master)\n[![PyPI version](https://badge.fury.io/py/pyblastbio.svg)](https://badge.fury.io/py/pyblastbio)\n![Build package](https://github.com/jvrana/pyblast2/workflows/Build%20package/badge.svg)\n\n\n# pyblast\n\nThis is a wrapper for other applications to run blast searches on SeqRecord objects and JSON objects. Intended to\nbe used in small python applications.\n\nFeatures include:\n* Automatic BLAST parsing to JSON\n* Alignment to circular queries, using either linear or circular subjects\n* Blast self installation\n\n# Installation\n\nYou can install BLAST to the pyblast directory using the following command:\n\n```\npyblast install\n```\n\nThis will install it to pyblast/blast_bin in your python install location. If you want BLAST installed somewhere else, move the *ncbi-blast-X.X.X+* folder\nto your desired location and add *path/to/ncbi-blast-X.X.X+/bin* to you $PATH. **PyBlast** will prefer to use the blast stored\nin your executable path. If it cannot find a blast executable there, it looks for it in that paths in the pyblast/blast_bin/_paths.txt.\nfile. _paths.txt is automatically updated when you run install_blast.py so theres no need to manage the paths manually.\n\nAfter installing and verifying the `blastn` command works from the cmd line,\n\n```\npip install pyblastbio\n```\n\n## Usage\n\nThis package is a python wrapper for the BLAST command line, intended to be run along with a microservice (e.g. Flask) or for a quick alignment in a jupyter notebook or small python script/app.\n\nThis package also includes a basic python-based installation script which is used in unit-testing.\n\n### Running a blast query on a Bio.SeqRecord object\n\nWe can do a quick alignment to some sequences using the following, which gives us a nice dictionary of the results:\n\n```python\nfrom pyblast import BioBlast\nfrom pyblast.utils import make_linear, make_circular\nfrom Bio.SeqRecord import SeqRecord\nfrom Bio.Seq import Seq\n\nqueries = [\n  SeqRecord(Seq("ACGTGATTCGTCGTGTAGTTGAGTGTTACGTTGCATGTCGTACGTGTGTAGTGTCGTGTAGTGCTGATGCTACGTGATCG"))\n]\nsubjects = [\n  SeqRecord(Seq("ACGTGATTCGTCGTGTAGTTGAGTGTTACGTTGCATGTCGTTACGTGATCG"))\n]\n\n# pyblast requires a \'topology\' annotation on the SeqRecords.\n# we can make records circular or linear using `make_linear` or `make_circular` methods\nsubjects = make_linear(subjects)\nqueries = make_linear(queries)\n\nblast = BioBlast(subjects, queries)\nresults = blast.quick_blastn()\nprint(results)\n```\n\n```json\n[\n  {\n    "query": {\n      "start": 1,\n      "end": 46,\n      "bases": "ACGTGATTCGTCGTGTAGTTGAGTGTTACGTTGCATGTCGT-ACGTG",\n      "strand": 1,\n      "length": 80,\n      "sequence_id": "11e17df2-579f-4234-a1e6-f4e3fadfe277",\n      "circular": false,\n      "name": "<unknown name>",\n      "origin_key": "bbadd55c-9413-4394-a23c-0da983630b98",\n      "origin_record_id": "<unknown id>",\n      "origin_sequence_length": 80\n    },\n    "subject": {\n      "start": 1,\n      "end": 47,\n      "bases": "ACGTGATTCGTCGTGTAGTTGAGTGTTACGTTGCATGTCGTTACGTG",\n      "strand": 1,\n      "length": 51,\n      "sequence_id": "69248d23-1044-4a75-80c9-53b999796d48",\n      "circular": false,\n      "name": "<unknown name>",\n      "origin_key": "1f627d51-93df-458b-ba36-9b5a7b483a4d",\n      "origin_record_id": "<unknown id>",\n      "origin_sequence_length": 51\n    },\n    "meta": {\n      "query acc.": "11e17df2-579f-4234-a1e6-f4e3fadfe277",\n      "subject acc.": "69248d23-1044-4a75-80c9-53b999796d48",\n      "score": 43,\n      "evalue": 0,\n      "bit score": 80,\n      "alignment length": 47,\n      "identical": 46,\n      "gap opens": 1,\n      "gaps": 1,\n      "query length": 80,\n      "q. start": 1,\n      "q. end": 46,\n      "subject length": 51,\n      "s. start": 1,\n      "s. end": 47,\n      "subject strand": "plus",\n      "query seq": "ACGTGATTCGTCGTGTAGTTGAGTGTTACGTTGCATGTCGT-ACGTG",\n      "subject seq": "ACGTGATTCGTCGTGTAGTTGAGTGTTACGTTGCATGTCGTTACGTG",\n      "span_origin": true\n    }\n  }\n]\n```\n\n### Running blast on circular subjects and queries\n\nPyblast handles alignments to circular subjects and queries as well. As you can see below, we get a complete alignment of the subject (1 to 50) to the circular query (82 over origin to 30). Circular subjects and circular queries can be mixed together, as well as multiple queries.\n\n```\nseq = "ACGTTGTAGTGTAGTTGATGATGATGTCTGTGTCGTGTGATGTGCTGTAGTGTTTAGGGGCGGCGCGGAGTATGCTG"\nqueries = [\n\tSeqRecord(Seq(seq))\n]\n\nsubjects = [\n\tSeqRecord(Seq(seq[-20:] + seq[:30]))\n]\n\n# pyblast requires a \'topology\' annotation on the SeqRecords.\n# we can make records circular or linear using `make_linear` or `make_circular` methods\nsubjects = make_circular(subjects)\nqueries = make_circular(queries)\n\nblast = BioBlast(subjects, queries)\nresults = blast.quick_blastn()\nprint(results)\n```\n\n```json\n[\n  {\n    "query": {\n      "start": 82,\n      "end": 30,\n      "strand": 1,\n      "...": "..."\n    },\n    "subject": {\n      "start": 1,\n      "end": 50,\n      "strand": 1,\n      "...": "..."\n    },\n    "meta": {\n    \t"...": "..."\n    }\n]\n```\n\n### BioBlastFactory\n\nIn some cases, we will want to share the same sequences for different types of alignments. For example, we may want to align a set of primers and a set of templates to the same query records. In these types of cases, we can use the **BioBlastFactory**:\n\n```python\nfrom pyblast import BioBlastFactory\n\n# initialize a new factory\nfactory = BioBlastFactory()\n\n# add records accessible by keyword\nfactory.add_records(records1, "primers")\nfactory.add_records(records2, "templates")\nfactory.add_records(records3, "queries")\n\n# we spawn new BioBlast alignmers from the keywords above\nprimer_alignment = factory("primers", "queries")\ntemplate_alignment = factory("templates", "queries")\n\n# we can then run alignments, ensuring the queries in both results\n# refer to the exact same query\nprimer_results = primer_alignment.quick_short_blastn()\ntemplate_results = template_alignment.quick_blastn()\n```\n\n### Utilities for reading files\n\n**pyblast** includes utilities for reading in *fasta* and *genbank* files.\n\n```python\nfrom pyblast.utils import load_glob, load_genbank_glob, load_fasta_glob\n\n# load many genbank files into a list of SeqRecords\n# \'topology\' is automatically detected here\n# we enforce all record_ids to be unique (a requirement for pyblast)\nrecords1 = load_genbank_glob("~/mydesigns/*.gb", force_unique_ids=True)\n\n# load many fasta files into a list of SeqRecords\n# \'topology\' is NOT detected\n# we enforce all record_ids to be unique (a requirement for pyblast)\nrecords2 = make_linear(load_fasta_glob("~/mydesigns/*.fasta"), force_unique_ids=True)\n\n```\n',
    'author': 'Justin Vrana',
    'author_email': 'justin.vrana@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.github.com/jvrana/pyblast2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
