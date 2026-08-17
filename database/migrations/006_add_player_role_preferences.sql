-- ==========================================
-- Migration 006
-- Add player role preferences
-- ==========================================

BEGIN TRANSACTION;


CREATE TABLE player_role_preferences (
    preference_id INTEGER PRIMARY KEY,

    player_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,

    priority INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY(player_id)
        REFERENCES players(player_id),

    FOREIGN KEY(role_id)
        REFERENCES roles(role_id),

    UNIQUE(player_id, role_id)
);


COMMIT;