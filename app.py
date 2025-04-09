from flask import Flask, render_template
from models.database import db
import requests
import os
from dotenv import load_dotenv

# Criando a instância do Flask na variável app
app = Flask(__name__, template_folder='views')
app.secret_key = 'f299atv'
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config.update(
        SECRET_KEY = os.getenv('SECRET_KEY', 'f299atv'),
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        UPLOAD_FOLDER = 'static/uploads',
        MAX_CONTENT_LENGTH = 16 * 1024 * 1024
        )

    # Inicializa o banco de dados
    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    return app

app = create_app()
from controllers import routes
routes.init_app(app)

# Iniciar o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)