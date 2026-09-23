import obd
import time
import pygame

pygame.mixer.init()

peringatan1 = "peringatan1.wav"   # >60
peringatan2 = "peringatan2.wav"   # >80
peringatan3 = "peringatan3.wav"   # >120 (looping)

def play_once(file):
    sound = pygame.mixer.Sound(file)
    sound.play()
    time.sleep(sound.get_length())

def play_loop(file):
    sound = pygame.mixer.Sound(file)
    sound.play(loops=-1)
    return sound

connection = obd.OBD(portstr="/dev/ttyACM0", fast=False)  # ganti sesuai port

if connection.is_connected():
    print("✅ OBD terhubung")
else:
    print("❌ Gagal terhubung ke OBD")
    exit()

cmd = obd.commands.SPEED

looping_sound = None
last_zone = None   # nyimpen status terakhir

try:
    while True:
        response = connection.query(cmd)
        if not response.is_null():
            kecepatan = response.value.to("km/h").magnitude
            print(f"Kecepatan: {kecepatan:.1f} km/h")

            # tentukan zona
            if 60 < kecepatan <= 80:
                zone = "60"
            elif 80 < kecepatan <= 120:
                zone = "80"
            elif kecepatan > 120:
                zone = "120"
            else:
                zone = "normal"

            # cek perubahan zona
            if zone != last_zone:
                if zone == "60":
                    play_once(peringatan1)

                elif zone == "80":
                    for _ in range(3):
                        play_once(peringatan2)

                elif zone == "120":
                    if looping_sound is None:
                        looping_sound = play_loop(peringatan3)

                elif zone == "normal":
                    if looping_sound is not None:
                        looping_sound.stop()
                        looping_sound = None

                last_zone = zone  # update zona terakhir

        else:
            print("⚠️ Data kecepatan tidak tersedia")

        time.sleep(1)

except KeyboardInterrupt:
    print("\n⏹️ Pembacaan dihentikan")
    if looping_sound is not None:
        looping_sound.stop()
    connection.close()
