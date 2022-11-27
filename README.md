# Projeto de Computação em Nuvem

## Tecnologias utilizadas no projeto:

- <img src="https://img.shields.io/static/v1?label=Code&message=Python&color=blue&style=plastic&labelColor=black&logo=python"/>

- <img src="https://img.shields.io/static/v1?label=Code&message=Terraform&color=purple&style=plastic&labelColor=black&logo=Terraform"/>

- <img src="https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white"/>

## Features :fire: :

### Conceito C :heavy_check_mark::heavy_check_mark:

- Criação automática de VPC e sub-rede :white_check_mark:
- Criação de instâncias e pelo menos 2 tipos de hosts :white_check_mark:
- Criação de grupos de segurança e associação com instâncias :white_check_mark:
- Criação de usuário no IAM :white_check_mark:
- Deletar instâncias :white_check_mark:
- Deletar grupos de segurança :white_check_mark:
- Deletar usuários :white_check_mark:
- Listar instâncias :white_check_mark:
- Listar usuários :white_check_mark:
- Listar grupos de segurança :white_check_mark:
- Listar regras :white_check_mark:

### Conceito B :heavy_check_mark::heavy_check_mark:

- Criação de novas regras em grupos de segurança :white_check_mark:
- Criação de instâncias em mais de uma região :white_check_mark:
- Associação de restrição de acesso à usuário :white_check_mark:
- Deletar regras de grupos de segurança :white_check_mark:

## Objetivo :computer: :

O objetivo desse projeto é oferecer uma interface amigável, intuitiva e simples que visa facilitar e automatizar a criação de uma infraestrutura na AWS. Por baixo dos panos contamos com o Terraform para a automatização do gerenciamento de todos os recursos que irão para a AWS e o Python que comanda todo o fluxo e a lógica da plataforma, conforme o usuário interage com a interface.

## Instalação :gear: : 

### Instalação do Terraform <img src="https://img.shields.io/static/v1?label=Code&message=Terraform&color=purple&style=plastic&labelColor=black&logo=Terraform"/>

Para instalar o terraform siga o tutorial da HashiCorp disponível em https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

### Instalação do AWS CLI <img src="https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white"/>

Para instalar a AWS CLI siga o tutorial da AWS disponível em https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

## Manual do usuário :scroll: :

Primeiramente, siga o tutorial da AWS para configurar a AWS CLI com variáveis ambientes e poder utilizar a plataforma: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html

A plataforma permite:
  - Escolher Norte da Virgínia ou São Paulo para provisionar sua infraestrutura :earth_americas:
  - Criar grupos de segurança :cop:
    * Escolher nome
    * Dar uma descrição
    * Adicionar pelo menos uma regra de **ingresso**
  - Listar grupos de segurança :page_with_curl:
  - Deletar grupos de segurança :x:
  - Associar novas regras de **ingresso** a grupos de segurança :book:
    * Digitar o nome do grupo de segurança que vai ser associado a nova regra
    * Escolher o nome da regra
    * Escolher a porta de origem
    * Escolher a porta de destino
    * Escolher o protocolo
    * Escolher os blocos CIDR 
  - Listar regras :page_with_curl:
  - Deletar regras de grupos de segurança :x:
  - Criar instâncias :computer:
    * Escolher nome
    * Escolher imagem Ubuntu
    * Escolher tipo da instância
  - Listar instâncias :page_with_curl:
  - Deletar instâncias :x:
  - Associar instâncias à grupos de segurança :police_car:
  - Desassociar instâncias de grupos de segurança :x:
  - Criar usuários :baby:
    * Escolher nome
    * Adicionar restrições de ação
    * Adicionar restrições à recursos
  - Listar usuários :page_with_curl:
  - Deletar usuários :skull_and_crossbones:	

### Observações importantes :warning: :
- Ao criar uma instância ela será associada ao grupo de segurança padrão
- Não é possível adicionar regras ou deletar o grupo de segurança padrão
- Não é possível remover a última regra de um grupo de segurança
- Ao desassociar o último grupo de segurança de uma instância ela será associada ao grupo de segurança padrão automaticamente
- Ao criar um usuário sem restrições, a ele será garantido **acesso total**
  


    
