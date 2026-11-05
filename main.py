import streamlit as st
import pandas as pd
import mysql.connector as sql
import os
from dotenv import load_dotenv as ld

ld()
senha_forte = os.getenv("senhas")
def conectar_banco():
    return sql.connect(
        host="localhost",      
        user="root",     
        password=senha_forte, 
        database="planilha_project",
    )

#pego um parametro do streamlit o titulo 
st.title("Controle Financeiro")
#
st.divider()

st.subheader("Criar nova planilha")

#form de formulario, basicamente vai criar um formulario basico
with st.form("form_carteira"):
    nome_planilha = st.text_input("Nome da planilha ou mes")
    tipo_planilha = st.selectbox("Categoria",["Pessoal","Empresarial"])
    salvar_planilha = st.form_submit_button("Salvar dados")
    if salvar_planilha:
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            inserir_sql = f"INSERT INTO base (base,tipo) VALUES ('{nome_planilha}','{tipo_planilha}')"
            cursor.execute(inserir_sql)
            conexao.commit()
            st.success(f"Planilha {nome_planilha} criada com sucesso")
        except Exception as erro:
            st.error(f"Erro ao salvar:{erro}")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()