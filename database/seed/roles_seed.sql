-- ==========================================
-- Role seed data
-- ==========================================

INSERT OR IGNORE INTO roles
(
    external_id,
    name
)
VALUES
('mining', 'Mining'),
('gardening', 'Gardening'),
('fishing', 'Fishing'),
('foraging', 'Foraging'),
('digging', 'Digging');