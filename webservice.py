#!flask/bin/python
from flask import Flask
from flask import request
from reader import *
import os

app = Flask(__name__)

@app.route('/getCrawler', methods=['GET'])

def get():

	# Verifico se existe algum arquivo de dados
	if os.path.exists('return.json'):

		# Se sim, deleto
		os.remove('return.json')

	# Chamo o Crawler criando um arquivo .json
	os.system("scrapy runspider scraper.py -o return.json")

	# Armazeno a resposta
	response = Crawler().getJson()

	# Deleto o Arquivo de auxilio
	os.remove('return.json')

	return(response)

app.run(host='0.0.0.0', port=5000)
