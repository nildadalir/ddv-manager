from backend.services.insights import generate_player_insights
from backend.services.recommendation import generate_player_recommendations


def generate_home_summary(
    player_id,
    player,
    db,
):
    """
    Generate the decision-support data needed by Home.

    Home should consume this result rather than querying
    the database directly.
    """

    recommendations = generate_player_recommendations(
        player_id,
        player,
        db,
    )

    insights = generate_player_insights(
        player_id,
        player,
        db,
    )

    # ==================================================
    # NEXT BEST ACTION
    # ==================================================

    next_best_action = None

    if recommendations:
        recommendation = recommendations[0]

        next_best_action = {
            "type": recommendation["type"],
            "character": recommendation["character"],
            "reason": recommendation["reason"],
        }

    elif insights:
        insight = insights[0]

        next_best_action = {
            "type": "insight",
            "title": insight["title"],
            "reason": insight["message"],
        }

    # ==================================================
    # HOME SUMMARY
    # ==================================================

    return {
        "next_best_action": next_best_action,
        "recommendations": recommendations,
        "insights": insights,
    }