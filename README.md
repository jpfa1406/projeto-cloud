# projeto-cloud
## Descrição
Essa é uma aplicação capaz de provisionar uma infraestrutura por meio de uma interface amigável para gerenciar e administrá-la (construir, alterar e deletar recursos).
### Pré-requisitos:
 - Python3
 - [Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) (1.2.0+) instalado
 - [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) instalado 
 - Conta AWS e credenciais associadas que permitem criar recursos.
 
 ### Configuração AWS
 No AWS CLI:
 ```
 aws configure 
 ```
 Depois:
 ```
AWS Access Key ID [None]: {ACCESS_KEY}
AWS Secret Access Key [None]: {SECRET_ACCESS_KEY}
```
## Uso
Na primeira vez de uso. Usar comando:
```
terraform init
```
Para iniciar o programa use o comando:
```
python3 controle.py
```
O programa permite criar, alterar e destruir recursor AWS, esses recursor são criados navegando os comandos apresentados:
1. Criar instancia
2. Adicionar usuario
3. Status
4. Destruir
5. Apply
6. Exit

Após a criação ou remoção de instancias e usuários desejados é necessário aplicar essas criações/destruições com o comando ```Apply```.
 
