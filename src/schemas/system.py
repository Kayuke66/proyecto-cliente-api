from pydantic import BaseModel


class VersionResponseDto(BaseModel):
    name: str
    version: str
    build: str