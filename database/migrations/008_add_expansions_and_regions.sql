-- ==========================================
-- Migration 008
-- Add expansions, regions, and player world progress
-- ==========================================
BEGIN TRANSACTION;
-- ==========================================
-- EXPANSIONS
-- ==========================================
CREATE TABLE expansions (
    expansion_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    external_id TEXT UNIQUE,
    is_base_game BOOLEAN NOT NULL DEFAULT FALSE
);
-- ==========================================
-- REGIONS
-- ==========================================
CREATE TABLE regions (
    region_id INTEGER PRIMARY KEY,
    expansion_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    external_id TEXT UNIQUE,
    region_type TEXT NOT NULL,
    parent_region_id INTEGER,
    FOREIGN KEY(expansion_id) REFERENCES expansions(expansion_id),
    FOREIGN KEY(parent_region_id) REFERENCES regions(region_id),
    UNIQUE(expansion_id, name)
);
-- ==========================================
-- PLAYER REGION PROGRESS
-- ==========================================
CREATE TABLE player_regions (
    player_region_id INTEGER PRIMARY KEY,
    player_id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,
    unlocked BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY(player_id) REFERENCES players(player_id),
    FOREIGN KEY(region_id) REFERENCES regions(region_id),
    UNIQUE(player_id, region_id)
);
COMMIT;