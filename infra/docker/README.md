# Free-path local development
The Compose file runs API + MinIO + idempotent bucket initialization only. It does not deploy Oracle, GADS, MongoDB or Android emulators. Local Docker/MinIO compatibility has not been tested here because Docker is unavailable.

From repository root, after setting local MinIO credentials in .env:
```sh
docker compose --env-file .env -f infra/docker/compose.yaml up --build -d --wait
```
No /dev/kvm mapping, privileged container, public noVNC/ADB port or cross-architecture emulation workaround is enabled. A separate reviewed compatibility ADR is required for the requested emulator stack. GADS discovers/adopts running emulators; it is not the lifecycle launcher. Its additional MongoDB prerequisite must be budgeted in the same local VM if later adopted.
