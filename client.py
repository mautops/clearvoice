import pyaudio
import logging
import socketio
from typing import Dict

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceEnhancerNamespace(socketio.ClientNamespace):
    """语音增强器命名空间"""

    def on_connect(self) -> None:
        logger.info("客户端连接成功")
        self.emit("message", "客服端发来的消息")
        # 读取本地文件
        with open("speech_with_noise.wav", "rb") as f:
            # 使用文件名作为房间号加入
            self.emit("join", {"room": f.name})
            # 发送音频数据
            audio_data = f.read()
            self.emit("audio", audio_data)

    def on_disconnect(self, reason: str) -> None:
        logger.info(f"客户端断开连接, 原因: {reason}")

    def on_enter_room(self, data: Dict) -> None:
        """加入房间

        Args:
            data (Dict): example: {"room": "room_id_in_str"}

        Returns:
            None
        """
        room = data.get("room")
        logger.info(f"加入房间: {room}")

    def on_leave_room(self, data: Dict) -> None:
        """离开房间

        Args:
            data (Dict): example: {"room": "room_id_in_str"}

        Returns:
            None
        """
        room = data.get("room")
        logger.info(f"离开房间: {room}")

    def on_message(self, data: str) -> None:
        """处理消息

        Args:
            data (str): 消息内容

        Returns:
            None
        """
        logger.info(f"收到消息: {data}")

    def on_audio(self, data: bytes) -> None:
        """处理音频数据

        Args:
            data (bytes): 音频数据

        Returns:
            None
        """
        logger.info(f"收到音频数据, 长度: {len(data)}")
        # 使用 pyaudio 直接播放
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, output=True)
        stream.write(data)
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    sio = socketio.Client()
    sio.register_namespace(VoiceEnhancerNamespace("/enhancer"))
    try:
        # 连接到服务器
        sio.connect("ws://127.0.0.1:5000")
        sio.wait()
    except KeyboardInterrupt:
        logger.info("手动断开连接")
    except Exception as e:
        logger.error(f"连接失败: {e}")
    finally:
        sio.disconnect()
