#!/bin/sh
set -eu

copy_auth_file() {
    source_file=$1
    target_file=$2

    if [ -f "${source_file}" ] && [ ! -e "${target_file}" ]; then
        cp "${source_file}" "${target_file}"
        chmod 600 "${target_file}"
    fi
}

mkdir -p "${HOME}/.codex" "${HOME}/.claude"

# Safe-mode credentials are copied at container start into the tmpfs-backed
# home. The host mounts remain read-only and no secret enters an image layer.
for file in auth.json config.toml .env; do
    copy_auth_file "/run/ara-auth/codex/${file}" "${HOME}/.codex/${file}"
done

for file in .credentials.json settings.json settings.local.json; do
    copy_auth_file "/run/ara-auth/claude/${file}" "${HOME}/.claude/${file}"
done

exec "$@"
