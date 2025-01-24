import sqlite3

conn = sqlite3.connect("tasks.sqlite3", check_same_thread=False)
cursor = conn.cursor()


# Função para deletar linha
def delete_row(tabela, id):
    cursor.execute(f"DELETE FROM tarefas WHERE id_tarefa = {id}")
    conn.commit()

# Função para selecionar todas as linhas
def select_all():
    cursor.execute(f"SELECT * FROM tarefas")
    return cursor.fetchall()

# Função para selecionar linha por ID
def select_by_id(id):
    cursor.execute(f"SELECT * FROM tarefas WHERE id_tarefa = {id}")
    return cursor.fetchone()

def convert_tasks(tuple_list):
 
    tasks = []
    for t in tuple_list:
        task = {
            "id": str(t[0]),          # Convertendo o ID para string
            "titulo": t[1],
            "descricao": t[2]
        }
        tasks.append(task)
    return tasks

def insert_tarefa(nome, descricao):
                
    print(f"\n tarefas CADASTRADA! \n")    
    insert = (f"INSERT INTO tarefas ( nome, descricao ) VALUES ('{nome}', '{descricao}');")
    print(insert)
    cursor.execute(insert)
    conn.commit()
    
    resposta = {
        "mensage": "Tarefa cadastrada com sucesso!",
        "tasks": convert_tasks( select_all()),
    }
    return resposta
 