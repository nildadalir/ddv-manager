-- ==========================================
-- DDV Manager Migration 001
-- Initial Game Data Schema
-- ==========================================
PRAGMA foreign_keys = ON;
-- ==========================================
-- GAME DATA
-- ==========================================
CREATE TABLE IF NOT EXISTS franchises (
    franchise_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS characters (
    character_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    franchise_id INTEGER,
    species TEXT,
    is_assignable BOOLEAN DEFAULT FALSE,
    max_friendship_level INTEGER DEFAULT 10,
    FOREIGN KEY (franchise_id) REFERENCES franchises(franchise_id)
);
CREATE TABLE IF NOT EXISTS roles (
    role_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS character_roles (
    character_id INTEGER,
    role_id INTEGER,
    PRIMARY KEY(character_id, role_id),
    FOREIGN KEY(character_id) REFERENCES characters(character_id),
    FOREIGN KEY(role_id) REFERENCES roles(role_id)
);
-- ==========================================
-- ITEMS
-- ==========================================
CREATE TABLE IF NOT EXISTS item_categories (
    category_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    category_id INTEGER,
    rarity TEXT,
    sell_price INTEGER,
    energy INTEGER,
    FOREIGN KEY(category_id) REFERENCES item_categories(category_id)
);
-- ==========================================
-- STORAGE
-- ==========================================
CREATE TABLE IF NOT EXISTS storage_containers (
    storage_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    size TEXT,
    location TEXT
);
CREATE TABLE IF NOT EXISTS storage_items (
    storage_id INTEGER,
    item_id INTEGER,
    quantity INTEGER DEFAULT 0,
    PRIMARY KEY(storage_id, item_id),
    FOREIGN KEY(storage_id) REFERENCES storage_containers(storage_id),
    FOREIGN KEY(item_id) REFERENCES items(item_id)
);