from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Local database
DATABASE_PATH = BASE_DIR / "database" / "ddv_manager.sqlite"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)