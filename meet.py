import cv2 as cv
import socket
import pickle
import struct
import threading

# Configurações de conexão
HOST = '10.25.2.157'
PORT = 5000
PORT_VIDEO = 5001
CHUNK_SIZE = 60000
PORT_MSG = 5001

def handle_client(conn, addr):
    print(f'Cliente conectado: {addr}')
    try:
        camera = cv.VideoCapture(0)
        while True:
            # Finaliza se o usuário pressionar 'q'
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            status, frame = camera.read()
            if not status:
                print("Erro ao capturar o frame.")
                pass

            # Codifica o frame em JPEG
            _, buffer = cv.imencode('.jpg', frame)

            # Serializa o frame
            data = pickle.dumps(buffer)
    
            # Envia em blocos menores
            total_chunks = (len(data) // CHUNK_SIZE) + 1
            for i in range(total_chunks):
                start = i * CHUNK_SIZE
                end = start + CHUNK_SIZE
                chunk = data[start:end]
                sock_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                # Envia cada bloco com um índice para controle
                sock_video.sendto(struct.pack("H", i) + chunk, (addr[0], PORT_VIDEO))

            # Exibe o frame localmente
            cv.imshow("Transmitindo", frame)

          
    finally:
        conn.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORT))
sock.listen(5)  # Aguarda até 5 conexões simultâneas

print("Aguardando conexões de clientes...")

while True:
    conn, addr = sock.accept()
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()

