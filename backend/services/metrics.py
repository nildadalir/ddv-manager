from backend.database.models import Player


def calculate_player_metrics(player_id, player, db):
    """
    Calculate derived metrics from the player's current state.

    This function does not modify the database.
    It only reads player state and returns derived data.
    """

    # ==================================================
    # CHARACTER METRICS
    # ==================================================

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

    unlocked_character_count = len(unlocked_characters)
    locked_character_count = len(locked_characters)
    unknown_character_count = len(unknown_characters)

    # ==================================================
    # FRIENDSHIP METRICS
    # ==================================================

    friendship_levels = [
        character.friendship_level
        for character in unlocked_characters
        if character.friendship_level is not None
    ]

    total_friendship_levels = sum(friendship_levels)

    max_friendship_levels = sum(
        character.character.max_friendship_level
        for character in unlocked_characters
        if character.character.max_friendship_level > 0
        and character.friendship_level is not None
    )

    if max_friendship_levels > 0:
        friendship_completion_percentage = (
            total_friendship_levels
            / max_friendship_levels
            * 100
        )
    else:
        friendship_completion_percentage = None

    # ==================================================
    # ROLE METRICS
    # ==================================================

    assigned_roles = [
    character
    for character in unlocked_characters
    if character.role is not None
    ]

    unassigned_roles = [
        character
        for character in unlocked_characters
        if character.role is None
    ]

    # ==================================================
    # UNLOCK SOURCE METRICS
    # ==================================================

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

    # ==================================================
    # RETURN DERIVED DATA
    # ==================================================

    return {
        "characters": {
            "total": total_characters,
            "unlocked": unlocked_character_count,
            "locked": locked_character_count,
            "unknown": unknown_character_count,
        },
        "friendship": {
            "total_levels": total_friendship_levels,
            "max_levels": max_friendship_levels,
            "completion_percentage": friendship_completion_percentage,
        },
        "roles": {
            "assigned": len(assigned_roles),
            "unassigned": len(unassigned_roles),
        },
        "unlock_sources": {
            "total": len(unlock_sources),
            "unlocked": len(unlocked_unlock_sources),
            "locked": len(locked_unlock_sources),
            "unknown": len(unknown_unlock_sources),
        },
    }