import cv2 as cv
import socket
import pickle
import struct
import threading

# Configurações de conexão
HOST = '127.0.0.1'
PORT_VIDEO = 5000
PORT_MSG = 5001
CHUNK_SIZE = 60000

# Cria os sockets
sock_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_msg = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_msg.bind((HOST, PORT_MSG))

# Inicializa a captura da câmera
camera = cv.VideoCapture(0)

# Variável para armazenar a mensagem atual
current_message = ""

def receive_messages():
    """Função para receber mensagens do cliente."""
    global current_message
    while True:
        data, addr = sock_msg.recvfrom(1024)  # Tamanho máximo de uma mensagem
        current_message = data.decode('utf-8')
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

# Thread para receber mensagens
thread = threading.Thread(target=receive_messages, daemon=True)
thread.start()

print("Transmissão iniciada. Pressione 'q' para sair.")

try:
    while True:
        # Captura o frame
        status, frame = camera.read()
        if not status:
            print("Erro ao capturar o frame.")
            break

        # Adiciona a mensagem ao frame
        if current_message:
            cv.putText(frame, current_message, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)

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

            # Envia cada bloco com um índice para controle
            sock_video.sendto(struct.pack("H", i) + chunk, (HOST, PORT_VIDEO))

        # Exibe o frame localmente
        cv.imshow("Transmitindo", frame)

        # Finaliza se o usuário pressionar 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    camera.release()
    cv.destroyAllWindows()
    sock_video.close()
    sock_msg.close()
    print("Transmissão encerrada.")
