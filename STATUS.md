# SimuFarm status — 2 November 2026

StageD and StageE accepted. The user selected real Redroid14 plus a genuine China X100 Android14 fingerprint, then authorized runtime promotion and PR9 merge after validation. Two fresh containers and both restarts passed actual release14, SDK34 and unmodified`:14/` fingerprint checks. Serial and synthetic IMEI properties differ and persist. First boots10.158s/16.854s; restarts9.424s/9.254s; after-restart Docker RAM625.6MiB/610.5MiB. See docs/STAGE_E_IDENTITY.md and docs/CAPACITY.md.

**Human-reviewed runtime-eligible subset:1 — vivo-x100, China V2309A/PD2309/vivo.** The previous India reference is archived separately. Other reference/generated drafts retain their review state; all932generated static profiles still build:null/runtime_eligible:false. Production admission uses the existing review/schema policy. The isolated rehearsal profile remains false.

Local Ubuntu22.04 ARM64 UTM VM:4CPUs/8GiB on external-drive storage, SSH localhost2222, Docker and Binder/ashmem verified. Four containers currently run: historical StageD13pair plus new StageE14pair. Old StageE13pair is stopped and retained. Configured ceiling5,2GiB Ubuntu reserve; five-way workload capacity unbenchmarked. Post-test MemAvailable3,549,794,304bytes.

Telephony limitation: getprop IMEI works, cellular services do not. The service probe returns no usable IMEI. Matching release/SDK/fingerprint does not reproduce Vivo firmware, hardware, OEM APIs or certified-device behavior. README documents this.

PR9 update is undergoing final CI before the authorized merge. StageF interactive chrome and local StageG harness preparation are a separate follow-up change. No GADS/Appium service deployment, APK session, nightly schedule or StageG completion is claimed.

Oracle launch scripts remain disabled, ADR015 superseded. Zero Oracle/MobileAPI calls and zero paid resources touched during this work. Ordinary SSH permissions remain unchanged; specific administrative VM diagnostics use the existing UTM guest agent. C2 and seven C2.1unknown-geometry deviations were previously accepted; integration from the other data branches remains separate, with no new catalog-quality claim here.
