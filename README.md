# SimuFarm

SimuFarm provides original HTML device previews and a local Android test runtime. The approved closeout scope is complete: the PR4–10stack is merged to main; StageD/E work locally, StageF interactive chrome is implemented, and StageG is prepared with a successful manual GADS-managed Appium test. [Appium proof](docs/proof/appium-test-results.md): ApiDemos passed in **13.631seconds**. Test services and project containers were stopped afterward.

## Project contents

- **932 generated static candidate profiles**, with no padding. All retain build:null/runtime_eligible:false.
- **22 retained reference profiles**, including the first human-reviewed runtime profile, vivo-x100 China V2309A/PD2309. There are **954 current profiles and HTML pages total**, plus20templates. These are artifact counts, not954distinct verified physical devices.
- **20 original brand shells** with mock status/time, keyboard/text input, rotation and dark mode. HTML controls do not execute Android apps.
- A shared official Redroid14 ARM64 64-only runtime, pinned by digest, with a genuine China Android14 fingerprint and distinct synthetic test identifiers applied before zygote.
- Local UTM deployment/controllers, source/schema validation, browser checks, an Appium harness, proof artifacts and handoff documentation.

C2 removed or merged68records; the earlier duplicate-free claim was incorrect. Documented source checks cover105models for named existence/geometry/spec fields, not complete verification of all932candidate specifications. Cutout coverage is100/932. Sources, conflicts and rejections remain in data/research/stage-c2/ and data/rejections.md.

## Quick Start

Follow [the developer guide](docs/QUICK_START.md). Its **under-ten-minute warm path** assumes a prepared/imported Ubuntu22.04 ARM64 UTM VM, verified SSH access and cached image/Magisk downloads. Fresh OS installation and large downloads are one-time prerequisites and cannot be guaranteed within ten minutes on every connection.

```sh
git clone https://github.com/kpnitinr6/simufarm.git
cd simufarm
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ./packages/device-schema -e '.[dev]'

python scripts/local_quickstart.py \
  --vm-id YOUR-UTM-VM-UUID \
  --identity /absolute/path/to/your/ssh-key \
  --known-hosts /absolute/path/to/verified/known_hosts \
  --magisk-apk /absolute/path/to/Magisk-v31.1.apk \
  --execute
```

Replace the UUID and paths with your own. Omit --execute for a plan without VM/SSH/Docker actions. The controller starts a stopped VM, boots two fresh identity-rehearsal containers, verifies properties and restart persistence, and saves observations. It does not promote profiles or create cloud resources. Stop the specifically named containers afterward as described in the guide.

For HTML previews, run `npm ci`, `npm run build`, then `npm run dev`; open http://127.0.0.1:5173. Device pages under /simulators/ expose **Enable interactive chrome**. The catalog cards remain static.

## Local capacity

Tested on a Mac Mini with16GiB RAM and an external-drive UTM Ubuntu22.04 ARM64 VM allocated **4CPU /8GiB**. The configured Redroid planning ceiling is **5concurrent containers**, reserving2GiB for Ubuntu. Five-way workload capacity is not benchmarked. Android14 first boots were10.158s/16.854s; restart boots9.424s/9.254s; after-restart Docker memory625.6MiB/610.5MiB. The local Appium sample also passed. [Capacity actuals](docs/CAPACITY.md).

SSH uses localhost2222, not an Android/Appium endpoint. ADB and automation services bind to guest loopback and are accessed through distinct SSH tunnels. The VM uses the stock Binder/ashmem modules and binderfs; Redroid requires no KVM. Ordinary SSH permissions are unchanged: no unrestricted passwordless sudo or Docker-group grant was added.

## Limitations

- **Cellular/telephony is non-functional.** IMEI/serial properties are synthetic test identifiers. No modem, SIM registration, calls, SMS or cellular data is provided. TelephonyManager/Binder IMEI may return null or an error even when getprop succeeds.
- **Play Integrity/SafetyNet must be treated as failing or unavailable on this uncertified emulated setup.** It is not a certified physical phone and no bypass is implemented. No live attestation test was performed; do not present a measured attestation verdict that was not observed. Integrity-protected apps may reject it.
- Android release14/SDK34 and the genuine China`:14/`fingerprint agree, but Redroid is not Vivo firmware. OEM APIs, drivers, sensors, cameras, DRM, radio, battery/thermal behavior and physical-device performance are not reproduced. One passing sample does not guarantee every app works.
- HTML chrome is a visual mock, not OEM pixel fidelity or an Android stream. No manufacturer logos, wallpapers or firmware images are bundled.
- Only vivo-x100 is runtime-eligible. Other profiles remain research/static artifacts with their documented uncertainty. No functional iOS emulation is provided.
- StageG has a proven manual sample path. Production grid queuing, persisted result APIs and nightly scheduling remain future extensions, not claims made by this handoff. No nightly automation is enabled.

## Evidence, tests and handoff

[Final handoff](docs/FINAL_HANDOFF.md) · [Appium result](docs/proof/appium-test-results.md) · [Android identity](docs/STAGE_E_IDENTITY.md) · [Interactive UI](docs/STAGE_F_INTERACTIVE.md) · [Appium/GADS replay](docs/STAGE_G_LOCAL_PREP.md).

```sh
pytest -q
ruff check .
python scripts/validate_data.py --allow-draft
python scripts/stage_e_gate.py
npm run contracts:check
npx playwright install chromium
npm run test:web
```

CI runs on Python3.12/Node22 with code/schema/static/browser checks. It does not provision cloud resources or run Android/Appium. Oracle launch paths remain disabled. This closeout made **zero Oracle calls, zero MobileAPI calls and touched zero paid resources**. VM disks, private keys, credentials, APKs and local logs are excluded from public Git. The VM/key is user-owned and is not distributed in the repository.
