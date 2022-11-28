from time import sleep
import subprocess
import json
import os

def display_opening_message():

    init_text = """
\033[36m/---------------------------------- LARRYSFORM -----------------------------------/\033[0m

Esta plataforma é capaz de provisionar, gerenciar e administrar uma infraestutura, 
sendo possível construiur, alterar e deletar recursos por meio de uma interface 
amigável, simples e intituitiva. É possível parar a execução a qualquer momento
pressionando CTRL+C.

\033[32mBy: LarrysCorp®\033[0m
    """
    
    print(init_text)
    sleep(5)
    print("\033[34mPrimeiramente escolha a região onde deseja provisionar a infraestrutura: " + "\033[0m")
    print("")
    print("\033[33m1. Norte da Virgínia (us-east-1)" + "\033[0m")
    print("\033[32m2. São Paulo (sa-east-1)" + "\033[0m")
    print(" ")
    sleep(2)
    region = input("\033[34mDigite o número da região desejada: " + "\033[0m")

    while region not in ["1", "2"]:
        print(" ")
        print("\033[31mRegião inválida." + "\033[0m")
        print(" ")
        sleep(2)
        region = input("\033[34mDigite o número da região desejada: " + "\033[0m")

    if region == "1":
        os.chdir("us-east-1")
       
    elif region == "2":
        os.chdir("sa-east-1")

    print(" ")
    print("\033[96mAguarde enquanto o LarrysForm é inicializado..." + "\033[0m")
    sleep(2)
    subprocess.run(["terraform", "init"], stdout=subprocess.DEVNULL)

    return region


def display_main_menu():

    menu = """
\033[36m/------------------------------- LARRYSFORM - MENU -------------------------------/\033[0m

1. GRUPOS DE SEGURANÇA

2. INSTÂNCIAS

3. USUÁRIOS 

4. SAIR
    """

    print(menu)


def display_security_groups_menu():

    menu = """
\033[36m/----------------------- LARRYSFORM - GRUPOS DE SEGURANÇA ------------------------/\033[0m

1. CRIAR

2. LISTAR

3. DELETAR

4. REGRAS

5. VOLTAR
    """

    print(menu)


def create_security_group():

    print(" ")
    print("\033[94mPrimeiramente digite o nome do grupo de segurança que deseja criar." + "\033[0m")
    print(" ")

    sleep(1)

    security_group_name = input("Digite o nome do grupo de segurança a ser criado: ")
    print(" ")

    sleep(1)

    while len(security_group_name) == 0:
        print("\033[31mNão é possível criar um grupo de segurança sem nome.." + "\033[0m")
        security_group_name = input("Por favor, digite o nome do grupo de segurança a ser criado: ")

    security_group_description = input("\033[36mEscreva uma descrição para o grupo de segurança a ser criado: " + "\033[0m")
    print(" ")

    sleep(1)

    security_group_rules = []

    first_rule = True
    add_more_rules = True

    while add_more_rules:

        if not first_rule:

            add_more_rules_answer = input("Deseja adicionar mais regras? (y/n): ")

            while add_more_rules_answer not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                print("\033[31mOpção inválida..." + "\033[0m")
                print("'\033[31mPor favor, digite o número da opção dentre as apresentadas." + "\033[0m")
                add_more_rules = input("Deseja adicionar mais regras? (y/n): ")

        if first_rule or add_more_rules_answer in ['y','Y','yes', 'YES']:
            security_group_rule_name = input("Digite o nome da regra para o grupo de segurança a ser criado: ")
            print(" ")
            sleep(0.5)

            security_group_from_port = input("Digite a porta de origem para o grupo de segurança a ser criado: ")
            print(" ")
            sleep(0.5)

            security_group_to_port = input("Digite a porta de destino para o grupo de segurança a ser criado: ")
            print(" ")
            sleep(0.5)

            security_group_protocol = input("Digite o protocolo para o grupo de segurança a ser criado: ")
            print(" ")
            sleep(0.5)

            security_group_cidr_blocks = input("Digite os blocos CIDR para o grupo de segurança a ser criado: ")
            print(" ")
            sleep(0.5)

            security_group_rule = {
                'rule_name': security_group_rule_name, 
                'from_port': security_group_from_port, 
                'to_port': security_group_to_port, 
                "protocol": security_group_protocol, 
                "cidr_blocks": security_group_cidr_blocks.split(",")
            }

            security_group_rules.append(security_group_rule)

            first_rule = False

        elif add_more_rules_answer in ['n','N','no', 'NO']:
            add_more_rules = False

    security_group = {
        'name': security_group_name,
        'description': security_group_description,
        'ingress': security_group_rules
    }

    review_security_group_text = f"""
Nome do grupo de segurança: \033[32m{security_group_name}\033[0m
Descrição do grupo de segurança: {security_group_description}
    """

    print(review_security_group_text)
    sleep(2)

    for rule in security_group_rules:
        review_security_group_rules_text = f"""
Nome da regra: {rule['rule_name']}
Porta de origem: {rule['from_port']}
Porta de destino: {rule['to_port']}
Protocolo: {rule['protocol']}
Blocos CIDR: {rule['cidr_blocks']}
        """

        print(review_security_group_rules_text)
        sleep(2)

    confirm_security_group_creation = input("Deseja criar o grupo de segurança com as configurações e regras atuais? (y/n): ")

    while confirm_security_group_creation not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
        print("\033[31mOpção inválida..." + "\033[0m")
        print("'\033[31mPor favor, digite uma opção válida (y/n)." + "\033[0m")
        confirm_security_group_creation = input("Deseja adicionar mais regras? (y/n): ")

    if confirm_security_group_creation in ['y','Y','yes', 'YES']:

        with open('.auto.tfvars.json', 'r') as file:
            terraform_variables = json.load(file)
                
        terraform_variables["security_groups"].append(security_group)
        
        
        with open('.auto.tfvars.json', 'w') as file:
            json.dump(terraform_variables, file, indent=2, separators=(',',': '))

        os.system('terraform apply -auto-approve')

    elif confirm_security_group_creation in ['n','N','no', 'NO']:
        print("\033[32mCancelando operação..." + "\033[0m")
        sleep(2)


