# syntax=docker/dockerfile:1

FROM node:22-bookworm-slim

ARG ARA_UID=1000
ARG ARA_GID=1000
ARG CODEX_CLI_VERSION=0.149.0
ARG CLAUDE_CODE_VERSION=2.1.239

LABEL org.opencontainers.image.title="Adapted Research Architecture"
LABEL org.opencontainers.image.description="ARA runtime with Codex CLI and Claude Code"
LABEL org.opencontainers.image.version="0.1.0"

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DISABLE_AUTOUPDATER=1 \
    PATH="/opt/ara/bin:${PATH}"

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        ca-certificates \
        curl \
        git \
        jq \
        python3 \
        python3-venv \
        ripgrep \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/ara-src
COPY pyproject.toml README.md ./
COPY src ./src
COPY tests ./tests

RUN PYTHONPATH=src python3 -m unittest discover -s tests -v \
    && python3 -m venv /opt/ara \
    && /opt/ara/bin/python -m pip install --no-cache-dir . \
    && rm -rf /opt/ara-src

RUN npm install --global --omit=dev \
        "@openai/codex@${CODEX_CLI_VERSION}" \
        "@anthropic-ai/claude-code@${CLAUDE_CODE_VERSION}" \
    && codex --version \
    && claude --version \
    && npm cache clean --force

COPY --chmod=0755 docker-entrypoint.sh /usr/local/bin/ara-container-entrypoint

# The official Node image supplies the unprivileged node user. Reusing it avoids
# leaving a second fixed-ID account while allowing private host credentials to be
# read without changing their permissions.
RUN test "${ARA_UID}" -gt 0 \
    && test "${ARA_GID}" -gt 0 \
    && groupmod --gid "${ARA_GID}" --new-name ara node \
    && usermod --uid "${ARA_UID}" --gid "${ARA_GID}" \
        --login ara --home /home/ara --move-home node \
    && mkdir -p \
        /home/ara/.codex \
        /home/ara/.claude \
        /run/ara-auth/codex \
        /run/ara-auth/claude \
        /workspace \
    && chown -R "${ARA_UID}:${ARA_GID}" \
        /home/ara /run/ara-auth /workspace

USER ara
ENV HOME=/home/ara
WORKDIR /workspace

ENTRYPOINT ["ara-container-entrypoint"]
CMD ["ara", "doctor"]
