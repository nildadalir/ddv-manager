import json
from pathlib import Path


RAW_DATA_PATH = (
    Path("database")
    / "raw"
    / "regions.json"
)


def load_regions() -> list[dict]:
    with RAW_DATA_PATH.open(
        encoding="utf-8"
    ) as file:
        return json.load(file)