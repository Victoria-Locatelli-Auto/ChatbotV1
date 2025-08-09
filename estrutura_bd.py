import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('pizzaria.db')
cursor = conn.cursor()

# Criar tabela de pizzas
cursor.execute('''
CREATE TABLE IF NOT EXISTS pizzas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cod TEXT UNIQUE,
    sabor TEXT,
    p REAL,
    m REAL,
    g REAL
)
''')

# Criar tabela de bordas
cursor.execute('''
CREATE TABLE IF NOT EXISTS bordas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cod TEXT UNIQUE,
    sabor TEXT,
    p REAL,
    m REAL,
    g REAL
)
''')

# Criar tabela de bebidas
cursor.execute('''
CREATE TABLE IF NOT EXISTS bebidas (
    cod TEXT PRIMARY KEY,
    nome TEXT,
    valor REAL
)
''')

# Criar tabela de endereços
cursor.execute('''
CREATE TABLE IF NOT EXISTS enderecos (
    cod TEXT PRIMARY KEY,
    bairro TEXT,
    valor REAL
)
''')

conn.commit()
conn.close()
print("Banco de dados criado com sucesso!")
