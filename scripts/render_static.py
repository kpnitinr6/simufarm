"""Deterministic Stage A page generation, not the Stage C CSV profile generator."""

import argparse
import html
import json
from pathlib import Path

from simufarm_schema import DeviceProfile, is_review_approved

ROOT = Path(__file__).resolve().parents[1]

SITE_CSS = """*{box-sizing:border-box}body{margin:0;background:#f6f7fb;color:#202738;font:15px/1.6 system-ui,-apple-system,sans-serif}a{color:#4058bc;text-decoration:none}header{max-width:1160px;margin:auto;padding:27px 36px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #e0e4ee}.wordmark{font-size:20px;font-weight:750;letter-spacing:-.7px;color:#202738}.wordmark span{color:#6f66d8}.pill{border:1px solid #dedfee;color:#736696;font-size:10px;letter-spacing:1.5px;padding:6px 12px;border-radius:20px}.layout{max-width:1060px;margin:48px auto;display:grid;grid-template-columns:1.1fr 1fr;gap:76px;align-items:center;padding:0 36px}.device-stage{padding:36px 50px 47px;background:radial-gradient(ellipse at 50% 60%,#e3ddf4,#edf1f8 70%);border-radius:28px;position:relative}.device-stage::after{content:'ORIGINAL CSS ARTWORK';display:block;text-align:center;font-size:9px;letter-spacing:2px;color:#8b8ba0;margin-top:26px}.kicker{font-size:10px;font-weight:700;letter-spacing:2px;color:#7c73ac}.detail h1{font-size:62px;font-weight:550;line-height:1.1;letter-spacing:-3px;margin:17px 0 20px}.detail h1 small{display:block;font-size:25px;font-weight:400;letter-spacing:-.5px;color:#85899c;margin-bottom:6px}.lead{font-size:16px;color:#71788c;max-width:360px}.specs{display:grid;grid-template-columns:1fr 1fr;gap:24px 16px;padding:26px 0;border-top:1px solid #e0e4ee;border-bottom:1px solid #e0e4ee;margin:28px 0}.specs dt{font-size:10px;text-transform:uppercase;letter-spacing:1.3px;color:#8b90a1}.specs dd{margin:6px 0 0;font-size:17px;color:#394054}.notice{font-size:12px;color:#767085;background:#eeebf5;border-radius:10px;padding:14px 16px}.sources{font-size:11px;margin-top:22px}.sources a{display:block;margin-top:4px}footer{max-width:1160px;margin:35px auto;padding:0 36px 25px;font-size:11px;color:#969bac;display:flex;justify-content:space-between}@media(max-width:760px){.layout{grid-template-columns:1fr;gap:28px;margin-top:24px;padding:0 22px}.device-stage{padding:30px 40px}.detail h1{font-size:48px}header{padding:20px 22px}.pill{font-size:8px}footer{padding:0 22px;display:block}}"""


def write_if_changed(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text() != content:
        path.write_text(content)


def render_page(profile: DeviceProfile) -> str:
    e = html.escape
    p = profile
    review = "Human-reviewed" if is_review_approved(p) else "Human review pending"
    source_links = "".join(
        f'<a href="{e(str(url), quote=True)}" rel="noreferrer">Manufacturer source {i + 1} ↗</a>'
        for i, url in enumerate(p.sources)
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>vivo {e(p.model)} — SimuFarm</title><link rel="stylesheet" href="../assets/static.css"><script type="module" src="../assets/shells/vivo/shell.js"></script></head>
<body><header><a class="wordmark" href="../">simu<span>farm</span></a><span class="pill">STAGE A / STATIC PROOF</span></header>
<main class="layout"><section class="device-stage" aria-label="Device preview"><vivo-shell model="{e(p.model, quote=True)}" screen-width="{p.screen.width_px}" screen-height="{p.screen.height_px}" notch="{p.notch.type}"></vivo-shell></section>
<section class="detail"><span class="kicker">ONE SHELL. THREE PROFILES.</span><h1><small>vivo</small>{e(p.model)}</h1><p class="lead">A static device preview, built from an original web shell and a sourced India-market profile.</p>
<dl class="specs"><div><dt>Resolution</dt><dd>{p.screen.width_px} × {p.screen.height_px}</dd></div><div><dt>Android</dt><dd>{e(p.os_version)}</dd></div><div><dt>Physical density*</dt><dd>{p.screen.dpi:g} PPI</dd></div><div><dt>Hardware RAM</dt><dd>{p.ram_gb:g} GB</dd></div></dl>
<p class="notice">{review}. Build identity is unknown; runtime is disabled. This is original artwork, not a Funtouch OS screenshot.</p><div class="sources">*Physical PPI; Y100/V30 values are calculated from manufacturer resolution and diagonal. Not Android logical DPI.{source_links}</div></section></main>
<footer><span>SOFTWARE ONLY · NO HANDSETS · NO CLOUD RESOURCES</span><span>India variant · {p.release_year}</span></footer></body></html>
"""


def generate(profile_dir: Path, output: Path, *, allow_draft=False, root=ROOT):
    profiles = []
    for path in sorted(profile_dir.rglob("*.json")):
        if "_templates" in path.parts:
            continue
        p = DeviceProfile.model_validate_json(path.read_text())
        if p.shell_id != "vivo":
            raise ValueError("Only the Stage A Vivo shell is implemented")
        if not allow_draft and not is_review_approved(p):
            raise ValueError(
                "Human review required; use explicit --allow-draft for labeled previews"
            )
        if p.id != path.stem:
            raise ValueError("Profile filename identity mismatch")
        profiles.append(p)
    if len({p.id for p in profiles}) != len(profiles):
        raise ValueError("Duplicate profile identities")
    # All profiles are validated before output writes.
    catalog = []
    for p in profiles:
        write_if_changed(output / "simulators" / f"{p.id}.html", render_page(p))
        data = p.model_dump(mode="json", by_alias=True)
        write_if_changed(output / "profiles" / f"{p.id}.json", json.dumps(data, indent=2) + "\n")
        catalog.append(
            {
                **data,
                "url": f"/simulators/{p.id}.html",
                "review_status": "human-reviewed" if is_review_approved(p) else "needs-human",
            }
        )
    write_if_changed(output / "catalog.json", json.dumps(catalog, indent=2) + "\n")
    write_if_changed(output / "assets/static.css", SITE_CSS + "\n")
    for name in ("shell.html", "shell.css", "shell.js", "meta.json"):
        write_if_changed(
            output / "assets/shells/vivo" / name, (root / "shells/vivo" / name).read_text()
        )
    return len(profiles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", type=Path, default=ROOT / "profiles")
    parser.add_argument("--output", type=Path, default=ROOT / "apps/web/public")
    parser.add_argument("--allow-draft", action="store_true")
    args = parser.parse_args()
    print(
        f"Generated {generate(args.profiles, args.output, allow_draft=args.allow_draft)} static preview pages"
    )
