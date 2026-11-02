# SimuFarm

SimuFarm combines original HTML device previews with a local Redroid runtime. Stage D and Stage E are accepted. The first reviewed runtime profile is **vivo-x100 (China V2309A / PD2309)**, running Android14/SDK34 with an unmodified, sourced China Android14 fingerprint. See [identity evidence](docs/STAGE_E_IDENTITY.md) and [capacity actuals](docs/CAPACITY.md).

The runtime runs inside an Ubuntu22.04 ARM64 UTM VM on the Mac Mini's external drive:4CPU cores,8GiB RAM, SSH at `127.0.0.1:2222`. ADB is separate and bound only to loopback inside the VM. Oracle provisioning remains disabled. Five concurrent containers is a planning ceiling with2GiB reserved for Ubuntu, not a completed load benchmark.

## Run the visual catalog

Python3.12 and Node22 are the intended CI versions:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ./packages/device-schema -e '.[dev]'
npm ci
npm run build
npm run dev
```

Open http://127.0.0.1:5173. Device pages live under `/simulators/`, including `/simulators/vivo-x100.html`. The HTML is original artwork and does not stream Android or run APKs. Each device page has an **Enable interactive chrome** button for mock status controls, text input/keyboard, rotation and dark mode. These local UI controls are available across all20brand shells; they do not imply real OS or cellular behavior. The visual reference catalog retains22profiles across20brands; one reference now has reviewed runtime eligibility. Generated draft data and the accepted C2 remediation remain separate branches; source presence and round-number generation are not claims that every row is a verified distinct device.

## Telephony limitation — this is not a real phone

`adb shell getprop persist.radio.imei` and `ro.serialno` return distinct **synthetic test identifiers**. This does not provide a modem, SIM or cellular service. Calls, SMS, cellular data, network registration and radio-HAL dependent operations are unavailable. A TelephonyManager or Binder request for an IMEI may return null or an error even when getprop is populated. Tests requiring cellular services need another test strategy.

The Android release and sourced fingerprint now both identify Android14, with actual SDK34. Redroid does not reproduce Vivo firmware, OEM services, hardware drivers, camera/sensor behavior, DRM, battery/thermal behavior or physical-device performance. Apps requiring OEM APIs or certified devices may still fail. No Play Integrity/SafetyNet/certification bypass is implemented, and no broad crash-free compatibility claim is made.

## Evidence and review

The active runtime profile is `profiles/runtime/vivo-x100.json`; its conditional human approval is in `data/reviews/vivo-x100.runtime.json`. The earlier India X100 source profile is archived separately; India model strings are not mixed with China firmware. Complete field provenance and literal OTA metadata are under `data/research/stage-e-x100-china/android14/`. Runtime admission still requires complete sourced builds and human review. Generated drafts remain build:null/runtime_eligible:false.

```sh
pytest -q
ruff check .
python scripts/validate_data.py --allow-draft
npm run contracts:check
npx playwright install chromium
npm run test:web
```

CI performs code/schema/static/browser checks on public standard runners. It never provisions cloud resources, boots Android, runs nightly APK tests or consumes MobileAPI quota. MobileAPI conservative cap remains50requests/month; this work made zero calls. Runtime observations remain in local evidence rather than public Git. Do not commit private keys, VM disks, APKs or credentials.


## Local automation preparation

StageG topology, provider UI-field recipe and plan-only Appium harness are prepared in [STAGE_G_LOCAL_PREP.md](docs/STAGE_G_LOCAL_PREP.md). GADS/Appium were not installed or started, no Appium session or nightly APK run was executed, and SSH2222 is not an Appium/ADB endpoint. StageF interaction evidence is in [STAGE_F_INTERACTIVE.md](docs/STAGE_F_INTERACTIVE.md).
