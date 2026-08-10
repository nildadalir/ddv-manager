-- ==========================================
-- Migration 005
-- Add external IDs and data sources
-- ==========================================

BEGIN TRANSACTION;


-- ==========================================
-- External IDs
-- ==========================================

ALTER TABLE franchises
ADD COLUMN external_id TEXT;

ALTER TABLE characters
ADD COLUMN external_id TEXT;

ALTER TABLE roles
ADD COLUMN external_id TEXT;

ALTER TABLE items
ADD COLUMN external_id TEXT;

ALTER TABLE recipes
ADD COLUMN external_id TEXT;


-- ==========================================
-- External ID indexes
-- ==========================================

CREATE UNIQUE INDEX idx_franchises_external_id
ON franchises(external_id);


CREATE UNIQUE INDEX idx_characters_external_id
ON characters(external_id);


CREATE UNIQUE INDEX idx_roles_external_id
ON roles(external_id);


CREATE UNIQUE INDEX idx_items_external_id
ON items(external_id);


CREATE UNIQUE INDEX idx_recipes_external_id
ON recipes(external_id);


-- ==========================================
-- Data source tracking
-- ==========================================

CREATE TABLE data_sources (
    source_id INTEGER PRIMARY KEY,

    name TEXT NOT NULL UNIQUE,

    url TEXT,

    last_sync TEXT
);


COMMIT;