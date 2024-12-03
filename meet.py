import pygame
import pygame.camera
import cv2 as cv
 
pygame.init()
pygame.camera.init()

# Define a largura e altura da janela
WIDTH, HEIGHT = 640, 480
camera = cv.VideoCapture(0)
rodando = True

while rodando:

    status, frame = camera.read()

    if not status or cv.waitKey(1) & 0xff == ord('q'):
        rodando = False

    cv.imshow("Camera", frame)
    

