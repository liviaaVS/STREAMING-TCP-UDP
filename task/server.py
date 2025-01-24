import grpc
from concurrent import futures
import tarefa_pb2
import tarefa_pb2_grpc
import funcoes
import sqlite3

conn = sqlite3.connect("tasks.sqlite3",  check_same_thread=False)
cursor = conn.cursor()

class TaskService(tarefa_pb2_grpc.TaskServiceServicer):
    def CreateTask(self, request, context):
        resposta = funcoes.insert_tarefa(request.nome, request.descricao)
        return resposta.copy()

    # def RemoveTask(self, request, context):
    #     return funcoes.insert_tarefa(request.id)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tarefa_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(), server)
    server.add_insecure_port('localhost:50051')
    print("Server is running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()