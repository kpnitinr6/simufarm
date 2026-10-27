# Emulator and GADS compatibility review

Reviewed 27 October 2026. **Source review only: no Docker pulls, deployment, emulator boot, benchmarks, or specification extraction occurred.** Upstream branch URLs are mutable; pin a commit and image digest before validation.

## Blocking compatibility finding

The unmodified `budtmo/docker-android` emulator path cannot be treated as a working Oracle ARM/no-KVM solution. Its [image Dockerfile](https://raw.githubusercontent.com/budtmo/docker-android/master/docker/emulator/Dockerfile) installs an **x86_64** guest image. Native Linux ARM64 support was not established; no registry manifest was inspected. Its [launcher](https://raw.githubusercontent.com/budtmo/docker-android/master/cli/src/device/emulator.py) checks `/dev/kvm`, throws if absent, and requests CPU acceleration before startup. Passing `-no-accel` through extra arguments cannot skip that earlier check. This is a source-based blocker, not a measured boot result.

[Android documentation](https://developer.android.com/studio/run/emulator-acceleration) distinguishes GPU rendering from VM acceleration. SwiftShader renders graphics in software; it does not provide CPU virtualization or turn an x86 image into an ARM image. The current guide deprecates `swiftshader_indirect`. The [CLI reference](https://developer.android.com/studio/run/emulator-commandline) also lists `-no-accel` as deprecated, with behavior dependent on the installed version. A separate custom software-emulation solution remains research work; neither viability nor usable latency on Oracle ARM is established.

## Upstream documented invocation

The [budtmo quick start](https://github.com/budtmo/docker-android) supplies this example, shown for review only:

```sh
docker run -d -p 6080:6080 \
  -e EMULATOR_DEVICE="Samsung Galaxy S10" -e WEB_VNC=true \
  --device /dev/kvm --name android-container \
  budtmo/docker-android:emulator_11.0
```

It assumes a suitable Ubuntu environment and working virtualization. It is not an ARM/no-KVM command, a pinned production deployment, or a successful local validation. [Custom configuration](https://raw.githubusercontent.com/budtmo/docker-android/master/documentations/CUSTOM_CONFIGURATIONS.md) supports `EMULATOR_ADDITIONAL_ARGS`; that is an argument extension interface, not a documented bypass of the launch preconditions.

## GADS prerequisites and lifecycle

The [GADS README](https://raw.githubusercontent.com/shamanec/GADS/main/README.md) requires MongoDB and recommends version 6.0. It also identifies a separately licensed proprietary `hub-ui`; assess that license before redistribution or UI modification. The existing PostgreSQL and Redis services do not satisfy GADS database requirements.

The [Hub guide](https://raw.githubusercontent.com/shamanec/GADS/main/docs/hub.md) requires a running MongoDB instance and at least one Provider to expose devices. Provider configuration is created through the Hub. An embedded Appium grid avoids requiring a separate Selenium Grid.

The [Provider guide](https://raw.githubusercontent.com/shamanec/GADS/main/docs/provider.md) requires ADB for Android. Enable its Android emulator option to discover running AVDs. GADS **adopts existing emulators and does not launch or terminate them**. Appium, its Android driver, SDK and Java dependencies are additionally needed for test execution. Ephemeral emulator rows are not stored as device configurations, but this does not remove the overall MongoDB requirement. A separate lifecycle owner must start and stop emulator processes.

Container-to-Provider ADB discovery, AVD identity, remote streaming, and Appium routing remain untested integration steps. An exposed container ADB TCP port alone does not prove that GADS recognizes it through its emulator discovery path.

## Recommended ADR updates and release gates

1. Record Oracle ARM/no-KVM plus the unmodified budtmo image as **blocked**, with no promised boot or concurrent-session capacity. Permit a separate research alternative only after architecture, binary, image and runtime evidence exists.
2. Treat static device visuals and live Android runtimes as separate capability tiers. Visual availability does not imply a runnable vendor firmware image.
3. If GADS remains selected, add MongoDB and a separately owned emulator lifecycle component to the design. Pin versions and resolve UI licensing/distribution scope.
4. Require host architecture and `/dev/kvm` evidence, pinned image manifest inspection, emulator boot completion, ADB visibility, streaming and Appium smoke tests before claiming the native runtime path green. A no-KVM alternative needs its own measured acceptance test.

Machine-readable findings: `data/sources/emulator-compatibility.json`. None of these findings authorizes provisioning.
