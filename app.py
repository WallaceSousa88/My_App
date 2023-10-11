# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    cargo = db.Column(db.String(80))
    departamento = db.Column(db.String(80))
    cpf = db.Column(db.String(11))

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    nome = request.form['nome']
    cargo = request.form['cargo']
    departamento = request.form['departamento']
    cpf = request.form['cpf']

    new_user = User(nome=nome, cargo=cargo, departamento=departamento, cpf=cpf)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/save', methods=['POST'])
def save():
    user_id = request.form.get('user_id')
    nome = request.form['nome']
    cargo = request.form['cargo']
    departamento = request.form['departamento']
    cpf = request.form['cpf']

    if user_id:
        # Se user_id estiver presente, atualiza o registro existente
        user = User.query.get(user_id)
        user.nome = nome
        user.cargo = cargo
        user.departamento = departamento
        user.cpf = cpf
    else:
        # Caso contrário, cria um novo registro
        new_user = User(nome=nome, cargo=cargo, departamento=departamento, cpf=cpf)
        db.session.add(new_user)

    db.session.commit()
    return redirect(url_for('index'))

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

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)