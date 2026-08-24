def validate_region(region: dict) -> bool:
    required_fields = [
        "name",
        "expansion",
        "region_type",
    ]

    for field in required_fields:
        value = region.get(field)

        if not isinstance(value, str):
            return False

        if not value.strip():
            return False

    return True