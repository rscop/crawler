#!/usr/bin/python
import json
import descriptionParse
import codecs

# Funcao que le arquivo auxiliar e transforma e Json
def fileToJson():

	myfile = open('return.json', 'r')

	return json.loads(myfile.read())

# Classe Pai
class Crawler:

	def __init__(self):

		# Transformo os dados em Json
		self.obj = fileToJson()

		# Chamo o Parse do Dado
		self.Rjson = self.parseHeader(self.obj)

	def parseHeader(self, obj):

		item = {}

		item['feed'] = []

		for d in obj:


			# Em Content eu chamo a funcao para parser do Description
			data = {

				'titulo' : d['title'],
				'link' : d['link'],
				'content': descriptionParse.parser(d['description'])

			}
			
			# Adiciono o item formatado ao array
			item['feed'].append(data)

		return item

	# Funcao para extracao do dado
	def getJson(self):
		
		return self.Rjson
