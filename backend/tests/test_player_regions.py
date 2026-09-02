from backend.database.connection import SessionLocal
from backend.database.models import Player, Region, PlayerRegion


def main():
    db = SessionLocal()

    try:
        player = db.query(Player).first()

        if not player:
            print("ERROR: No player found.")
            return

        regions = db.query(Region).all()

        unlocked_regions = {
            "dreamlight_valley",
            "plaza",
            "peaceful_meadow",
        }

        for region in regions:
            existing = db.query(PlayerRegion).filter(
                PlayerRegion.player_id == player.player_id,
                PlayerRegion.region_id == region.region_id,
            ).first()

            if not existing:
                existing = PlayerRegion(
                    player_id=player.player_id,
                    region_id=region.region_id,
                    unlocked=False,
                )

                db.add(existing)

            if region.external_id in unlocked_regions:
                existing.unlocked = True

        db.commit()

        print("\nPlayer region progress:")
        print("-" * 40)

        progress = (
            db.query(PlayerRegion)
            .filter(
                PlayerRegion.player_id == player.player_id
            )
            .all()
        )

        for item in progress:
            print(
                item.region.name,
                "|",
                "UNLOCKED" if item.unlocked else "LOCKED",
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()