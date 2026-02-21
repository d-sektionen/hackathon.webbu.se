-- migrate:up
CREATE TABLE sessions (
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token uuid NOT NULL DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
);

-- migrate:down
DROP TABLE sessions;