def list_security_groups():
    with open('.auto.tfvars.json', 'r') as file:
            terraform_variables = json.load(file)
                
    security_groups = terraform_variables["security_groups"]

    if len(security_groups) == 0:
        print("Não há grupos de segurança criados.")
        sleep(2)
        return

    for security_group in security_groups:
        print(f"""
\033[32m{security_group['name']}\033[0m

\033[32mDescrição do grupo de segurança: {security_group['description']}\033[0m

\033[35mRegras:\033[0m
        """)

        for rule in security_group['ingress']:
            print(f"""
Nome da regra: {rule['rule_name']}
Porta de origem: {rule['from_port']}
Porta de destino: {rule['to_port']}
Protocolo: {rule['protocol']}
Blocos CIDR: {rule['cidr_blocks']}
            """)

            sleep(0.5)

        sleep(1)


def delete_security_group():
    with open('.auto.tfvars.json', 'r') as file:
        terraform_variables = json.load(file)
                
    security_groups = terraform_variables["security_groups"]

    if len(security_groups) == 0:
        print("Não há grupos de segurança criados.")
        sleep(2)
        return

    security_group_name = input("Digite o nome do grupo de segurança a ser deletado: ")

    while True:

        if security_group_name not in [security_group['name'] for security_group in security_groups]:
            print("\033[31mO grupo de segurança não existe." + "\033[0m")
            sleep(2)

            delete_security_group = input("Deseja tentar novamente? (y/n): ")

            while delete_security_group not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                print("\033[31mOpção inválida..." + "\033[0m")
                print("'\033[31mPor favor, digite uma opção válida (y/n)." + "\033[0m")
                delete_security_group = input("Deseja tentar novamente? (y/n): ")

            if delete_security_group in ['n','N','no', 'NO']:
                return

            elif delete_security_group in ['y','Y','yes', 'YES']:
                security_group_name = input("Digite o nome do grupo de segurança a ser deletado: ")

        elif security_group_name == "default":
            print("\033[31mO grupo de segurança padrão não pode ser deletado." + "\033[0m")
            sleep(2)

            delete_security_group = input("Deseja tentar novamente? (y/n): ")

            while delete_security_group not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                print("\033[31mOpção inválida..." + "\033[0m")
                print("'\033[31mPor favor, digite uma opção válida (y/n)." + "\033[0m")
                delete_security_group = input("Deseja tentar novamente? (y/n): ")

            if delete_security_group in ['n','N','no', 'NO']:
                return

            elif delete_security_group in ['y','Y','yes', 'YES']:
                security_group_name = input("Digite o nome do grupo de segurança a ser deletado: ")
            
        else:
            print("\033[32mDeletando o grupo de segurança..." + "\033[0m")
            sleep(2)
            for security_group in security_groups:
                if security_group['name'] == security_group_name:
                    security_groups.remove(security_group)
                    break

            instances = terraform_variables["instances"]

            for instance in instances:
                if instance['security_groups'] == [security_group_name]:
                    instance['security_groups'].remove(security_group_name)
                    if len(instance['security_groups']) == 0:
                        instance['security_groups'].append('default')

            with open('.auto.tfvars.json', 'w') as file:
                json.dump(terraform_variables, file, indent=2, separators=(',',': '))

            os.system('terraform apply -auto-approve')

            delete_security_group = input("Deseja deletar outro grupo de segurança? (y/n): ")

            while delete_security_group not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                print("\033[31mOpção inválida..." + "\033[0m")
                print("'\033[31mPor favor, digite uma opção válida (y/n)." + "\033[0m")
                delete_security_group = input("Deseja deletar outro grupo de segurança? (y/n): ")

            if delete_security_group in ['n','N','no', 'NO']:
                return

            elif delete_security_group in ['y','Y','yes', 'YES']:
                security_group_name = input("Digite o nome do grupo de segurança a ser deletado: ")


def display_rules_menu():

    menu = """
\033[36m/------------------------------ LARRYSFORM - REGRAS ------------------------------/\033[0m

1. CRIAR

2. LISTAR

3. DELETAR

4. VOLTAR
    """

    print(menu)


