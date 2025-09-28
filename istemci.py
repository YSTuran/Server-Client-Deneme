import socket
import os

HOST = "127.0.0.1"
PORT = 5000

def istemciyiCalistir():
    istemci = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    istemci.connect((HOST, PORT))

    while True:
        secim = input("Mesaj mı dosya mı göndermek istiyorsun? (mesaj/dosya/çıkış): ")

        # Mesaj gönder
        if secim == "mesaj":
            mesaj = input("Gönderilecek mesaj: ")
            istemci.send(f"MSG:{mesaj}".encode())
            print("[İSTEMCİ] Sunucudan cevap:", istemci.recv(1024).decode())

        # Dosya gönder
        elif secim == "dosya":
            dosyaYolu = input("Gönderilecek dosya yolu: ")

            if not os.path.exists(dosyaYolu):
                print("Dosya bulunamadı!")
                continue

            dosyaAdi = os.path.basename(dosyaYolu)
            dosyaBoyut = os.path.getsize(dosyaYolu)

            # Önce HEADER gönder (dosya adı ve boyut bilgisi)
            istemci.send(f"FILE:{dosyaAdi}:{dosyaBoyut}".encode())

            # Ardından dosya içeriğini binary olarak gönder
            with open(dosyaYolu, "rb") as f:
                while chunk := f.read(1024):
                    istemci.send(chunk)

            print("[İSTEMCİ] Dosya gönderildi.")
            print("[İSTEMCİ] Sunucudan cevap:", istemci.recv(1024).decode())

        # Çıkış
        elif secim == "çıkış":
            break

    istemci.close()
