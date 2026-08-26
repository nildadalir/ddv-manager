def validate_character(character: dict) -> bool:
    required_fields = [
        "name",
        "franchise",
        "region",
    ]

    for field in required_fields:
        value = character.get(field)

        if not isinstance(value, str):
            return False

        if not value.strip():
            return False

    species = character.get("species")

    if species is not None and not isinstance(
        species,
        str,
    ):
        return False

    return True