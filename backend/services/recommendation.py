from backend.database.models import (
    Character,
    PlayerRolePreference,
)


def generate_player_recommendations(
    player_id,
    player,
    db,
):
    recommendations = []

    # ==================================================
    # WORLD ACCESS
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
    # ==================================================

    for player_character in player.characters:

        if not player_character.unlocked:
            continue

        character = player_character.character

        if (
            player_character.friendship_level
            >= character.max_friendship_level
        ):
            continue

        if character.max_friendship_level <= 0:
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
    # ROLE PREFERENCES
    # ==================================================

    role_preferences = db.query(
        PlayerRolePreference
    ).filter(
        PlayerRolePreference.player_id == player_id
    ).all()

    role_priority_map = {
        preference.role_id: preference.priority
        for preference in role_preferences
    }

    # ==================================================
    # ACCESSIBLE CHARACTER DISCOVERY
    #
    # Find characters whose region is unlocked by
    # the player but who are not yet unlocked.
    # ==================================================

    for character in db.query(Character).all():

        if character.character_id in unlocked_character_ids:
            continue

        if character.region_id is None:
            continue

        if character.region_id not in unlocked_region_ids:
            continue

        # --------------------------------------------------
        # Character is accessible to the player.
        #
        # We deliberately don't assign a role-based
        # recommendation here. Roles are preferences,
        # not reasons to recommend a random character.
        # --------------------------------------------------

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
    # SORT
    # ==================================================

    recommendations.sort(
        key=lambda recommendation: recommendation["_score"],
        reverse=True,
    )

    for recommendation in recommendations:
        recommendation.pop("_score")

    return recommendations