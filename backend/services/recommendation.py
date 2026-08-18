from backend.database.models import (
    PlayerRolePreference,
    Role,
)


def generate_player_recommendations(
    player_id,
    player,
    db,
):

    recommendations = []


    # --------------------------------------------------
    # Load player's role priorities
    # --------------------------------------------------

    role_preferences = db.query(
        PlayerRolePreference
    ).filter(
        PlayerRolePreference.player_id == player_id
    ).all()


    role_priority_map = {
        preference.role_id: preference.priority
        for preference in role_preferences
    }


    # --------------------------------------------------
    # Friendship recommendations
    # --------------------------------------------------

    for pc in player.characters:

        if pc.friendship_level >= pc.character.max_friendship_level:
            continue


        completion_percentage = (
            pc.friendship_level
            /
            pc.character.max_friendship_level
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
                "character": pc.character.name,
                "reason": (
                    f"Friendship level "
                    f"{pc.friendship_level}/"
                    f"{pc.character.max_friendship_level}"
                ),
                "_score": score,
            }
        )


    # --------------------------------------------------
    # Missing roles
    # --------------------------------------------------

    assigned_role_ids = {
        pc.assigned_role
        for pc in player.characters
        if pc.assigned_role is not None
    }


    all_roles = db.query(Role).all()


    for role in all_roles:

        if role.role_id in assigned_role_ids:
            continue


        role_priority = role_priority_map.get(
            role.role_id,
            len(all_roles) + 1,
        )


        if role_priority <= 2:
            priority = "high"

        elif role_priority <= 4:
            priority = "medium"

        else:
            priority = "low"


        score = max(
            0,
            100 - (role_priority * 10),
        )


        recommendations.append(
            {
                "type": "role",
                "priority": priority,
                "character": None,
                "reason": (
                    f"No character assigned to {role.name}"
                ),
                "_score": score,
            }
        )


    # --------------------------------------------------
    # Sort
    # --------------------------------------------------

    recommendations.sort(
        key=lambda x: x["_score"],
        reverse=True,
    )


    for recommendation in recommendations:
        recommendation.pop("_score")


    return recommendations