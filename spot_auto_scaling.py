import http.client
import boto3
import json
import os 
import sys
from base64 import b64encode


def obter_mensagens_rabbit():

    usuario = os.environ['USUARIO_RABBIT']
    senha = os.environ['SENHA_RABBIT']
    url_rabbit = os.environ['URL_RABBIT']

    base64_auth = b64encode('{}:{}'.format(usuario, senha).encode())
    headers = {'Authorization': 'Basic {}'.format(base64_auth.decode())}

    connection = http.client.HTTPConnection(url_rabbit)
    connection.request(
        'GET', '/api/queues/%2F/processador.area', headers=headers)
    resposta = connection.getresponse()
    fila = json.loads(resposta.read().decode())

    return fila['messages_ready']


def obter_imagem_id(imagem_nome, client):

    filtros = [
        {
            'Name': 'name',
            'Values': [imagem_nome]
        }
    ]

    imagens = client.describe_images(Filters=filtros)['Images']

    for imagem in imagens:
        if imagem['Name'] == imagem_nome:
            return imagem['ImageId']


def criar_launch_specification(tipos_instancia, imagem_id):

    security_group_id = os.environ['SECURITY_GROUP_ID']
    subnet = os.environ['SUBNET']
    specifications = []

    for tipo_instancia in tipos_instancia:
        specification = {
            'SecurityGroups': [{'GroupId': security_group_id}],
            'ImageId': imagem_id,
            'InstanceType': tipo_instancia,
            'SubnetId': subnet,
            'TagSpecifications': [
                {   
                    'ResourceType': 'instance',
                    'Tags':[{'Key':'componente','Value':'worker-area'}]
                }
            ]
        }
        specifications.append(specification)

    return specifications


def criar_spot_fleet(imagem_id, client):

    iam_fleet_role = os.environ['IAM_FLEET_ROLE']
    preco_spot = os.environ['PRECO_SPOT']
    tipos_instancia = ('t3.micro', 't3.small', 't3.medium','t3a.micro','t3a.small','t3a.medium')

    launch_specifications = criar_launch_specification(
        tipos_instancia, imagem_id)
    print(launch_specifications)

    response = client.request_spot_fleet(
        SpotFleetRequestConfig={
            'IamFleetRole': iam_fleet_role,
            'SpotPrice': preco_spot,
            'TargetCapacity': 1,
            'LaunchSpecifications': launch_specifications
        }
    )

    return response 


def obter_spot_fleets(client):

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
                    spot_fleets_filtradas.append(spot_fleet)

    return tuple(spot_fleets_filtradas)


def cancelar_spot_fleet(spot_fleet_ids,client):
    response = client.cancel_spot_fleet_requests(
        SpotFleetRequestIds=spot_fleet_ids,
        TerminateInstances=True
    )

    return response

def escalar_para_cima(quantidade_maquinas_escalaveis,client):
    print('devo escalar {} maquinas'.format(quantidade_maquinas_escalaveis))

    for _ in range(0,quantidade_maquinas_escalaveis):
        criar_spot_fleet(os.environ['AMI_ID'],client)


def escalar_para_baixo(quantidade_maquinas_escalaveis,spot_fleets, client):
    print('devo tirar {} maquinas'.format(quantidade_maquinas_escalaveis))
    spot_fleets_ids = []

    quantidade_maquinas_escalaveis =  abs(quantidade_maquinas_escalaveis)

    for fleet in spot_fleets[:quantidade_maquinas_escalaveis]:
        spot_fleets_ids.append(fleet['SpotFleetRequestId'])

    cancelar_spot_fleet(spot_fleets_ids, client)

def avaliar_escalabilidade(quantidade_mensagens,quantidade_atual_de_spots,estado_desejado,spot_fleets,client):

    quantidade_maquinas_escalaveis = estado_desejado['quantidade_spots'] - quantidade_atual_de_spots

    if quantidade_maquinas_escalaveis > 0:
        escalar_para_cima(quantidade_maquinas_escalaveis,client)
    elif quantidade_maquinas_escalaveis < 0:  
        escalar_para_baixo(quantidade_maquinas_escalaveis,spot_fleets,client)


def __main__():

    client = boto3.client('ec2')

    limite_mensagens = int(os.environ['LIMITE_MENSAGEM'])
    quantidade_mensagens = obter_mensagens_rabbit()
    spot_fleets = obter_spot_fleets(client)
    quantidade_de_spots = len(spot_fleets)
    limite_final_de_mensagens = sum([limite_mensagens,limite_mensagens])
    estados_desejados = [
        {'quantidade_mensagens': range(0,limite_mensagens), 'quantidade_spots':0},
        {'quantidade_mensagens': range(limite_mensagens,limite_final_de_mensagens), 'quantidade_spots':1}, 
        {'quantidade_mensagens': range(limite_final_de_mensagens,sys.maxsize), 'quantidade_spots':2}
    ]

    for estado_desejado in estados_desejados:
        if quantidade_mensagens in estado_desejado['quantidade_mensagens'] and quantidade_de_spots != estado_desejado['quantidade_spots']:
            avaliar_escalabilidade(quantidade_mensagens,quantidade_de_spots,estado_desejado,spot_fleets,client)
            break 

 
__main__()

