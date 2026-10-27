CREATE TABLE device_profiles (
 id text PRIMARY KEY,
 profile jsonb NOT NULL,
 revision text NOT NULL,
 updated_at timestamptz NOT NULL DEFAULT now(),
 CHECK (profile->>'id' = id),
 CHECK (profile->>'verified_by' = 'human')
);
CREATE INDEX device_profiles_brand_idx ON device_profiles ((profile->>'brand'));
CREATE INDEX device_profiles_document_idx ON device_profiles USING gin(profile);
CREATE TABLE simulator_manifests (
 simulator_id text PRIMARY KEY,
 profile_id text NOT NULL REFERENCES device_profiles(id),
 manifest jsonb NOT NULL,
 CHECK (manifest->>'simulator_id' = simulator_id),
 CHECK (manifest->>'profile_id' = profile_id)
);
CREATE TABLE test_runs (
 id uuid PRIMARY KEY,
 simulator_id text NOT NULL REFERENCES simulator_manifests(simulator_id),
 status text NOT NULL CHECK (status IN ('queued','running','passed','failed')),
 result_ref text,
 created_at timestamptz NOT NULL DEFAULT now()
);
