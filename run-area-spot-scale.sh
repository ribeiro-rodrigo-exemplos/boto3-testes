#!/bin/bash

export USUARIO_RABBIT=guest
export SENHA_RABBIT=guest
export URL_RABBIT=localhost:8080
export SECURITY_GROUP_ID=sg-d35827a9
export SUBNET=subnet-747f573d
export IAM_FLEET_ROLE="arn:aws:iam::290389913576:role/AmazonEC2SpotFleetRole"
export PRECO_SPOT="0.0050"
export AMI_ID="ami-0b727a1fcb3da4c5c"
export LIMITE_MENSAGEM=3

python3.5 spot_auto_scaling.py