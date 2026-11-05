import mysql.connector as sql
import streamlit as st
import pandas as pd
import dotenv as dt #dotenv é a enviroment variable q é basicamente variavies escondidas de se usar
import os #biblioteca q faz a porta entre meu programa e o sistema operacional
dt.load_dotenv()
try:
    senha_forte = os.getenv("senhas")
    conexao = sql.connect(
    host="localhost",       # Endereço do servidor (ex: localhost ou IP)
    user="root",     # Nome de usuário do MySQL
    password="senha_forte",   # Não sei se é o ideal 
    #deixar senha no codigo... sempre penso q não mas n sei resolver
    database="planilha_project",# Nome do banco de dados
    )   
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carteiras (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome_projeto VARCHAR(100) NOT NULL,
            tipo VARCHAR(50) NOT NULL
        )
    """)
    conexao.commit()
    print("Tabela verificada/criada com sucesso. Fim do código!")
except sql.Error as error:
    print(f"Deu erro man na {error}")
except sql.Error as erro_geral:
    print(f"Deu erro man na {erro_geral}")
finally:
    if "conexão" in locals() and conexao.is_connected():
        cursor.close()
        conexao.close()
#cursor = conexao.cursor()


