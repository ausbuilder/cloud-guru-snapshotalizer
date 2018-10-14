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

# Create function to filter instances instead of repeating code for each function
def filter_instances(project):
    #Create empty list
    instances = []

    # If the project name (TAG) is supplied
    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances



@click.group()
def instances():
    """ Commands for Instances"""

@instances.command('list')
@click.option('--project', default=None,
    help="Only instances for project")
#    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        # Join fields with a comma
        print (', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>')
            )))
    return

# Start code for stopping Instances
@instances.command('stop')
@click.option('--project', default=None,
    help="Only instances for project")
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

    return

# Start code for starting Instances
@instances.command('start')
@click.option('--project', default=None,
    help="Only instances for project")
def start_instances(project):
    "Start EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()

    return


if __name__ == '__main__':
    instances()
