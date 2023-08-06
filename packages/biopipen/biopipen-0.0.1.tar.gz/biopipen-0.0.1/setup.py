# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biopipen',
 'biopipen.cli',
 'biopipen.cli.commands',
 'biopipen.scripts',
 'biopipen.scripts.bcftools',
 'biopipen.scripts.bed',
 'biopipen.scripts.bedtools',
 'biopipen.scripts.bwtool',
 'biopipen.scripts.chipseq',
 'biopipen.scripts.cnvkit',
 'biopipen.scripts.common',
 'biopipen.scripts.docx',
 'biopipen.scripts.fastx',
 'biopipen.scripts.gatk',
 'biopipen.scripts.gene',
 'biopipen.scripts.gsea',
 'biopipen.scripts.hic',
 'biopipen.scripts.imtherapy',
 'biopipen.scripts.misc',
 'biopipen.scripts.mlearn',
 'biopipen.scripts.network',
 'biopipen.scripts.picard',
 'biopipen.scripts.plink',
 'biopipen.scripts.resource',
 'biopipen.scripts.sambam',
 'biopipen.scripts.seq',
 'biopipen.scripts.snp',
 'biopipen.scripts.snparray',
 'biopipen.scripts.sql',
 'biopipen.scripts.tabix',
 'biopipen.scripts.tcga',
 'biopipen.scripts.tcgamaf',
 'biopipen.scripts.tfbs',
 'biopipen.scripts.tsv',
 'biopipen.scripts.tumhet',
 'biopipen.scripts.vcf',
 'biopipen.scripts.web',
 'biopipen.sets',
 'biopipen.utils']

package_data = \
{'': ['*'],
 'biopipen': ['reports/bcftools/*',
              'reports/gsea/*',
              'reports/imtherapy/*',
              'reports/mlearn/*',
              'reports/plot/*',
              'reports/rnaseq/*',
              'reports/stats/*',
              'reports/tcgamaf/*',
              'reports/tumhet/*'],
 'biopipen.scripts': ['algorithm/*',
                      'cluster/*',
                      'eqtl/*',
                      'genomeplot/*',
                      'marray/*',
                      'plot/*',
                      'power/*',
                      'rank/*',
                      'rnaseq/*',
                      'stats/*']}

install_requires = \
['PyPPL>=3.0.0,<4.0.0',
 'diot',
 'pyparam',
 'pyppl_annotate',
 'pyppl_export',
 'pyppl_report',
 'rich>=6.0.0,<7.0.0',
 'toml<1.0.0']

entry_points = \
{'console_scripts': ['biopipen = biopipen.cli:main',
                     'biopipen-abc = biopipen.cli.proxy:abc']}

setup_kwargs = {
    'name': 'biopipen',
    'version': '0.0.1',
    'description': 'A set of PyPPL processes for bioinformatics.',
    'long_description': None,
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
