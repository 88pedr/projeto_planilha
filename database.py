import mysql.connector as sql
from dotenv import load_dotenv  #dotenv é a enviroment variable q é basicamente variavies escondidas de se usar
import os #biblioteca q faz a porta entre meu programa e o sistema operacional
#mude o diretorio para o local que vc usa pedro,,,,,
diretorio_atual =r'C:\Users\Allure_Informatica\Desktop\finaceiro\projeto_planilha\senhas.env'
load_dotenv(diretorio_atual) 
db_name = "projeto_planilha" #coloque o nome local do DB aqui pedro...
db_host = "localhost"
db_user = "root"
try:
    senha_forte = os.getenv("senhas")
    conexao = sql.connect(
    host=db_host,       # Endereço do servidor (ex: localhost ou IP)
    user=db_user,     # Nome de usuário do MySQL
    password=senha_forte, #uso de .env
    database=db_name,# Nome do banco de dados
    )   
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tabela (
            id INT AUTO_INCREMENT PRIMARY KEY,
            base VARCHAR(100) NOT NULL,
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
        FOREIGN KEY (carteira_id) REFERENCES tabela(id)
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


