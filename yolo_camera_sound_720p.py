#!/usr/bin/env python3
import cv2
from ultralytics import YOLO
import pygame

# Inisialisasi pygame mixer
pygame.mixer.init()
peringatan_sound = pygame.mixer.Sound("/home/thyaa/Documents/peringatan_hp.wav")

# Load model YOLO
model = YOLO("/home/thyaa/Documents/best.pt")

# Pipeline kamera CSI, resolusi 1280x720, 30fps
gst_str = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM),width=1280,height=720,framerate=30/1 ! "
    "nvvidconv flip-method=0 ! "
    "video/x-raw, format=BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=BGR ! "
    "appsink drop=true sync=false"
)

cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
if not cap.isOpened():
    print("❌ Gagal buka kamera.")
    exit(1)
    
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

suara_sedang_bermain = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Gagal ambil frame.")
        break

    # Prediksi YOLOv8
    results = model.predict(source=frame, conf=0.4, stream=True)

    handphone_terdeteksi = False
    annotated = frame.copy()  # default kalau gak ada deteksi

    for r in results:
        for cls in r.boxes.cls:
            if int(cls) == 0:  # ganti "0" sesuai class HP di modelmu
                handphone_terdeteksi = True
        annotated = r.plot()

    # Mainkan / hentikan suara
    if handphone_terdeteksi:
        if not suara_sedang_bermain:
            peringatan_sound.play(loops=-1)  # looping terus
            suara_sedang_bermain = True
    else:
        if suara_sedang_bermain:
            peringatan_sound.stop()
            suara_sedang_bermain = False

    cv2.imshow("YOLOv8 Realtime - 720p", annotated)

    if cv2.waitKey(1) == 27:  # tekan ESC untuk keluar
        break

cap.release()
cv2.destroyAllWindows()
