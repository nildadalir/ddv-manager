import json
from pathlib import Path

from sqlalchemy.orm import Session

from backend.database.models import (
    Character,
    CharacterUnlockSource,
)


RAW_DATA_PATH = (
    Path("database")
    / "raw"
    / "character_unlock_source_links.json"
)


def load_character_unlock_source_links():
    with RAW_DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def import_character_unlock_source_links(db: Session):
    links = load_character_unlock_source_links()

    imported = 0
    skipped = 0

    for link in links:
        character = (
            db.query(Character)
            .filter(
                Character.name == link["character"].strip()
            )
            .first()
        )

        if character is None:
            print(
                f"Skipping unknown character: "
                f"{link['character']}"
            )
            skipped += 1
            continue

        unlock_source = (
            db.query(CharacterUnlockSource)
            .filter(
                CharacterUnlockSource.name
                == link["unlock_source"].strip()
            )
            .first()
        )

        if unlock_source is None:
            print(
                f"Skipping unknown unlock source: "
                f"{link['unlock_source']}"
            )
            skipped += 1
            continue

        if unlock_source in character.unlock_sources:
            skipped += 1
            continue

        character.unlock_sources.append(unlock_source)
        imported += 1

    db.commit()

    return {
        "imported": imported,
        "skipped": skipped,
    }