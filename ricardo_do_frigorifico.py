from flask import Flask, render_template, request
import psycopg2
import os

aplicativo = Flask(__name__)

#Método que faz a conexão com banco de dados

def conecta_db():
    conecta = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='1234')
    return conecta

#Rota principal
    
@aplicativo.route("/")
def homepage():
        return render_template('clienteback.html')
    

#Rota para fazer inserção no banco
@aplicativo.route("/cadastro", methods=['POST'])
def cadastro():
     if request.method == 'POST':
          nome = request.form['nome']
          email = request.form['email']


          conexao = conecta_db()
          cursor = conexao.cursor()
          cursor.execute("INSERT INTO cliente(nome, email) VALUES(%s,%s)", (nome, email))
          conexao.commit()
          cursor.close()
          conexao.close()

          return render_template('sucesso.html')


    #Informações padrão do sistema web

if __name__ == "__main__":
    aplicativo.run(debug=True, port=8085, host='127.0.0.2')
