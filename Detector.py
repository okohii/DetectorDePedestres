from ultralytics import YOLO
import cv2
import numpy as np
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Usando dispositivo: {device}')

modelo = YOLO('yolov8l.pt').to(device)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao abrir a câmera!")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

threshold = 0.4
cores_classes = {}

def gerar_cor_unica():
    return tuple(np.random.randint(0, 256, 3).tolist())

def processar_frame(frame):
    frame_resized = cv2.resize(frame, (640, 640))
    frame_tensor = torch.from_numpy(frame_resized).permute(2, 0, 1).float().unsqueeze(0) / 255.0
    frame_tensor = frame_tensor.to(device)
    return frame_tensor

def desenhar_deteccoes(frame, detecções_filtradas):
    height, width, _ = frame.shape
    scale_x = width / 640
    scale_y = height / 640
    for det in detecções_filtradas:
        x1, y1, x2, y2 = det.xyxy[0].cpu().numpy()
        x1, y1, x2, y2 = int(x1 * scale_x), int(y1 * scale_y), int(x2 * scale_x), int(y2 * scale_y)
        
        label = modelo.names[int(det.cls)]

        if label not in cores_classes:
            cores_classes[label] = gerar_cor_unica()

        cor = cores_classes[label]

        cv2.rectangle(frame, (x1, y1), (x2, y2), cor, 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, cor, 2)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Falha ao capturar imagem")
        break

    frame_tensor = processar_frame(frame)
    resultados = modelo(frame_tensor)
    detecções_filtradas = [det for det in resultados[0].boxes if det.conf > threshold]
    desenhar_deteccoes(frame, detecções_filtradas)

    cv2.imshow("Detector em tempo real", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()