from pydantic import BaseModel


class PlayerCharacterResponse(BaseModel):
    name: str
    unlocked: bool
    friendship_level: int
    role: str | None


class PlayerResponse(BaseModel):
    username: str
    characters: list[PlayerCharacterResponse]


class PlayerCharacterCreate(BaseModel):
    character_id: int
    unlocked: bool = True
    friendship_level: int = 0
    role_id: int | None = None
    
class PlayerCharacterUpdate(BaseModel):
    unlocked: bool | None = None
    friendship_level: int | None = None
    role_id: int | None = None