from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.database.models import (
    Franchise,
    Character,
    Expansion,
    Region,
)

from backend.ingestion.character_importer import (
    load_characters,
)
from backend.ingestion.expansion_importer import (
    load_expansions,
)
from backend.ingestion.region_importer import (
    load_regions,
)

from backend.transform.character_transformer import (
    transform_character,
)
from backend.transform.expansion_transformer import (
    transform_expansion,
)
from backend.transform.region_transformer import (
    transform_region,
)

from backend.validation.character_validator import (
    validate_character,
)
from backend.validation.expansion_validator import (
    validate_expansion,
)
from backend.validation.region_validator import (
    validate_region,
)


def import_characters() -> None:
    db: Session = SessionLocal()

    try:
        raw_characters = load_characters()

        for raw_character in raw_characters:
            if not validate_character(raw_character):
                print(
                    f"Skipping invalid character: "
                    f"{raw_character}"
                )
                continue

            character_data = transform_character(
                raw_character
            )

            franchise_name = character_data.pop(
                "franchise"
            )

            franchise = db.query(Franchise).filter(
                Franchise.name == franchise_name
            ).first()

            if not franchise:
                franchise = Franchise(
                    name=franchise_name,
                    external_id=(
                        franchise_name.lower()
                        .replace(" ", "_")
                    ),
                )

                db.add(franchise)
                db.flush()

            existing_character = db.query(Character).filter(
                Character.external_id
                == character_data["external_id"]
            ).first()

            if existing_character:
                for key, value in character_data.items():
                    setattr(
                        existing_character,
                        key,
                        value,
                    )

                existing_character.franchise_id = (
                    franchise.franchise_id
                )

            else:
                db.add(
                    Character(
                        **character_data,
                        franchise_id=franchise.franchise_id,
                    )
                )

        db.commit()

        print(
            "Character import completed successfully."
        )

    finally:
        db.close()


def import_expansions() -> None:
    db: Session = SessionLocal()

    try:
        raw_expansions = load_expansions()

        for raw_expansion in raw_expansions:
            if not validate_expansion(raw_expansion):
                print(
                    f"Skipping invalid expansion: "
                    f"{raw_expansion}"
                )
                continue

            expansion_data = transform_expansion(
                raw_expansion
            )

            existing_expansion = db.query(
                Expansion
            ).filter(
                Expansion.external_id
                == expansion_data["external_id"]
            ).first()

            if existing_expansion:
                for key, value in expansion_data.items():
                    setattr(
                        existing_expansion,
                        key,
                        value,
                    )

            else:
                db.add(
                    Expansion(**expansion_data)
                )

        db.commit()

        print(
            "Expansion import completed successfully."
        )

    finally:
        db.close()


def import_regions() -> None:
    db: Session = SessionLocal()

    try:
        raw_regions = load_regions()

        # First pass:
        # create all regions without parent links.
        for raw_region in raw_regions:
            if not validate_region(raw_region):
                print(
                    f"Skipping invalid region: "
                    f"{raw_region}"
                )
                continue

            region_data = transform_region(
                raw_region
            )

            expansion = db.query(Expansion).filter(
                Expansion.name
                == region_data["expansion"]
            ).first()

            if not expansion:
                print(
                    f"Skipping region because expansion "
                    f"was not found: "
                    f"{region_data['name']}"
                )
                continue

            existing_region = db.query(Region).filter(
                Region.external_id
                == region_data["external_id"]
            ).first()

            if existing_region:
                existing_region.name = (
                    region_data["name"]
                )
                existing_region.region_type = (
                    region_data["region_type"]
                )
                existing_region.expansion_id = (
                    expansion.expansion_id
                )

            else:
                db.add(
                    Region(
                        name=region_data["name"],
                        external_id=(
                            region_data["external_id"]
                        ),
                        region_type=(
                            region_data["region_type"]
                        ),
                        expansion_id=(
                            expansion.expansion_id
                        ),
                    )
                )

        db.commit()

        # Second pass:
        # connect parent regions.
        for raw_region in raw_regions:
            parent_name = raw_region.get(
                "parent_region"
            )

            if not parent_name:
                continue

            region_name = raw_region["name"]

            region = db.query(Region).filter(
                Region.name == region_name
            ).first()

            parent_region = db.query(Region).filter(
                Region.name == parent_name
            ).first()

            if region and parent_region:
                region.parent_region_id = (
                    parent_region.region_id
                )

        db.commit()

        print(
            "Region import completed successfully."
        )

    finally:
        db.close()


def import_world_data() -> None:
    import_expansions()
    import_regions()