FROM m.daocloud.io/docker.io/library/python:3.10

WORKDIR /workspace

COPY . .

RUN which python && python --version && \
    pip install -r requirements.txt gevent -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

CMD ["python", "server.py"]
