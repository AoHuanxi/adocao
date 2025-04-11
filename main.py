from flask import Flask, request, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db' 
db = SQLAlchemy(app)  

class tUsers(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    senha = db.Column(db.String(80), nullable=False)

    def __repr__(self) :
        return f'<Usuario {self.email}>'


@app.route('/') 
def homepage() :
    return render_template("index.html")


@app.route('/login', methods=['POST']) 
def login() : 
    dados = request.get_json()
    
    if not dados or 'email' not in dados or 'senha' not in dados:
        return jsonify({"erro": "Email e senha são obrigatórios"})
    
    email = dados['email']
    senha = dados['senha']

    usuario = tUsers.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({"mensagem": "Credenciais inválidas"})
    
    if check_password_hash(usuario.senha, senha):
        return jsonify({
            "mensagem": "Login bem-sucedido",
            "usuario_id": usuario.id
        })
    else:
        return jsonify({"mensagem": "Credenciais inválidas"})
    
@app.route('/cadastro', methods=['GET'])
def cadastro():
    return render_template("cadastro.html")


@app.route('/cadastrar/cadastro', methods = ['POST']) 
def cadastrar() :
    dados = request.get_json()

    if not dados or 'email' not in dados or 'senha' not in dados:
        return jsonify({"erro": "Email e senha são obrigatórios"})
    
    nome = dados['nome']
    email = dados['email']
    senha = dados['senha']

    novo_usuario = tUsers(nome=nome, email=email, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()
    return render_template('index.html')

    
if __name__ == "__main__" :
    with app.app_context():
        db.create_all()
    app.run(debug=True)




