-- ==========================================
-- Recipe seed data
-- ==========================================

INSERT OR IGNORE INTO recipes (
    external_id,
    name,
    category,
    stars,
    energy,
    sell_price
)
VALUES (
    'test_ratatouille',
    'Test Ratatouille',
    'Meal',
    5,
    1000,
    500
);


INSERT OR IGNORE INTO recipe_ingredients (
    recipe_id,
    item_id,
    quantity
)
VALUES
(
    (
        SELECT recipe_id
        FROM recipes
        WHERE external_id = 'test_ratatouille'
    ),
    (
        SELECT item_id
        FROM items
        WHERE external_id = 'iron_ore'
    ),
    2
);