from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Character(Base):
    __tablename__ = "characters"

    character_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    franchise_id: Mapped[int | None] = mapped_column(
        ForeignKey("franchises.franchise_id")
    )

    species: Mapped[str | None]

    is_assignable: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    max_friendship_level: Mapped[int] = mapped_column(
        Integer,
        default=10
    )