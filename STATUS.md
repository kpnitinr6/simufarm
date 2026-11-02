# SimuFarm — final local handoff, 2 November 2026

The authorized closeout scope is complete. PR4,5,6,7,8and10are merged into main; PR9was merged into PR8and is included in main. StageD/E are complete locally, StageF is complete, StageG is prepared and its authorized manual GADS-managed Appium test passed. StageH handoff documentation and startup/shutdown helpers are finalized. The final handoff change has its own CI/merge record.

| Counter | Final state |
|---|---:|
| Generated static candidate profiles | 932 |
| Retained reference profiles | 22 |
| Current profiles / HTML pages, including references | 954 /954 |
| Reference profiles eligible for runtime | 1: vivo-x100 China |
| Brand shells / templates | 20 /20 |
| Running project containers / automation services | 0 /0 |
| UTM VM | Stopped; data retained |
| Redroid planning ceiling | 5 concurrent,2GiB Ubuntu reserve |
| Oracle calls / MobileAPI calls / paid resources in closeout | 0 /0 /0 |

The932static profiles are retained sourced candidates, not a blanket claim that every specification is independently verified. The earlier duplicate-free claim was incorrect:68records were removed or merged, with no padding. Source checks cover105models for documented fields. Known cutout coverage100/932; unknown geometry remains unknown. Generated profiles still build:null/runtime_eligible:false. The21other reference profiles remain unpromoted; only vivo-x100 China has complete reviewed build identity and runtime eligibility.

Local runtime: Ubuntu22.04 ARM64 UTM,4CPU/8GiB, external-drive128GiB sparse disk. Official Redroid14 ARM64 64-only; actual14/SDK34and genuine China`:14/`fingerprint match. Distinct synthetic serial/IMEI properties persist across restart. StageE first boots10.158s/16.854s, restarts9.424s/9.254s, after-restart RAM625.6MiB/610.5MiB. Five-way workload capacity remains unbenchmarked.

**Manual Appium PASS:13.631s.** GADS v6.1.0ARM64, Appium3.9.0, UiAutomator2 8.7.3, ApiDemos Views→Buttons→Normal, native screenshot/XML, successful session deletion. Proof: docs/proof/appium-test-results.md. GADS/Appium/hub/MongoDB/tunnel stopped. Android-aware final shutdowns used private PID namespaces, no Docker-stop fallback, exit130. The VM is stopped and no project service autostarts; only a non-daemon kernel-preparation oneshot is enabled for future boots.

**Developer quick-start PASS:326.985s** from a stopped prepared VM through VM startup, SSH and a fresh pair's boot/restart identity checks. Cached prerequisites; fresh OS installation/download time excluded. An early cold-boot ADB timeout was corrected with bounded readiness retry and a regression test. Quick Start: docs/QUICK_START.md.

StageF: mock status/time, keyboard, rotation and dark mode across20brand shells and954current pages;26browser tests, including all20brands and mobile checks. Local HTML control readiness maximum70ms on a warm server; not Android/app TTI. StageG's full production queue/result API/nightly extensions are not claimed or enabled by the manual test.

Telephony is non-functional despite getprop IMEI. Play Integrity/SafetyNet is unsupported and should be assumed failing/unavailable on this uncertified emulated runtime; no attestation result was fabricated. No handset hardware or OEM firmware equivalence is claimed. See README limitations and docs/FINAL_HANDOFF.md for inventory and evidence.
