from flask import Flask, render_template, request, redirect
import psycopg2
import os

aplicativo = Flask(__name__)

# Método que faz a conexão com o banco de dados
def conectar_db():
    conecta = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='1234')
    return conecta

# Rota principal
@aplicativo.route("/")
def homepage():
    return render_template('form.html')


@aplicativo.route("/cadastro", methods=['POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        senha = request.form['senha']
        
        conexao = conectar_db()  
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO aula (nome, email, telefone, senha) VALUES (%s, %s, %s, %s )", (nome, email, telefone, senha))
        conexao.commit()
        cursor.close()
        conexao.close()
        
        return render_template('cadastroform.html')
    
#Grid (relatorio)  
 
@aplicativo.route("/relatorio", methods=['GET', 'POST'])
def grid():
    if request.method == 'POST':
        relatorio = request.form['gerar_relatorio']
        conexao = conectar_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM aula")
        resultado = cursor.fetchall()
        
        cursor.close()
        
        return render_template('relatorio.html', resultado=resultado)
    else:
        return render_template('relatorio.html', resultado=None)

#Grid filtro 
 
@aplicativo.route("/filtro_rota", methods=['GET', 'POST'])
def filtro():
    if request.method == 'POST':
        filtro_pesquisa = request.form['filtro_input']
        conexao = conectar_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, email, telefone, senha  FROM aula WHERE nome like %s", ('%' + filtro_pesquisa + '%', ))
        resultado = cursor.fetchall()
        
        cursor.close()
        
        return render_template('filtro.html', resultado=resultado)
    else:
        return render_template('filtro.html', resultado=None)



# Informações padrão do sistema web
if __name__ == "__main__":
    aplicativo.run(debug=True, port=8085, host='127.0.0.1')