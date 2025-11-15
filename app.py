from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash  # Para segurança da senha
import datetime

# --- 1. CONFIGURAÇÃO ---
app = Flask(__name__)

# ######################################################################
# *** SUBSTITUA ESTA LINHA COM SUA STRING DE CONEXÃO REAL DO MONGODB ***
CONNECTION_STRING = "mongodb://localhost:27017/"
# ######################################################################

try:
    client = MongoClient(CONNECTION_STRING)
    db = client.cadastro_db
    usuarios_collection = db.usuarios
    print("Conexão com MongoDB estabelecida com sucesso.")
except Exception as e:
    print(f"Erro ao conectar ao MongoDB: {e}")


# --- 2. ROTA DE CADASTRO ---
@app.route('/', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha_pura = request.form.get('senha')

        # Geração do HASH da senha para segurança
        senha_hashed = generate_password_hash(senha_pura)

        documento_usuario = {
            "nome": nome,
            "email": email,
            "senha_hash": senha_hashed,
            "data_cadastro": datetime.datetime.now()
        }

        usuarios_collection.insert_one(documento_usuario)

        # Redireciona para atualizar a lista
        return redirect(url_for('cadastro_usuario'))

    # Busca e exibe usuários (apenas nome e email)
    usuarios_cadastrados = usuarios_collection.find({}, {"nome": 1, "email": 1, "_id": 0}).sort("data_cadastro", -1)

    # Renderiza o arquivo HTML
    return render_template('formulario_cadastro.html', usuarios=usuarios_cadastrados)


# --- 3. INICIALIZAÇÃO ---
if __name__ == '__main__':
    app.run(debug=True)