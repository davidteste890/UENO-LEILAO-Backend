import jwt
from datetime import datetime, timedelta

# Chave secreta (mantenha segura e não suba ela para repositórios públicos)
SECRET_KEY = 'chave_secreta_super_segura'

# Função para gerar o token JWT
def gerar_token(usuario_id):
    payload = {
        'usuario_id': usuario_id,
        'exp': datetime.utcnow() + timedelta(hours=2)  # Token válido por 2h
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Função para verificar o token JWT
def verificar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['usuario_id']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
