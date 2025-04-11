from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leilao.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Importa modelos e rotas
from models import *
from rotas import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria o banco e as tabelas se não existirem
    app.run(host='0.0.0.0', port=10000)
