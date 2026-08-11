from pydantic import BaseModel


class PlayerCharacterResponse(BaseModel):
    name: str
    unlocked: bool
    friendship_level: int
    role: str | None


class PlayerResponse(BaseModel):
    username: str
    characters: list[PlayerCharacterResponse]