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

## Sequential Traffic Bot

Inside the prepared **Linux VM**, use the standard-library runner for sequential URL/scroll/screenshot tests on a site you control or are authorized to test:

```sh
python3 scripts/run_traffic_bot.py --url "https://example.com" --proxy-file proxies.txt --limit 5
# Validate the complete CSV without starting Docker/ADB or visiting any URL:
python3 scripts/run_traffic_bot.py --url "https://example.com" --dry-run
```

`python scripts/run_traffic_bot.py ...` also works where `python` selects Python 3.10+.
Run as an account already authorized for Docker; the script does not grant Docker access or start the VM. Install `adb`, and `aapt` when using `--apk /absolute/path/browser.apk`. Cache `redroid/redroid:14.0.0_64only-latest` first (the default matches the manually validated image tag); use `--image` with the pinned digest in `infra/redroid-identity/toolchain.json` for reproducibility; the runner never pulls an image. The host must already have working Binder/ashmem/binderfs. Stop other containers first. No GADS/Appium service is needed.

Without `--limit`, all **932 CSV rows are screen-size/DPI scenarios**, each on a fresh stock Android 14 container. The CSV has no build block; it does **not** supply 932 runtime-approved identities or OS versions. This runner never injects build properties, changes runtime eligibility, or claims genuine/organic users. Random timing and scrolling are test inputs, not a guarantee of human-like behavior or fraud-detection bypass. The reviewed X100 identity remains a separate runtime track.

`--proxy-file` cycles one endpoint per scenario; omit it for direct traffic. Format: `http://host:port` or `host:port` (one per line, blank lines and `#` comments accepted). Files ending in `.csv` are parsed with Python CSV handling and must have a `proxy` column; additional columns and quoted CSV fields are supported. Endpoints are normalized to `http://host:port` before cycling, then converted to Android host/port settings. Android's global `http_proxy` setting accepts host/port, **not username/password credentials or SOCKS URLs**; those inputs are rejected before any device boots. Authenticated upstreams need a separately configured local relay. The setting is not a VPN, and apps may bypass it; the runner verifies the setting, not the effective egress IP. No proxy address/credentials or target URL is printed in logs. Keep proxy lists out of Git.

`--apk` accepts either a single APK or an extracted split bundle directory:

```sh
python3 scripts/run_traffic_bot.py --url "https://example.com" --apk ./chrome --limit 5
python3 scripts/run_traffic_bot.py --url "https://example.com" --apk ./browser.apk --limit 5
```

A folder must contain `base.apk` and matching `split_config.*.apk` files directly inside it. All top-level `*.apk` files are installed together with `adb install-multiple -r`; use a folder containing only one app's matching bundle, compatible with Android 14 / ARM64. A single file uses `adb install -r`. Archives (`.apks`/`.xapk`) must be extracted first. The runner checks `sys.boot_completed`, waits for ADB and pauses briefly before installation; package detection uses `base.apk` for split bundles. APK validation also runs during `--dry-run` without installing anything. Installation still requires all required compatible splits; External APK dependencies are not automatically resolved.

The stock image may have **no Chrome**. Supply the Chrome APK or split folder using `--apk`. The pipeline explicitly launches `com.android.chrome/com.google.android.apps.chrome.Main` with the URL instead of resolving a generic VIEW intent; non-Chrome APKs are rejected for this browser pipeline. Before URL launch, Chrome is force-stopped and `chrome --disable-fre --no-default-browser-check --no-first-run` is written to `/data/local/tmp/chrome-command-line` with mode 0644 and verified by reading it back. These test flags request skipping Chrome onboarding; acceptance depends on the Chrome build/rooted environment, and file verification does not prove page loading. See [Chromium command-line guidance](https://www.chromium.org/developers/how-tos/run-chromium-with-flags/). Screenshots are captures, not assertions that website content loaded successfully.

After Docker starts, the runner waits 15 seconds before its first ADB connection; boot readiness is still bounded. The enforced flow is boot/ADB → proxy → optional APK install → Chrome first-run flags → URL launch → scrolling/waits → screenshot → proxy reset/teardown. Logs label these actual steps. Each scenario waits 5 seconds, makes 3–4 randomized upward swipes, waits 10 seconds, captures `results/traffic/<profile_id>.png`, and resets the Android global HTTP proxy to `:0` before removing its owned container and anonymous data volume. If ADB is unavailable, a warning is logged and container removal still proceeds. `runs.jsonl` records pass/fail, elapsed time, actual Android release and the geometry-only scope. Logs show progress and cleanup. Default inter-scenario delay is uniformly randomized **60–120 seconds**, configurable with `--delay-min`/`--delay-max`; there is no final delay. Docker assigns a free guest-loopback ADB port by default; `--adb-port 5575` explicitly chooses a port, which is checked before creation (a subsequent allocation race is still reported by Docker). Only the exact UUID-named container is pre-removed, never other project containers. Docker failures print captured stderr immediately and abort the batch; private PID isolation uses Docker's default rather than an unsupported `--pid=private` flag. Processing is strictly sequential with a VM-wide file lock; cleanup failure aborts the batch. Ctrl-C/SIGTERM attempt cleanup; power loss/SIGKILL cannot, so inspect owned `simufarm-traffic-*` containers after an unclean exit. Ordinary Docker stop may need its 30-second forced-stop fallback; disposable test data is removed, not retained.

For a full 932-row batch the default inter-scenario delays alone take approximately 15.5–31 hours; loading/scroll waits, boots and teardown add to that. Use `--limit 5` first. Exit status is nonzero if any scenario fails. Screenshots/results are ignored by Git. See [Android ADB documentation](https://developer.android.com/tools/adb) and [AOSP proxy setting definition](https://android.googlesource.com/platform/frameworks/base/+/c52839277b8714d150a9fe276b6ba3fa8a0cbf38/core/java/android/provider/Settings.java).

### Diagnosing Docker startup

The startup banner shows `chrome-first-run-v3`, the resolved script path, its SHA-256 prefix and selected image. Verify `python3 scripts/run_traffic_bot.py --version` shows this marker after pulling. The older bare `docker command failed (exit 125)` message is not emitted by this version.

The runner prints the exact generated `docker run -d --privileged ...` command and, on failure, Docker's captured stderr immediately (falling back to stdout when stderr is empty). Credentials in HTTP URLs are redacted. The default is the cached `redroid/redroid:14.0.0_64only-latest` tag; no image is silently pulled. Disposable `/data` uses an anonymous Docker volume. APK paths such as `./chrome` are **never Docker mounts**; files are installed using ADB after Android boots. Proxy settings are likewise applied through ADB, not Docker environment variables.

The default uses Redroid's privileged startup with no host binderfs bind, matching the working manual command. If your host explicitly requires sharing its existing binderfs, add `--binderfs /dev/binderfs`; the source must already exist and is mounted via `--mount type=bind` so Docker cannot silently create a missing source directory. This flag does not load modules or create a binderfs mount. The separate reviewed identity runtime keeps its digest pin.

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
