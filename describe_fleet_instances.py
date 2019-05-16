import boto3 

def obter_spot_fleets():

    client = boto3.client('ec2')

    response = client.describe_spot_fleet_requests()

    spot_fleets = response['SpotFleetRequestConfigs']
    spot_fleets_filtradas = []

    for spot_fleet in spot_fleets:
        launch_specifications = spot_fleet['SpotFleetRequestConfig']['LaunchSpecifications']
        if spot_fleet['SpotFleetRequestState'] == 'active' and launch_specifications:
            tag_specifications = launch_specifications[0]['TagSpecifications']
            if tag_specifications and tag_specifications[0]['Tags'] and tag_specifications[0]['ResourceType'] == 'instance':
                tags = tag_specifications[0]['Tags']
                if {'Key': 'componente', 'Value': 'worker-area'} in tags:
                    spot_fleets_filtradas.append(spot_fleets)

    return tuple(spot_fleets_filtradas)


fleets = obter_spot_fleets()
print(len(fleets))
