import mysql.connector as sql
from dotenv import load_dotenv  #dotenv é a enviroment variable q é basicamente variavies escondidas de se usar
import os #biblioteca q faz a porta entre meu programa e o sistema operacional
#mude o diretorio para o local que vc usa pedro,,,,,

#FUNÇÃO_INICIAL DE CONEXÃO DE DADOS
diretorio_atual ="/home/pedro_peixoto/Área de trabalho/projetos/projeto_planilha/senhas.env"
load_dotenv(diretorio_atual) 
db_name = "projeto_planilha" #coloque o nome local do DB aqui pedro...
db_host = "localhost"
db_user = "root"
senha_forte = os.getenv("senhas")
#----------------------------------------------------------------------------
def conectar_banco1():
    return sql.connect(
        host=db_host,       # Endereço do servidor (ex: localhost ou IP)
        user=db_user,     # Nome de usuário do MySQL
        password=senha_forte, #uso de .env
        database=db_name,   # Nome do banco de dados
    )
#----------------------------------------------------------------------------


#CRIAR TABELAS
#----------------------------------------------------------------------------
try:
    conexao = conectar_banco1()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fornecedores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(30) NOT NULL,
            saldo FLOAT NOT NULL,
            data DATE NOT NULL,
            pago BOOLEAN
        )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(30) NOT NULL,
        saldo FLOAT,
        data DATE NOT NULL,
        pago BOOLEAN
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS debitos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(30) NOT NULL,
    saldo FLOAT NOT NULL,
    data DATE NOT NULL,
    pago BOOLEAN
    )
    """)
#----------------------------------------------------------------------------
    conexao.commit()
    print("Tabela verificada/criada com sucesso. Fim do código!")
except sql.Error as error:
    print(f"Deu erro man na {error}")
except Exception as erro_geral:
    print(f"Deu erro geral na {erro_geral}")
finally:
    if "conexao" in locals() and conexao.is_connected():
        cursor.close()
        conexao.close()
#cursor = conexao.cursor()


