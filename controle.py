from terraform import Terraform
import json
import os

operando = True

tf = Terraform()

options:dict()
with open("vars/vars.json", "r") as file:
    options = json.load(file)


def options_cria_instancia(options):
    print(f"    {len(options['configuration'])} instancias ja criadas: {[i['instance_name'] for i in options['configuration']]}")
    instance = dict()
    quant = input("""
    Quantas instancias quer criar?
    """)
    instance['instance_count'] = quant

    name = input("""
    Qual o nome das instancias?
    """)
    instance['instance_name'] = name

    tipo = input("""
    Qual o tipo da instancia?
        -t2.small(1)
        -t2.medium(2)
        -t2.large(3)
    """)
    if(tipo == '1'):
        instance["instance_type"] = "t2.small"
    if(tipo == '2'):
        instance["instance_type"] = "t2.medium"
    if(tipo == '3'):
        instance["instance_type"] = "t2.large"

    ami = input("""
    Qual o OS da instancia?
        -Ubuntu Server 20.04 LTS(1)
        -Ubuntu Server 18.04 LTS(2)
    """)
    if(ami == '1'):
        instance["instance_ami"] = "ami-0149b2da6ceec4bb0"
    elif(ami == '2'):
        instance["instance_ami"] = "ami-0ee23bfc74a881de5"
    return instance

def options_cria_usuario():
    users_set = set(options['user_name'])
    user = dict()
    users_set.add(input("""
    Nome de usuario:"""))
    user['user_name'] = list(users_set)
    #user['user_password'] = input("""
    #criar senha:""")
    return user

def destroy_instace(options):
    try:
        options['configuration']
    except:
        print("Nenhuma instancia criada")
        return
    else:
        print(f"{len(options['configuration'])} configuracoes criadas: {[i['instance_name'] for i in options['configuration']]}")
        des_instance = input("Qual instancia quer remover?\n    ")          #pega o nome da instancia
        for index, instance in enumerate(options['configuration']):
            if des_instance == instance["instance_name"]:
                instance_count = int(instance["instance_count"])
                if instance_count > 1:
                    options['configuration'][index]["instance_count"] = str(instance_count - int(input(f"Quantas das {instance_count} instancias quer remover?")))
                    return options
                else:
                    del options['configuration'][index]
                    return options
        print("Instancia nao existe")
        return

def destroy_user(options):
    try:
        options['user_name']
    except:
        print("Nenhum usuario criado")
        return
    else:
        print(f"Usuarios criados: {options['user_name']}")
        des_user = input("Qual usuario quer remover? ")
        if des_user in options['user_name']:
            options['user_name'].remove(des_user)
        else:
            print("\nUsuario nao existe")
    return

def instace_status():
    print("     Instancias:\n")
    with open("terraform.tfstate", "r") as file:
        status = json.load(file)
        for k in status["resources"]:
            if k["type"] == "aws_instance":
                for i, instances in enumerate(k["instances"]):
                    print(f"     Instancia {i}:")
                    name = instances["attributes"]["tags"]["Name"]
                    instance_type = instances["attributes"]["instance_type"]
                    state = instances["attributes"]["instance_state"]
                    region = instances["attributes"]["availability_zone"]
                    print(f"""
                    -Nome:   {name}
                    -Tipo:   {instance_type}
                    -Status: {state}
                    -Regiao: {region}
                    \n""")
                return
    print("Sem instancia existente")
    return

def user_status():
    with open("terraform.tfstate", "r") as file:
        print("")
        status = json.load(file)
        for k in status["resources"]:
            if k["type"] == "aws_iam_user":
                for i, users in enumerate(k["instances"]):
                    print(f"     Usuario {i}:")
                    name = users["attributes"]["name"]
                    arn = users["attributes"]["arn"]
                    print(f"""
                -Nome: {name}
                -ARN: {arn}\n""")
                return
    print("Sem usuario existente")
    return


def sec_group_status():
    with open("terraform.tfstate", "r") as file:
        print("")
        status = json.load(file)
        for k in status["resources"]:
            if k["type"] == "aws_security_group":
                for i, secs in enumerate(k["instances"]):
                    print(f"     Grupo de seguranca {i}:")
                    name = secs["attributes"]["name"]
                    entrada = secs["attributes"]["ingress"][0]["cidr_blocks"][0]
                    ent_porta = secs["attributes"]["ingress"][0]["from_port"]
                    saida = secs["attributes"]["egress"][0]["cidr_blocks"][0]
                    sai_porta = secs["attributes"]["egress"][0]["from_port"]
                    print(f"""
                -Nome: {name}
                -Entrada: {entrada} na porta {ent_porta}
                -Saida:   {saida} na porta {sai_porta}\n""")
                return
    return

while(operando):
    comando = input("""
    O que deseja fazer:
        1- Criar instancia\n
        2- Adicionar usuario\n
        3- Status\n
        4- Destruir\n
        5- Apply\n
        6- Exit
    """)
    if comando == "1":
        options.setdefault("configuration",[]).append(options_cria_instancia(options))
    if comando == "2":
        print(f"    Usuarios criados: {options['user_name']}")
        name = input("""
        Nome de usuario:""") 
        options.setdefault("user_name",[]).append(name)
    if comando == "3":
        status = input("""
        O que quer verificar:
        1- Instancias\n
        2- Usuarios\n
        3- Grupos de seguranca
        """)
        if status == "1":
            instace_status()
        if status == "2":
            user_status()
        if status == "3":
            sec_group_status()
    if comando == "4":
        destroy = input("""
        O que quer remover:\n
        1- User\n
        2- Instances\n
        3- All\n
        """)
        if destroy == '1':
            destroyed = destroy_user(options)
            if destroyed is not None:
                options = destroyed
        if destroy == '2':
            destroyed = destroy_instace(options)
            if destroyed is not None:
                options = destroyed
        if destroy == '3':
            destroy = input("Toda a infrestrutura sera destruida! Continuar(y/n)?")
            if destroy == "y":
                options = {"user_name": [], "configuration": []}
                os.system(f'cmd /c terraform apply -var-file="vars/vars.json" -auto-approve')
                os.system(f'cmd /c terraform destroy --target aws_subnet.public -auto-approve')
                os.system(f'cmd /c terraform destroy --target aws_vpc.joao_vpc -auto-approve')
                os.system(f'cmd /c terraform destroy --target aws_security_group.ssh_access -auto-approve')
    if comando == "5":
        #tf.apply(var = options)
        with open("vars/vars.json", "w") as outfile:
            json.dump(options, outfile)
        os.system(f'cmd /c terraform plan -var-file="vars/vars.json" -auto-approve')
    if comando == "6":
        operando = False
