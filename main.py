import streamlit as st
import pandas as pd
import mysql.connector as sql
import os
import database as dt
import sqlalchemy as chemy
from dotenv import load_dotenv
#APENAS COISAS DEFINIDAS NO COMEÇO (VARIAVEIS/VALORES)
#-----------------------------------------------------------------------------
db_name = "projeto_planilha" #coloque o nome local do DB aqui pedro...
db_host = "localhost"
db_user = "root"
diretorio_atual =r"C:\Users\Allure_Informatica\Desktop\finaceiro\projeto_planilha\senhas.env"
#ele pega o dir que mandei ler os enviroment e joga na memoria rapida do sistema
load_dotenv(diretorio_atual)
#ele vai ler essa memoria rapido do sistema e tentar pegar a enviroment lançada mais recente
senha_forte = os.getenv("senhas")

#------------------------------------------------------------------------------
url_conexao = f"mysql+mysqlconnector://{dt.db_user}:{dt.senha_forte}@{dt.db_host}:{3306}/{dt.db_name}"
engine = chemy.create_engine(url_conexao)

#FUNÇÕES PARA SER CHAMADA POSTERIOMENTES
#------------------------------------------------------------------------------
def conectar_banco():
    return sql.connect(
        host=db_host,      
        user=db_user,     
        password=senha_forte, 
        database=db_name,
    )
#------------------------------------------------------------------------------
#sistema de navegação de paginas
#------------------------------------------------------------------------------
if "logado"not in st.session_state:
    st.session_state["logado"] = False

if (st.session_state["logado"]==True):
    pg=st.navigation([
        st.Page("pg/ds.py", title="Preferences", url_path="test")],
        position="hidden")#esconde a barra lateral de navegação
    pg.run()    
else:
    #FRONTENT DA PAGINA
    #------------------------------------------------------------------------------
    #pego um parametro do streamlit o titulo 
    st.title("CONTROLE FINANCEIRO")
    #faz uma linha que separa
    st.divider()
    #subtitulo
    st.subheader("LOGIN")

    #sistema de email ainda sem filto e segurança
    email = st.text_input("Usuario/Email")
    senha = st.text_input("Senha", type="password")#type="password" esconde o texto
    #------------------------------------------------------------------------------
    #SISTEMA DE LOGIN
    #------------------------------------------------------------------------------
    #BOTÃO DE ENTRAR
    if st.button("Entrar"):
        if (email=="allure") and (senha=="admin"):
            st.success("Usuario conseguio passar para proxima pagina")
            st.session_state["logado"]=True
            st.rerun()
        else:
            st.write("Senha ou Usuario incorretos")
    @st.dialog("Criar conta")#@ é um decorador que envolve a função abaixo e modifica ela
    def criar_pop_up():
        criar_email = st.text_input
        criar_senha = st.text_input
        query =# parei aqui por causa da trovoada muito forte vou para o note.
    if st.button("Criar Conta"):
        st.popover("zasp")

    #------------------------------------------------------------------------------