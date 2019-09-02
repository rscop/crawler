# crawler
Usado Python3 para testes
<hr />

Modulos necessários: <br />
PIP3 <br />
Flask <br />
Flash_sqlalchemy <br />
Flask_httpauth <br />
passlib <br />
HTML <br />
HTMLparser <br />
scrapy <br />
<hr />

Ubuntu: <br />
sudo python webservice.py

Windows: <br />
python webservice.py
<hr />

<h1>Requests</h1>
<hr />
Criar usuario:  <br />
url:5000/users<br />
body:<br />
```json
{
  "username": "user",
  "password": "pass"
}```
<br />
<hr />
Consultar dados: <br />
url:5000/getCrawler <br />
body: vazio <br />
Header <br />
Authorization: Basic .token. <br />
O .token. é recebido ao se criar um usuario<br />


