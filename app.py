from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'leilao.db')
db = SQLAlchemy(app)

# Modelo de usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    senha = db.Column(db.String(200))
    telefone = db.Column(db.String(20))

# Criar o banco de dados
with app.app_context():
    db.create_all()

# Rota de cadastro
@app.route('/api/cadastro', methods=['POST'])
def cadastrar_usuario():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    telefone = data.get('telefone')

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"erro": "Email já cadastrado"}), 400

    hash_senha = generate_password_hash(senha)
    novo_usuario = Usuario(nome=nome, email=email, senha=hash_senha, telefone=telefone)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201

# Rota simples pra testar se está online
@app.route('/')
def index():
    return "API do UENO LEILÃO está online 🚀"
