def transform_expansion(expansion: dict) -> dict:
    name = expansion["name"].strip()

    return {
        "name": name,
        "external_id": (
            name.lower()
            .replace(" ", "_")
            .replace("'", "")
        ),
        "is_base_game": bool(
            expansion.get("is_base_game", False)
        ),
    }