# Local developer quick start

The warm path is designed to take **under10minutes** once the one-time local VM and downloads below are ready. It boots two containers, verifies Android14 identity properties and checks restart persistence. Actual container boots were10.158s/16.854s and restarts9.424s/9.254s. A fresh Ubuntu installation, dependency downloads and slow-network time are not included in that target; a cold machine cannot honestly be guaranteed a ten-minute setup.

**Measured validation:326.985seconds (5minutes27seconds)** from a stopped VM through VM startup, SSH readiness, two fresh containers and restart identity checks, with prerequisites cached. [Timing result](proof/quickstart-result.json). The stopped-VM test found an early ADB shell timeout; the controller now retries that transient condition within its unchanged180second per-boot deadline.

## One-time prerequisites

- Apple Silicon Mac, UTM5+, Python3.12 and Node22. A4-core/8GiB Ubuntu22.04 ARM64 VM is the tested target. Keep the VM disk on an APFS external drive if desired; do not format any drive as part of these instructions.
- Import the existing user-owned SimuFarm.utm bundle into UTM, or create your own Ubuntu22.04 ARM64 VM with4CPU/8GiB and a128GiB sparse disk. Enable the QEMU guest agent and localhost-only forwarding2222→guest22. Use username simufarm and your own SSH key. The VM/key is not distributed through Git. [Detailed VM setup](STAGE_D_UTM.md).
- Inside Ubuntu, install Docker, ADB and qemu-guest-agent, plus the stock modules for the running5.15kernel (for example: `sudo apt-get install docker.io adb qemu-guest-agent linux-modules-extra-$(uname -r)`, then `sudo systemctl enable --now docker qemu-guest-agent`). No KVM is required. The ordinary account needs no Docker-group or passwordless-sudo grant: the controller uses the existing local UTM guest agent for the specific administrative commands.
- As the VM administrator, install the repeatable host preparation once:

```sh
sudo install -m755 infra/local-automation/kernel/prepare-redroid.sh /usr/local/sbin/simufarm-redroid-host
sudo install -m644 infra/local-automation/kernel/simufarm-redroid-host.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now simufarm-redroid-host.service
```

Run those installation commands inside the VM after copying the two files there. The oneshot unit prepares Binder/ashmem and binderfs on boot; it starts no containers or network services. It was enabled and executed successfully on the handoff VM. It is inactive after execution by design.

- Cache the official Redroid14 ARM64 image in the VM:

```sh
sudo docker pull --platform linux/arm64 redroid/redroid@sha256:46478a567194aed24cd0877d4434a9e58b534d4aad30931eb21999a52f2ce131
```

- Download official [Magisk v31.1](https://github.com/topjohnwu/Magisk/releases/download/v31.1/Magisk-v31.1.apk) onto the Mac. SHA256 must be `89cefac0a318afa39fb3880c45c87b036c05bc1ebf02a7a715b7f8d7c26ac6e7`. The controller verifies it before extracting the ARM64 applet. No Magisk manager or daemon is installed in Android.
- Verify the VM SSH host key independently through the local UTM console/guest agent and save it in known_hosts. Do not disable host-key verification or copy someone else's private key. `utmctl list` gives your VM UUID.

## Warm path from a clone

On the Mac:

```sh
git clone https://github.com/kpnitinr6/simufarm.git
cd simufarm
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ./packages/device-schema -e '.[dev]'

python scripts/local_quickstart.py \
  --vm-id YOUR-UTM-VM-UUID \
  --identity /absolute/path/to/your/ssh-private-key \
  --known-hosts /absolute/path/to/verified/known_hosts \
  --magisk-apk /absolute/path/to/Magisk-v31.1.apk \
  --execute
```

The UUID placeholder must be replaced with the real UTM UUID. Omit `--execute` to print a plan with no VM, SSH or Docker actions. The helper starts a stopped VM, waits up to120seconds for strict localhost SSH, then runs the bounded two-container controller. It checks that the reviewed runtime profile is eligible first. The identity rehearsal uses its matching China test copy and does not promote additional profiles.

The existing handoff VM UUID is F28BDEF7-5053-4B12-A98D-A33831B72167. Its bundle is `/Volumes/SimuFarmDrive/SimuFarm/VMs/SimuFarm.utm/`, SSH user simufarm, port2222. Those paths describe this machine; a new developer supplies their own VM, key and paths.

Both containers use fresh data volumes and guest-loopback ADB5561/5562. They remain running after the rehearsal so you can inspect them. Read the printed local observations.json for names and properties. A pair is refused if it would exceed the five-container planning ceiling or the2GiB Ubuntu reserve. The controller never clones Android data or provisions cloud resources.

## Stop after use

Copy `scripts/local_redroid_stop.py` into the VM. For each exact container name from observations.json, invoke it through the local guest agent:

```sh
utmctl exec YOUR-UTM-VM-UUID --cmd /usr/bin/python3 \
  /home/simufarm/local_redroid_stop.py EXACT-CONTAINER-NAME \
  --output /home/simufarm/stop-result.json
```

It accepts only the owned SimuFarm StageE naming pattern and verifies a private PID namespace before requesting Android shutdown. It flushes data, powers off that namespace and retains the volume. The observed shutdown took2.176s with exit130, the expected [SIGINT namespace-poweroff result](https://man7.org/linux/man-pages/man2/reboot.2.html); Ubuntu stayed running. A bounded docker-stop fallback is recorded explicitly if needed. Never run Android poweroff in a host PID namespace.

## HTML UI and Appium

For the web previews:

```sh
npm ci
npm run dev
```

`npm run build` regenerates the932-profile static cohort plus22reference pages before producing the web build. Open a device page and enable interactive chrome for mock status/time, keyboard, rotation and dark mode. This is not an Android stream.

[Local Appium/GADS setup and replay](STAGE_G_LOCAL_PREP.md) documents the separate automation services. The actual provider-managed ApiDemos test passed in13.631s; [proof](proof/appium-test-results.md). Those services and all project containers were stopped at handoff. No nightly task is enabled.