def create_rules():
    with open('.auto.tfvars.json', 'r') as file:
        terraform_variables = json.load(file)
                
    security_groups = terraform_variables["security_groups"]

    if len(security_groups) == 0:
        print("\033[31mNão há grupos de segurança criados." + "\033[0m")
        sleep(2)
        print("\033[31mRegras só podem ser aplicadas a grupos de segurança existentes." + "\033[0m")
        return

    security_group_name = input("Digite o nome do grupo de segurança para o qual deseja adicionar a regra: ")

    while True:

        if security_group_name not in [security_group['name'] for security_group in security_groups]:
            print("\033[31mO grupo de segurança não existe." + "\033[0m")
            sleep(2)

            add_rule = input("Deseja tentar novamente? (y/n): ")

            while add_rule not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                print("\033[31mOpção inválida..." + "\033[0m")
                print("'\033[31mPor favor, digite uma opção válida (y/n)." + "\033[0m")
                add_rule = input("Deseja tentar novamente? (y/n): ")

            if add_rule in ['n','N','no', 'NO']:
                return

            elif add_rule in ['y','Y','yes', 'YES']:
                security_group_name = input("Digite o nome do grupo de segurança para o qual deseja adicionar a regra: ")
                
            
        else:

            if security_group_name == "default":
                print("\033[31mNão é possível adicionar regras no grupo de segurança padrão." + "\033[0m")
                sleep(2)
                return

            rule_name = input("Digite o nome da regra: ")

            if rule_name in [rule['name'] for rule in security_groups[security_groups.index({'name': security_group_name})]['rules']]:
                print("\033[31mJá existe uma regra com esse nome." + "\033[0m")
                sleep(2)
                rule_name = input("Digite o nome da regra: ")

            sleep(0.5)
            from_port = input("Digite a porta de origem: ")
            sleep(0.5)
            to_port = input("Digite a porta de destino: ")
            sleep(0.5)
            protocol = input("Digite o protocolo: ")
            sleep(0.5)
            cidr_blocks = input("Digite os blocos CIDR: ")
            sleep(0.5)
            print("\033[32mAdicionando a regra..." + "\033[0m")

            for security_group in security_groups:
                if security_group['name'] == security_group_name:
                    security_group['ingress'].append({
                        'rule_name': rule_name,
                        'from_port': from_port,
                        'to_port': to_port,
                        'protocol': protocol,
                        'cidr_blocks': cidr_blocks.split(",")
                    })
                    break

            with open('.auto.tfvars.json', 'w') as file:
                json.dump(terraform_variables, file, indent=2, separators=(',',': '))

            os.system('terraform apply -auto-approve')

            add_rule = input("Deseja adicionar mais regras a grupos de segurança? (y/n): ")

            while add_rule not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                print("\033[31mOpção inválida..." + "\033[0m")
                print("'\033[31mPor favor, digite uma opção válida (y/n)." + "\033[0m")
                add_rule = input("Deseja adicionar mais regras a grupos de segurança? (y/n): ")

            if add_rule in ['n','N','no', 'NO']:
                return

            elif add_rule in ['y','Y','yes', 'YES']:
                security_group_name = input("Digite o nome do grupo de segurança para o qual deseja adicionar a regra: ")


def list_rules():
    with open('.auto.tfvars.json', 'r') as file:
        terraform_variables = json.load(file)

    security_groups = terraform_variables["security_groups"]

    if len(security_groups) == 0:
        print("\033[31mNão há grupos de segurança criados." + "\033[0m")
        sleep(2)
        print("\033[31mNão existem regras sem grupos de segurança existentes." + "\033[0m")
        return

    for security_group in security_groups:
        print("")
        print("\033[36m" + security_group['name'] + "\033[0m")
        print("")
        sleep(0.5)
        for ingress in security_group['ingress']:
            print("\033[32m" + ingress['rule_name'] + "\033[0m")
            print("Porta de origem: " + ingress['from_port'])
            print("Porta de destino: " + ingress['to_port'])
            print("Protocolo: " + ingress['protocol'])
            print("Blocos CIDR: " + ",".join(ingress['cidr_blocks']))
            print("")


def delete_rules():
    with open('.auto.tfvars.json', 'r') as file:
        terraform_variables = json.load(file)

    security_groups = terraform_variables["security_groups"]

    if len(security_groups) == 0:
        print("\033[31mNão há grupos de segurança criados." + "\033[0m")
        sleep(2)
        print("\033[31mNão existem regras sem grupos de segurança existentes." + "\033[0m")
        return

    security_group_name = input("Digite o nome do grupo de segurança do qual deseja remover a regra: ")

    while True:
            
        if security_group_name not in [security_group['name'] for security_group in security_groups]:
            print("\033[31mO grupo de segurança não existe." + "\033[0m")
            sleep(2)

            delete_rule = input("Deseja tentar novamente? (y/n): ")

            while delete_rule not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                print("\033[31mOpção inválida..." + "\033[0m")
                print("'\033[31mPor favor, digite uma opção válida (y/n)." + "\033[0m")
                delete_rule = input("Deseja tentar novamente? (y/n): ")

            if delete_rule in ['n','N','no', 'NO']:
                return

            elif delete_rule in ['y','Y','yes', 'YES']:
                security_group_name = input("Digite o nome do grupo de segurança do qual deseja remover a regra: ")
                
            
        else:

            if security_group_name == "default":
                print("\033[31mNão é possível remover regras do grupo de segurança padrão." + "\033[0m")
                sleep(2)
                return

            rule_name = input("Digite o nome da regra: ")
            sleep(0.5)

            rule_removed = False 

            while not rule_removed:
                for security_group in security_groups:
                    if security_group['name'] == security_group_name:
                        for ingress in security_group['ingress']:
                            if ingress['rule_name'] == rule_name:
                                security_group['ingress'].remove(ingress)
                                if len(security_group['ingress']) == 0:
                                    security_group['ingress'].append(ingress)
                                    print("\033[31mNão é possível remover a última regra de um grupo de segurança." + "\033[0m")
                                    sleep(2)
                                    return
                                rule_removed = True
                                break
                        break

                if not rule_removed:
                    print("\033[31mA regra não existe." + "\033[0m")
                    sleep(2)

                    delete_rule = input("Deseja tentar novamente? (y/n): ")

                    while delete_rule not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                        print("\033[31mOpção inválida..." + "\033[0m")
                        print("'\033[31mPor favor, digite uma opção válida (y/n)." + "\033[0m")
                        delete_rule = input("Deseja tentar novamente? (y/n): ")

                    if delete_rule in ['n','N','no', 'NO']:
                        return

                    elif delete_rule in ['y','Y','yes', 'YES']:
                        rule_name = input("Digite o nome da regra: ")
                        sleep(0.5)

                print("\033[32mRemovendo a regra..." + "\033[0m")
                
            with open('.auto.tfvars.json', 'w') as file:
                json.dump(terraform_variables, file, indent=2, separators=(',',': '))

            os.system('terraform apply -auto-approve')

            delete_rule = input("Deseja remover mais regras de grupos de segurança? (y/n): ")

            while delete_rule not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                print("\033[31mOpção inválida..." + "\033[0m")
                print("'\033[31mPor favor, digite uma opção válida (y/n)." + "\033[0m")
                delete_rule = input("Deseja remover mais regras de grupos de segurança? (y/n): ")

            if delete_rule in ['n','N','no', 'NO']:
                return

            elif delete_rule in ['y','Y','yes', 'YES']:
                security_group_name = input("Digite o nome do grupo de segurança do qual deseja remover a regra: ")


