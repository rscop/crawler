#!/usr/bin/python
import json

def parser(obj):

	# Remocao de carateres indesejados para a formatacao do texto
	# Remocao de tags <p> vazias
	obj = obj.replace("\t", "").replace("\n", "").replace('\xc2', '').replace('\xa0', '').replace("<p></p>", "")

	# Adciono um [ para geracai inicial da lista
	finaljson = "["
	
	# For para validar qual tag esta sendo lida
	for d in range(len(obj)):

		if obj[d] == "<":
			
			# Armazeno uma tag inicial para validacoes
			tag = obj[d:d+3]

			# <img> Esta sendo lido
			if tag == "<im":

				# Chamo funcao de validacao
				data = closeTag(tag, d, obj)

				# Formato a saida da string
				formated = '{"type": "image", "content": "%s"},'%data

				# Adiciono ao objeto Pai
				finaljson += formated

			elif tag == "<p>":

				# Chamo funcao de validacao
				data = closeTag(tag, d, obj)
				
				# Formato a saida da string
				# Trocado Aspas Dupla para Aspas normal
				data = data.replace('"',"'")
				formated = ('{"type": "text", "content": "%s"},'%data).replace("<strong>", "").replace("</strong>", "")
				
				# Adiciono ao objeto Pai
				finaljson += formated


			elif tag == "<ul":

				# Chamo funcao de validacao
				data = closeTag(tag, d, obj)

				# Formato a saida da string
				formated = '{"type": "links", "content": "%s"},'%data

				# Adiciono ao objeto Pai
				finaljson += formated

	# Termino a formatacao com ] para finalizar a lista
	finaljson = (finaljson[:len(finaljson)-1]+']')
	
	return json.loads(finaljson)

def closeTag(tag, pos, obj):

	if tag == "<p>":

		# Endtag para formatacao do dado
		endtag = "</p>"

		# Posicao final do dado
		end = obj[pos:].find(endtag)

		# String que sera formatada
		verify = obj[pos:pos+end]

		# Contagem de links (Se assim houver) dentro de <p>
		nlinks = verify.count("<a href")
		
		if nlinks > 0:

			verify = verify.replace("</a>", "")

			for d in range(nlinks):

				# Busco o link
				inipos = verify.find("<a href=")

				# Busco o fim dele
				endpos = verify[inipos:].find(">")

				# Seleciono parte para remocao
				remove = verify[inipos:endpos+inipos+1]

				# Removo o link, deixando apenas o texto
				verify = verify.replace(remove, "")

			# Removo os parenteses que possam ter vindo junto com o link
			verify = verify.replace("(", "").replace(")", "")

			return verify[+3:]
		# Se nao houver nenhum link, apenas busco a endtag
		endpos = obj[pos:].find(endtag)

		# Remocao de algumas tags que possam ter ficados perdidas dentro dos blocos P
		return obj[pos+3:pos+endpos].replace("<em>", '').replace("</em>", '').replace("<br />", ' ').replace("<u>", '').replace("</u>", '')

	elif tag == "<im":

		# Posicao inicial do link da imagem
		pos = obj[pos:].find('src="')+2+pos

		# Endtag para formatacao do dado
		endtag = '"'

		# Armazendo os dados da URL da imagem
		endpos = obj[pos+3:].find('"')

		return obj[pos+3:pos+endpos+3]


	elif tag == "<ul":

		# Endtag para formatacao do dado
		endtag = "</ul>"

		# Posicao final do dado
		end = obj[pos:].find(endtag)

		# Array para validacao
		links = obj[pos:pos+end]

		links = links.replace("<ul>", "").replace("<li>", "")

		# Contagem de links (Se assim houver) dentro de <p>
		nlinks = links.count("<a href")

		# Separacao de links para construcao do retorno
		links = links.split("<a href=")

		for d in range(len(links)):

			# Pego a URl indo ate o primeiro "
			endpos = links[d][+1:].find('"')

			links[d] = links[d][1:endpos+1]

		# Removo O primeiro valor que sempre fica vazio nesse algoritimo
		links.remove("")
		
		return links