from database.connection import SessionLocal
from database.queries import (
    get_all_characters,
    get_unlocked_characters,
    get_characters_by_role,
)


def main():

    session = SessionLocal()

    print("\n=== ALL CHARACTERS ===")

    characters = get_all_characters(session)

    for character in characters:
        print(
            f"{character.name} "
            f"({character.franchise.name})"
        )


    print("\n=== UNLOCKED CHARACTERS ===")

    unlocked = get_unlocked_characters(
        session,
        player_id=1
    )

    for progress in unlocked:
        print(
            f"{progress.character.name} "
            f"- Level {progress.friendship_level}"
        )


    print("\n=== MINING CHARACTERS ===")

    miners = get_characters_by_role(
        session,
        player_id=1,
        role_id=1
    )

    for progress in miners:
        print(
            f"{progress.character.name} "
            f"- Level {progress.friendship_level}"
        )


    session.close()


if __name__ == "__main__":
    main()