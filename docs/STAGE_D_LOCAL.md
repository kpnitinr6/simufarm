# Stage D — local Ubuntu 22.04 over Meshnet

Status: **Prepared; awaiting Meshnet IP and SSH username.** No server connection or local runtime measurement has occurred. Oracle is disabled by `config/stage-d-target.json`; ADR015 is superseded by ADR016. Both Oracle launch entry points refuse execution before credential loading. No Oracle API calls were made for this pivot.

The retry process and its sleep inhibitor are absent. The former monitor was already deleted after the HTTP429 halt on29October. Historical run:16attempts, no returned instance OCID. Free Oracle network resources remain until the user runs the separately supplied cleanup commands; their current state has not been queried.

## Connection and preflight

After the server is installed, provide its Meshnet IPv4 and SSH username. The controller accepts the Meshnet shared-address range100.64.0.0/10, uses key-based batch SSH and requires an existing verified known-host key. Verify the SSH host-key fingerprint from the server console and enroll it using normal SSH first; do not bypass host verification. Enable incoming Meshnet traffic and SSH access on the server. No public router port-forwarding or public ADB is needed.

```sh
python3 scripts/stage_d_local.py --host MESHNET_IP --user SSH_USER
python3 scripts/stage_d_local.py --host MESHNET_IP --user SSH_USER --preflight
```

The first command only prints a plan. `--preflight` performs read-only SSH checks: Ubuntu22.04, CPU architecture, kernel, RAM, available disk, Docker access, adb, noninteractive sudo and binder/ashmem module availability. It saves `host-preflight.json` locally. Optional `--identity /absolute/path/to/private-key` selects a local SSH key; the private key is never copied.

No assumption is made that a spare hard drive means ARM hardware. x86_64 and ARM64 are accepted; a verified immutable Redroid digest matching the actual architecture is mandatory before deployment. The previously verified ARM image cannot be used as an x86 image. No image has yet been selected for this server.

## Runtime prerequisites and execution

The server needs Python3, OpenSSH, Docker Engine, adb and binder_linux/ashmem_linux support. Missing kernel modules stop deployment and produce diagnostics. The script does not install arbitrary kernel modules, change boot settings or reboot the machine. If the installed Ubuntu kernel lacks ashmem, review the actual kernel/Redroid compatibility after preflight; do not claim runtime readiness now. KVM may exist on local hardware and is only recorded; Redroid does not require it.

After successful preflight and image verification:

```sh
python3 scripts/stage_d_local.py --host MESHNET_IP --user SSH_USER \
  --apk /absolute/path/sample.apk --apk-sha256 VERIFIED_SHA256 \
  --image redroid/redroid@sha256:VERIFIED_ARCH_DIGEST --execute
```

The controller uploads the collector, existing vivo-x100 diagnostic profile and checksum-verified APK to a fresh server work directory. It boots two independent containers with fresh volumes, verifies ADB and APK installation, and collects boot time, memory and all four identity fields. Profile build properties are not applied; runtime eligibility is not promoted. Both ADB ports bind to127.0.0.1 on the server. No Oracle CLI/SDK/API is used. Redroid containers are privileged and therefore run only on the explicitly authorized spare server.

Evidence is copied back under `data/runtime/local/`, including on collector failure. Containers and volumes remain available for inspection; they are not silently deleted. Missing/identical IMEI or serial is reported as failure, never replaced with invented data. Optional manual ADB tunnels may use `ssh -L 15555:127.0.0.1:5555 -L 15556:127.0.0.1:5556 SSH_USER@MESHNET_IP`; local adb can then connect to the tunnel ports. StageE remains unstarted and requires a human-reviewed runtime profile.
