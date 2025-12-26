import base64
import socket
from flask import Flask
from flask_socketio import SocketIO, emit
from config import Config
from routes.main_routes import main_bp
from routes.caesar_routes import caesar_bp
from routes.vigenere_routes import vigenere_bp
from routes.railfence_routes import railfence_bp
from routes.substitution_routes import substitution_bp
from routes.hill_routes import hill_bp
from routes.polybius_routes import polybius_bp
from routes.columnar_routes import columnar_bp
from routes.des_routes import des_bp
from routes.aes_routes import aes_bp


socketio = SocketIO(cors_allowed_origins="*")
SERVER_XOR_KEY = 123


def xor_text(text, key):
    return "".join(chr(ord(c) ^ key) for c in text)


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
    app.register_blueprint(des_bp)
    app.register_blueprint(aes_bp)

    socketio.init_app(app)
    return app


app = create_app()

@socketio.on("client_to_server")
def handle_client_message(data):
    try:
        encrypted_packet = data.get("text")
        method = data.get("method")
        emit(
            "display_on_server",
            {
                "method": method,
                "text": encrypted_packet, 
                "encrypted": data.get("encrypted_raw"), 
            },
            broadcast=True
        )

    except Exception as e:
        print("CLIENT ERROR:", e)

@socketio.on('server_to_client')
def handle_server_message(data):
    input_text = data.get('text', '')
    method = data.get('method', 'SİSTEM')

    xor_val = "".join([chr(ord(c) ^ 123) for c in input_text])
    encoded_packet = base64.b64encode(xor_val.encode()).decode()

    emit('server_to_client', {
        'method': method,
        'encrypted_resp': encoded_packet 
    }, broadcast=True)

if __name__ == "__main__":
    local_ip = socket.gethostbyname(socket.gethostname())
    socketio.run(app, host=local_ip, port=5000, debug=True)
