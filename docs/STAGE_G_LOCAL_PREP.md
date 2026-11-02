# Stage G — prepared and manually validated locally

The authorized local manual test is complete: GADS's provider-managed Appium server ran ApiDemos successfully in **13.631seconds**. [Proof and artifacts](proof/appium-test-results.md). Services and project containers were stopped afterward. This establishes the sample path; production queue scheduling, nightly execution and a persisted results API are future extensions.

## Tested topology

All runtime services ran inside the existing Ubuntu22.04 ARM64 UTM VM. The Mac used the verified SSH connection on127.0.0.1:2222. Port2222 is SSH, not ADB or Appium.

| Component | VM endpoint during test | Mac access |
|---|---|---|
| GADS hub | 127.0.0.1:10000 | Optional SSH forward10000 |
| GADS provider | 127.0.0.1:10001 | Optional SSH forward10001 |
| GADS-managed Appium | 127.0.0.1:41229, dynamically allocated | SSH forward14723 |
| ADB server | 127.0.0.1:5037 | VM only |
| Android14 X100 | 127.0.0.1:5561 | VM only, through ADB |
| MongoDB7 | 127.0.0.1:27017 | VM only |

Do not reuse41229as a guaranteed future port: read the provider's actual assigned port from its startup log. Standalone4723in the topology template is a separate example, not the tested GADS-owned endpoint.

## Verified tools

- GADS v6.1.0, source commit d8abfc32e282d872a08484cd6a1e4a535c0cebe9. Official Linux binary is x86-64, so the source was built for Linux ARM64 with Go1.26.10.
- Official release UI archive SHA25629516b50ed109d5a040e75a908aed9d90a29599bf020a1c5463341151d96a0a0, extracted under hub-ui/build before the tagged UI build.
- Node22.22.2, Appium3.9.0, UiAutomator2driver8.7.3, OpenJDK17 and native Ubuntu ARM64 Android build-tools29.0.3 with ANDROID_HOME=/usr/lib/android-sdk.
- Local pinned GADS Appium plugin0.0.13. Its declared npm dependencies must exist in the local source folder before installing it through Appium.
- Mongo image pinned in infra/local-automation/toolchain.json, loopback-only, memory512MiB and WiredTiger cache0.25GiB.

The preparation's UiAutomator2v9/Appium3pair was incompatible: v9requires Appium4. The executed/tested pair is8.7.3/3.9.0. Do not reinstall the old incompatible combination.

## Reproduce prerequisites

Use local user-owned tool directories; no Docker-group or unrestricted sudo grant is needed. In the VM, after the one-time administrator installs Java, git, native Android tools and Docker:

```sh
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
export ANDROID_HOME=/usr/lib/android-sdk
export ANDROID_SDK_ROOT="$ANDROID_HOME"
export APPIUM_HOME="$HOME/tools/appium-home"
# Put the verified Node22and Go1.26tool directories on PATH first.
npm install --prefix "$HOME/tools/appium" appium@3.9.0
export PATH="$HOME/tools/appium/node_modules/.bin:$PATH"
appium driver install uiautomator2@8.7.3

git clone --depth 1 --branch v6.1.0 https://github.com/shamanec/GADS.git "$HOME/tools/GADS-source"
cd "$HOME/tools/GADS-source"
git rev-parse HEAD  # must equal the pinned commit above
# Fetch the official ui-files.zip, verify its SHA256, and extract its build/ under hub-ui/.
go run github.com/swaggo/swag/cmd/swag@v1.16.4 init -g hub/hub.go -o docs
go build -p 2 -tags ui -ldflags '-X main.AppVersion=v6.1.0-simufarm-arm64' -o "$HOME/tools/GADS" .
npm install --prefix ./appium-plugin --omit=dev --ignore-scripts
appium plugin install --source=local "$HOME/tools/GADS-source/appium-plugin"
```

Download hashes for the toolchain used here are recorded in the local setup evidence; versions and the Mongo digest are committed. The source's own Swagger step is required: skipping it produces the missing GADS/docs build error observed during setup.

## Provider and virtual-device registration

`provider-ui-fields.json` matches upstream provider field names. Configure it through authenticated Hub Admin → Providers, or seed the same fields in the dedicated local test MongoDB gads.providers collection. The tested virtual-device entry in gads.new_devices used UDID127.0.0.1:5561, OSandroid, provider simufarm-utm, usage automation and device_type emulator. Automatic AVD discovery remained disabled: Redroid was explicitly registered as an ordinary ADB TCP endpoint, not an Android Studio AVD or physical handset. The hub assigned its default workspace.

Start the hub/provider after local registration and an actual Android14 boot/APK install:

```sh
./GADS hub --host-address=127.0.0.1 --port=10000 --auth=true --mongo-db=127.0.0.1:27017
./GADS provider --nickname=simufarm-utm --mongo-db=127.0.0.1:27017 \
  --hub=http://127.0.0.1:10000 --provider-folder=./provider --log-level=debug
```

Keep credentials local. GADS provider manages its own Appium instance; do not start a competing server on the same port. Confirm GET /device/127.0.0.1:5561/info on the provider reports provider_state live and is_appium_up true before testing.

The local compatibility wrapper is `scripts/local_appium_wrapper.py`. Install/copy it as appium in a dedicated bin directory before the real binary on the provider's PATH. Set SIMUFARM_APPIUM_REAL to the real Appium executable and SIMUFARM_APPIUM_LOG to a local log path. It normalizes --use-plugin=gads to --use-plugins=gads and enforces address127.0.0.1 for server startup; driver/plugin-management commands pass through unchanged. The captured startup log confirmed gads0.0.13 ACTIVE and provider registration. GADS enables relaxed security for its managed Appium server; this tested route is local-only.

## Execute the sample

Install the official checksum-verified ApiDemos-debug.apk into the selected container. See [proof](proof/appium-test-results.md) for its source hash. On the Mac, forward the actual GADS Appium port:

```sh
ssh -N -p2222 -i /path/to/your/key \
  -o BatchMode=yes -o StrictHostKeyChecking=yes -o ExitOnForwardFailure=yes \
  -o UserKnownHostsFile=/path/to/verified/known_hosts \
  -L127.0.0.1:14723:127.0.0.1:ACTUAL-APPIUM-PORT simufarm@127.0.0.1
```

In a second Mac terminal:

```sh
python scripts/stage_g_appium_smoke.py --execute --gads-managed \
  --output data/runtime/local/my-appium-run
```

Without --execute it only prints a plan. The harness uses W3C capabilities, confirms the ApiDemos hierarchy, clicks Views→Buttons→Normal, captures screenshot/XML, deletes the session even on failure and writes result.json with pass/fail and elapsed time. This uses the GADS-owned per-device Appium server directly; the GADS grid queue endpoint was not exercised.

Afterward, stop the provider/Appium process group and hub, stop MongoDB, close the owned SSH tunnel and shut down the specifically owned Redroid containers with the namespace-guarded utility in the quick-start guide. Retain the result artifacts. No nightly schedule is enabled.

Primary sources: [pinned provider guide](https://github.com/shamanec/GADS/blob/d8abfc32e282d872a08484cd6a1e4a535c0cebe9/docs/provider.md), [hub flags](https://github.com/shamanec/GADS/blob/d8abfc32e282d872a08484cd6a1e4a535c0cebe9/docs/hub.md), [UiAutomator2 compatibility](https://appium.github.io/appium-uiautomator2-driver/latest/getting-started/).
