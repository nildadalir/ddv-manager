import json

from sqlalchemy.orm import Session

from backend.database.models import (
    Character,
    Franchise,
)
from backend.ingestion.base_importer import BaseImporter
from backend.ingestion.sources import CHARACTERS_SOURCE
from backend.transform.character_transformer import (
    transform_character,
)
from backend.validation.character_validator import (
    validate_character,
)


class CharacterImporter(BaseImporter):

    def __init__(self, db: Session):
        self.db = db

    def load(self) -> list[dict]:
        with open(
            CHARACTERS_SOURCE,
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def validate(self, item: dict) -> bool:
        return validate_character(item)

    def transform(self, item: dict) -> dict:
        return transform_character(item)

    def save(self, data: list[dict]) -> None:

        for character_data in data:

            # ----------------------------------------
            # Find or create franchise
            # ----------------------------------------
            franchise = self.db.query(Franchise).filter(
                Franchise.name == character_data["franchise"]
            ).first()

            if not franchise:
                franchise = Franchise(
                    name=character_data["franchise"]
                )

                self.db.add(franchise)
                self.db.flush()

            # ----------------------------------------
            # Skip character if already imported
            # ----------------------------------------
            existing_character = (
                self.db.query(Character)
                .filter(
                    Character.external_id
                    == character_data["external_id"]
                )
                .first()
            )

            if existing_character:
                continue

            # ----------------------------------------
            # Create character
            # ----------------------------------------
            character = Character(
                name=character_data["name"],
                franchise_id=franchise.franchise_id,
                species=character_data["species"],
                external_id=character_data["external_id"],
            )

            self.db.add(character)

        self.db.commit()