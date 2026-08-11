-- ==========================================
-- Player Character Progress Seed
-- ==========================================

INSERT INTO player_characters (
    player_id,
    character_id,
    unlocked,
    friendship_level,
    assigned_role
)
VALUES
(
    1,
    (
        SELECT character_id
        FROM characters
        WHERE external_id = 'kristoff'
    ),
    TRUE,
    10,
    (
        SELECT role_id
        FROM roles
        WHERE external_id = 'mining'
    )
),
(
    1,
    (
        SELECT character_id
        FROM characters
        WHERE external_id = 'mickey'
    ),
    TRUE,
    10,
    (
        SELECT role_id
        FROM roles
        WHERE external_id = 'gardening'
    )
);