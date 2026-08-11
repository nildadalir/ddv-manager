from pydantic import BaseModel


class CharacterResponse(BaseModel):
    name: str
    species: str | None
    franchise: str | None