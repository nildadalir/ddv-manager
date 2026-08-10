from database.connection import SessionLocal
from database.models import Character


def main():

    session = SessionLocal()

    characters = session.query(Character).all()

    for character in characters:
        print(
            character.name,
            character.species
        )

    session.close()


if __name__ == "__main__":
    main()