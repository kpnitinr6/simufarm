import argparse
import json
import subprocess
from pathlib import Path

from simufarm_schema import DeviceProfile, SimulatorManifest

root = Path(__file__).resolve().parents[1]
check = argparse.ArgumentParser()
check.add_argument("--check", action="store_true")
args = check.parse_args()
base = root / "packages/device-schema"
for model in (DeviceProfile, SimulatorManifest):
    path = base / "json-schema" / f"{model.__name__}.json"
    content = json.dumps(model.model_json_schema(), indent=2) + "\n"
    if args.check:
        assert path.read_text() == content, f"Schema drift: {path}"
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
parts = []
for name in ("DeviceProfile", "SimulatorManifest"):
    result = subprocess.run(
        [
            str(root / "node_modules/.bin/json2ts"),
            "--input",
            str(base / f"json-schema/{name}.json"),
            "--additionalProperties",
            "false",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    parts.append(result.stdout)
# Separate modules avoid duplicate nested interface names.
for name, content in zip(("DeviceProfile", "SimulatorManifest"), parts):
    path = base / "src" / f"{name}.d.ts"
    if args.check:
        assert path.read_text() == content, f"Type drift: {path}"
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
index = 'export type { DeviceProfile } from "./DeviceProfile";\nexport type { SimulatorManifest } from "./SimulatorManifest";\n'
if args.check:
    assert (base / "src/index.d.ts").read_text() == index
else:
    (base / "src/index.d.ts").write_text(index)
