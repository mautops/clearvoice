import os
import logging
from flask import Flask
from flask_socketio import SocketIO
from namespace.enhancer import VoiceEnhancerNamespace


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "CHANGE_ME")
socketio = SocketIO(app, cors_allowed_origins="*")


if __name__ == "__main__":
    logger.info("WebSocket 服务器已启动...")
    socketio.on_namespace(VoiceEnhancerNamespace("/enhancer"))
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
