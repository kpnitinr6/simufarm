# SimuFarm status — 2 November 2026

StageD and StageE accepted. The user selected real Redroid14 plus a genuine China X100 Android14 fingerprint, then authorized runtime promotion and PR9 merge after validation. Two fresh containers and both restarts passed actual release14, SDK34 and unmodified`:14/` fingerprint checks. Serial and synthetic IMEI properties differ and persist. First boots10.158s/16.854s; restarts9.424s/9.254s; after-restart Docker RAM625.6MiB/610.5MiB. See docs/STAGE_E_IDENTITY.md and docs/CAPACITY.md.

**Human-reviewed runtime-eligible subset:1 — vivo-x100, China V2309A/PD2309/vivo.** The previous India reference is archived separately. Other reference/generated drafts retain their review state; all1000generated drafts still build:null/runtime_eligible:false. Production admission uses the existing review/schema policy. The isolated rehearsal profile remains false.

Local Ubuntu22.04 ARM64 UTM VM:4CPUs/8GiB on external-drive storage, SSH localhost2222, Docker and Binder/ashmem verified. Four containers currently run: historical StageD13pair plus new StageE14pair. Old StageE13pair is stopped and retained. Configured ceiling5,2GiB Ubuntu reserve; five-way workload capacity unbenchmarked. Post-test MemAvailable3,549,794,304bytes.

Telephony limitation: getprop IMEI works, cellular services do not. The service probe returns no usable IMEI. Matching release/SDK/fingerprint does not reproduce Vivo firmware, hardware, OEM APIs or certified-device behavior. README documents this.

PR9 MERGED on2November2026 after green Python3.12/Node22 CI:115Python tests and19browser tests. Merge ddb0c62990f09fca4f9ca301352abd1040cca728 into the existing UTM branch agent/codex/stage-d-utm-local; The parent PR8/PR7 stack remains open; this merge does not put the UTM branch into main. No other PR was merged.

StageF IMPLEMENTED in the separate follow-up: mock status/time, keyboard/text input, rotation and dark mode on all20brand shells, available on1022currently rendered pages (22references plus1000generated drafts; not a verified-device count). All26local browser tests pass, including7new interaction checks and all20brand traversal. Warm local navigation-to-controls-ready maximum70ms across20brands; real Android/app TTI is not measured. Six screenshots saved and visually inspected.

StageG PREPARATION COMPLETE in the follow-up, not deployed. Local-only topology, pinned GADS/UiAutomator2/Appium prerequisites, provider UI-field recipe, W3C capabilities, plan-only smoke harness and thin lifecycle task are prepared. SSH2222 forwards to separate service ports. No GADS/Appium service was installed/started, no Appium/APK session was run, no nightly task was enabled, and full StageG DoD is not claimed. Local Python tests121passed. Implementation CI run41455739854 passed onPython3.12/Node22 with121Python and26browser tests; the final documentation update changes no executable code. Draft PR10 awaits StageF/G review and is not merged.

Oracle launch scripts remain disabled, ADR015 superseded. Zero Oracle/MobileAPI calls and zero paid resources touched during this work. Ordinary SSH permissions remain unchanged; specific administrative VM diagnostics use the existing UTM guest agent. C2 and seven C2.1unknown-geometry deviations were previously accepted; integration from the other data branches remains separate, with no new catalog-quality claim here.
