import mysql.connector as sql
from dotenv import load_dotenv  # Carrega variáveis de ambiente de um arquivo .env (se existir)
import os  # Acesso às variáveis de ambiente do sistema

# Carrega .env do diretório atual/projeto quando disponível
load_dotenv()

# Configurações do banco via variáveis de ambiente (com padrões para desenvolvimento local)
db_name = os.getenv("DATABASE", "projeto_planilha")
db_host = os.getenv("HOST", "localhost")
db_user = os.getenv("DB_USER", os.getenv("USER", "root"))
senha_forte = os.getenv("SENHAS") or os.getenv("senhas")


# ----------------------------------------------------------------------------
def conectar_banco1():
    return sql.connect(
        host=db_host,       # Endereço do servidor (ex: localhost ou IP)
        user=db_user,     # Nome de usuário do MySQL
        password=senha_forte, #uso de .env
        database=db_name   # Nome do banco de dados
    )
#----------------------------------------------------------------------------


#CRIAR TABELAS
#----------------------------------------------------------------------------
def criar_tabela():
    conexao=None
    try:
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
#----------------------------------------------------------------------------

