from flask import Flask, render_template, request, redirect, make_response, session, jsonify, url_for, redirect
import psycopg2
import math
import os
import secrets
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from reportlab.pdfgen import canvas
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Table, TableStyle, Paragraph


aplicativo = Flask(__name__)


aplicativo.secret_key = secrets.token_hex(16)
aplicativo.config['UPLOAD_FOLDER'] = 'uploads'


#Método que faz a conexão com o banco de dados
def conecta_db():
    conecta = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='1234')
    return conecta

#Rota principal
@aplicativo.route("/")
def homepage():
    return render_template('login.html')
#Rota para direcionar para uma página de erro, caso o usuário erre o login/senha

@aplicativo.route("/erro")
def erro():
    return render_template('erro.html')

#Rota para pegar o nome do usuário e enviar para a tela principal "BEM-VINDO nome do usuário"

@aplicativo.route("/enviar_nome_usuario")
def enviar_nome_usuario():
    # Verifique se o usuário está logado
    if 'usuario_logado' in session:
        usuario_logado = session['usuario_logado']
       
        # Conecte ao banco de dados e execute uma consulta para buscar o nome do usuário
        conexao = conecta_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT nome FROM usuario WHERE nome = %s", (usuario_logado,))
        nome_usuario = cursor.fetchone()[0]  # Supondo que o nome do usuário está na primeira coluna

        cursor.close()
        conexao.close()

        return jsonify({"nome_usuario": nome_usuario})

    return jsonify({"nome_usuario": "Visitante"})  # Se o usuário não estiver logado, retorne um valor padrão, como "Visitante"


