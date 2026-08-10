from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class Franchise(Base):
    __tablename__ = "franchises"

    franchise_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )

    characters: Mapped[list["Character"]] = relationship(
        back_populates="franchise"
    )


class Character(Base):
    __tablename__ = "characters"

    character_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
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

    franchise: Mapped["Franchise | None"] = relationship(
        back_populates="characters"
    )

    player_progress: Mapped[list["PlayerCharacter"]] = relationship(
        back_populates="character"
    )


class Role(Base):
    __tablename__ = "roles"

    role_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )

    player_characters: Mapped[list["PlayerCharacter"]] = relationship(
        back_populates="role"
    )


class ItemCategory(Base):
    __tablename__ = "item_categories"

    category_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )

    items: Mapped[list["Item"]] = relationship(
        back_populates="category"
    )


class Item(Base):
    __tablename__ = "items"

    item_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("item_categories.category_id")
    )

    rarity: Mapped[str | None]

    sell_price: Mapped[int | None]

    energy: Mapped[int | None]

    category: Mapped["ItemCategory | None"] = relationship(
        back_populates="items"
    )

    recipe_links: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="item"
    )


class Recipe(Base):
    __tablename__ = "recipes"

    recipe_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )

    category: Mapped[str | None]

    stars: Mapped[int | None]

    energy: Mapped[int | None]

    sell_price: Mapped[int | None]

    ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="recipe"
    )


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.recipe_id"),
        primary_key=True
    )

    item_id: Mapped[int] = mapped_column(
        ForeignKey("items.item_id"),
        primary_key=True
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    recipe: Mapped["Recipe"] = relationship(
        back_populates="ingredients"
    )

    item: Mapped["Item"] = relationship(
        back_populates="recipe_links"
    )


class Player(Base):
    __tablename__ = "players"

    player_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )

    created_at: Mapped[str | None]

    characters: Mapped[list["PlayerCharacter"]] = relationship(
        back_populates="player"
    )


class PlayerCharacter(Base):
    __tablename__ = "player_characters"

    player_character_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.player_id"),
        nullable=False
    )

    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.character_id"),
        nullable=False
    )

    unlocked: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    friendship_level: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    assigned_role: Mapped[int | None] = mapped_column(
        ForeignKey("roles.role_id")
    )

    player: Mapped["Player"] = relationship(
        back_populates="characters"
    )

    character: Mapped["Character"] = relationship(
        back_populates="player_progress"
    )

    role: Mapped["Role | None"] = relationship(
        back_populates="player_characters"
    )