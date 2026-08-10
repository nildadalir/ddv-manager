from database.connection import SessionLocal
from database.models import PlayerCharacter


def main():

    session = SessionLocal()

    progress = session.query(PlayerCharacter).first()

    print("Character:", progress.character.name)
    print("Franchise:", progress.character.franchise.name)
    print("Friendship:", progress.friendship_level)
    print("Role:", progress.role.name)
    print("Player:", progress.player.username)

    session.close()


if __name__ == "__main__":
    main()