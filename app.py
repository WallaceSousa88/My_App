from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/funcionarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Defina o modelo de dados aqui
class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cargo = db.Column(db.String(50))
    departamento = db.Column(db.String(50))
    cpf = db.Column(db.Integer)
    cnpj = db.Column(db.Integer)

# Verifique se o banco de dados existe; se não, crie-o
with app.app_context():
    db.create_all()

# Rotas e lógica de visualização e adição de funcionários

@app.route('/')
def index():
    funcionarios = Funcionario.query.all()
    return render_template('index.html', funcionarios=funcionarios)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_funcionario():
    if request.method == 'POST':
        nome = request.form['nome']
        cargo = request.form['cargo']
        departamento = request.form['departamento']
        cpf = request.form['cpf']
        cnpj = request.form['cnpj']

        funcionario = Funcionario(nome=nome, cargo=cargo, departamento=departamento, cpf=cpf, cnpj=cnpj)

        db.session.add(funcionario)
        db.session.commit()

        flash('Funcionário adicionado com sucesso!', 'success')

        return redirect(url_for('index'))

    return render_template('adicionar_funcionario.html')

if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    app.run(debug=True)