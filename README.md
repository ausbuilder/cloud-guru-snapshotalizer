# cloud-guru-snapshotalizer
Tutorial to manage AWS EC2 instance snapshots

## About
This project is a demo, and uses boto3 to manage AWS EC2 instance snapshots.

## Configuring
shotty uses the configuration file created by the AWS cli.

'aws configure --profile shotty'

## Running
python shotty/shotty.py <command> <subcommand>
<--project=PROJECT_NAME>

*command* is instance, volumes, or snapshots
*subcommand* - depends on command
*project* is optional
