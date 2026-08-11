-- ==========================================
-- Character seed data
-- ==========================================

INSERT OR IGNORE INTO characters
(
    external_id,
    name,
    franchise_id,
    species,
    is_assignable
)
VALUES

(
'kristoff',
'Kristoff',
(SELECT franchise_id FROM franchises WHERE external_id='frozen'),
'Human',
TRUE
),

(
'mickey',
'Mickey Mouse',
(SELECT franchise_id FROM franchises WHERE external_id='mickey_mouse'),
'Mouse',
TRUE
),

(
'remy',
'Remy',
(SELECT franchise_id FROM franchises WHERE external_id='ratatouille'),
'Rat',
TRUE
);