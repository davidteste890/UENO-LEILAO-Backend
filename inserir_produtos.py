import sqlite3

conn = sqlite3.connect('produtos.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        preco_inicial REAL NOT NULL
    )
''')

cursor.execute('''
    INSERT INTO produtos (nome, descricao, preco_inicial)
    VALUES ('Notebook Gamer', 'Notebook com RTX 3060 e 16GB RAM', 4500.00)
''')

conn.commit()
conn.close()

