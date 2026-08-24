import json
from pathlib import Path


RAW_DATA_PATH = (
    Path("database")
    / "raw"
    / "expansions.json"
)


def load_expansions() -> list[dict]:
    with RAW_DATA_PATH.open(
        encoding="utf-8"
    ) as file:
        return json.load(file)