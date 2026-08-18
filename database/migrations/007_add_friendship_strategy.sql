-- ==========================================
-- Migration 007
-- Add player friendship strategy preference
-- ==========================================

BEGIN TRANSACTION;

ALTER TABLE players
ADD COLUMN friendship_strategy TEXT NOT NULL DEFAULT 'balanced';

COMMIT;