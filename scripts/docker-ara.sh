#!/bin/sh
set -eu

REPOSITORY_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

: "${ARA_UID:=$(id -u)}"
: "${ARA_GID:=$(id -g)}"
: "${ARA_PROJECT_DIR:=${REPOSITORY_DIR}/docker-project}"

if [ "${ARA_UID}" -eq 0 ] || [ "${ARA_GID}" -eq 0 ]; then
    echo "docker-ara: refusing to run the agent image as root" >&2
    exit 2
fi

export ARA_UID ARA_GID ARA_PROJECT_DIR
mkdir -p "${ARA_PROJECT_DIR}"

if [ "${1:-}" = "--writable-auth" ]; then
    shift
    exec docker compose --project-directory "${REPOSITORY_DIR}" \
        --file "${REPOSITORY_DIR}/compose.yaml" \
        --file "${REPOSITORY_DIR}/compose.auth-rw.yaml" "$@"
fi

exec docker compose --project-directory "${REPOSITORY_DIR}" \
    --file "${REPOSITORY_DIR}/compose.yaml" "$@"
