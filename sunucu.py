import socket
import os

HOST = "127.0.0.1"
PORT = 5000

def sunucuyuCalistir():
    sunucu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sunucu.bind((HOST, PORT))
    sunucu.listen(1)
    print("[SUNUCU] Dinleniyor...")

    conn, addr = sunucu.accept()
    print(f"[SUNUCU] {addr} bağlandı!")

    while True:
        # İlk paket her zaman kontrol mesajıdır
        header = conn.recv(1024).decode()
        if not header:
            break

        # Mesaj işleme
        if header.startswith("MSG:"):
            mesaj = header[4:]
            print(f"[SUNUCU] Mesaj alındı: {mesaj}")
            conn.send("Mesaj alındı.".encode())

        # Dosya işleme
        elif header.startswith("FILE:"):
            _, dosyaAdi, boyutStr = header.split(":")
            dosyaBoyut = int(boyutStr)

            print(f"[SUNUCU] '{dosyaAdi}' adlı dosya ({dosyaBoyut} bayt) alınıyor...")

            with open("gelen_" + dosyaAdi, "wb") as f:
                kalan = dosyaBoyut
                while kalan > 0:
                    chunk = conn.recv(min(1024, kalan))
                    if not chunk:
                        break
                    f.write(chunk)
                    kalan -= len(chunk)

            print("[SUNUCU] Dosya kaydedildi!")
            conn.send("Dosya başarıyla alındı.".encode())

    conn.close()
