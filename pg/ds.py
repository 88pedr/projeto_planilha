#DEFINIÇÕES INICIAIS
#-------------------------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import os
import sys
#para conseguir importa e transporta os dados de maneira eficiente e segura
from sqlalchemy import create_engine, text
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#ele pega a pasta que quero para inserir no codigo e com insert mando ele preocurar nesta pasta primeiro antes de tudo
sys.path.insert(0,r"C:\Users\Allure_Informatica\Desktop\finaceiro\projeto_planilha")
import database as dt
tabela1 = "fornecedores"#altere de acordo com o nome do banco de dados
tabela2 = "clientes"
tabela3 = "debitos"
url_conexao = f"mysql+mysqlconnector://{dt.db_user}:{dt.senha_forte}@{dt.db_host}:{3306}/{dt.db_name}"
engine = create_engine(url_conexao)
conexao = dt.conectar_banco1()
cursor = conexao.cursor()
usuario = "ALLURE"
st.title(f"BEM VINDO {usuario}")
st.divider()
#-------------------------------------------------------------------------------------------------------------------


#FUNÇÕES DE CRIAR GRAFICO, MANIPULAR DB, AVANÇAR DIVIDAS, E DASHBORD
#-------------------------------------------------------------------------------------------------------------------
#codigo que gera as tabelas para inserir os dados/manipular
#-------------------------------------------------------------------------------------------------------------------
def criar_grafico(nome_db,saldo_db,pago_db,nome,saldo,pago,aba, mes_ref,data=False):
    colunas = ["id",nome_db,saldo_db,pago_db]
    #fiz isso por causa da duvida de se em alguns colocava data ou não *DESCARTAVEL*
    if data:
        colunas.insert(2,"data")
    #sql n aceita lista, ent o join vai colocar entre cada espaço uma , deixando o texto limpo
    colunas_sql = ", ".join(colunas)
    #text() usa para q o sqlalchemy pegue os placeholder dinamicos e os transformes em comuns %(nome)s
    query=f"SELECT {colunas_sql} FROM {aba} WHERE mes_referencia = :mes"
    #pega o valor da barra lateral e o injeta db de forma isolada, falha de segurança..sql injection
    df_planilha = pd.read_sql(text(query), con=engine, params={"mes": mes_ref})
    #preferia isso aplicado direto mas por causa do data n sera possivel
    configs = {
        "id": None,#para o id n aparecer na tabela
        nome_db:st.column_config.TextColumn(label=nome),
        saldo_db:st.column_config.NumberColumn(label=saldo,format="R$ %.2f", min_value=0),#apenas duas casa decimais
        pago_db: st.column_config.CheckboxColumn(pago, default=False)
    }
    if data:
        configs["data"] = st.column_config.DateColumn("Data")

    # cria a planilha na tela
    tabela_editada = st.data_editor(
        df_planilha, 
        num_rows="dynamic",
        use_container_width=True,# estica para caber na tela
        hide_index=True,
        column_config=configs
    )
    return tabela_editada
#-------------------------------------------------------------------------------------------------------------------

#manipulador do DB
#-------------------------------------------------------------------------------------------------------------------
def gerenciador_db(planilha_tela,tab,nome,saldo,pago,data,id,mes_ref):
    if st.button("Salvar banco de dados",key=f"botao_salvar{tab}"):#para diferencias os nomes e nao causar duplicatas e o streamlit dar error
        try:
            with engine.begin() as conn:
                id_db=pd.read_sql(text(f"SELECT id FROM {tab} WHERE mes_referencia = :mes"),con=engine, params={"mes":mes_ref})
                ls_id_db = id_db["id"].tolist()#
                ls_id_planilha = planilha_tela["id"].dropna().tolist()#dropna() remove valores null
                id_apagar =[id_delete for id_delete in ls_id_db if id_delete not in ls_id_planilha]
                for deletar in id_apagar:
                    query_delete =f"""DELETE FROM {tab} WHERE id = :id"""
                    conn.execute(text(query_delete),{"id": deletar})

                for indice,linha in planilha_tela.iterrows():#nao gosto da ideia do iterrows pelas minhas pesquisas ele é bem mal otimizado
                    if pd.isna(linha["id"]):
                        query = f"""INSERT INTO {tab} ({nome}, {saldo}, {pago},{data},mes_referencia) VALUES (:nome, :saldo, :pago, :data, :mes)"""#gostaria de usar %(nome)s pq lembra a linguagem C que estou estudando
                        conn.execute(text(query),{"nome": linha["nome"], "saldo": linha["saldo"], "pago": linha["pago"], "data": linha["data"],"mes": mes_ref})
                    else:
                        query = f"""UPDATE {tab} SET {nome} = :nome, {saldo} = :saldo, {pago} = :pago, {data} = :data WHERE {id} = :id """
                        conn.execute(text(query),{
                            "nome": linha["nome"], 
                            "saldo": linha["saldo"], 
                            "pago": linha["pago"], 
                            "id": linha["id"],
                            "data":linha["data"]
                        })
            st.success("Dados salvos e atualizados!")
            st.rerun()
        except dt.sql.Error as error:
            print(f"Deu erro man na {error}")
            st.write("O banco de dados falhou")
        except Exception as erro_geral:
            print(f"Deu erro geral na {erro_geral}")
            st.write("Por favor preencha corretamente...")

