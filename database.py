import mysql.connector as sql
from dotenv import load_dotenv  # Carrega variáveis de ambiente de um arquivo .env (se existir)
import os  # Acesso às variáveis de ambiente do sistema
from pathlib import Path

# carrega .env do diretório atual melhor do que hardcoded que nem antes
env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env_path, override=True)

# Se existir /.dockerenv, está dentro do container; caso contrário, está rodando localmente no PC
if os.path.exists("/.dockerenv"):
    db_host = os.getenv("HOST", "mysql")
else:
    db_host = "localhost"


db_name = os.getenv("DATABASE", "projeto_planilha")
db_host = os.getenv("HOST", "localhost")
db_user = os.getenv("DB_USER", os.getenv("USER", "root"))
senha_forte = os.getenv("SENHAS") or os.getenv("senhas")


# ----------------------------------------------------------------------------
def conectar_servidor():
    """Conecta ao servidor MySQL sem selecionar um banco específico."""
    return sql.connect(
        host=db_host,
        user=db_user,
        password=senha_forte
    )
def conectar_banco1():
    return sql.connect(
        host=db_host,       # endereço do servidor (ex: localhost ou IP)
        user=db_user,     # nome de usuário do MySQL
        password=senha_forte, #uso de .env
        database=db_name   # nome do banco de dados
    )
#----------------------------------------------------------------------------

def criar_database():
    conexao = None
    cursor = None
    try:
        conexao = conectar_servidor()
        cursor = conexao.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        conexao.commit()
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()
#CRIAR TABELAS
#----------------------------------------------------------------------------
def criar_tabela():
    conexao=None
    
    try:
        criar_database()
        conexao = conectar_banco1()
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fornecedores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(30) NOT NULL,
                saldo FLOAT NOT NULL,
                data DATE NOT NULL,
                mes_referencia VARCHAR(10),
                pago BOOLEAN
            )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(30) NOT NULL,
            saldo FLOAT,
            data DATE NOT NULL,
            mes_referencia VARCHAR(10),
            pago BOOLEAN
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS debitos(
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(30) NOT NULL,
        saldo FLOAT NOT NULL,
        data DATE NOT NULL,
        mes_referencia VARCHAR(10),
        pago BOOLEAN
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user(
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255),
        pawssword VARCHAR(255),
        is_activate BOOLEAN,
        data DATE DEFAULT (CURRET_DATE)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data(
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(30),
        phone VARCHAR(20),
        foto_url VARCHAR(255)
        )""")
        cursor.execute("""
        ALTER""")
        conexao.commit()
        print("Tabela verificada/criada com sucesso. Fim do código!")
    except sql.Error as error:
        print(f"Deu erro man na {error}")
    except Exception as erro_geral:
        print(f"Deu erro geral na {erro_geral}")
    finally:
        if conexao in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
    #cursor = conexao.cursor()
#----------------------------------------------------------------------------
if __name__ == "__main__":
    criar_tabela()