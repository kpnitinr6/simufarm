# SimuFarm v3 — Stage A Vivo proof of concept

One handmade Vivo-style shell, three manual sourced profiles and three static pages. This branch follows MASTER_PROMPT.md and supersedes all previous runtime-first plans. No cloud, paid resource, emulator, API-quota call or deployment is involved.

## Run locally
Python 3.12 and Node 22 are the intended CI runtime. From repository root:
```sh
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ./packages/device-schema -e '.[dev]'
npm ci
npm run build
npm run dev
```
Open http://127.0.0.1:5173. The catalog lists Y100,X100,V30 India variants. Individual pages are /simulators/vivo-y100.html, /simulators/vivo-x100.html and /simulators/vivo-v30.html. Static assets and catalog are generated under apps/web/public; one shared shells/vivo component supplies all three.

```sh
pytest -q
ruff check .
python scripts/validate_data.py --allow-draft
npm run contracts:check
npx playwright install chromium
npm run test:web
```
The browser tests save one actual page screenshot per model in docs/proof/. They also test the three-card catalog and mobile overflow. Rendering is deterministic/idempotent; tests verify that rerunning leaves bytes and modification times unchanged.

## Source and review status
All three profiles are manually researched from Vivo India parameter/launch pages. Field evidence is in data/sources/vivo-*.evidence.json. No manufacturer photographs, logos, wallpapers or firmware binaries are bundled. All on-screen art is original CSS. The shell is a generic visual interpretation, not OEM pixel fidelity.

Draft profiles have genuine firmware build identity unknown and human review pending. See proposed ADR 014: null values are honest unknowns and runtime admission rejects them. An explicit --allow-draft flag generates only labeled visual previews. Default profile validation and the approved-profile API exclude unreviewed data; it must not be presented as a verified runtime catalog. No fabricated fingerprint or false reviewer label is used.

Screen dpi currently denotes physical PPI, including disclosed calculations for Y100/V30; it is not an Android logical-density setting. Profile base_image_id values are future mapping identifiers, not proof of installed/bootable images. No static mockup establishes actual RAM allocation, OEM firmware compatibility or device attestation.

## Runtime limitations and later gates
Redroid ARM64 only; no docker-android or /dev/kvm. No per-device disk images, /data copying, baked per-model build.prop, functional iOS or physical-device farm. Fresh containers and actual identity evidence belong to Stage D; unique IMEI/GSF/advertising IDs are not assumed if absent. No Play Integrity/SafetyNet/certification spoofing is attempted. Apps requiring certified devices may reject the runtime. Emulator results do not establish real-radio/sensor/camera/DRM/battery/thermal or hardware-performance behavior.

No Oracle resources are created until Stage D and verified nonbillable eligibility. Capacity is unmeasured, not promised. GADS lifecycle/Appium is Stage G; Magisk Stage E. Stage B is blocked pending human approval of Stage A. The Stage C 1,000-row allocation has an arithmetic discrepancy recorded in DECISIONS.md. No CSV profile generator, additional brand shell, bulk collection or runtime executor is started here.

MobileAPI conservative cap 50/month; zero calls made by this work and account remaining quota unknown. API key existence is operator-confirmed; its contents were not read. Repository PUBLIC was already explicitly authorized and verified; no visibility change was needed for this stage. CI uses standard runners only, code/schema/static/browser checks, no emulator or cloud deployment.
