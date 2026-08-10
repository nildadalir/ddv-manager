-- Migration 002
-- Add item categories and items
BEGIN TRANSACTION;
CREATE TABLE item_categories (
    category_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE items (
    item_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    category_id INTEGER,
    rarity TEXT,
    sell_price INTEGER,
    energy INTEGER,
    FOREIGN KEY(category_id) REFERENCES item_categories(category_id)
);
COMMIT;