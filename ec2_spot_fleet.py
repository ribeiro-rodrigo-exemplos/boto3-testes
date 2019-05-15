import boto3

client = boto3.client('ec2')


# ----------- m2m ---------------------
# SUBNET = 'subnet-747f573d'
# IAM_FLEET_ROLE = 'arn:aws:iam::290389913576:role/AmazonEC2SpotFleetRole'
# IMAGE_ID = 'ami-0b727a1fcb3da4c5c'
# SECURITY_GROUP_ID = 'sg-d35827a9'
# --------------------------------------
# ---------- casa ----------------------
SUBNET = ''
IAM_FLEET_ROLE = 'arn:aws:iam::193348742955:role/AmazonEC2SpotFleetRole'
IMAGE_ID = 'ami-0a313d6098716f372'
SECURITY_GROUP_ID = 'sg-767fc035'

response = client.request_spot_fleet(
    SpotFleetRequestConfig={
        'IamFleetRole': IAM_FLEET_ROLE,
        'SpotPrice': '0.30',
        'TargetCapacity': 1,
        'LaunchSpecifications': [
            {
                'SecurityGroups': [
                    {
                        'GroupId': SECURITY_GROUP_ID
                    }
                ],
                'ImageId': IMAGE_ID,
                'InstanceType': 't3.micro',
                'SubnetId': SUBNET,
            },
            {
                'SecurityGroups': [
                    {
                        'GroupId': SECURITY_GROUP_ID
                    }
                ],
                'ImageId': IMAGE_ID,
                'InstanceType': 't3.medium',
                'SubnetId': SUBNET,
            }
        ]
    }
)

print(response)
