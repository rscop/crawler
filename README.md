# Modulos
#### Usado Python3
PIP3 <br />
Flask <br />
Flash_sqlalchemy <br />
Flask_httpauth <br />
passlib <br />
HTML <br />
HTMLparser <br />
scrapy

# Métodos
### Criar Usuário (POST)
##### Caminho: url:5000/users
###### Body (Json): 

    {"username": "user", "password": "pass"}

##### Retorno:

    {"username": <user>,  "Token": <token>}

#### Consulta de dados (GET)
##### Caminho: url:5000/getCrawler
##### Body Vazio
##### Header:

    Authorization: Basic <token> 

## TODO:
- [ ] Client
- [ ] Melhorar Segurança do WS
- [ ] Implementar requisições Async

# SERVIÇO RODANDO ATUALMENTE NA SEGUINTE URL:
    api.tisp.club:5000
