from pydantic import BaseModel


class CharacterResponse(BaseModel):

    name: str

    species: str | None

    franchise: str | None

    unlocked: bool | None

    friendship_level: int | None

    role: str | None

    role_status: str