Evidence sidecar format (required before any profile promotion):
- profile_id, reviewer identity, reviewed_at (timezone-aware ISO8601), approval reference.
- fields: map every leaf path (screen.width_px, body.width_mm, etc.) to source URL,
  source excerpt/reference, retrieval date, and extraction method.
- Distinguish model-level facts from configurable RAM/storage variants.
- Store only permitted reference material; do not mirror branded assets.
P2 must add executable evidence validation and a review queue before extraction is promoted.

Schema 0.2.0 additionally requires source_type. Scraped data retains confidence<0.9 after human review; review approval and source confidence are separate. API/manual promotion still requires confidence>=0.9. No source truth is proved by a JSON label.
