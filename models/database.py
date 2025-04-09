from flask_sqlalchemy import SQLAlchemy
# Criando uma instância do SQLAlchemy
db = SQLAlchemy()

# Classe para imagens
class Imagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, filename):
        self.filename = filename

class Celular(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    concluida = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Celular {self.nome}>'
        
# Classe de usuários:
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    # Método construtor da classe
    def __init__(self, email, password):
        self.email = email
        self.password = password