from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from models import db  # importa o db do models.py
from routes import app_routes  # importa as rotas

# Criar a instância do Flask
app = Flask(__name__)

# Configurações do banco e JWT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/leilao.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Trocar por uma chave segura em produção

# Inicializar o banco e JWT
db.init_app(app)
jwt = JWTManager(app)

# Registrar as rotas
app.register_blueprint(app_routes)

# Rota inicial simples
@app.route('/')
def home():
    return jsonify(message="Bem-vindo ao UENO LEILÃO!"), 200

# Criar o banco e rodar o app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
