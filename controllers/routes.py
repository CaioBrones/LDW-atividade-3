from flask import Flask, render_template, request, redirect, url_for, flash
from bs4 import BeautifulSoup
import requests
import sqlite3
import os
import uuid
from models.database import db, Usuario, Celular, Imagem

DATABASE = 'database.py'

# Lista de celulares pré-cadastrados
celulares = [
    {"nome": "iPhone 13", "preco": "5.999,00"},
    {"nome": "Samsung Galaxy S21", "preco": "4.499,00"},
    {"nome": "Xiaomi Mi 11", "preco": "3.999,00"},
    {"nome": "Google Pixel 6", "preco": "4.299,00"},
    {"nome": "OnePlus 9 Pro", "preco": "4.799,00"},
    {"nome": "Motorola Edge 20", "preco": "3.499,00"},
]

def init_app(app):

    @app.route('/')
    def home():
        return render_template('index.html')


    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        if request.method == 'POST':
            nome = request.form['nome']
            preco = float(request.form['preco'].replace('.', '').replace(',', '.'))
            
            novo_produto = Celular(nome=nome, preco=preco)
            db.session.add(novo_produto)
            db.session.commit()
            flash('Produto cadastrado com sucesso!', 'success')
        
        produtos_db = Celular.query.all()
        return render_template('cadastro.html', celulares=celulares, produtos=produtos_db)


    @app.route('/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        produto = Celular.query.get_or_404(id)
        
        if request.method == 'POST':
            produto.nome = request.form['nome']
            produto.preco = float(request.form['preco'].replace('.', '').replace(',', '.'))
            db.session.commit()
            flash('Produto atualizado!', 'success')
            return redirect(url_for('cadastro'))
        
        return render_template('editar.html', produto=produto)


    @app.route('/excluir/<int:id>')
    def excluir(id):
        produto = Celular.query.get_or_404(id)
        db.session.delete(produto)
        db.session.commit()
        flash('Produto excluído!', 'success')
        return redirect(url_for('cadastro'))


    @app.route('/produtos', methods=['GET', 'POST'])
    def produtos():
        if request.method == 'POST':
            # Processar o formulário de cadastro de novos celulares
            nome = request.form.get('nome')
            preco = request.form.get('preco')

            if nome and preco:
                novo_celular = {
                    "nome": nome,
                    "preco": preco,
                }
                celulares.append(novo_celular)
                return redirect(url_for('produtos'))

        return render_template('produtos.html', celulares=celulares)


    @app.route('/consumo')
    def consumo():
        url = "https://www.gsmarena.com/makers.php3"
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            marcas = [{
                'nome': a.text.strip(),
                'link': f"https://www.gsmarena.com/{a['href']}"
            } for a in soup.find('table').find_all('a')]
            return render_template('consumo.html', marcas=marcas)
        except Exception as e:
            return f"Erro: {e}", 500
        
    # Definindo os tipos de arquivos permitidos para upload
    FILE_TYPES = set(['png', 'jpg', 'jpeg', 'gif'])
    def arquivos_permitidos(filename):
        if '.' not in filename:
            return False
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in FILE_TYPES
        # return '.' in filename and filename.rsplit('.', 1)[1].lower() in FILE_TYPES


    @app.route('/galeria', methods=['GET', 'POST'])
    def galeria():
        imagens = Imagem.query.all()
        if request.method == 'POST':
            file = request.files['file']
            if not arquivos_permitidos(file.filename):
                flash("Apenas arquivos PNG, JPG, JPEG e GIF são permitidos.", 'danger')
                return redirect(request.url)
            
            try:
                file_ext = file.filename.rsplit('.', 1)[1].lower()
            except IndexError:
                    flash("Arquivo sem extensão válida.", 'danger')
                    return redirect(request.url)

            filename = f"{uuid.uuid4()}.{file_ext}"
            file_ext = file.filename.rsplit('.', 1)[1].lower()

            img = Imagem(filename)
            db.session.add(img)
            db.session.commit()

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Imagem enviada com sucesso!", 'success')
        return render_template('galeria.html', imagens = imagens)