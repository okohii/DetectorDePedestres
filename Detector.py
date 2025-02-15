from ultralytics import YOLO
import cv2
import numpy as np

print(f'OpenCV Version: {cv2.__version__}')


modelo = YOLO('yolov8l.pt')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao abrir a câmera!")
    exit()


threshold = 0.5 

cores_classes = {}

def gerar_cor_unica():
    return tuple(np.random.randint(0, 256, 3).tolist())

while True:
    ret, frame = cap.read()

    if not ret:
        print("Falha ao capturar imagem")
        break

    resultados = modelo(frame)

    detecções_filtradas = [det for det in resultados[0].boxes if det.conf > threshold]

    for det in detecções_filtradas:
        x1, y1, x2, y2 = det.xyxy[0].cpu().numpy()
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        
        label = modelo.names[int(det.cls)]

        if label not in cores_classes:
            cores_classes[label] = gerar_cor_unica()

        cor = cores_classes[label]

        cv2.rectangle(frame, (x1, y1), (x2, y2), cor, 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, cor, 2)

    cv2.imshow("Detecção em Tempo Real", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
