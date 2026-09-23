#!/usr/bin/env python3
import cv2
from ultralytics import YOLO

# Inisialisasi model YOLOv8 Pose dan Handphone
pose_model = YOLO("yolov8n-pose.pt")   # Model pose
hp_model   = YOLO("best.pt")           # Model HP hasil training kamu

# Gunakan pipeline GStreamer untuk kamera CSI
gst_pipeline = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), width=1280, height=720, framerate=15/30 ! "
    "nvvidconv flip-method=0 ! "
    "video/x-raw, width=640, height=480, format=BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=BGR ! appsink"
)

cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("❌ Kamera tidak terbuka! Pastikan terhubung dan driver aktif.")
    exit()

print("✅ Kamera aktif, memulai deteksi pose dan handphone...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Tidak dapat membaca frame dari kamera.")
        break

    # Jalankan deteksi pose
    pose_results = pose_model(frame, stream=True, conf=0.5)

    # Jalankan deteksi HP
    hp_results = hp_model(frame, stream=True, conf=0.5)

    # Gabungkan hasil pose dan HP
    for r in pose_results:
        frame = r.plot()

    for r in hp_results:
        frame = r.plot()

    # Tampilkan hasil di layar
    cv2.imshow("Deteksi Pose + HP Real-time", frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
