REQUIRED_FIELDS = (
    "name",
    "franchise",
)


def validate_character(data: dict) -> bool:
    for field in REQUIRED_FIELDS:
        if field not in data:
            return False

        if not isinstance(data[field], str):
            return False

        if not data[field].strip():
            return False

    if "species" in data:
        species = data["species"]

        if species is not None and not isinstance(
            species,
            str,
        ):
            return False

    return True