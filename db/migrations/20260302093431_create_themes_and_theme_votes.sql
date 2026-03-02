-- migrate:up
CREATE TABLE themes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text UNIQUE NOT NULL,
  is_selected BOOLEAN NOT NULL DEFAULT FALSE,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX unique_selected_theme ON themes (is_selected) WHERE is_selected = TRUE;

CREATE TABLE theme_votes (
  user_id uuid NOT NULL,
  theme_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (theme_id) REFERENCES themes(id) ON DELETE CASCADE,
  UNIQUE (user_id, theme_id)  -- Ensures a user can vote once per theme
);

-- migrate:down

DROP TABLE themes;
DROP INDEX unique_selected_theme;
DROP TABLE theme_votes;
