import boto3
import click
'''
This session was initialised with the following commands:
aws configure --profile shotty
  # aws access key ID
  # AWS secret access key
  # Default region: ap-southeast-2
  # Default output format: none at this stage
'''
session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

@click.command()
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances(Project):
    "List EC2 instances"
    # Initialise empty list to contain our instances
    instances = []

    if project:
        filters = [{'name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

        for i in instances:
            # Join fields with a comma
            print (', '.join((
                i.id,
                i.instance_type,
                i.placement['AvailabilityZone'],
                i.state['Name'],
                i.public_dns_name)))
        return

if __name__ == '__main__':
    list_instances()
