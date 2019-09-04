#!flask/bin/python
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from base64 import b64encode
import sys
import configparser
from Crawler import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '\x8b\xcbG\x95\xda\xb8\xbbz.x\xc5\xd7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# Funcao que le arquivo de configurações
def get_ConfigFile(inifile, section):
	c = configparser.ConfigParser()
	dataset = c.read(inifile)
	if len(dataset) != 1:
		raise ValueError

	try:
		c.read(inifile)
	except Exception:
		raise e

	# Verifca as keys do arquivo de configuração
	for key in c[section]:
		if len(c[section][key]) == 0:
			fatal("fatal: %s: could not find %s string" % (inifile, key), 1)

	return c[section]


class User(db.Model):

	# Nome da tabela a ser usada
	__tablename__ = 'users'

	# Aramzendo coluna a ser usada
	id = db.Column(db.Integer, primary_key=True)

	# Tipo do campo Username
	username = db.Column(db.String(32), index=True)

	# Tipo do campo senha
	password_hash = db.Column(db.String(64))

	# Funcao para hash da senha
	def hash_password(self, password):

		self.password_hash = pwd_context.encrypt(password)

	# Funcao que valida senha(login)
	def verify_password(self, password):

		return pwd_context.verify(password, self.password_hash)

	# Funcao para geracao do Token de Acesso
	def generate_auth_token(self, expiration=600):

		s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)

		return s.dumps({'id': self.id})

	# Funcao de verificacao do Token de Acesso
	@staticmethod
	def verify_auth_token(token):

		s = Serializer(app.config['SECRET_KEY'])

		try:

			data = s.loads(token)

		# Token valido e expirado
		except SignatureExpired:

			return None

		# Token Invalido
		except BadSignature:

			return None

		user = User.query.get(data['id'])

		return user

@auth.verify_password
def verify_password(username_or_token, password):

	# Tenta autenticar com token
	user = User.verify_auth_token(username_or_token)

	# Se nao conseguir, tenta login e senha
	if not user:

		user = User.query.filter_by(username=username_or_token).first()

		# Se nap conseguir, retorna Inautorizado
		if not user or not user.verify_password(password):

			return False

	g.user = user

	return True



@app.route('/users', methods = ['POST'])
def new_user():

	# Pego o usuario recebido
	username = request.json.get('username')

	# Pego a senha recebida
	password = request.json.get('password')

	# Gero pass para o Token (Header) de acesso
	userpass = bytes((username+":"+password), 'utf-8')

	# Gero o token (Header)
	userAndPass = b64encode(b"%s"%userpass).decode("ascii")

	# Se usuario ou senha vazio, retorna erro
	if username is None or password is None:

		abort(400)

	# Se ja existir usuario, erro
	if User.query.filter_by(username = username).first() is not None:

		abort(400)

		return jsonify({'Error Message': 'Usuario já existente'})

	# Salvo user para insercao no banco
	user = User(username = username)

	# Gero Hash da senha
	user.hash_password(password)

	# Adiciono dados ao Banco
	db.session.add(user)

	# Commito os dados
	db.session.commit()
	
	return jsonify({ 'username': user.username , 'Authorization': 'Basic ' + userAndPass}), 201, {'Location': url_for('get_user', id = user.id, _external = True)}

# Consulta para buscar usuario
# Validacoes internas
@app.route('/users/<int:id>')
def get_user(id):

	user = User.query.get(id)

	if not user:

		abort(400)

	return jsonify({'username': user.username})

# Metodo para geração de Token de Acesso
@app.route('/token')
@auth.login_required
def get_auth_token():
	
	# Tempo de expiração de 10 minutos
	token = g.user.generate_auth_token(600)

	return jsonify({'token': token.decode('ascii'), 'duration': 600})

# Metodo para consulta dos dados
@app.route('/getCrawler', methods=['GET'])
@auth.login_required
def get():

	# Tendo deletar arquivo auxiliar, caso exista
	try:
		os.remove('return.json')
	except:
		pass

	# Chamo o Crawler criando um arquivo .json

	# Windows
	os.system("scrapy runspider scraper.py -o return.json")

	# Ubuntu 18.04
	# os.system("sudo scrapy runspider scraper.py -o return.json")

	# Armazeno a resposta
	response = Crawler().getJson()

	# Deleto o Arquivo de auxilio
	os.remove('return.json')

	return(response)

if __name__ == '__main__':

	config = get_ConfigFile(sys.argv[0]+'.cfg', 'production')
	ip = config['listen_ip']
	port = config['listen_port']

	if not os.path.exists('db.sqlite'):
	
		# Crio DB se nao houver
		db.create_all()

	app.run(host=ip, port=port, debug=False)
	
