FROM ubuntu:22.04

WORKDIR /workspace

COPY . .

RUN curl -LsSf https://astral.sh/uv/install.sh | bash \
    && source $HOME/.local/bin/env \
    && uv sync

CMD ["python", "server.py"]
