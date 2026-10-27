Evidence sidecar format (required before any profile promotion):
- profile_id, reviewer identity, reviewed_at (timezone-aware ISO8601), approval reference.
- fields: map every leaf path (screen.width_px, body.width_mm, etc.) to source URL,
  source excerpt/reference, retrieval date, and extraction method.
- Distinguish model-level facts from configurable RAM/storage variants.
- Store only permitted reference material; do not mirror branded assets.
P2 must add executable evidence validation and a review queue before extraction is promoted.
