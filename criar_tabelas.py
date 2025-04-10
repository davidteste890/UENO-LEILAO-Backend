# criar_tabelas.py

import sqlite3

conn = sqlite3.connect('leilao.db')

cursor = conn.cursor()

# Tabela de usuários
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
''')

# Tabela de produtos
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    imagem TEXT,
    preco_inicial REAL NOT NULL,
    usuario_id INTEGER,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
''')

# Tabela de lances
cursor.execute('''
CREATE TABLE IF NOT EXISTS lances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER,
    usuario_id INTEGER,
    valor REAL NOT NULL,
    data TEXT NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
''')

conn.commit()
conn.close()

print("Tabelas criadas com sucesso!")
