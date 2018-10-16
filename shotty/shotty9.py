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

    # Constrain selection if the TAG contents '--project=name' is supplied
    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

# This version of the code adds AWS volume management. It places the
# instances and volume mgt functions into a click CLI group.
@click.group()
def cli():
    """Shotty manages snapshots"""

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None,
    help="Only snapshots for project")
#    help="Only instances for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 snapshots"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                 )))

    return

@cli.group('volumes')
def volumes():
    """ Commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None,
    help="Only volumes for project")
#    help="Only instances for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 volumes such as volumes list"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
                i.id,
                v.id,
                v.state,
                str(v.size) + "GB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))

    return


@cli.group('instances')
def instances():
    """ Commands for Instances"""

@instances.command('snapshot',
    help="Create snapshots of all volumes")
@click.option('--project', default=None,
    help="Only instances for project")
def create_snapshots(project):
    "Create snapshots for EC2 instances"

    instances = filter_instances(project)

# Stop instance and snapshot, then wait until it restarts before stopping next instance.
    for i in instances:
        print("Stopping {0}...".format(i.id))

        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print("Creating snapshot of (0)".format(v.id))
            v.create_snapshot(Description="Created by snapalyzer")

        print("Starting {0}...".format(i.id))

        i.start()
        i.wait_until_running()

    return


@instances.command('list')
@click.option('--project', default=None,
    help="Only instances for project")
#    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances such as instances list"

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

# Begin code for stopping Instances
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

# Begin code for starting Instances
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
    cli()