def display_instances_menu():

    menu = """
\033[36m/---------------------------- LARRYSFORM - INSTÂNCIAS ----------------------------/\033[0m

1. CRIAR

2. LISTAR

3. DELETAR

4. ASSOCIAR GRUPOS DE SEGURANÇA

5. DESASSOCIAR GRUPOS DE SEGURANÇA

6. VOLTAR
    """

    print(menu)


def create_instance():

    with open('.auto.tfvars.json', 'r') as file:
        terraform_variables = json.load(file)

    instances = terraform_variables["instances"]

    print(" ")
    print("\033[94mPrimeiramente digite o nome da instância que deseja criar." + "\033[0m")
    print(" ")

    sleep(1)

    instance_name = input("Digite o nome da instância a ser criada: ")

    while instance_name == "" or instance_name == " ":  
        print("\033[31mO nome da instância não pode ser vazio." + "\033[0m")
        sleep(2)
        instance_name = input("Digite o nome da instância a ser criada: ")

    while instance_name in [instance['name'] for instance in instances]:
        print("\033[31mJá existe uma instância com esse nome." + "\033[0m")
        sleep(2)
        instance_name = input("Digite o nome da instância a ser criada: ")
        

    if region == "1":
        ami_options_list = ['ami-0ee23bfc74a881de5', 'ami-0149b2da6ceec4bb0', 'ami-08c40ec9ead489470']
    else:
        ami_options_list = ['ami-0c59dc4ecf61872e2', 'ami-00742e66d44c13cd9', 'ami-04b3c23ec8efcc2d6']

    ami_options_text = """
\033[35mEscolha uma das AMIs abaixo:\033[0m

1. Ubuntu Server 18.04 LTS (HVM), SSD Volume Type
2. Ubuntu Server 20.04 LTS (HVM), SSD Volume Type
3. Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
    """

    print(ami_options_text)
    sleep(2)
    ami_choice = input("Digite o número da opção desejada: ")

    while ami_choice not in ['1','2','3']:
        print("\033[31mOpção inválida..." + "\033[0m")
        print("'\033[31mPor favor, digite o número da opção dentre as apresentadas." + "\033[0m")
        ami_choice = input("Digite o número da opção desejada: ")

    instance_ami = ami_options_list[int(ami_choice)-1]
   
    instance_types_list = ['t1.micro', 't2.nano', 't2.micro', 't2.small', 't2.medium', 't2.large', 't2.xlarge', 't2.2xlarge', 't3.nano', 't3.micro', 't3.small', 't3.medium', 't3.large', 't3.xlarge', 't3.2xlarge']

    instance_types_text = """
\033[36mEscolha um dos tipos abaixo:\033[0m

1. t1.micro (1 vCPU, 1 GiB RAM, EBS only)
2. t2.nano (1 vCPU, 0.5 GiB RAM, EBS only)
3. t2.micro (1 vCPU, 1 GiB RAM, EBS only)
4. t2.small (1 vCPU, 2 GiB RAM, EBS only)
5. t2.medium (2 vCPU, 4 GiB RAM, EBS only)
6. t2.large (2 vCPU, 8 GiB RAM, EBS only)
7. t2.xlarge (4 vCPU, 16 GiB RAM, EBS only)
8. t2.2xlarge (8 vCPU, 32 GiB RAM, EBS only)
9. t3.nano (2 vCPU, 0.5 GiB RAM, EBS only)
10. t3.micro (2 vCPU, 1 GiB RAM, EBS only)
11. t3.small (2 vCPU, 2 GiB RAM, EBS only)
12. t3.medium (2 vCPU, 4 GiB RAM, EBS only)
13. t3.large (2 vCPU, 8 GiB RAM, EBS only)
14. t3.xlarge (4 vCPU, 16 GiB RAM, EBS only)
15. t3.2xlarge (8 vCPU, 32 GiB RAM, EBS only)
    """

    print(instance_types_text)
    sleep(3)
    instance_type_choice = input("Digite o número da opção desejada: ")

    while instance_type_choice not in ['1','2','3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']:
        print("\033[31mOpção inválida..." + "\033[0m")
        print("'\033[31mPor favor, digite o número da opção dentre as apresentadas." + "\033[0m")
        instance_type_choice = input("Digite o número da opção desejada: ")

    instance_type = instance_types_list[int(instance_type_choice)-1]

    ami_list = ["Ubuntu Server 18.04 LTS (HVM), SSD Volume Type", "Ubuntu Server 20.04 LTS (HVM), SSD Volume Type", "Ubuntu Server 22.04 LTS (HVM), SSD Volume Type"]

    review_instance_text = f"""
Nome da instância: \033[32m{instance_name}\033[0m
AMI: \033[35m{ami_list[int(ami_choice)-1]}\033[0m
Tipo: \033[36m{instance_type}\033[0m
    """

    print(review_instance_text)
    sleep(3)
    confirm = input("Digite 'Y' para confirmar ou 'N' para cancelar: ")

    while confirm not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
        print("\033[31mOpção inválida..." + "\033[0m")
        confirm = input("Por favor, digite 'Y' para confirmar ou 'N' para cancelar: ")

    if confirm in ['y','Y','yes', 'YES']:
        print(" ")
        print("\033[32mCriando instância..." + "\033[0m")
        
        # Read JSON file
        with open('.auto.tfvars.json', 'r') as file:
            terraform_variables = json.load(file)
                
        terraform_variables["instances"].append({
            "name": instance_name,
            "ami": instance_ami,
            "instance_type": instance_type,
            "security_groups": ["default"]
        })
        
        
        with open('.auto.tfvars.json', 'w') as file:
            json.dump(terraform_variables, file, indent=2, separators=(',',': '))

        sleep(5)

        os.system('terraform apply -auto-approve')

        print(" ")
        print("\033[32mInstância criada com sucesso!" + "\033[0m")
        sleep(5)
    else:
        print("\033[32mCancelando criação da instância..." + "\033[0m")
        sleep(5)


