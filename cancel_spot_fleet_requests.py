import boto3

client = boto3.client('ec2')

response = client.cancel_spot_fleet_requests(
    SpotFleetRequestIds=[
    'sfr-f5ab094b-1f99-4084-ac64-fd87b2a3be94'
    ], 
    TerminateInstances=True
)

print(response)