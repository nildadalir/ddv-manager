from pydantic import BaseModel


class RolePreferenceItem(BaseModel):
    role_id: int
    priority: int


class RolePreferenceUpdate(BaseModel):
    preferences: list[RolePreferenceItem]


class RolePreferenceResponse(BaseModel):
    role_id: int
    role: str
    priority: int