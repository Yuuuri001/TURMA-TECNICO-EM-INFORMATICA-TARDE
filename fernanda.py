from flask import Flask, render_template, request, redirect
import psycopg2
import os

aplicativo = Flask(__name__)

#Método que faz a conexão com o banco de dados
def conecta_db():
    conecta = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='1234')
    return conecta

#Rota principal
@aplicativo.route("/")
def homepage():
    return render_template('form.html')



#Cadastro
@aplicativo.route("/cadastro", methods=['POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']

        conexao = conecta_db()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO aula (nome, email, telefone) VALUES (%s, %s, %s)", (nome, email, telefone))
        conexao.commit()
        cursor.close()
        conexao.close()

        return render_template('form_sucesso.html')



#Grid(realatorio)
@aplicativo.route("/grid", methods=['GET','POST'])
def grid():
    if request.method == 'POST':
       relatorio = request.form['gerar_grid']
       conexao = conecta_db()
       cursor = conexao.cursor()
       cursor.execute("SELECT * FROM aula")
       resultado = cursor.fetchall()

       cursor.close()

       return render_template('grid.html', resultado=resultado)
    else:
       return render_template('grid.html', resultado=None)

#Informações padrão do sistema web
if __name__ == "__main__":
    aplicativo.run(debug=True, port=8085, host='127.0.0.1')