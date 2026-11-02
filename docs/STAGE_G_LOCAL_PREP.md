# Stage G — local preparation, not deployed

StageG preparation is authorized. GADS, MongoDB, Appium and UiAutomator2 are **not installed or running by this change**, no Appium session has been executed, and no nightly schedule is enabled. The prepared harness has local unit tests; integration and device registration remain future execution work.

## Topology

Run the GADS hub/provider, MongoDB, ADB and Appium together inside the existing Ubuntu UTM VM. Mac access goes through the already verified SSH endpoint127.0.0.1:2222. Port2222 is SSH, not ADB, GADS or Appium.

| Service | VM endpoint | Mac access |
|---|---|---|
| SSH | guest22 | 127.0.0.1:2222 |
| GADS hub | 127.0.0.1:10000 | SSH forward10000 |
| GADS provider | 127.0.0.1:10001 | SSH forward10001 |
| Standalone Appium | 127.0.0.1:4723 | SSH forward14723 |
| ADB server | 127.0.0.1:5037 | VM only |
| Android14 containers | 127.0.0.1:5561 and5562 | VM only, discovered through ADB |
| MongoDB | 127.0.0.1:27017 | VM only |

`infra/local-automation/topology.json` records the plan. No cloud IP, Oracle endpoint or public ADB listener is configured. The new services' memory consumption has not been benchmarked; recheck the2GiB Ubuntu reserve before enabling them. The five-container ceiling covers the Redroid pool, not a promise that every service can fit at once.

## Pinned prerequisites

GADS source is pinned to `d8abfc32e282d872a08484cd6a1e4a535c0cebe9`, not the discontinued standalone provider repository. The provider UI model and flags were checked against that commit. Build/install GADS and its local MongoDB dependency only in a separately executed StageG task.

Prepared Appium versions: **3.9.0**, UiAutomator2 driver **9.0.1**. Their official npm metadata requires npm>=10; the combined Node22 requirement is **>=22.22.2**. Plan JDK17+ and an Android SDK with platform-tools/build-tools appropriate to API34, in addition to the existing ADB binary. Versions/engine metadata are in `infra/local-automation/toolchain.json`.

Later VM commands, not executed here:

```sh
npm install --prefix "$HOME/simufarm-tools/appium" appium@3.9.0
export APPIUM_HOME="$HOME/simufarm-tools/appium-home"
"$HOME/simufarm-tools/appium/node_modules/.bin/appium" driver install uiautomator2@9.0.1
adb connect 127.0.0.1:5561
adb connect 127.0.0.1:5562
```

Use a dedicated service user and local SDK environment. Before session execution, install the previously checksum-verified sample ApiDemos APK into the selected Android14 container and confirm package io.appium.android.apis. A successful StageD Android13 install is not proof of installation in the new fresh Android14 data volumes.

## GADS provider recipe

Create the provider through **Hub Admin → Providers**, using the fields in `provider-ui-fields.json`. That file is a UI-field recipe matching upstream JSON names; GADS does not consume it via an invented `--config` flag. Android-only is enabled; iOS/TV/AVD discovery is disabled. Redroid is an ADB TCP Android device, not an Android Studio AVD.

After the local binaries/dependencies and admin account exist, the verified command shapes are:

```sh
./GADS hub --host-address=127.0.0.1 --port=10000 --auth=true --mongo-db=127.0.0.1:27017
./GADS provider --nickname=simufarm-utm --mongo-db=127.0.0.1:27017 \
  --hub=http://127.0.0.1:10000 --provider-folder=./simufarm-utm
```

Register only the selected Android14 device UDIDs127.0.0.1:5561/5562 through the hub's device UI and assign provider simufarm-utm. Verify discovery and readiness; no registration API is invented or called by this preparation. Confirm GADS streaming/proxy ports separately during integration. The recipe is not a claim that GADS has discovered these containers.

GADS may own per-device Appium servers after Setup Appium servers is enabled. Do not run a competing standalone Appium server on those same ports. The standalone smoke route below is an independent preliminary test; provider-assigned Appium endpoints must be discovered during GADS integration, not assumed to equal4723.

## Local standalone harness

When explicitly executing the later standalone check, start Appium inside the VM bound to127.0.0.1:4723 and open a foreground tunnel from the Mac:

```sh
ssh -N -p2222 -i /Users/nitinkarwauth/.ssh/simufarm_stage_d_ed25519 \
  -o BatchMode=yes -o StrictHostKeyChecking=yes -o ExitOnForwardFailure=yes \
  -o UserKnownHostsFile=/Volumes/SimuFarmDrive/SimuFarm/evidence/known_hosts \
  -L127.0.0.1:14723:127.0.0.1:4723 \
  -L127.0.0.1:10000:127.0.0.1:10000 \
  -L127.0.0.1:10001:127.0.0.1:10001 simufarm@127.0.0.1
```

`scripts/stage_g_appium_smoke.py` defaults to a plan with no network calls. It targets http://127.0.0.1:14723 and uses W3C capabilities from appium-capabilities.json. The appium:udid is the VM-local ADB endpoint because Appium runs in the VM. For a second simultaneous standalone session use a separate Appium server/tunnel and unique systemPort8202; the default harness intentionally supports only the first local endpoint.

An explicit `--execute` checks server readiness, creates a UiAutomator2 ApiDemos session, captures XML and a screenshot, deletes the session even on failure, and writes result.json under ignored local evidence. It does not start/stop Redroid containers, register GADS devices or prove GADS integration. No execution flag was used in this preparation.

## Lifecycle work prepared for execution

`tasks/stage-g-local-lifecycle.yaml` records the remaining thin executor: enforce reviewed profiles and the shared capacity ceiling; start one fresh container; wait for ADB and Android completion; make it available to the provider; run the Appium task; deregister/disconnect and tear down only the owned container in finally. Do not clone data volumes. GADS does not create or destroy Redroid containers itself. Pool locking, queue overflow, results persistence/API and nightly execution are later StageG implementation work.

Primary sources: [GADS provider guide](https://github.com/shamanec/GADS/blob/d8abfc32e282d872a08484cd6a1e4a535c0cebe9/docs/provider.md), [hub flags](https://github.com/shamanec/GADS/blob/d8abfc32e282d872a08484cd6a1e4a535c0cebe9/docs/hub.md), [provider model](https://github.com/shamanec/GADS/blob/d8abfc32e282d872a08484cd6a1e4a535c0cebe9/common/models/config.go), [official UiAutomator2 setup](https://appium.github.io/appium-uiautomator2-driver/latest/getting-started/).
