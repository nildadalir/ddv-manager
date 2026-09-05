BEGIN TRANSACTION;

CREATE TABLE player_unlock_sources_new (
    player_unlock_source_id INTEGER PRIMARY KEY,

    player_id INTEGER NOT NULL,

    unlock_source_id INTEGER NOT NULL,

    unlocked BOOLEAN DEFAULT NULL,

    UNIQUE (
        player_id,
        unlock_source_id
    ),

    FOREIGN KEY(player_id)
        REFERENCES players(player_id),

    FOREIGN KEY(unlock_source_id)
        REFERENCES character_unlock_sources(unlock_source_id)
);

INSERT INTO player_unlock_sources_new (
    player_unlock_source_id,
    player_id,
    unlock_source_id,
    unlocked
)
SELECT
    player_unlock_source_id,
    player_id,
    unlock_source_id,
    NULL
FROM player_unlock_sources;

DROP TABLE player_unlock_sources;

ALTER TABLE player_unlock_sources_new
RENAME TO player_unlock_sources;

COMMIT;