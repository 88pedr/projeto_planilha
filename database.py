import mysql.connector as sql
import dotenv as dt #dotenv é a enviroment variable q é basicamente variavies escondidas de se usar
import os #biblioteca q faz a porta entre meu programa e o sistema operacional
dt.load_dotenv()
try:
    senha_forte = os.getenv("senhas")
    conexao = sql.connect(
    host="localhost",       # Endereço do servidor (ex: localhost ou IP)
    user="root",     # Nome de usuário do MySQL
    password=senha_forte, #uso de .env
    database="planilha_project",# Nome do banco de dados
    )   
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS base (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tipo VARCHAR(100) NOT NULL
        )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        carteira_id INT NOT NULL,
        data DATE NOT NULL,
        descricao VARCHAR(255),
        valor DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (carteira_id) REFERENCES base(id)
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


