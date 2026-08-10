from database.connection import SessionLocal
from database.models import Recipe


def main():

    session = SessionLocal()

    recipes = session.query(Recipe).all()

    print("\n=== RECIPES ===")

    for recipe in recipes:
        print(
            f"{recipe.name} "
            f"| {recipe.category} "
            f"| {recipe.stars} stars"
        )

        print("Ingredients:")

        for ingredient in recipe.ingredients:
            print(
                f" - {ingredient.item.name} "
                f"x{ingredient.quantity}"
            )

    session.close()


if __name__ == "__main__":
    main()