from flask import Flask, render_template, request, redirect
import psycopg2
import os


aplicativo = Flask(__name__)

#Método que faz a conexão com o banco de dados
def conecta_db():
    conecta = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='1234')
    return conecta


#MEU SITE
@aplicativo.route("/")
def homepage():
    return render_template('index.html')



#Rota para fazer inserção no banco (CADASTRO)
@aplicativo.route("/cadastro", methods=['POST'])
def cadastro():
    if  request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        cidade = request.form['cidade']
        estado = request.form['estado']
        profissao = request.form['profissao']

        conexao = conecta_db()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO cliente (nome, cpf, cidade, estado, profissao) VALUES (%s, %s, %s, %s, %s)", (nome, cpf, cidade, estado, profissao))
        conexao.commit()
        cursor.close()
        conexao.close()


        return render_template('form_sucesso.html')
#Rota para fazer inserção no banco (CADASTRO)    





#Grid (Relatório)
@aplicativo.route("/grid", methods=['GET','POST'])
def grid():
    if  request.method == 'POST':
        relatorio = request.form['gerar_grid']
        conexao = conecta_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM cliente")
        resultado = cursor.fetchall()

        cursor.close()

        return render_template('grid.html', resultado=resultado)
    else:
        return render_template('grid.html', resultado=None)
#Grid (Relatório)



#
@aplicativo.route("/filtro_rota", methods=['GET','POST'])
def filtro():
    if  request.method == 'POST':
        filtro_pesquisa = request.form['filtro_input']
        conexao = conecta_db()
        cursor = conexao.cursor()
        filtro_pesquisa = '%' + filtro_pesquisa + '%'
        cursor.execute("SELECT nome, cpf, cidade, estado, profissao FROM cliente WHERE nome LIKE %s", (filtro_pesquisa,))
        resultado = cursor.fetchall()

        cursor.close()

        return render_template('filtro.html', resultado=resultado)
    else:
        return render_template('filtro.html', resultado=None)















#informações padrão do sistema web
if __name__ == "__main__":
    aplicativo.run(debug=True, port=8085, host='127.0.0.1')



