from backend.services.metrics import calculate_player_metrics


def generate_player_insights(
    player_id,
    player,
    db,
):
    """
    Generate human-readable insights from derived player metrics.

    Insights describe meaningful patterns in the player's state.
    They do not modify the database.
    """

    metrics = calculate_player_metrics(
        player_id,
        player,
        db,
    )

    insights = []

    # ==================================================
    # FRIENDSHIP
    # ==================================================

    friendship = metrics["friendship"]

    completion_percentage = friendship[
        "completion_percentage"
    ]

    if completion_percentage is not None:

        if completion_percentage >= 80:
            insights.append(
                {
                    "type": "friendship",
                    "priority": "high",
                    "title": "Friendship is nearly complete",
                    "message": (
                        f"Your unlocked characters are "
                        f"{completion_percentage:.0f}% through "
                        "their available friendship levels."
                    ),
                }
            )

        elif completion_percentage >= 50:
            insights.append(
                {
                    "type": "friendship",
                    "priority": "medium",
                    "title": "Friendship is progressing well",
                    "message": (
                        f"Your unlocked characters are "
                        f"{completion_percentage:.0f}% through "
                        "their available friendship levels."
                    ),
                }
            )

        elif completion_percentage > 0:
            insights.append(
                {
                    "type": "friendship",
                    "priority": "low",
                    "title": "Friendship has room to grow",
                    "message": (
                        f"Your unlocked characters are "
                        f"{completion_percentage:.0f}% through "
                        "their available friendship levels."
                    ),
                }
            )

    # ==================================================
    # CHARACTER STATE
    # ==================================================

    characters = metrics["characters"]

    if characters["unknown"] > 0:
        insights.append(
            {
                "type": "data_quality",
                "priority": "medium",
                "title": "Character data is incomplete",
                "message": (
                    f"{characters['unknown']} character states "
                    "are still unknown."
                ),
            }
        )

    # ==================================================
    # UNLOCK SOURCE STATE
    # ==================================================

    unlock_sources = metrics["unlock_sources"]

    if (
        unlock_sources["total"] > 0
        and unlock_sources["unknown"]
        == unlock_sources["total"]
    ):
        insights.append(
            {
                "type": "data_quality",
                "priority": "medium",
                "title": "Unlock progress is not set",
                "message": (
                    "Your unlock-source progress has not been "
                    "set yet. Marking known unlock sources will "
                    "make character recommendations more useful."
                ),
            }
        )

    # ==================================================
    # ROLE COVERAGE
    # ==================================================

    roles = metrics["roles"]

    if (
        characters["unlocked"] > 0
        and roles["no_role"] > 0
    ):
        insights.append(
            {
                "type": "roles",
                "priority": "medium",
                "title": "Some characters need roles",
                "message": (
                    f"{roles['unassigned']} unlocked characters "
                    "do not currently have a role assigned."
                ),
            }
        )

    # ==================================================
    # SORT BY PRIORITY
    # ==================================================

    priority_order = {
        "high": 3,
        "medium": 2,
        "low": 1,
    }

    insights.sort(
        key=lambda insight: priority_order[
            insight["priority"]
        ],
        reverse=True,
    )

    return insights
