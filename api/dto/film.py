import typing
from pydantic import BaseModel, validator


class CreateFilmBody(BaseModel):
    """
    CreateFilmBody is used as the body for the create film endpoint
    """

    title: str
    description: str
    release_year: int
    watched: bool = False

    @validator("title")
    def title_length_gt_three(cls, v):
        if len(v) < 4:
            raise ValueError("Title's length must be greater than 3 characters")
        return v

    @validator("description")
    def description_length_gt_three(cls, v):
        if len(v) < 4:
            raise ValueError(
                "Description length must be greater than 3 characters"
                "")
        return v

    @validator("release_year")
    def release_year_gt_1900(cls, v):
        if v < 1900:
            raise ValueError("release years must be greater than 1900")
        return v


class FilmCreatedResponse(BaseModel):
    id: str


class FilmResponse(FilmCreatedResponse):
    title: str
    description: str
    release_year: int
    watched: bool


class FilmUpdateBody(BaseModel):
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    release_year: typing.Optional[int] = None
    watched: typing.Optional[bool] = None
