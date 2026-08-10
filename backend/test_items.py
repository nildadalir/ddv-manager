from database.connection import SessionLocal
from database.models import Item


def main():

    session = SessionLocal()

    items = session.query(Item).all()

    for item in items:
        print(
            f"{item.name} "
            f"({item.category.name})"
        )

    session.close()


if __name__ == "__main__":
    main()