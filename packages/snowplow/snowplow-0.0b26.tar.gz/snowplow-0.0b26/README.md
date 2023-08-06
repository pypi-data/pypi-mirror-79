# S3 to Synapse Orchestration

- Utilities for provisioning EBS volumes and attaching them to an EC2 instance.
- Pull a S3 bucket to the EBS volume.
- Transfer the contents of the S3 bucket to Synapse. 
- List files in S3.
- List local files.
- Compare local objects to S3 objects.

## Dependencies

- [Python3.7](https://www.python.org/)
- A [Synapse](https://www.synapse.org/) account with a username/password. Authentication through a 3rd party (.e.g., Google) will not work, you must have a Synapse user/pass for the [API to authenticate](http://docs.synapse.org/python/#connecting-to-synapse).
- [synapse-uploader](https://github.com/ki-tools/synapse_uploader)
- [AWS CLI](https://aws.amazon.com/cli)

## Installation

```shell script
pip install snowplow
```

or 
```shell script
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple --no-cache-dir snowplow
```

## Usage

```text
usage: snowplow [-h] {list-local,list-s3,compare-s3,compare-csv,new} ...

S3 to Synapse Orchestration

optional arguments:
  -h, --help            show this help message and exit

Commands:
  {list-local,list-s3,compare-s3,compare-csv,new}
    list-local          List all the folders and files with their size and
                        MD5.
    list-s3             List all the files in an S3 bucket with their file
                        size.
    compare-s3          Compare a local directory against an S3 bucket.
    compare-csv         Compare a CSV file from the list-local command with a
                        local directory.
    new                 Provision a new transfer instance. This will create an
                        EBS volume and attach it to the host system
```
