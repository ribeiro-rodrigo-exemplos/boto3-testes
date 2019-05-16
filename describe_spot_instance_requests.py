import boto3 

client =  boto3.client('ec2')

response = client.describe_spot_instance_requests()

requestsId = response['SpotInstanceRequests']

for request in requestsId:
    tags = request['Tags']
    print(tags)
    for tag in tags:
        if tag['Key'] == 'aws:ec2spot:fleet-request-id':
            print(tag['Value'])
#print(response['SpotInstanceRequests'])