def list_instances():
    print(" ")
    print("\033[32mListando instâncias..." + "\033[0m")
    
    with open('.auto.tfvars.json', 'r') as file:
        terraform_variables = json.load(file)

    instances = terraform_variables["instances"]

    if len(instances) == 0:
        print(" ")
        print("\033[31mNão há instâncias criadas..." + "\033[0m")
        sleep(5)

    for instance in instances:
        print(" ")
        print(f"\033[32mNome da instância: \033[0m{instance['name']}")
        print(f"\033[32mAMI: \033[0m{instance['ami']}")
        print(f"\033[32mTipo: \033[0m{instance['instance_type']}")
        print(f"\033[32mSecurity Groups: \033[0m{instance['security_groups']}")
        print(" ")


def delete_instances():
    with open('.auto.tfvars.json', 'r') as file:
        terraform_variables = json.load(file)

    instances = terraform_variables["instances"]

    if len(instances) == 0:
        print(" ")
        print("\033[31mNão há instâncias criadas..." + "\033[0m")
        sleep(5)

    instance_name = input("Digite o nome da instância que deseja deletar: ")

    delete_instances = True
    
    while delete_instances:

        instance_exists = False

        for instance in instances:
            if instance["name"] == instance_name:
                print(" ")
                print("\033[32mDeletando instância..." + "\033[0m")
                sleep(3)
                instance_exists = True
                instances.remove(instance)
                with open('.auto.tfvars.json', 'w') as file:
                    json.dump(terraform_variables, file, indent=2, separators=(',',': '))
                os.system('terraform apply -auto-approve')
                print(" ")
                print("\033[32mInstância deletada com sucesso!" + "\033[0m")
                sleep(5)
                delete_instances = input("Deseja deletar outra instância? (y/n): ")

                while delete_instances not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                    print("\033[31mOpção inválida..." + "\033[0m")
                    delete_instances = input("Por favor, digite 'Y' para deletar outra instância ou 'N' para cancelar: ")

                if delete_instances in ['y','Y','yes', 'YES']:
                    instance_name = input("Digite o nome da instância que deseja deletar: ")

                elif delete_instances in ['n','N','no', 'NO']:
                    delete_instances = False
                
        
        if not instance_exists:
            print("\033[31mInstância não encontrada..." + "\033[0m")
            sleep(2)
            delete_instances = input("Deseja tentar novamente? (y/n): ")

            while delete_instances not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                print("\033[31mOpção inválida..." + "\033[0m")
                delete_instances = input("Por favor, digite 'Y' para confirmar ou 'N' para cancelar: ")

            if delete_instances in ['y','Y','yes', 'YES']:
                instance_name = input("Digite o nome da instância que deseja deletar: ")

            elif delete_instances in ['n','N','no', 'NO']:
                delete_instances = False


