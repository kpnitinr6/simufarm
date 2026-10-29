import base64
import configparser
import email.utils
import hashlib
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlencode

c = None
region = None


def configure():
    global c, region
    cfg = configparser.ConfigParser()
    cfg.read(Path.home() / ".oci/config")
    c = cfg["DEFAULT"]
    region = c["region"]
    return c, region


class OCIError(Exception):
    def __init__(self, status, data):
        self.status = status
        self.data = data
        super().__init__(str(status) + " " + str(data))


def call(service, path, body=None, method=None, extra=None):
    if c is None:
        configure()
    host = (
        f"iaas.{region}.oraclecloud.com"
        if service == "iaas"
        else f"{service}.{region}.oci.oraclecloud.com"
    )
    method = method or ("GET" if body is None else "POST")
    date = email.utils.formatdate(usegmt=True)
    headers = {"date": date, "host": host}
    signed = ["date", "(request-target)", "host"]
    lines = [f"date: {date}", f"(request-target): {method.lower()} {path}", f"host: {host}"]
    data = None
    if body is not None:
        data = json.dumps(body, separators=(",", ":")).encode()
        headers.update(
            {
                "x-content-sha256": base64.b64encode(hashlib.sha256(data).digest()).decode(),
                "content-type": "application/json",
                "content-length": str(len(data)),
            }
        )
        for key in ["x-content-sha256", "content-type", "content-length"]:
            signed.append(key)
            lines.append(f"{key}: {headers[key]}")
    sig = base64.b64encode(
        subprocess.run(
            [
                "openssl",
                "dgst",
                "-sha256",
                "-sign",
                str(Path(c["key_file"]).expanduser()),
                "-passin",
                "env:SIMUFARM_OCI_SIGN_PASSPHRASE",
            ],
            input="\n".join(lines).encode(),
            capture_output=True,
            check=True,
            env=dict(os.environ, SIMUFARM_OCI_SIGN_PASSPHRASE=c.get("pass_phrase", "")),
        ).stdout
    ).decode()
    headers["Authorization"] = (
        f'Signature version="1",keyId="{c["tenancy"]}/{c["user"]}/{c["fingerprint"]}",algorithm="rsa-sha256",headers="{" ".join(signed)}",signature="{sig}"'
    )
    headers.update(extra or {})
    req = urllib.request.Request(
        "https://" + host + path, data=data, headers=headers, method=method
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return json.load(res), dict(res.headers)
    except urllib.error.HTTPError as e:
        try:
            d = json.load(e)
        except (ValueError, UnicodeDecodeError):
            d = {"code": "Unknown", "message": e.reason}
        raise OCIError(e.code, d) from None


def get(service, path):
    return call(service, path)[0]


def listing(service, path, params):
    result = []
    while True:
        d, h = call(service, path + "?" + urlencode(params))
        result.extend(d)
        page = next((v for k, v in h.items() if k.lower() == "opc-next-page"), None)
        if not page:
            return result
        params = dict(params, page=page)
