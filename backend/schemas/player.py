from pydantic import BaseModel


class PlayerCharacterResponse(BaseModel):
    name: str
    unlocked: bool
    friendship_level: int
    role: str | None


class PlayerResponse(BaseModel):
    username: str
    characters: list[PlayerCharacterResponse]


class PlayerSummaryResponse(BaseModel):
    username: str
    total_characters: int
    unlocked_characters: int
    max_friendship_characters: int
    assigned_roles: list[dict]
    missing_roles: list[str]


class PlayerCharacterCreate(BaseModel):
    character_id: int
    unlocked: bool = True
    friendship_level: int = 0
    role_id: int | None = None


class PlayerCharacterUpdate(BaseModel):
    unlocked: bool | None = None
    friendship_level: int | None = None
    role_id: int | None = None
    
class PlayerRecommendationResponse(BaseModel):
    type: str
    priority: str
    character: str | None = None
    reason: str
    
class PlayerPreferenceUpdate(BaseModel):
    friendship_strategy: str