def associate_instances():
    with open('.auto.tfvars.json', 'r') as file:
        terraform_variables = json.load(file)

    instances = terraform_variables["instances"]

    security_groups = terraform_variables["security_groups"]

    instance_name = input("Digite o nome da instância que deseja associar um security group: ")

    instance_exists = False
    associate_security_group = True

    while associate_security_group:

        for instance in instances:
            if instance["name"] == instance_name:
                instance_exists = True
                security_group_name = input("Digite o nome do security group ao qual deseja associar a instância: ")
                security_group_exists = False

                for security_group in security_groups:
                    if security_group["name"] == security_group_name:
                        security_group_exists = True
                        print(" ")
                        print("\033[32mAssociando security group..." + "\033[0m")
                        sleep(3)
                        instance["security_groups"].remove("default")
                        instance["security_groups"].append(security_group_name)
                        with open('.auto.tfvars.json', 'w') as file:
                            json.dump(terraform_variables, file, indent=2, separators=(',',': '))
                        os.system('terraform apply -auto-approve')
                        print(" ")
                        print("\033[32mSecurity group associado com sucesso!" + "\033[0m")
                        sleep(5)
                        associate_security_group = input("Deseja associar outro security group? (y/n): ")

                        while associate_security_group not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                            print("\033[31mOpção inválida..." + "\033[0m")
                            associate_security_group = input("Por favor, digite 'Y' para associar outro security group ou 'N' para cancelar: ")

                        if associate_security_group in ['y','Y','yes', 'YES']:
                            instance_name = input("Digite o nome da instância que deseja associar um security group: ")

                        elif associate_security_group in ['n','N','no', 'NO']:
                            associate_security_group = False

                if not security_group_exists:
                    print("\033[31mSecurity group não encontrado..." + "\033[0m")
                    sleep(2)
                    associate_security_group = input("Deseja tentar novamente? (y/n): ")

                    while associate_security_group not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                        print("\033[31mOpção inválida..." + "\033[0m")
                        associate_security_group = input("Por favor, digite 'Y' para confirmar ou 'N' para cancelar: ")

                    if associate_security_group in ['y','Y','yes', 'YES']:
                        instance_name = input("Digite o nome da instância que deseja associar um security group: ")

                    elif associate_security_group in ['n','N','no', 'NO']:
                        associate_security_group = False

        if not instance_exists:
            print("\033[31mInstância não encontrada..." + "\033[0m")
            sleep(2)
            associate_security_group = input("Deseja tentar novamente? (y/n): ")

            while associate_security_group not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                print("\033[31mOpção inválida..." + "\033[0m")
                associate_security_group = input("Por favor, digite 'Y' para confirmar ou 'N' para cancelar: ")

            if associate_security_group in ['y','Y','yes', 'YES']:
                instance_name = input("Digite o nome da instância que deseja associar um security group: ")

            elif associate_security_group in ['n','N','no', 'NO']:
                associate_security_group = False


def disassociate_instances():
    with open('.auto.tfvars.json', 'r') as file:
        terraform_variables = json.load(file)

    instances = terraform_variables["instances"]

    security_groups = terraform_variables["security_groups"]

    instance_name = input("Digite o nome da instância que deseja desassociar de um security group: ")

    instance_exists = False
    disassociate_security_group = True

    while disassociate_security_group:
            
            for instance in instances:
                if instance["name"] == instance_name:
                    instance_exists = True
                    security_group_name = input("Digite o nome do security group que deseja desassociar da instância: ")
                    security_group_exists = False
    
                    for security_group in security_groups:
                        if security_group["name"] == security_group_name:
                            security_group_exists = True
                            print(" ")
                            print("\033[32mDesassociando security group..." + "\033[0m")
                            sleep(3)
                            instance["security_groups"].remove(security_group_name)
                            if len(instance["security_groups"]) == 0:
                                instance["security_groups"].append("default")
                            with open('.auto.tfvars.json', 'w') as file:
                                json.dump(terraform_variables, file, indent=2, separators=(',',': '))
                            os.system('terraform apply -auto-approve')
                            print(" ")
                            print("\033[32mSecurity group desassociado com sucesso!" + "\033[0m")
                            sleep(5)
                            disassociate_security_group = input("Deseja desassociar outro security group? (y/n): ")
    
                            while disassociate_security_group not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                                print("\033[31mOpção inválida..." + "\033[0m")
                                disassociate_security_group = input("Por favor, digite 'Y' para desassociar outro security group ou 'N' para cancelar: ")
    
                            if disassociate_security_group in ['y','Y','yes', 'YES']:
                                instance_name = input("Digite o nome da instância que deseja desassociar de um security group: ")
    
                            elif disassociate_security_group in ['n','N','no', 'NO']:
                                disassociate_security_group = False
    
                    if not security_group_exists:
                        print("\033[31mSecurity group não encontrado..." + "\033[0m")
                        sleep(2)
                        disassociate_security_group = input("Deseja tentar novamente? (y/n): ")
    
                        while disassociate_security_group not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                            print("\033[31mOpção inválida..." + "\033[0m")
                            disassociate_security_group = input("Por favor, digite 'Y' para confirmar ou 'N' para cancelar: ")
    
                        if disassociate_security_group in ['y','Y','yes', 'YES']:
                            instance_name = input("Digite o nome da instância que deseja desassociar de um security group: ")

                        elif disassociate_security_group in ['n','N','no', 'NO']:
                            disassociate_security_group = False

            if not instance_exists:
                print("\033[31mInstância não encontrada..." + "\033[0m")
                sleep(2)
                disassociate_security_group = input("Deseja tentar novamente? (y/n): ")

                while disassociate_security_group not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                    print("\033[31mOpção inválida..." + "\033[0m")
                    disassociate_security_group = input("Por favor, digite 'Y' para confirmar ou 'N' para cancelar: ")

                if disassociate_security_group in ['y','Y','yes', 'YES']:
                    instance_name = input("Digite o nome da instância que deseja desassociar de um security group: ")

                elif disassociate_security_group in ['n','N','no', 'NO']:
                    disassociate_security_group = False


def display_users_menu():

    os.system("cls")

    menu = """
\033[36m/----------------------------- LARRYSFORM - USUÁRIOS -----------------------------/\033[0m

1. CRIAR

2. LISTAR

3. DELETAR

4. VOLTAR
    """

    print(menu)


