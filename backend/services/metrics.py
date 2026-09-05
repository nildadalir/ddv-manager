def calculate_player_metrics(
    player_id,
    player,
    db,
):
    """
    Calculate derived metrics from the player's current state.

    This function does not modify the database.
    It only reads player state and returns derived data.
    """

    characters = player.characters

    total_characters = len(characters)

    unlocked_characters = [
        character
        for character in characters
        if character.unlocked is True
    ]

    locked_characters = [
        character
        for character in characters
        if character.unlocked is False
    ]

    unknown_characters = [
        character
        for character in characters
        if character.unlocked is None
    ]

    friendship_levels = [
        character.friendship_level
        for character in unlocked_characters
        if character.friendship_level is not None
    ]

    total_friendship_levels = sum(friendship_levels)

    max_friendship_levels = sum(
        character.character.max_friendship_level
        for character in unlocked_characters
        if (
            character.character.max_friendship_level > 0
            and character.friendship_level is not None
        )
    )

    if max_friendship_levels > 0:
        friendship_completion_percentage = (
            total_friendship_levels
            / max_friendship_levels
            * 100
        )
    else:
        friendship_completion_percentage = None

    assigned_roles = [
        character
        for character in unlocked_characters
        if character.role_status == "assigned"
    ]

    no_role_characters = [
        character
        for character in unlocked_characters
        if character.role_status == "no_role"
    ]

    unknown_role_characters = [
        character
        for character in unlocked_characters
        if character.role_status == "unknown"
    ]

    unlock_sources = player.unlock_source_progress

    unlocked_unlock_sources = [
        source
        for source in unlock_sources
        if source.unlocked is True
    ]

    locked_unlock_sources = [
        source
        for source in unlock_sources
        if source.unlocked is False
    ]

    unknown_unlock_sources = [
        source
        for source in unlock_sources
        if source.unlocked is None
    ]

    return {
        "characters": {
            "total": total_characters,
            "unlocked": len(unlocked_characters),
            "locked": len(locked_characters),
            "unknown": len(unknown_characters),
        },
        "friendship": {
            "total_levels": total_friendship_levels,
            "max_levels": max_friendship_levels,
            "completion_percentage": friendship_completion_percentage,
        },
        "roles": {
            "assigned": len(assigned_roles),
            "no_role": len(no_role_characters),
            "unknown": len(unknown_role_characters),
        },
        "unlock_sources": {
            "total": len(unlock_sources),
            "unlocked": len(unlocked_unlock_sources),
            "locked": len(locked_unlock_sources),
            "unknown": len(unknown_unlock_sources),
        },
    }