from ultralytics import YOLO
import cv2

print(f'OpenCV Version: {cv2.__version__}')

modelo = YOLO('yolov8n.pt')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao abrir a câmera!")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Falha ao capturar imagem")
        break

    resultados = modelo(frame)

    modelo.predict(source='0', show=True);

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
