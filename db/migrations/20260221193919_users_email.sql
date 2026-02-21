-- migrate:up
ALTER TABLE users
  ADD COLUMN email VARCHAR(255);

UPDATE users
SET email = name;

ALTER TABLE users
  ALTER COLUMN email SET NOT NULL,
  ADD CONSTRAINT users_email_unique UNIQUE (email),
  DROP COLUMN name;

-- migrate:down
ALTER TABLE users
  ADD COLUMN name VARCHAR(255);

UPDATE users
SET name = email;

ALTER TABLE users
  DROP COLUMN email;