#Rota para fazer a checagem dos dados de login (email e senha)
@aplicativo.route("/telaprincipal", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        conexao = conecta_db()
        cursor = conexao.cursor()

        # Consulta para checar e-mail e senha
        cursor.execute("SELECT * FROM usuario WHERE email = %s AND senha = %s", (email, senha))
        usuario = cursor.fetchone()
        conexao.close()

        #Caso as credenciais do usuário estejam corretas, o programa desce para este bloco
        if usuario:
            session['usuario_logado'] = usuario[0]  # Supondo que o login do usuário está na primeira posição da tupla (índice 0)
            # Entra na tela para o usuário escolher para onde ir: Área Empresa, Área Senac ou Área Aluno
            return render_template('tela_principal.html')
           
        else:
            # Se alguma coisa der errado, ele vai chamar esta página de erro. Exemplo: Se o usuário digitar a senha errada
            return redirect(url_for('erro'))




#Entra na tela principal após o usuário conseguir colocar o usuário e senha correto
@aplicativo.route("/telaprincipal2", methods=["GET", "POST"])
def login2():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        conexao = conecta_db()
        cursor = conexao.cursor()

        # Consulta para checar e-mail e senha
        cursor.execute("SELECT * FROM usuario WHERE email = %s AND senha = %s", (email, senha))
        usuario = cursor.fetchone()
        conexao.close()

        return render_template('tela_principal.html')







###############################################################################################################################



'''''

#Método que faz a conexão com o banco de dados

def conecta_db():
    conecta = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='1234')
    return conecta

'''''
@aplicativo.route("/cadas")
def cadas():
    return render_template('cads.html')

 





#Rota para fazer inserção no banco
@aplicativo.route("/cadastro", methods=['POST'])
def cadastro():
    if request.method == 'POST':
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


        return render_template('cadastro.html')
    
@aplicativo.route("/grid", methods=['GET','POST'])
def grid():
    if request.method == 'POST':
        relatorio = request.form['gerar_grid']
        conexao = conecta_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM cliente")
        resultado = cursor.fetchall()

        cursor.close()

        return render_template('grid.html', resultado=resultado)
    else:
        return render_template('grid.html', resultado=None)




#Filtro de pesquisa

@aplicativo.route("/filtro_rota", methods=['GET','POST'])
def filtro():
    if request.method == 'POST':
        filtro_pesquisa = request.form['filtro_input']
        conexao = conecta_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, cpf, estado FROM cliente WHERE nome LIKE %s", ('%' + filtro_pesquisa + '%',))
        resultado = cursor.fetchall()

        cursor.close()

        return render_template('filtro.html', resultado=resultado)
    else:
        return render_template('filtro.html', resultado=None)




#Páginação

@aplicativo.route("/paginacao", methods=['GET', 'POST'])
def paginacao():
    page = request.args.get('page', 1, type=int)
    quantidade = 5

    conexao = conecta_db()
    cursor = conexao.cursor()

    #Aqui ele vai contar a quantidade de registros
    cursor.execute('SELECT count(*) FROM cliente')
    total_items = cursor.fetchone()[0]

    #Calcular o número total de páginas
    total_pages = math.ceil(total_items / quantidade)

    #Calcular a saída da consulta
    offset = (page - 1) * quantidade

    cursor.execute('''SELECT nome, cpf, cidade, estado, profissao FROM cliente ORDER BY nome LIMIT %s OFFSET %s''', (quantidade, offset))

    clientes = cursor.fetchall()
    cursor.close()
    conexao.close()

    clientes_lista = []
    for cliente in clientes:
        clientes_lista.append({
            'nome':cliente[0],
            'cpf':cliente[1],
            'cidade':cliente[2],
            'estado':cliente[3],
            'profissao':cliente[4]
        })
        

#return render_template('grid_completo.html', clientes=clientes_lista, page=page, total_pages=total_pages)
    return render_template('grid_test.html', clientes=clientes_lista, page=page, total_pages=total_pages)




#Gerar relatório em pdf
@aplicativo.route('/gerar_pdf')
def gerar_pdf():
    conexao = conecta_db()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM cliente")
    dados = cursor.fetchall()
    conexao.close()

# Pdf_buffer é uma variável que usa a função da classe BytesIO para armazenar o PDF em memória
    pdf_buffer = BytesIO()


# Cria o canvas para o PDF com um tamanho de página personalizado
    custom_page_size = (800, 500)  # Exemplo de tamanho personalizado
    p = canvas.Canvas(pdf_buffer, pagesize=custom_page_size)
    width, height = custom_page_size

    # Adiciona a imagem de fundo
    #p.drawImage("static/imgs/senac.jpg", 0, 0, width=width, height=height, mask='auto')

    # Estilos
   
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name='TitleStyle', parent=styles['Title'], fontName='Helvetica-bold', fontSize=18, textColor=colors.black, underline=True)
    table_header_style = ParagraphStyle(name='TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, textColor=colors.white)
    table_cell_style = ParagraphStyle(name='TableCell', parent=styles['Normal'], fontName='Helvetica', fontSize=12, textColor=colors.darkblue)

   
    def adicionar_pagina(tabela_dados):
        p.drawString(30, height - 40, "Relatório de Clientes")
        tabela = Table(tabela_dados, colWidths=colWidths)
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Courier')
        ]))
        tabela.wrapOn(p, width - 100, height - 200)
        tabela.drawOn(p, 50, height - 150 - (len(tabela_dados) * 20))

    colWidths = [110, 110, 110, 160, 240]
    max_linhas_por_pagina = (height - 170) // 40  # Aproximadamente quantas linhas cabem na página
    dados_paginados = [dados[i:i + max_linhas_por_pagina] for i in range(0, len(dados), max_linhas_por_pagina)]

    for pagina_dados in dados_paginados:
        tabela_dados = [["Nome", "CPF", "Cidade", "Estado", "Profissão"]] + pagina_dados
        adicionar_pagina(tabela_dados)
        p.showPage()  # Finaliza a página e começa uma nova

    p.save()

    pdf_buffer.seek(0)
    response = make_response(pdf_buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=relatorio.pdf'

    return response






#informações padrão do sistema web

if __name__ == "__main__":
    aplicativo.run(debug=True, port=8085, host='127.0.0.1')

