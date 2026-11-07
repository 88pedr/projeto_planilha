import streamlit as st
import pandas as pd
from database.py import conectar_banco

conexao = conectar_banco()
usuario = "Allure"
st.title(f"BEM VINDO {usuario}")
st.divider()


fornecedor,cliente,dividas = st.tabs(["FORNECEDOR", "CLIENTES","DIVIDAS"])

fornecedor.write("-------------FORNEDORES-------------")

df_vazio = pd.DataFrame(columns=["NOME", "DIVIDA"])
# Cria a planilha interativa na tela
tabela_editada = st.data_editor(
    df_vazio, 
    num_rows="dynamic", # Isso faz aparecer o botão de "adicionar linha" embaixo!
    use_container_width=True # Estica para caber na tela
)
