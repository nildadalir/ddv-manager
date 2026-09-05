-- ==========================================
-- Migration 015
-- Backfill role status for existing assignments
-- ==========================================

BEGIN TRANSACTION;

UPDATE player_characters
SET role_status = 'assigned'
WHERE assigned_role IS NOT NULL;

COMMIT;