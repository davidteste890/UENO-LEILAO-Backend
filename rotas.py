from flask import Blueprint, request, jsonify
from app import db
from models import Usuario, Produto, Lance
from datetime import datetime

rotas_api = Blueprint('api', __name__)

@rotas_api.route("/api/produtos")
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([
        {
            "id": p.id,
            "nome": p.nome,
            "descricao": p.descricao,
            "imagem": p.imagem,
            "preco_inicial": p.preco_inicial,
            "data_fim": p.data_fim.strftime("%Y-%m-%d %H:%M:%S")
        } for p in produtos
    ])

@rotas_api.route("/api/lances", methods=["POST"])
def registrar_lance():
    dados = request.json
    novo_lance = Lance(
        produto_id=dados["produto_id"],
        usuario_id=1,  # Simulado. Ideal: extrair do token.
        valor=dados["valor"]
    )
    db.session.add(novo_lance)
    db.session.commit()
    return jsonify({"mensagem": "Lance registrado com sucesso"})
