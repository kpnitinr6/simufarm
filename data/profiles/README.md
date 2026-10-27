# Device profile source of truth
Only schema 0.2.0 human-reviewed profiles belong here as *.json. None are present.
source_type=api|scraper|manual is required. Scraper confidence must remain <0.9; actual human review/evidence is required even at low confidence. API/manual profiles need >=0.9 and human review. Every technical field needs source mappings and reviewer evidence in data/sources/<id>.evidence.json.
The original _targets.yaml approval is static-only and explicitly not extraction authorization. The separate top100 proposal remains unapproved. Names are not verified dimensions. iOS visual proposal is iPhone-only. Do not populate profiles from invented specs or unverified reviewer claims.
