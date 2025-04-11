from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from ext import db
from models import Usuario, Produto, Lance

rotas_api = Blueprint('api', __name__)

@rotas_api.route("/api/produtos")
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([
        {
            "id": p.id,
            "titulo": p.titulo,
            "descricao": p.descricao,
            "preco_inicial": p.preco_inicial,
            "data_fim": p.data_fim
        } for p in produtos
    ])

@rotas_api.route("/api/lances", methods=["POST"])
@jwt_required()
def registrar_lance():
    dados = request.json
    usuario_id = get_jwt_identity()
    produto = Produto.query.get(dados["produto_id"])

    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    if datetime.strptime(produto.data_fim, "%Y-%m-%d %H:%M:%S") < datetime.now():
        return jsonify({"erro": "Leilão encerrado"}), 400

    novo_lance = Lance(
        valor=dados["valor"],
        produto_id=produto.id,
        usuario_id=usuario_id,
        data_hora=datetime.now()
    )
    db.session.add(novo_lance)
    db.session.commit()

    return jsonify({"mensagem": "Lance registrado com sucesso"})

@rotas_api.route("/api/lances", methods=["GET"])
@jwt_required()
def listar_lances():
    usuario_id = get_jwt_identity()
    lances = Lance.query.filter_by(usuario_id=usuario_id).all()
    return jsonify([
        {
            "id": l.id,
            "valor": l.valor,
            "produto_id": l.produto_id,
            "data_hora": l.data_hora.strftime("%Y-%m-%d %H:%M:%S")
        } for l in lances
    ])
