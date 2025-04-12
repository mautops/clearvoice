import logging
from flask_socketio import Namespace
from typing import Optional, Dict
from flask_socketio import join_room, leave_room
from service.enhancer import enhancer


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceEnhancerNamespace(Namespace):
    """语音增强器命名空间"""

    def on_connect(self, auth: Optional[Dict] = None) -> None:
        """连接成功

        Args:
            auth (Optional[Dict], optional): 认证信息. Defaults to None.

        Returns:
            None
        """
        logger.info(f"client connected, auth: {auth}")

    def on_disconnect(self, reason: str) -> None:
        """断开连接

        Args:
            reason (str): 断开连接原因

        Returns:
            None
        """
        logger.info(f"client disconnected, reason: {reason}")

    def on_join(self, data: Dict) -> None:
        """加入房间

        Args:
            data (Dict): example: {"room": "room_id_in_str"}

        Returns:
            None
        """
        room = data.get("room")
        if not room:
            self.emit("error", "room is required")
            return None
        join_room(room)
        self.emit("message", f"client {room} joined rooms", room=room)

    def on_leave(self, data: Dict) -> None:
        """离开房间

        Args:
            data (Dict): example: {"room": "room_id_in_str"}

        Returns:
            None
        """
        room = data.get("room")
        if not room:
            self.emit("error", "room is required")
            return None

        # 判断 room 是否在房间列表
        if room not in self.rooms():
            self.emit("error", f"room {room} not found")
            return None

        # 离开房间
        leave_room(room)
        self.emit("message", f"client {room} left rooms", to=room)

    def on_message(self, data: str) -> None:
        """处理消息

        Args:
            data (str): 消息内容

        Returns:
            None
        """
        logger.info(f"received message: {data}")
        self.emit("message", f"server received message: {data}")

    def on_audio(self, data: bytes) -> None:
        """处理音频数据

        Args:
            data (bytes): 音频数据

        Returns:
            None
        """
        logger.info(f"received audio: {len(data)} bytes")
        enhanced_data = enhancer.enhance_audio(data)
        if enhanced_data:
            self.emit("audio", enhanced_data)
        else:
            logger.error("音频处理失败")
