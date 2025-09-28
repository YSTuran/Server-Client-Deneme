import threading
from sunucu import sunucuyuCalistir
from istemci import istemciyiCalistir

if __name__ == "__main__":
    sunucu_thread = threading.Thread(target=sunucuyuCalistir, daemon=True)
    istemci_thread = threading.Thread(target=istemciyiCalistir)

    sunucu_thread.start()
    istemci_thread.start()
