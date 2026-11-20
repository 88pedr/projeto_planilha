import streamlit as st
import pandas as pd
import mysql.connector as sql
import os
import database as dt
import sqlalchemy as chemy
import email_validator as ev
from dotenv import load_dotenv
#APENAS COISAS DEFINIDAS NO COMEÇO (VARIAVEIS/VALORES)
#------------------------------------------------------------------------------
url_conexao = f"mysql+mysqlconnector://{dt.db_user}:{dt.senha_forte}@{dt.db_host}:{3306}/{dt.db_name}"
engine = chemy.create_engine(url_conexao)

#FUNÇÕES PARA SER CHAMADA POSTERIOMENTES
#------------------------------------------------------------------------------
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
        criar_email = st.text_input("EMAIL")
        criar_senha = st.text_input("SENHA")

        if st.button("Confirma"):
            try:
                with engine.begin() as conn:
                    email_info = ev.validate_email(criar_email,check_deliverability=False)
                    criar_email=email_info.normalized
                    query_email =f"""
                    INSERT INTO :table (:column)
                    VALUES (:values)
                    """
                    conn.execute(chemy.text(query_email),{
                        ":table": "user",
                        ":column":"email",
                        ":values":criar_email
                        })
                    st.success("DEU BOM")
                    st.rerun()
            except ev.EmailNotValidError as e:
                st.write("DEU ERRO CHEFE")
    if st.button("Cria conta"):
        criar_pop_up()
    #------------------------------------------------------------------------------
    #def chamar_sql(test1,test2):
    #            query =f"""SELECT :email FROM :user WHERE is_active"""
    #            dados = pd.read_sql(chemy.text(query), con=engine , params= test1,test2)
     #       emails = chamar_sql("email","user")
     #       senhas = chamar_sql("password","user")
     #       chamar_sql()