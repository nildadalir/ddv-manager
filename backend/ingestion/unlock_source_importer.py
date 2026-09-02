import json
from pathlib import Path

from sqlalchemy.orm import Session

from backend.database.models import CharacterUnlockSource


RAW_DATA_PATH = (
    Path("database")
    / "raw"
    / "character_unlock_sources.json"
)


def load_unlock_sources():
    with RAW_DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def import_unlock_sources(db: Session):
    sources = load_unlock_sources()

    imported = 0
    skipped = 0

    for source in sources:
        external_id = source["external_id"]

        existing = (
            db.query(CharacterUnlockSource)
            .filter(
                CharacterUnlockSource.external_id
                == external_id
            )
            .first()
        )

        if existing:
            skipped += 1
            continue

        unlock_source = CharacterUnlockSource(
            name=source["name"].strip(),
            source_type=source["source_type"].strip().lower(),
            external_id=external_id,
        )

        db.add(unlock_source)
        imported += 1

    db.commit()

    return {
        "imported": imported,
        "skipped": skipped,
    }