#CONSEGUIR PÁSSAR AS DIVIDAS PARA O MES QUE VÉM
def rolar_dividas(mes_atual, mes_seguinte):
    # colocando dois botões, podemos prevenir o clique acidental com um st.warning
    if st.sidebar.button(f"Rolagem de {mes_atual} para  {mes_seguinte}"):
        with engine.begin() as conn:
            # lista para varrer preocurando
            tabelas = ["fornecedores", "clientes", "debitos"]
            
            for tab in tabelas:
                # puxa quem n tem 1 na aba pagos de cada table
                query_busca = text(f"""
                    SELECT nome, saldo, data 
                    FROM {tab} 
                    WHERE mes_referencia = :mes_atual AND pago = 0
                """)
                adiante = pd.read_sql(query_busca, con=conn, params={"mes_atual": mes_atual})
                
                # Se houver dívidas para rolar nesta tabela
                if not adiante.empty:
                    query_insere = text(f"""
                        INSERT INTO {tab} (nome, saldo, pago, data, mes_referencia)
                        VALUES (:nome, :saldo, 0, :data, :mes_seguinte)
                    """)
                    for indice, linha in adiante.iterrows():
                        conn.execute(query_insere, {
                            "nome": linha["nome"], "saldo": linha["saldo"],
                            "data": linha.get("data", None), "mes_seguinte": mes_seguinte
                        })
                
        st.sidebar.success(f"Dívidas de {mes_atual} roladas para {mes_seguinte} com sucesso!")

#-------------------------------------------------------------------------------------------------------------
def painel_dashboard(mes_atual):
    st.subheader(f"Resumo Financeiro - {mes_atual}")
    
    query_receitas = text("SELECT COALESCE(SUM(saldo), 0) FROM clientes WHERE mes_referencia = :mes AND pago = 1")
    query_fornecedores = text("SELECT COALESCE(SUM(saldo), 0) FROM fornecedores WHERE mes_referencia = :mes AND pago = 1")
    query_debitos = text("SELECT COALESCE(SUM(saldo), 0) FROM debitos WHERE mes_referencia = :mes AND pago = 1")
    
    with engine.connect() as conn:
        total_receita = conn.execute(query_receitas, {"mes": mes_atual}).scalar()
        total_custo_fornecedor = conn.execute(query_fornecedores, {"mes": mes_atual}).scalar()
        total_custo_debitos = conn.execute(query_debitos, {"mes": mes_atual}).scalar()
    
    total_despesas = total_custo_fornecedor + total_custo_debitos
    lucro = total_receita - total_despesas
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Receitas (Entradas)", f"R$ {total_receita:,.2f}")
    col2.metric("Despesas (Saídas)", f"R$ {total_despesas:,.2f}")
    
    cor_lucro = "normal" if lucro >= 0 else "inverse"
    col3.metric("Lucro Líquido", f"R$ {lucro:,.2f}")
    st.divider()
#-------------------------------------------------------------------------------------------------------------

st.sidebar.title("Filtro de Tempo")
meses = ["10/2026", "11/2026", "12/2026", "01/2027"]
mes_atual = st.sidebar.selectbox("Mês de Referência:", meses)

# identificar o mes que precisa passar
indice_mes_atual = meses.index(mes_atual)
if indice_mes_atual < len(meses) - 1:
    mes_seguinte = meses[indice_mes_atual + 1]
    rolar_dividas(mes_atual, mes_seguinte)
else:
    st.sidebar.warning("Cadastre novos meses na lista para habilitar a rolagem.")

#chama o Dashboard visual
painel_dashboard(mes_atual)
#-----------------------------------------------------------------------------------------------
fornecedor,cliente,dividas = st.tabs(["FORNECEDOR", "CLIENTES","DIVIDAS"])
with fornecedor:
    tb =criar_grafico("nome","saldo","pago","FORNECEDOR","DEBITO","PAGO?","fornecedores",mes_atual,True)
    gerenciador_db(tb,"fornecedores","nome","saldo","pago","data","id",mes_atual)
with cliente:
    tb =criar_grafico("nome","saldo","pago","CLIENTES","DEBITO","PAGO?","clientes",mes_atual,True)
    gerenciador_db(tb,"clientes","nome","saldo","pago","data","id",mes_atual)
with dividas:
    tb =criar_grafico("nome","saldo","pago","CONTAS","DIVIDA","PAGO?","debitos",mes_atual,True)
    gerenciador_db(tb,"debitos","nome","saldo","pago","data","id",mes_atual)
#-------------------------------------------------------------------------------------------------------------