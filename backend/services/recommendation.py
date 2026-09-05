from backend.database.models import Character


def generate_player_recommendations(
    player_id,
    player,
    db,
):
    recommendations = []

    # ==================================================
    # PLAYER CHARACTER STATE
    # ==================================================

    unlocked_character_ids = {
        player_character.character_id
        for player_character in player.characters
        if player_character.unlocked
    }

    # ==================================================
    # PLAYER UNLOCK SOURCE STATE
    #
    # True  = confirmed unlocked
    # False = confirmed locked
    # None  = unknown
    #
    # Only confirmed unlocked sources can trigger a
    # character unlock recommendation.
    # ==================================================

    unlocked_unlock_source_ids = {
        progress.unlock_source_id
        for progress in player.unlock_source_progress
        if progress.unlocked is True
    }

    # ==================================================
    # FRIENDSHIP RECOMMENDATIONS
    #
    # Only characters already unlocked by the player
    # are considered here.
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
    # CHARACTER UNLOCK RECOMMENDATIONS
    #
    # We use the character's actual unlock source.
    #
    # We DO NOT use character.region_id here.
    #
    # Example:
    #
    # Aladdin
    #   -> Aladdin Realm
    #
    # Jafar
    #   -> Eternity Isle Storyline
    #
    # This prevents an unlocked Valley region from
    # incorrectly making every character in that region
    # appear available.
    # ==================================================

    characters = db.query(Character).all()

    for character in characters:

        # Already unlocked by the player
        if character.character_id in unlocked_character_ids:
            continue

        # Get this character's actual unlock sources
        unlock_source_ids = {
            source.unlock_source_id
            for source in character.unlock_sources
        }

        # No unlock source means we cannot safely determine
        # whether this character can currently be unlocked.
        if not unlock_source_ids:
            continue

        # Recommend the character only when at least one
        # confirmed unlock source is unlocked.
        if unlock_source_ids.isdisjoint(
            unlocked_unlock_source_ids
        ):
            continue

        unlock_source = next(iter(character.unlock_sources))

        recommendations.append(
            {
                "type": "character",
                "priority": "low",
                "character": character.name,
                "reason": (
                    f"{character.name} can now be unlocked "
                    f"through {unlock_source.name}."
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