from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Conexão com banco
def get_db_connection():
    conn = sqlite3.connect('produtos.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota de teste
@app.route('/api/teste')
def rota_teste():
    return {'mensagem': 'Servidor Flask funcionando!'}

# Rota de produtos
@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    conn = get_db_connection()
    produtos = conn.execute("SELECT * FROM produtos").fetchall()
    conn.close()
    return jsonify([dict(produto) for produto in produtos])

# Run app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)



