import pandas as pd
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('pizzaria.db')

# Carregar o arquivo Excel
xlsx = pd.ExcelFile("pizzaria.xlsx")

# Mapear abas para tabelas
abas_para_tabelas = {
    "pizzas": "pizzas",
    "bordas": "bordas",
    "bebidas": "bebidas",
    "enderecos": "enderecos"
}

# Loop para popular as tabelas
for aba, tabela in abas_para_tabelas.items():
    if aba in xlsx.sheet_names:
        df = pd.read_excel(xlsx, sheet_name=aba)

        # Remover coluna ID se existir (autogerada no banco)
        if "ID" in df.columns:
            df = df.drop(columns=["ID"])

        # Inserir os dados no banco
        df.to_sql(tabela, conn, if_exists="append", index=False)
        print(f"✔ Tabela '{tabela}' populada com sucesso!")
    else:
        print(f"⚠ Aba '{aba}' não encontrada no arquivo.")

conn.close()
