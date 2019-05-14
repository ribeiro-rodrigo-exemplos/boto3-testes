import boto3

client = boto3.client('ec2')

SUBNET = 'subnet-747f573d'

response = client.request_spot_fleet(
    SpotFleetRequestConfig={
        'IamFleetRole':'arn:aws:iam::290389913576:role/AmazonEC2SpotFleetRole',
        'SpotPrice': '0.30',
        'TargetCapacity':1,
        'LaunchSpecifications':[
            {
                'SecurityGroups':[
                    {
                        'GroupId': 'sg-d35827a9'
                    }
                ],
                'ImageId': 'ami-0b727a1fcb3da4c5c',
                'InstanceType': 't3.micro',
                'SubnetId': SUBNET,
            },
            {
                'SecurityGroups':[
                    {
                        'GroupId': 'sg-d35827a9'
                    }
                ],
                'ImageId': 'ami-0b727a1fcb3da4c5c',
                'InstanceType': 't3.medium',
                'SubnetId': SUBNET,
            }
        ]
    }
)

print(response)