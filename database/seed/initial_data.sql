-- ======================================
-- DDV Manager Initial Seed Data
-- ======================================
INSERT INTO franchises (name)
VALUES ('Frozen');
INSERT INTO roles (name)
VALUES ('Mining');
INSERT INTO characters (
        name,
        franchise_id,
        species,
        is_assignable
    )
VALUES (
        'Kristoff',
        1,
        'Human',
        TRUE
    );
INSERT INTO character_roles (character_id, role_id)
VALUES (1, 1);