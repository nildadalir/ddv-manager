from backend.database.models import Character


def generate_player_recommendations(
    player_id,
    player,
    db,
):
    recommendations = []

    # ==================================================
    # PLAYER WORLD ACCESS
    # ==================================================

    unlocked_region_ids = {
        player_region.region_id
        for player_region in player.regions
        if player_region.unlocked
    }

    # ==================================================
    # PLAYER CHARACTER STATE
    # ==================================================

    unlocked_character_ids = {
        player_character.character_id
        for player_character in player.characters
        if player_character.unlocked
    }

    # ==================================================
    # FRIENDSHIP RECOMMENDATIONS
    #
    # Only characters already unlocked by the player
    # are considered here.
    #
    # We do NOT filter these by region because if the
    # player already owns/unlocked the character,
    # their friendship progress is actionable.
    # ==================================================

    for player_character in player.characters:

        if not player_character.unlocked:
            continue

        character = player_character.character

        if character.max_friendship_level <= 0:
            continue

        if (
            player_character.friendship_level
            >= character.max_friendship_level
        ):
            continue

        completion_percentage = (
            player_character.friendship_level
            / character.max_friendship_level
        )

        if completion_percentage >= 0.8:
            priority = "high"

        elif completion_percentage >= 0.4:
            priority = "medium"

        else:
            priority = "low"

        score = int(
            completion_percentage * 50
        )

        recommendations.append(
            {
                "type": "friendship",
                "priority": priority,
                "character": character.name,
                "reason": (
                    f"Friendship level "
                    f"{player_character.friendship_level}/"
                    f"{character.max_friendship_level}"
                ),
                "_score": score,
            }
        )

    # ==================================================
    # ACCESSIBLE CHARACTER DISCOVERY
    #
    # Characters can appear here when:
    #
    # - their region is unlocked
    # - the player has not unlocked them yet
    #
    # This is separate from friendship recommendations.
    # ==================================================

    characters = db.query(Character).all()

    for character in characters:

        if character.character_id in unlocked_character_ids:
            continue

        if character.region_id is None:
            continue

        if character.region_id not in unlocked_region_ids:
            continue

        recommendations.append(
            {
                "type": "character",
                "priority": "low",
                "character": character.name,
                "reason": (
                    f"{character.name} is available "
                    f"in an unlocked region."
                ),
                "_score": 10,
            }
        )

    # ==================================================
    # SORT RECOMMENDATIONS
    # ==================================================

    recommendations.sort(
        key=lambda recommendation: recommendation["_score"],
        reverse=True,
    )

    # Internal scores are only used for sorting.
    for recommendation in recommendations:
        recommendation.pop("_score")

    return recommendations