def create_user():
    with open('.auto.tfvars.json', 'r') as file:
        terraform_variables = json.load(file)

    users = terraform_variables["users"]

    create_user = True

    while create_user: 

        print(" ")
        print("\033[94mPrimeiramente digite o nome do usuário deseja criar." + "\033[0m")
        print(" ")

        sleep(1)

        user_name = input("Digite o nome do usuário: ")
        print(" ")

        user_exists = False
        for user in users:
            if user["name"] == user_name:
                user_exists = True

        if user_exists:
            print("\033[31mUsuário já existe..." + "\033[0m")
            print(" ")
            sleep(2)
            create_user = input("\033[36mDeseja tentar novamente? (y/n): " + "\033[0m")

            while create_user not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                print("\033[31mOpção inválida..." + "\033[0m")
                create_user = input("Por favor, digite 'Y' para tentar novamente ou 'N' para cancelar: ")

            if create_user in ['y','Y','yes', 'YES']:
                create_user = True

            elif create_user in ['n','N','no', 'NO']:
                create_user = False

        else:

            add_restriction = input("\033[31mDeseja adicionar restrições ao usuário? (y/n): " + "\033[0m")
            print(" ")

            restriction = {}

            while add_restriction not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                print("\033[31mOpção inválida..." + "\033[0m")
                add_restriction = input("Por favor, digite 'Y' para adicionar restrições ou 'N' para cancelar: ")

            if add_restriction in ['y','Y','yes', 'YES']:
                add_restriction = True

                while add_restriction:

                    restriction_name = input("Digite o nome da restrição: ")
                    print(" ")

                    while restriction_name == "":
                        print("\033[31mRestrições não podem ter nomes vazios..." + "\033[0m")
                        restriction_name = input("Por favor, digite o nome da restrição: ")

                    sleep(1)

                    restriction_description = input("Digite a descrição da restrição: ")
                    print(" ")

                    while restriction_description == "":
                        print("\033[31mRestrições não podem ter descrições vazias..." + "\033[0m")
                        restriction_description = input("Por favor, digite a descrição da restrição: ")

                    sleep(1)

                    action_restrictions = input("Digite as restrições de ação: ")
                    print(" ")
                    sleep(1)

                    resources_restrictions = input("Digite as restrições de recursos: ")
                    print(" ")
                    sleep(1)

                    restriction = {
                        "name": restriction_name,
                        "description": restriction_description,
                        "actions": action_restrictions.split(","),
                        "resources": resources_restrictions.split(",")
                    }

                    add_restriction = False

            elif add_restriction in ['n','N','no', 'NO']:
                restriction = {
                    "name": "user_full_access_" + str(len(users) + 1),
                    "description": "Full Access",
                    "actions": ['*'],
                    "resources": ['*']
                }

            user = {
                "name": user_name,
                "restriction": restriction
            }

            print("\033[36mNome do usuário: " + "\033[0m" + user_name)
            print(" ")
            sleep(0.5)
            print("\033[31mRestrição: " + "\033[0m" + restriction["name"])
            print("\033[35mDescrição: " + "\033[0m" + restriction["description"])
            print("\033[35mRestrições de ação: " + "\033[0m" + (',').join(restriction["actions"]))
            print("\033[35mRestrições de recursos: " + "\033[0m" + (',').join(restriction["resources"]))
            print(" ")
            sleep(0.5)

            confirm_user = input("Deseja confirmar a criação do usuário? (y/n): ")

            while confirm_user not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                print("\033[31mOpção inválida..." + "\033[0m")
                confirm_user = input("Por favor, digite 'Y' para confirmar a criação do usuário ou 'N' para cancelar: ")

            if confirm_user in ['y','Y','yes', 'YES']:

                users.append(user)

                with open('.auto.tfvars.json', 'w') as file:
                    json.dump(terraform_variables, file, indent=2, separators=(',',': '))

                if region == "1":
                    with open('../sa-east-1/.auto.tfvars.json', 'r') as file:
                        terraform_variables = json.load(file)

                    terraform_variables["users"] = users

                    with open('../sa-east-1/.auto.tfvars.json', 'w') as file:
                        json.dump(terraform_variables, file, indent=2, separators=(',',': '))

                elif region == "2":
                    with open('../us-east-1/.auto.tfvars.json', 'r') as file:
                        terraform_variables = json.load(file)

                    terraform_variables["users"] = users

                    with open('../us-east-1/.auto.tfvars.json', 'w') as file:
                        json.dump(terraform_variables, file, indent=2, separators=(',',': '))

                os.system('terraform apply -auto-approve')

                create_user = input("\033[32mUsuário criado com sucesso! Deseja criar outro usuário? (y/n): " + "\033[0m")

                while create_user not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                    print("\033[31mOpção inválida..." + "\033[0m")
                    create_user = input("Por favor, digite 'Y' para criar outro usuário ou 'N' para cancelar: ")

                if create_user in ['y','Y','yes', 'YES']:
                    create_user = True

                elif create_user in ['n','N','no', 'NO']:
                    create_user = False

            elif confirm_user in ['n','N','no', 'NO']:
                create_user = input("Deseja criar outro usuário? (y/n): ")

                while create_user not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                    print("\033[31mOpção inválida..." + "\033[0m")
                    create_user = input("Por favor, digite 'Y' para criar outro usuário ou 'N' para cancelar: ")

                if create_user in ['y','Y','yes', 'YES']:
                    create_user = True

                elif create_user in ['n','N','no', 'NO']:
                    create_user = False


