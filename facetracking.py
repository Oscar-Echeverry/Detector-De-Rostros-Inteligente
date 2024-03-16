import cv2
from cvzone.FaceDetectionModule import FaceDetector
import pyfirmata
import numpy as np

# Configuración de la cámara
cap = cv2.VideoCapture(0)
ancho, alto = 1280, 720
cap.set(3, ancho)
cap.set(4, alto)

if not cap.isOpened():
    print("No se puede acceder a la cámara")
    exit()

# Configuración de Arduino
puerto = "COM7"
placa = pyfirmata.Arduino(puerto)
pinServoX = placa.get_pin('d:9:s') #pin 9 Arduino
pinServoY = placa.get_pin('d:10:s') #pin 10 Arduino

# Inicialización del detector de rostros
detector = FaceDetector()
posicionServo = [90, 90] # posición inicial del servo

while True:
    exito, img = cap.read()
    img, bboxs = detector.findFaces(img, draw=False)

    if bboxs:
        # Obtener las coordenadas
        fx, fy = bboxs[0]["center"]
        pos = [fx, fy]
        # Convertir las coordenadas a grados del servo
        servoX = np.interp(fx, [0, ancho], [0, 180])
        servoY = np.interp(fy, [0, alto], [0, 180])

        # Asegurar que los grados del servo estén dentro del rango permitido
        servoX = max(0, min(180, servoX))
        servoY = max(0, min(180, servoY))

        posicionServo = [servoX, servoY]

        # Dibujar en la imagen
        cv2.circle(img, (fx, fy), 80, (0, 0, 255), 2)
        cv2.putText(img, str(pos), (fx+15, fy-15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2 )
        cv2.line(img, (0, fy), (ancho, fy), (0, 0, 0), 2)  # línea x
        cv2.line(img, (fx, alto), (fx, 0), (0, 0, 0), 2)  # línea y
        cv2.circle(img, (fx, fy), 15, (0, 0, 255), cv2.FILLED)
        cv2.putText(img, "OBJETIVO BLOQUEADO", (850, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3 )

    else:
        cv2.putText(img, "SIN OBJETIVO", (880, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        cv2.circle(img, (640, 360), 80, (0, 0, 255), 2)
        cv2.circle(img, (640, 360), 15, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (0, 360), (ancho, 360), (0, 0, 0), 2)  # línea x
        cv2.line(img, (640, alto), (640, 0), (0, 0, 0), 2)  # línea y

    # Mostrar la posición del servo
    cv2.putText(img, f'Servo X: {int(posicionServo[0])} grados', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.putText(img, f'Servo Y: {int(posicionServo[1])} grados', (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    # Mover los servos
    pinServoX.write(posicionServo[0])
    pinServoY.write(posicionServo[1])

    # Mostrar la imagen
    cv2.imshow("Imagen", img)
    cv2.waitKey(1)
