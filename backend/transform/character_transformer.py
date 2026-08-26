def transform_character(character: dict) -> dict:
    name = character["name"].strip()

    return {
        "name": name,
        "franchise": character["franchise"].strip(),
        "species": (
            character["species"].strip()
            if character.get("species")
            else None
        ),
        "region": (
            character["region"].strip()
            if character.get("region")
            else None
        ),
        "external_id": (
            name.lower()
            .replace(" ", "_")
            .replace("'", "")
        ),
    }