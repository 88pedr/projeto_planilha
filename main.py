import streamlit as st
import pandas as pd
import mysql.connector as sql
import os
from dotenv import load_dotenv
db_name = "projeto_planilha" #coloque o nome local do DB aqui pedro...
db_host = "localhost"
db_user = "root"
diretorio_atual =r'C:\Users\Allure_Informatica\Desktop\finaceiro\projeto_planilha\senhas.env'
#ele pega o dir que mandei ler os enviroment e joga na memoria rapida do sistema
load_dotenv(diretorio_atual)
#ele vai ler essa memoria rapido do sistema e tentar pegar a enviroment lançada mais recente
senha_forte = os.getenv("senhas")
def conectar_banco():
    return sql.connect(
        host=db_host,      
        user=db_user,     
        password=senha_forte, 
        database=db_name,
    )
if "logado"not in st.session_state:
    st.session_state["logado"] = False
if not st.session_state["logado"]:
    pg =st.Page #pare nesta parte 
test_page = st.Page("pages/test.py", icon="🔒")
#pego um parametro do streamlit o titulo 
st.title("CONTROLE FINANCEIRO (PEIXOTO)")
#
st.divider()

st.subheader("LOGIN")


email = st.text_input("Usuario/Email")
senha = st.text_input("Senha")
if st.button("Entrar"):
    if ("email==test@gmail.com") and (senha=="admin"):
        st.success("Usuario conseguio passar para proxima pagina")
        st.session_state["logado"]=True
        pg = st.navigation([test_page])
        pg.run()
    else:
        st.write("Senha ou Usuario incorretos")

"""
#form de formulario, basicamente vai criar um formulario basico
with st.form("form_carteira"):
    nome_planilha = st.text_input("Nome da planilha ou mes")
    tipo_planilha = st.selectbox("Categoria",["Pessoal","Empresarial"])
    salvar_planilha = st.form_submit_button("Salvar dados")
    if salvar_planilha:
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            inserir_sql = f"INSERT INTO planilha (base,tipo) VALUES ('{nome_planilha}','{tipo_planilha}')"
            cursor.execute(inserir_sql)
            conexao.commit()
            st.success(f"Planilha {nome_planilha} criada com sucesso")
        except Exception as erro:
            st.error(f"Erro ao salvar:{erro}")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()
"""