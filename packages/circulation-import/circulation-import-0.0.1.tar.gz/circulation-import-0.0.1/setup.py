# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['circulation_import',
 'circulation_import.client',
 'circulation_import.metadata',
 'circulation_import.server',
 'circulation_import.sftp',
 'circulation_import.storage']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<21.0.0',
 'click>=7.1.2,<8.0.0',
 'paramiko>=2.7.2,<3.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'sqlalchemy-repr>=0.0.2,<0.0.3',
 'sqlalchemy>=1.3.19,<2.0.0',
 'typing-inspect>=0.6.0,<0.7.0',
 'watchdog>=0.10.3,<0.11.0']

setup_kwargs = {
    'name': 'circulation-import',
    'version': '0.0.1',
    'description': "Set of tools facilitating the process of importing book collections into SimplyE's Circulation Manager by using SFTP protocol",
    'long_description': '# circulation-import\nSet of tools facilitating the process of importing book collections into SimplyE\'s Circulation Manager by using SFTP protocol.\n\n## Architecture\n\ncirculation-import consists of two parts:\n- **client** responsible for uploading content to the SFTP server, waiting for a report, downloading it and converting it to CSV format\n- **server** responsible for watching for new book collections, importing them into CM using its **directory_import** script and uploading a report to the SFTP server\n  \nPicture below illustrates the architecture of the solution:\n  ![circulation-import architecture](docs/01-circulation-import-architecture.png "circulation-import architecture")\n\nAnother picture below contains a sequence diagram \n  ![Import workflow](docs/02-Import-workflow.png "Import workflow")\n\n\n## Usage\n1. Update all the submodules:\n```bash\ngit submodule update --remote --recursive\ncd circulation-lcp-test\ngit submodule update --remote --recursive\ncd ..\n```\n\n2. Run the LCP testbed:\n```bash\ndocker-compose --file circulation-lcp-test/docker-compose.yml --env-file circulation-lcp-test/.env up -d\n```\n\n3. Follow the instructions in LCP testbed\'s [README.md file](circulation-lcp-test/README.md) to set it up\n\n4. Run the server:\n```bash\ndocker-compose --file circulation-lcp-test/docker-compose.yml --file docker-compose.yml --env-file circulation-lcp-test/.env up -d\n```\n\n5. Create and activate a virtual environment:\n```bash\npython -m venv .venv\nsource .venv/bin/activate\n```\n\n3. Install *circulation-import* from PyPi:\n```bash\npip install circulation-import\n```\n\n7. Run the client:\n```bash\npython -m circulation-import client import \\\n    --collection-name=lcp \\\n    --data-source-name=data_source_1 \\\n    --books-directory=./circulation-lcp-test/lcp-collection/collection \\\n    --covers-directory=./circulation-lcp-test/lcp-collection/collection \\\n    --reports-directory=./reports \\\n    --metadata-file=./circulation-lcp-test/lcp-collection/collection/onix.xml \\\n    --metadata-format=onix \\\n    --configuration-file=./configuration/client-configuration.yml \\\n    --logging-configuration-file=./configuration/logging.yml\n```\n\n8. Go to [reports](./reports) folder and find a report in CSV format\n',
    'author': 'Viacheslav Bessonov',
    'author_email': 'viacheslav.bessonov@hilbertteam.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vbessonov/circulation-import',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
