import boto3

client = boto3.client('ec2')

SUBNET = 'subnet-747f573d'

response = client.request_spot_instances(
    AvailabilityZoneGroup='string',
    LaunchSpecification={
        'SecurityGroupIds':[
            'sg-d35827a9'
        ], 
        'ImageId': 'ami-0b727a1fcb3da4c5c', 
        'InstanceType': 't3.medium',
        'SubnetId': SUBNET
    }, 
    SpotPrice='0.50'
)

print(response)