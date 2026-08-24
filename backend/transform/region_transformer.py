def transform_region(region: dict) -> dict:
    name = region["name"].strip()

    return {
        "name": name,
        "expansion": region["expansion"].strip(),
        "region_type": region["region_type"].strip().lower(),
        "parent_region": (
            region["parent_region"].strip()
            if region.get("parent_region")
            else None
        ),
        "external_id": (
            name.lower()
            .replace(" ", "_")
            .replace("'", "")
        ),
    }