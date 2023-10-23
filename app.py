from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pdfkit

login_manager = LoginManager()
login_manager.init_app(app)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/data.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    cargo = db.Column(db.String(80))
    departamento = db.Column(db.String(80))
    cpf = db.Column(db.String(14))

class User(UserMixin, db.Model):
    # Defina os campos do usuário

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        nome = request.form['nome']
        cargo = request.form['cargo']
        departamento = request.form['departamento']
        cpf = request.form['cpf']

        new_user = User(nome=nome, cargo=cargo, departamento=departamento, cpf=cpf)
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_user/<int:id>')
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Implemente a função de login

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/generate_pdf')
def generate_pdf():
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'no-outline': None,
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
        'user-style-sheet': 'static/css/styles.css'  # Caminho para o arquivo CSS personalizado
    }

    users = User.query.all()
    html = render_template('pdf_template.html', users=users)

    pdf = pdfkit.from_string(html, False, configuration=config, options=options)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=users_list.pdf'

    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)