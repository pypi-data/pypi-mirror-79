# circulation-import
Set of tools facilitating the process of importing book collections into SimplyE's Circulation Manager by using SFTP protocol.

## Architecture

circulation-import consists of two parts:
- **client** responsible for uploading content to the SFTP server, waiting for a report, downloading it and converting it to CSV format
- **server** responsible for watching for new book collections, importing them into CM using its **directory_import** script and uploading a report to the SFTP server
  
Picture below illustrates the architecture of the solution:
  ![circulation-import architecture](docs/01-circulation-import-architecture.png "circulation-import architecture")

Another picture below contains a sequence diagram 
  ![Import workflow](docs/02-Import-workflow.png "Import workflow")


## Usage
1. Update all the submodules:
```bash
git submodule update --remote --recursive
cd circulation-lcp-test
git submodule update --remote --recursive
cd ..
```

2. Run the LCP testbed:
```bash
docker-compose --file circulation-lcp-test/docker-compose.yml --env-file circulation-lcp-test/.env up -d
```

3. Follow the instructions in LCP testbed's [README.md file](circulation-lcp-test/README.md) to set it up

4. Run the server:
```bash
docker-compose --file circulation-lcp-test/docker-compose.yml --file docker-compose.yml --env-file circulation-lcp-test/.env up -d
```

5. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install *circulation-import* from PyPi:
```bash
pip install circulation-import
```

7. Run the client:
```bash
python -m circulation-import client import \
    --collection-name=lcp \
    --data-source-name=data_source_1 \
    --books-directory=./circulation-lcp-test/lcp-collection/collection \
    --covers-directory=./circulation-lcp-test/lcp-collection/collection \
    --reports-directory=./reports \
    --metadata-file=./circulation-lcp-test/lcp-collection/collection/onix.xml \
    --metadata-format=onix \
    --configuration-file=./configuration/client-configuration.yml \
    --logging-configuration-file=./configuration/logging.yml
```

8. Go to [reports](./reports) folder and find a report in CSV format
