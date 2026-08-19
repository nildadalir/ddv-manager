def transform_character(data: dict) -> dict:
    return {
        "name": data["name"].strip(),
        "franchise": data["franchise"].strip(),
        "species": (
            data.get("species").strip()
            if data.get("species")
            else None
        ),
        "external_id": data["name"]
            .strip()
            .lower()
            .replace(" ", "_"),
    }