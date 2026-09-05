-- ==========================================
-- Migration 014
-- Add explicit player character role status
-- ==========================================

BEGIN TRANSACTION;

ALTER TABLE player_characters
ADD COLUMN role_status TEXT NOT NULL DEFAULT 'unknown';

COMMIT;