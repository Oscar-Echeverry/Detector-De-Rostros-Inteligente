import cv2
import numpy as np
import time

# Cargamos el clasificador de rostros
clasificadorRostros  = cv2.CascadeClassifier("C:/Users/echev/OneDrive/Escritorio/Proyecto uno/Face-Detection/haarcascade_frontalface_default.xml")

# Iniciamos la captura de video
videoCam = cv2.VideoCapture(0)

if not videoCam.isOpened():
    print("No se puede acceder a la cámara")
    exit()

while True:
    # Leemos un frame del video
    ret, frame = videoCam.read()

    if ret:
        # Convertimos el frame a escala de grises
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detectamos los rostros en el frame
        rostros = clasificadorRostros.detectMultiScale(gris, scaleFactor = 1.3, minNeighbors = 2)

        # Dibujamos un rectángulo alrededor de cada rostro detectado
        for (x, y, w, h) in rostros:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Mostramos el número de rostros detectados
        texto = "Numero de rostros detectados: " + str(len(rostros))
        cv2.putText(frame, texto, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)

        # Mostramos el resultado
        cv2.imshow("Resultado", frame)
        
        # Si se presiona la tecla 'q', salimos del bucle
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Liberamos los recursos y cerramos las ventanas
videoCam.release()
cv2.destroyAllWindows()
