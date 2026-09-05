from pydantic import BaseModel


class RoleCharacterResponse(BaseModel):
    name: str
    friendship_level: int | None
    unlocked: bool | None


class ActivityRoleResponse(BaseModel):
    role_id: int
    role: str

    assigned_count: int
    assigned_characters: list[RoleCharacterResponse]

    no_role_count: int
    unknown_count: int