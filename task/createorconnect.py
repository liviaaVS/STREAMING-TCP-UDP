import sqlite3

# Conecta ao banco de dados (cria um novo se não existir)
conn = sqlite3.connect("tasks.sqlite3")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR NOT NULL,
    descricao VARCHAR NOT NULL

); """)
