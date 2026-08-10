from database.connection import engine


def main():
    with engine.connect():
        print("Database connection successful!")


if __name__ == "__main__":
    main()