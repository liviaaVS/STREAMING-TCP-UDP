import cv2 as cv
import socket
import pickle
import struct
import threading

CHUNK_SIZE = 60000  # Tamanho dos blocos de dados

# Configurações de conexão
HOST = '10.25.2.157'  # IP do transmissor
HOST_L = '10.25.2.171'  # IP do transmissor (usado para o cliente)
PORT = 5000  # Porta do transmissor
PORT_V = 5001  # Porta de vídeo

# Criação do socket TCP para controle
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Criação do socket UDP para vídeo
sock_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Vincula o socket UDP a uma porta para receber os pacotes
sock_video.bind((HOST_L, PORT_V))  # O cliente precisa estar escutando nesta porta

# Conecta-se ao servidor para obter os dados de vídeo
try:
    frame_data = b""  # Inicializa a variável de dados

    while True:
        # Recebe os blocos de vídeo
        chunk, addr = sock_video.recvfrom(CHUNK_SIZE + 2)  # Inclui 2 bytes para o índice
        index = struct.unpack("H", chunk[:2])[0]  # Desempacota o índice do pacote
        data = chunk[2:]  # O restante é o dado do frame

        # Reconstrói o frame na ordem correta
        if index == 0:
            frame_data = data
        else:
            frame_data += data

        try:
            # Desserializa o frame recebido
            frame = pickle.loads(frame_data)
            frame = cv.imdecode(frame, cv.IMREAD_COLOR)
            cv.imshow("Recebendo transmissão", frame)  # Exibe o frame

        except Exception as e:
            # Ignora pacotes incompletos ou com erro de decodificação
            pass

        # Sai ao pressionar 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cv.destroyAllWindows()
    sock_video.close()
    print("Recepção encerrada.")