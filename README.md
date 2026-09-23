# Intelligent Driver Distraction & Vehicle Speed Monitoring System
Real-time Edge AI system developed using NVIDIA Jetson Nano, Python, and YOLO to detect driver mobile-phone distraction and monitor vehicle speed.

Tech Stack: Python • YOLO • NVIDIA Jetson Nano • Computer Vision • OBD-II • Embedded Systems

## Project Overview

This project is an edge AI-based road safety monitoring system designed
to detect driver mobile-phone distraction and monitor vehicle speed
in real time.

The system combines computer vision with vehicle data obtained through
OBD-II and runs on NVIDIA Jetson Nano.

## Features

- Real-time driver distraction detection
- Vehicle speed monitoring using OBD-II
- Audio feedback during detected events
- Real-time camera processing
- Edge AI deployment using NVIDIA Jetson Nano

## Project Components

### 1. Driver Distraction Detection
`yolo_camera_sound_720p.py`

Detects driver mobile-phone usage using YOLO and processes camera
input in real time.

### 2. Pose Detection
`pose_realtime.py`

Processes real-time human pose information for driver monitoring.

### 3. Vehicle Speed Monitoring
`kecepatan_obd_looping_suara.py`

Reads vehicle speed data through OBD-II and provides audio feedback
based on the monitoring process.

## Project Documentation

### Poster
[SIBOTAR Poster]

### Testing Video
[Testing Video of SIBOTAR]
