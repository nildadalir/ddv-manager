def validate_expansion(expansion: dict) -> bool:
    name = expansion.get("name")

    return bool(
        isinstance(name, str)
        and name.strip()
    )