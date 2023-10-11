# Importações

from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
import pdfkit


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    cargo = db.Column(db.String(80))
    departamento = db.Column(db.String(80))
    cpf = db.Column(db.String(11))

# Rota para a página inicial
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

# Rota para adicionar ou editar um usuário
@app.route('/save', methods=['POST'])
def save():
    user_id = request.form.get('user_id')
    nome = request.form['nome']
    cargo = request.form['cargo']
    departamento = request.form['departamento']
    cpf = request.form['cpf']

    if user_id:
        user = User.query.get(user_id)
        user.nome = nome
        user.cargo = cargo
        user.departamento = departamento
        user.cpf = cpf
    else:
        new_user = User(nome=nome, cargo=cargo, departamento=departamento, cpf=cpf)
        db.session.add(new_user)

    db.session.commit()
    return redirect(url_for('index'))

# Rota para excluir um usuário
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('index'))

# Rota para editar um usuário
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.nome = request.form['nome']
        user.cargo = request.form['cargo']
        user.departamento = request.form['departamento']
        user.cpf = request.form['cpf']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', user=user)

@app.route('/generate_pdf')
def generate_pdf():
    # Rota para gerar o PDF da lista de usuários
    users = User.query.all()
    html = render_template('pdf_template.html', users=users)
    
    # Caminho para o executável wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    options = {
    'page-size': 'A4',
    'margin-top': '3mm',
    'margin-right': '2mm',
    'margin-bottom': '2mm',
    'margin-left': '3mm',
    'no-outline': None,  # Oculta a borda do PDF
    'encoding': 'UTF-8',
    'disable-smart-shrinking': None,
    'footer-right': 'Data: [date]',
    'footer-font-size': '10',
    'footer-line': None,
    'footer-spacing': '5',
    'header-left': 'Página [page] de [toPage]',
    'header-right': '[section]',
    'header-line': None,
    'header-spacing': '5',
    'user-style-sheet': 'static/css/styles.css'
    }

    pdf = pdfkit.from_string(html, False, configuration=config, options=options)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=users_list.pdf'

    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
