from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import Usuario, Produto, Lance
from app import app, db
from datetime import timedelta

# Rota para cadastro de usuário
@app.route('/api/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()

    # Verificar se o email já está registrado
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify(message="Email já registrado!"), 400

    # Criar novo usuário
    novo_usuario = Usuario(
        nome=data['nome'],
        email=data['email'],
        senha=generate_password_hash(data['senha']),
        telefone=data['telefone']
    )

    # Adicionar ao banco de dados
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify(novo_usuario.to_dict()), 201


# Rota para login (gera o token JWT)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    # Verificar se o usuário existe
    usuario = Usuario.query.filter_by(email=data['email']).first()
    if not usuario or not check_password_hash(usuario.senha, data['senha']):
        return jsonify(message="Email ou senha incorretos!"), 401

    # Gerar o token JWT
    access_token = create_access_token(identity=usuario.id, expires_delta=timedelta(days=1))

    return jsonify(access_token=access_token), 200


# Rota para cadastro de produto
@app.route('/api/produtos', methods=['POST'])
@jwt_required()  # Protege a rota para apenas usuários autenticados
def create_produto():
    data = request.get_json()

    # Criar novo produto
    novo_produto = Produto(
        nome=data['nome'],
        descricao=data['descricao'],
        preco=data['preco'],
        data_fim=data['data_fim']
    )

    # Adicionar ao banco de dados
    db.session.add(novo_produto)
    db.session.commit()

    return jsonify(novo_produto.to_dict()), 201


# Rota para registrar um lance
@app.route('/api/lances', methods=['POST'])
@jwt_required()  # Protege a rota para apenas usuários autenticados
def create_lance():
    data = request.get_json()
    usuario_id = get_jwt_identity()  # Pega o ID do usuário logado
    produto_id = data['produto_id']

    # Verifica se o produto existe
    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify(message="Produto não encontrado!"), 404

    # Verifica se o lance é maior que o preço atual do produto
    if data['valor'] <= produto.preco:
        return jsonify(message="O valor do lance deve ser maior que o preço atual do produto!"), 400

    # Criar o lance
    novo_lance = Lance(
        valor=data['valor'],
        usuario_id=usuario_id,
        produto_id=produto_id
    )

    # Adicionar ao banco de dados
    db.session.add(novo_lance)
    db.session.commit()

    # Atualizar o preço do produto com o valor do lance
    produto.preco = data['valor']
    db.session.commit()

    return jsonify(novo_lance.to_dict()), 201


# Rota para obter os produtos
@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    return jsonify([produto.to_dict() for produto in produtos]), 200


# Rota para obter o perfil do usuário (com lances realizados)
@app.route('/api/usuarios/perfil', methods=['GET'])
@jwt_required()  # Protege a rota para apenas usuários autenticados
def get_perfil_usuario():
    usuario_id = get_jwt_identity()  # Pega o ID do usuário logado
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify(message="Usuário não encontrado!"), 404

    # Retorna os dados do usuário, incluindo lances realizados
    return jsonify({
        'nome': usuario.nome,
        'email': usuario.email,
        'telefone': usuario.telefone,
        'lances': [lance.to_dict() for lance in usuario.lances]
    }), 200


# Rota para editar perfil do usuário
@app.route('/api/usuarios/perfil', methods=['PUT'])
@jwt_required()  # Protege a rota para apenas usuários autenticados
def editar_perfil_usuario():
    data = request.get_json()
    usuario_id = get_jwt_identity()

    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify(message="Usuário não encontrado!"), 404

    # Atualizar os dados do usuário
    if 'nome' in data:
        usuario.nome = data['nome']
    if 'email' in data:
        usuario.email = data['email']
    if 'telefone' in data:
        usuario.telefone = data['telefone']

    # Commit as alterações no banco de dados
    db.session.commit()

    return jsonify(usuario.to_dict()), 200
