from pathlib import Path


BASE_DATA_DIR = Path("database") / "raw"


CHARACTERS_SOURCE = (
    BASE_DATA_DIR / "characters.json"
)

ITEMS_SOURCE = (
    BASE_DATA_DIR / "items.json"
)

RECIPES_SOURCE = (
    BASE_DATA_DIR / "recipes.json"
)