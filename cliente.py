import cv2 as cv
import socket
import pickle
import struct
import threading

# Configurações de conexão
HOST = '127.0.0.1'  # IP do transmissor
PORT_VIDEO = 5000  # Porta para vídeo
PORT_MSG = 5001  # Porta para mensagens
CHUNK_SIZE = 60000  # Tamanho máximo de cada bloco

# Cria o socket UDP para vídeo
sock_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_video.bind((HOST, PORT_VIDEO))

# Cria o socket UDP para mensagens
sock_msg = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Recepção iniciada. Pressione 'q' para sair.")

def send_messages():
    """Função para enviar mensagens para o transmissor."""
    while True:
        message = input("Digite uma mensagem para enviar: ")
        if message.lower() == "sair":
            break
        sock_msg.sendto(message.encode('utf-8'), (HOST, PORT_MSG))
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    print("Conexão de mensagens encerrada.")

# Thread para envio de mensagens
thread = threading.Thread(target=send_messages, daemon=True)
thread.start()

try:
    frame_data = b""

    while True:
        # Recebe os blocos de vídeo
        chunk, addr = sock_video.recvfrom(CHUNK_SIZE + 2)  # Inclui 2 bytes para o índice
        index = struct.unpack("H", chunk[:2])[0]
        data = chunk[2:]

        # Reconstrói o frame na ordem correta
        if index == 0:
            frame_data = data
        else:
            frame_data += data

        try:

            # Desserializa o frame recebido
            frame = pickle.loads(frame_data)
            frame = cv.imdecode(frame, cv.IMREAD_COLOR)
            cv.imshow("Recebendo transmissão", frame)

            # Exibe o frame
        except:
            pass  # Ignora pacotes incompletos

        # Sai ao pressionar 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cv.destroyAllWindows()
    sock_video.close()
    sock_msg.close()
    print("Recepção encerrada.")
