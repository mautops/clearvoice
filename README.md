# ClearVoice - 语音增强系统

ClearVoice 是一个基于 WebSocket 的实时语音增强系统，可以对带有噪声的语音进行处理和增强。系统包含服务端和客户端两个组件，使用 Python Socket.IO 实现实时通信。

## 功能特点

- 实时语音处理和增强
- WebSocket 双向通信
- 支持房间机制，可处理多个客户端
- 自动音频播放功能

## 环境要求

- Python 3.10+
- Docker（可选，用于容器化部署）

## 安装说明

### 方法一：使用 uv 安装（推荐）

1. 安装依赖：
```bash
uv pip install -r requirements.txt
```

2. 安装额外依赖 PyAudio（用于客户端音频播放）：
```bash
uv pip install pyaudio
```

### 方法二：使用 Docker（仅服务端）

1. 构建 Docker 镜像：
```bash
docker build -t clearvoice .
```

2. 运行容器：
```bash
docker run -d -p 5000:5000 clearvoice
```

## 使用说明

### 启动服务端

1. 直接运行：
```bash
python server.py
```

服务端将在 `0.0.0.0:5000` 启动，并监听 WebSocket 连接。

### 运行客户端

1. 确保服务端已经启动
2. 准备音频文件：将需要处理的音频文件命名为 `speech_with_noise.wav` 并放在项目根目录
3. 运行客户端：
```bash
python client.py
```

客户端将：
1. 连接到服务端
2. 自动加入以音频文件名为 ID 的房间
3. 发送音频数据进行处理
4. 接收处理后的音频并自动播放
5. 完成后自动断开连接

## 配置说明

- 服务端端口：默认为 5000，可在 `server.py` 中修改
- 客户端连接地址：默认为 `ws://0.0.0.0:5001`，可在 `client.py` 中修改
- 音频文件：默认读取 `speech_with_noise.wav`，可在 `client.py` 中修改

## 注意事项

1. 确保运行客户端前已安装 PyAudio
2. 使用 Docker 时只包含服务端功能
3. 客户端需要在本地运行以支持音频播放
4. 默认支持的音频格式为 16bit、单声道、16kHz 的 WAV 文件
