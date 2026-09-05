-- ==========================================
-- Migration 011
-- Add player unlock source progress
-- ==========================================

BEGIN TRANSACTION;

CREATE TABLE player_unlock_sources (
    player_unlock_source_id INTEGER PRIMARY KEY,

    player_id INTEGER NOT NULL,

    unlock_source_id INTEGER NOT NULL,

    unlocked BOOLEAN NOT NULL DEFAULT 0,

    UNIQUE (
        player_id,
        unlock_source_id
    ),

    FOREIGN KEY(player_id)
        REFERENCES players(player_id),

    FOREIGN KEY(unlock_source_id)
        REFERENCES character_unlock_sources(unlock_source_id)
);

COMMIT;