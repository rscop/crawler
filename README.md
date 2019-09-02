# Modulos
#### Usado Python3
PIP3 
Flask 
Flash_sqlalchemy 
Flask_httpauth
passlib
HTML
HTMLparser
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
