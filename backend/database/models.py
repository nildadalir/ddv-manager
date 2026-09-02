from sqlalchemy import (
    String,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


# ==================================================
# GAME DATA
# ==================================================

class Franchise(Base):
    __tablename__ = "franchises"

    franchise_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    external_id: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    characters: Mapped[list["Character"]] = relationship(
        back_populates="franchise",
    )


class Expansion(Base):
    __tablename__ = "expansions"

    expansion_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    external_id: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=True,
    )

    is_base_game: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    regions: Mapped[list["Region"]] = relationship(
        back_populates="expansion",
    )


class Region(Base):
    __tablename__ = "regions"

    region_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    expansion_id: Mapped[int] = mapped_column(
        ForeignKey("expansions.expansion_id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    external_id: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=True,
    )

    region_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    parent_region_id: Mapped[int | None] = mapped_column(
        ForeignKey("regions.region_id"),
        nullable=True,
    )

    expansion: Mapped["Expansion"] = relationship(
        back_populates="regions",
    )

    parent_region: Mapped["Region | None"] = relationship(
        remote_side="Region.region_id",
        back_populates="child_regions",
    )

    child_regions: Mapped[list["Region"]] = relationship(
        back_populates="parent_region",
    )

    characters: Mapped[list["Character"]] = relationship(
        back_populates="region",
    )

    player_progress: Mapped[list["PlayerRegion"]] = relationship(
        back_populates="region",
    )


class Character(Base):
    __tablename__ = "characters"

    character_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    external_id: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    franchise_id: Mapped[int | None] = mapped_column(
        ForeignKey("franchises.franchise_id"),
        nullable=True,
    )

    region_id: Mapped[int | None] = mapped_column(
        ForeignKey("regions.region_id"),
        nullable=True,
    )

    species: Mapped[str | None]

    is_assignable: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    max_friendship_level: Mapped[int] = mapped_column(
        Integer,
        default=10,
    )

    franchise: Mapped["Franchise | None"] = relationship(
        back_populates="characters",
    )

    region: Mapped["Region | None"] = relationship(
        back_populates="characters",
    )

    player_progress: Mapped[list["PlayerCharacter"]] = relationship(
        back_populates="character",
    )
    
    unlock_sources: Mapped[list["CharacterUnlockSource"]] = relationship(
        secondary="character_unlock_source_links",
        back_populates="characters",
    )


class Role(Base):
    __tablename__ = "roles"

    role_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    external_id: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    player_characters: Mapped[list["PlayerCharacter"]] = relationship(
        back_populates="role",
    )

    player_preferences: Mapped[list["PlayerRolePreference"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
    )


class PlayerRolePreference(Base):
    __tablename__ = "player_role_preferences"

    __table_args__ = (
        UniqueConstraint(
            "player_id",
            "role_id",
            name="uq_player_role_preference",
        ),
    )

    preference_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.player_id"),
        nullable=False,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.role_id"),
        nullable=False,
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    player: Mapped["Player"] = relationship(
        back_populates="role_preferences",
    )

    role: Mapped["Role"] = relationship(
        back_populates="player_preferences",
    )


# ==================================================
# ITEMS
# ==================================================

class ItemCategory(Base):
    __tablename__ = "item_categories"

    category_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    items: Mapped[list["Item"]] = relationship(
        back_populates="category",
    )


class Item(Base):
    __tablename__ = "items"

    item_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    external_id: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("item_categories.category_id"),
        nullable=True,
    )

    rarity: Mapped[str | None]

    sell_price: Mapped[int | None]

    energy: Mapped[int | None]

    category: Mapped["ItemCategory | None"] = relationship(
        back_populates="items",
    )

    recipe_links: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="item",
    )


# ==================================================
# RECIPES
# ==================================================

class Recipe(Base):
    __tablename__ = "recipes"

    recipe_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    external_id: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    category: Mapped[str | None]

    stars: Mapped[int | None]

    energy: Mapped[int | None]

    sell_price: Mapped[int | None]

    ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="recipe",
    )


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.recipe_id"),
        primary_key=True,
    )

    item_id: Mapped[int] = mapped_column(
        ForeignKey("items.item_id"),
        primary_key=True,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )

    recipe: Mapped["Recipe"] = relationship(
        back_populates="ingredients",
    )

    item: Mapped["Item"] = relationship(
        back_populates="recipe_links",
    )


# ==================================================
# DATA SOURCES
# ==================================================

class DataSource(Base):
    __tablename__ = "data_sources"

    source_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    url: Mapped[str | None]

    last_sync: Mapped[str | None]


# ==================================================
# PLAYER
# ==================================================

class Player(Base):
    __tablename__ = "players"

    player_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    username: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    friendship_strategy: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="balanced",
    )

    characters: Mapped[list["PlayerCharacter"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan",
    )

    role_preferences: Mapped[list["PlayerRolePreference"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan",
    )

    regions: Mapped[list["PlayerRegion"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan",
    )


class PlayerRegion(Base):
    __tablename__ = "player_regions"

    __table_args__ = (
        UniqueConstraint(
            "player_id",
            "region_id",
            name="uq_player_region",
        ),
    )

    player_region_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.player_id"),
        nullable=False,
    )

    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.region_id"),
        nullable=False,
    )

    unlocked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    player: Mapped["Player"] = relationship(
        back_populates="regions",
    )

    region: Mapped["Region"] = relationship(
        back_populates="player_progress",
    )


class PlayerCharacter(Base):
    __tablename__ = "player_characters"

    __table_args__ = (
        UniqueConstraint(
            "player_id",
            "character_id",
            name="uq_player_character",
        ),
    )

    player_character_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.player_id"),
        nullable=False,
    )

    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.character_id"),
        nullable=False,
    )

    unlocked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    friendship_level: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    assigned_role: Mapped[int | None] = mapped_column(
        ForeignKey("roles.role_id"),
        nullable=True,
    )

    player: Mapped["Player"] = relationship(
        back_populates="characters",
    )

    character: Mapped["Character"] = relationship(
        back_populates="player_progress",
    )

    role: Mapped["Role | None"] = relationship(
        back_populates="player_characters",
    )
    
class CharacterUnlockSource(Base):
    __tablename__ = "character_unlock_sources"

    unlock_source_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    source_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    external_id: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=True,
    )

    characters: Mapped[list["Character"]] = relationship(
        secondary="character_unlock_source_links",
        back_populates="unlock_sources",
    )


class CharacterUnlockSourceLink(Base):
    __tablename__ = "character_unlock_source_links"

    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.character_id"),
        primary_key=True,
    )

    unlock_source_id: Mapped[int] = mapped_column(
        ForeignKey("character_unlock_sources.unlock_source_id"),
        primary_key=True,
    )