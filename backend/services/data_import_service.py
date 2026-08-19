from backend.database.session import SessionLocal
from backend.ingestion.character_importer import (
    CharacterImporter,
)


def import_characters() -> None:
    db = SessionLocal()

    try:
        importer = CharacterImporter(db)

        importer.run()

        print(
            "Character import completed successfully."
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()