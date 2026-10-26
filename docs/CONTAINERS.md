# Container operation

The image installs ARA, Codex CLI, and Claude Code. CLI versions are pinned in the
Dockerfile and can be overridden through build arguments.

```bash
./scripts/docker-ara.sh build
./scripts/docker-ara.sh run --rm ara ara doctor
./scripts/docker-ara.sh run --rm ara codex login status
./scripts/docker-ara.sh run --rm ara claude auth status
```

The helper matches the host UID/GID and creates `./docker-project` as the writable
project. Select another directory explicitly:

```bash
ARA_PROJECT_DIR=/absolute/path/to/project \
  ./scripts/docker-ara.sh run --rm ara ara --project /workspace workflows
```

To open a shell or CLI:

```bash
./scripts/docker-ara.sh run --rm ara bash
./scripts/docker-ara.sh run --rm ara codex
./scripts/docker-ara.sh run --rm ara claude
```

The default mounts `~/.codex` and `~/.claude` read-only. The entrypoint copies required
authentication/configuration files into a writable tmpfs home. Credentials are excluded
from the image build context. Processes that read these mounts can use those credentials;
run trusted packages only.

To persist intentional host-side login or session updates, opt into writable mounts:

```bash
./scripts/docker-ara.sh --writable-auth run --rm ara codex
./scripts/docker-ara.sh --writable-auth run --rm ara claude
```

The root filesystem is read-only; capabilities are dropped and `no-new-privileges`
is enabled. Network access remains available for model CLIs. Compose sets
`ARA_OS_SANDBOX=off` because the container provides the deployment boundary.

The image build runs the conformance suite. Building and authenticating it requires
Docker, package-network access, and local CLI credentials.
