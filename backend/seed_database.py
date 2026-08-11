from pathlib import Path
import sqlite3

from database.connection import DATABASE_PATH


SEED_DIR = Path("database") / "seed"


SEEDS = [
    "franchises_seed.sql",
    "roles_seed.sql",
    "characters_seed.sql",
    "items_seed.sql",
    "recipes_seed.sql",
]


def run_seeds(connection):
    cursor = connection.cursor()

    for seed in SEEDS:
        print(f"RUN {seed}")

        path = SEED_DIR / seed

        sql = path.read_text(
            encoding="utf-8"
        )

        cursor.executescript(sql)

        connection.commit()


def main():
    print("Seeding DDV Manager database...")

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    run_seeds(connection)

    connection.close()

    print("Seed complete!")


if __name__ == "__main__":
    main()