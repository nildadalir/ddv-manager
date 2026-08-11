-- ==========================================
-- Item seed data
-- ==========================================

-- Categories

INSERT OR IGNORE INTO item_categories (name)
VALUES 
('Material'),
('Gem'),
('Ingredient'),
('Fish');


-- Items

INSERT OR IGNORE INTO items (
    external_id,
    name,
    category_id,
    rarity,
    sell_price,
    energy
)
VALUES

(
    'iron_ore',
    'Iron Ore',
    (
        SELECT category_id
        FROM item_categories
        WHERE name = 'Material'
    ),
    'Common',
    10,
    0
),

(
    'coal',
    'Coal',
    (
        SELECT category_id
        FROM item_categories
        WHERE name = 'Material'
    ),
    'Common',
    5,
    0
),

(
    'diamond',
    'Diamond',
    (
        SELECT category_id
        FROM item_categories
        WHERE name = 'Gem'
    ),
    'Rare',
    2400,
    0
),

(
    'raspberry',
    'Raspberry',
    (
        SELECT category_id
        FROM item_categories
        WHERE name = 'Ingredient'
    ),
    'Common',
    21,
    250
);