# SimuFarm — Stage C static generation

Twenty original brand shells and templates; twenty reference profiles plus two retained Stage A Vivo profiles (22 static previews). This branch follows MASTER_PROMPT.md and supersedes all previous runtime-first plans. No cloud, paid resource, emulator, API-quota call or deployment is involved.

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
Open http://127.0.0.1:5173. The catalog lists 22 drafts across 20 brands, with a reference-cohort toggle and brand filters. Individual pages are /simulators/vivo-y100.html, /simulators/vivo-x100.html and /simulators/vivo-v30.html. Static assets and catalog are generated under apps/web/public; each brand reuses its corresponding Web Component.

```sh
pytest -q
ruff check .
python scripts/validate_data.py --allow-draft
npm run contracts:check
npx playwright install chromium
npm run test:web
```
The browser tests save one actual page screenshot per model in docs/proof/. Ten masked-text frame/art snapshots provide visual regression checks; catalog filters and mobile overflow are also tested. Rendering is deterministic/idempotent; tests verify that rerunning leaves bytes and modification times unchanged.

## Source and review status
Profiles are manually researched from manufacturer specifications/launch material, preserving selected market variants. Field evidence is in data/sources/*.evidence.json. No manufacturer photographs, logos, wallpapers or firmware binaries are bundled. All on-screen art is original CSS. The shell is a generic visual interpretation, not OEM pixel fidelity.

Draft profiles have genuine firmware build identity unknown and human review pending. See approved ADR 014: null values are honest unknowns and runtime admission rejects them. An explicit --allow-draft flag generates only labeled visual previews. Default profile validation and the approved-profile API exclude unreviewed data; it must not be presented as a verified runtime catalog. No fabricated fingerprint or false reviewer label is used.

Screen dpi currently denotes physical PPI, including disclosed calculations for Y100/V30; it is not an Android logical-density setting. Profile base_image_id values are future mapping identifiers, not proof of installed/bootable images. No static mockup establishes actual RAM allocation, OEM firmware compatibility or device attestation.

## Runtime limitations and later gates
Redroid ARM64 only; no docker-android or /dev/kvm. No per-device disk images, /data copying, baked per-model build.prop, functional iOS or physical-device farm. Fresh containers and actual identity evidence belong to Stage D; unique IMEI/GSF/advertising IDs are not assumed if absent. No Play Integrity/SafetyNet/certification spoofing is attempted. Apps requiring certified devices may reject the runtime. Emulator results do not establish real-radio/sensor/camera/DRM/battery/thermal or hardware-performance behavior.

No Oracle resources are created until Stage D and verified nonbillable eligibility. Capacity is unmeasured, not promised. GADS lifecycle/Appium is Stage G; Magisk Stage E. Stage B static scope is accepted. Runtime evidence is separate and does not block Stage C. Stage C is planned as 20 brands × 50 rows, with diversity checked per brand. The Stage C generator is implemented; no runtime executor or provisioning runs here.

MobileAPI conservative cap 50/month; zero calls made by this work and account remaining quota unknown. API key existence is operator-confirmed; its contents were not read. Repository PUBLIC was already explicitly authorized and verified; no visibility change was needed for this stage. CI uses standard runners only, code/schema/static/browser checks, no emulator or cloud deployment.

## Stage C generation
Contract version 0.4.0 supports explicit static-only build: null and runtime_eligible: false. Generate the separate cohort with:
```sh
python scripts/generate_profiles.py data/devices.csv --require-cohort --exemptions data/devices.csv.exemptions.yaml
python scripts/validate_data.py --allow-draft
npm run build
```
Generated profiles live under profiles/generated/, preserving the 22 earlier reference profiles. The catalog defaults to reference drafts; select Generated drafts to browse the paginated collection. Sources and CSV column/line traces accompany every generated profile. All generated profiles are unreviewed static drafts; source presence is not independent technical verification. Unknown cutout geometry is explicitly marked unknown and omitted from illustration.

Per-brand exceptions and quota reallocations must be measured and recorded in data/devices.csv.exemptions.yaml. Global diversity cannot be waived. Third-party dataset attribution and source limitations accompany the source cohort; model-level popularity is unknown where public market reports expose only brand share. Do not advertise a sourced coverage order as model-level popularity.

Runtime eligibility requires complete sourced identity plus actual human review and explicit promotion. Stage E consumes only that subset. New evidence source types third_party_device_db and firmware_dump are accepted by the contract, but adding a source type does not verify a candidate. X100 China/India choice remains needs-human; no mixed-region identity is admitted. Stage D remains prepared-not-authorized until Stage C acceptance.
