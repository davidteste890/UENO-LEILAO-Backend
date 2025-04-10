from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

# Usuário de teste (poderia vir do banco depois)
USUARIO_FAKE = {
    "email": "admin@teste.com",
    "senha": "123456"
}

@auth_bp.route('/api/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    if email == USUARIO_FAKE["email"] and senha == USUARIO_FAKE["senha"]:
        token = create_access_token(identity=email, expires_delta=timedelta(hours=1))
        return jsonify({"token": token}), 200
    return jsonify({"erro": "Credenciais inválidas"}), 401
