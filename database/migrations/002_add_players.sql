-- ==========================================
-- Migration 002
-- Add player support
-- ==========================================

BEGIN TRANSACTION;


CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE player_characters (
    player_character_id INTEGER PRIMARY KEY,

    player_id INTEGER NOT NULL,
    character_id INTEGER NOT NULL,

    unlocked BOOLEAN DEFAULT FALSE,
    friendship_level INTEGER DEFAULT 0,
    assigned_role INTEGER,

    FOREIGN KEY(player_id)
        REFERENCES players(player_id),

    FOREIGN KEY(character_id)
        REFERENCES characters(character_id),

    FOREIGN KEY(assigned_role)
        REFERENCES roles(role_id),

    UNIQUE(player_id, character_id)
);


COMMIT;