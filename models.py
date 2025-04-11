from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    senha = db.Column(db.String(120))
    telefone = db.Column(db.String(20))

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    preco_inicial = db.Column(db.Float)
    data_fim = db.Column(db.String(100))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Lance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
