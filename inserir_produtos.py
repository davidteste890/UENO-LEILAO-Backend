import sqlite3

conexao = sqlite3.connect('leilao.db')
cursor = conexao.cursor()

produtos = [
    ("Notebook Gamer", "Notebook com placa de vídeo dedicada", 3500.00),
    ("iPhone 13", "Smartphone da Apple, 128GB", 4500.00),
    ("Smart TV 50\"", "Televisão 4K com HDR", 2800.00)
]

for nome, descricao, preco in produtos:
    cursor.execute("INSERT INTO produtos (nome, descricao, preco) VALUES (?, ?, ?)", (nome, descricao, preco))

conexao.commit()
conexao.close()

print("Produtos inseridos com sucesso!")