def list_users():
    with open('.auto.tfvars.json') as file:
        terraform_variables = json.load(file)

    users = terraform_variables["users"]

    print(" ")

    if len(users) == 0:
        print("\033[31mNão há usuários cadastrados..." + "\033[0m")
        sleep(2)
        return

    print("\033[32mUsuários cadastrados:" + "\033[0m")
    sleep(0.5)
    for user in users:
        print("\033[36mNome do usuário: " + "\033[0m" + user["name"])
        sleep(0.5)
        print("\033[31mRestrição: " + "\033[0m" + user["restriction"]["name"])
        print("\033[35mDescrição: " + "\033[0m" + user["restriction"]["description"])
        print("\033[35mRestrições de ação: " + "\033[0m" + (',').join(user["restriction"]["actions"]))
        print("\033[35mRestrições de recursos: " + "\033[0m" + (',').join(user["restriction"]["resources"]))
        print(" ")
        sleep(0.5)

    sleep(5)


def delete_user():
    with open('.auto.tfvars.json') as file:
        terraform_variables = json.load(file)

    users = terraform_variables["users"]

    print(" ")

    if len(users) == 0:
        print("\033[31mNão há usuários cadastrados..." + "\033[0m")
        sleep(2)
        return

    delete_users = True

    while  delete_users == True:

        user_name = input("Digite o nome do usuário que deseja deletar: ")
        print(" ")

        user_found = False

        for user in users:
            if user["name"] == user_name:
                user_found = True
                users.remove(user)

                print("\033[31m deletando usuário..." + "\033[0m")

                with open('.auto.tfvars.json', 'w') as file:
                    json.dump(terraform_variables, file, indent=2, separators=(',',': '))

                if region == "1":
                    with open('../sa-east-1/.auto.tfvars.json', 'r') as file:
                        terraform_variables = json.load(file)

                    terraform_variables["users"] = users

                    with open('../sa-east-1/.auto.tfvars.json', 'w') as file:
                        json.dump(terraform_variables, file, indent=2, separators=(',',': '))

                elif region == "2":
                    with open('../us-east-1/.auto.tfvars.json', 'r') as file:
                        terraform_variables = json.load(file)

                    terraform_variables["users"] = users

                    with open('../us-east-1/.auto.tfvars.json', 'w') as file:
                        json.dump(terraform_variables, file, indent=2, separators=(',',': '))

                os.system('terraform apply -auto-approve')

                print("\033[32mUsuário deletado com sucesso!" + "\033[0m")
                sleep(2)
                delete_users = input("Deseja deletar outro usuário? (y/n): ")

                while delete_users not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                    print("\033[31mOpção inválida..." + "\033[0m")
                    delete_users = input("Por favor, digite 'Y' para deletar outro usuário ou 'N' para cancelar: ")

                if delete_users in ['y','Y','yes', 'YES']:
                    delete_users = True

                elif delete_users in ['n','N','no', 'NO']:
                    delete_users = False

        if user_found == False:
            print("\033[31mUsuário não encontrado..." + "\033[0m")
            sleep(2)

            delete_users = input("Deseja tentar novamente? (y/n): ")

            while delete_users not in ['y','Y','yes', 'YES', 'n', 'N', 'no', 'NO']:
                print("\033[31mOpção inválida..." + "\033[0m")
                delete_users = input("Por favor, digite 'Y' para tentar novamente ou 'N' para cancelar: ")

            if delete_users in ['y','Y','yes', 'YES']:
                delete_users = True

            elif delete_users in ['n','N','no', 'NO']:
                delete_users = False
        

################################### MAIN LOOP ###################################
os.system("cls")

show_opening_message = True

while True:

    if show_opening_message:
        region = display_opening_message()
        show_opening_message = False

    display_main_menu()

    menu_answer = input("Digite o número da opção desejada: ")

    while menu_answer not in ['1','2','3', '4']:
        print("\033[31mOpção inválida..." + "\033[0m")
        print("'\033[31mPor favor, digite o número da opção dentre as apresentadas." + "\033[0m")
        menu_answer = input("Digite o número da opção desejada: ") 

    if menu_answer == '1':
        security_group_menu = True
        while security_group_menu:
            display_security_groups_menu()
            sleep(1)
            security_group_menu_answer = input("Digite o número da opção desejada: ")

            if security_group_menu_answer == '1':
                create_security_group()   

            elif security_group_menu_answer == '2':
                list_security_groups()

            elif security_group_menu_answer == '3':
                delete_security_group()

            elif security_group_menu_answer == '4':
                display_rules_menu()
                sleep(1)
                rules_menu_answer = input("Digite o número da opção desejada: ")

                if rules_menu_answer == '1':
                    create_rules()

                elif rules_menu_answer == '2':
                    list_rules()

                elif rules_menu_answer == '3':
                    delete_rules()
            
            elif security_group_menu_answer == '5':
                security_group_menu = False

    elif menu_answer == '2':
        instances_menu = True
        while instances_menu:
            display_instances_menu()
            sleep(1)
            instances_menu_answer = input("Digite o número da opção desejada: ")

            if instances_menu_answer == '1':
                create_instance()

            elif instances_menu_answer == '2':
                list_instances()

            elif instances_menu_answer == '3':
                delete_instances()

            elif instances_menu_answer == '4':
                associate_instances()

            elif instances_menu_answer == '5':
                disassociate_instances()

            elif instances_menu_answer == '6':
                instances_menu = False

    elif menu_answer == '3':
        users_menu = True
        while users_menu:
            display_users_menu()
            sleep(1)
            users_menu_answer = input("Digite o número da opção desejada: ")

            if users_menu_answer == '1':
                create_user()

            elif users_menu_answer == '2':
                list_users()

            elif users_menu_answer == '3':
                delete_user()

            elif users_menu_answer == '4':
                users_menu = False

    elif menu_answer == '4':

        print("\033[32mSaindo da plataforma..." + "\033[0m")
        sleep(2)
        break