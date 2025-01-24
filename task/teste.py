import sqlite3
import funcoes
conn = sqlite3.connect("tasks.sqlite3")
cursor = conn.cursor()

# print(funcoes.insert_tarefa("'titulo','descricao'"))
print(funcoes.select_all())