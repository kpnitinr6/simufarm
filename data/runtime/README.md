# Runtime evidence

No runtime observations have been collected. Do not add placeholder identity JSON or fabricated measurements.

After authorized execution, each new run directory contains `observations.json` with host/image metadata, two container records, boot seconds, measured RAM, APK hash/install output, ADB state, observed Android IDs/IMEI/serial/ADB serials, raw property/service-call output, and explicit pass/failure checks. Missing/identical identity values fail the run. ADB serial is the connection endpoint; Android serial is `ro.serialno`.

Treat observed device identifiers as sensitive operational evidence: review/redact before publishing this public repository. Keep unredacted files in ignored/private storage when necessary; commit sanitized measurements and hashes with disclosure noted. Never store credentials, private SSH keys, tenancy configs, or billing exports here.
