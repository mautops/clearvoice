import os
import logging
from typing import Optional
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 从环境变量获取模型配置，默认使用 iic/speech_frcrn_ans_cirm_16k
DEFAULT_MODEL = "iic/speech_frcrn_ans_cirm_16k"
MODEL_NAME = os.getenv("CLEARVOICE_MODEL", DEFAULT_MODEL)


class Singleton(type):
    """元类，用于实现单例模式"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class VoiceEnhancer(metaclass=Singleton):
    """使用元类实现的语音增强器单例类"""

    def __init__(self):
        if not hasattr(self, "initialized"):
            logger.info(f"正在加载语音增强模型: {MODEL_NAME}")
            self.pipe = pipeline(
                task=Tasks.acoustic_noise_suppression, model=MODEL_NAME
            )

    def enhance_audio(self, audio_data: bytes) -> Optional[bytes]:
        """
        直接处理音频字节数据并返回处理后的PCM数据

        Args:
            audio_data: 输入的音频字节数据

        Returns:
            Optional[bytes]: 处理后的PCM音频数据，处理失败时返回None
        """
        try:
            result = self.pipe(audio_data)

            if isinstance(result, dict) and "output_pcm" in result:
                return result["output_pcm"]
            return None
        except Exception as e:
            logger.error(f"音频处理错误: {str(e)}")
            return None


# 创建增强器实例
enhancer = VoiceEnhancer()
