-- ==========================================
-- Migration 004
-- Add recipe system
-- ==========================================

BEGIN TRANSACTION;


CREATE TABLE recipes (
    recipe_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    category TEXT,
    stars INTEGER,
    energy INTEGER,
    sell_price INTEGER
);


CREATE TABLE recipe_ingredients (
    recipe_id INTEGER,
    item_id INTEGER,
    quantity INTEGER DEFAULT 1,

    PRIMARY KEY(recipe_id, item_id),

    FOREIGN KEY(recipe_id)
        REFERENCES recipes(recipe_id),

    FOREIGN KEY(item_id)
        REFERENCES items(item_id)
);


COMMIT;