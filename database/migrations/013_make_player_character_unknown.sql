-- ==========================================
-- Migration 013
-- Allow unknown character unlock state
-- ==========================================

BEGIN TRANSACTION;

-- SQLite already permits NULL for the existing
-- unlocked column, so no table rebuild is required.
-- This migration documents the schema contract:
-- TRUE  = Unlocked
-- FALSE = Locked
-- NULL  = Unknown

COMMIT;