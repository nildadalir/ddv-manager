from backend.database.models import Character


def generate_player_recommendations(
    player_id,
    player,
    db,
):
    recommendations = []

    unlocked_character_ids = {
        player_character.character_id
        for player_character in player.characters
        if player_character.unlocked is True
    }

    unlocked_unlock_source_ids = {
        progress.unlock_source_id
        for progress in player.unlock_source_progress
        if progress.unlocked is True
    }

    for player_character in player.characters:

        if player_character.unlocked is not True:
            continue

        if player_character.friendship_level is None:
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

    characters = db.query(Character).all()

    for character in characters:

        if character.character_id in unlocked_character_ids:
            continue

        unlock_source_ids = {
            source.unlock_source_id
            for source in character.unlock_sources
        }

        if not unlock_source_ids:
            continue

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

    recommendations.sort(
        key=lambda recommendation: recommendation["_score"],
        reverse=True,
    )

    for recommendation in recommendations:
        recommendation.pop("_score")

    return recommendations