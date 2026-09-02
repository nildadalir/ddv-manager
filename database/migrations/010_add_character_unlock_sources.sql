-- ==========================================
-- Migration 010
-- Add character unlock sources
-- ==========================================

BEGIN TRANSACTION;

-- ==========================================
-- CHARACTER UNLOCK SOURCES
-- ==========================================

CREATE TABLE character_unlock_sources (
    unlock_source_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    source_type TEXT NOT NULL,
    external_id TEXT UNIQUE
);

-- ==========================================
-- CHARACTER ↔ UNLOCK SOURCE
-- ==========================================

CREATE TABLE character_unlock_source_links (
    character_id INTEGER NOT NULL,
    unlock_source_id INTEGER NOT NULL,

    PRIMARY KEY (
        character_id,
        unlock_source_id
    ),

    FOREIGN KEY(character_id)
        REFERENCES characters(character_id),

    FOREIGN KEY(unlock_source_id)
        REFERENCES character_unlock_sources(unlock_source_id)
);

COMMIT;