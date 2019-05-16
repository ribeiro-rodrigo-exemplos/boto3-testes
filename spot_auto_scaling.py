import http.client
import boto3
import json
from base64 import b64encode


def obter_mensagens_rabbit():

    usuario = 'guest'
    senha = 'guest'
    base64_auth = b64encode('{}:{}'.format(usuario, senha).encode())
    headers = {'Authorization': 'Basic {}'.format(base64_auth.decode())}

    connection = http.client.HTTPConnection('localhost:8080')
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

    return None


def criar_launch_specification(tipos_instancia, imagem_id):

    security_group_id = 'sg-d35827a9'
    subnet = 'subnet-747f573d'
    specifications = []

    for tipo_instancia in tipos_instancia:
        specification = {
            'SecurityGroups': [{'GroupId': security_group_id}],
            'ImageId': imagem_id,
            'InstanceType': tipo_instancia,
            'SubnetId': subnet
        }
        specifications.append(specification)

    return specifications


def criar_spot_fleet(imagem_id, client):

    iam_fleet_role = 'arn:aws:iam::290389913576:role/AmazonEC2SpotFleetRole'
    preco_spot = '0.30'
    tipos_instancia = ('t3.micro', 't3.medium',
                       't2.medium', 'c4.large', 'm4.large')

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

    print(response)

    return None


def __main__():
    # obter_mensagens_rabbit()
    client = boto3.client('ec2')
    criar_spot_fleet('ami-0a313d6098716f372', client)


__main__()


# client = boto3.client('ec2')

# imagem_id = obter_imagem_id('template-m2m-debian-9',client)

# print(imagem_id)
