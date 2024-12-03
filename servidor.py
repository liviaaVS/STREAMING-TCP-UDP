import socket
import pygame

HOST = '127.0.0.1'
PORT = 5000

# Cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

print('Aguardando conexão de um cliente')

try:
    conn, ender = s.accept()
    print('Conectado em', ender)
    
    while True:
        data = conn.recv(1024)
        if not data:
            print('Fechando a conexão')
            conn.close()
            break
        
        print('Recebido: ', repr(data))
        conn.sendall(data)
except KeyboardInterrupt:
    print('\nServidor interrompido pelo usuário.')
finally:
    s.close()
    print('Socket fechado. Servidor encerrado.')
