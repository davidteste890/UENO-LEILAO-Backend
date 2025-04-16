from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone
        }

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300), nullable=True)
    preco_inicial = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(300), nullable=True)
    data_fim = db.Column(db.String(100), nullable=True)  # Pode ser datetime no futuro

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco_inicial': self.preco_inicial,
            'imagem': self.imagem,
            'data_fim': self.data_fim
        }

class Lance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('lances', lazy=True))
    produto = db.relationship('Produto', backref=db.backref('lances', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'valor': self.valor,
            'usuario_id': self.usuario_id,
            'produto_id': self.produto_id
        }
