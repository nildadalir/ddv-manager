-- ==========================================
-- Migration 009
-- Link characters to their primary region
-- ==========================================
BEGIN TRANSACTION;
ALTER TABLE characters
ADD COLUMN region_id INTEGER REFERENCES regions(region_id);
COMMIT;