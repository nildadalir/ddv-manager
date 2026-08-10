from pathlib import Path
import sqlite3

from database.connection import DATABASE_PATH


MIGRATIONS_DIR = Path("database") / "migrations"


def create_database():

    DATABASE_PATH.parent.mkdir(
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            migration_id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL UNIQUE,
            applied_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()

    return connection


def get_applied_migrations(cursor):

    cursor.execute(
        "SELECT filename FROM schema_migrations"
    )

    return {
        row[0]
        for row in cursor.fetchall()
    }


def run_migrations(connection):

    cursor = connection.cursor()

    applied = get_applied_migrations(cursor)

    migrations = sorted(
        MIGRATIONS_DIR.glob("*.sql")
    )

    for migration in migrations:

        if migration.name in applied:
            print(
                f"SKIP {migration.name}"
            )
            continue

        print(
            f"APPLY {migration.name}"
        )

        sql = migration.read_text(
            encoding="utf-8"
        )

        cursor.executescript(sql)

        cursor.execute(
            """
            INSERT INTO schema_migrations(filename)
            VALUES (?)
            """,
            (migration.name,)
        )

        connection.commit()


def main():

    print("Setting up DDV Manager database...")

    connection = create_database()

    run_migrations(connection)

    connection.close()

    print("Database setup complete!")


if __name__ == "__main__":
    main()