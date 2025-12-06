from flask import Flask
from config import Config

# Blueprint dosyalarını import et
from routes.main_routes import main_bp
from routes.caesar_routes import caesar_bp
from routes.vigenere_routes import vigenere_bp
from routes.railfence_routes import railfence_bp
from routes.substitution_routes import substitution_bp
from routes.hill_routes import hill_bp
from routes.polybius_routes import polybius_bp
from routes.columnar_routes import columnar_bp

import socket, random

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(main_bp)
    app.register_blueprint(caesar_bp)
    app.register_blueprint(vigenere_bp)
    app.register_blueprint(railfence_bp)
    app.register_blueprint(substitution_bp)
    app.register_blueprint(hill_bp)
    app.register_blueprint(polybius_bp)
    app.register_blueprint(columnar_bp)

    return app


if __name__ == "__main__":
    app = create_app()

    local_ip = socket.gethostbyname(socket.gethostname())
    port = random.randint(5000, 9000)

    print(f"Uygulama çalışıyor: http://{local_ip}:{port}")

    app.run(debug=True, host=local_ip, port=port)
