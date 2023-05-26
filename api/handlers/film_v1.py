import uuid
from fastapi import APIRouter, Body, Depends
from api.responses.detail import DetailResponse
from api.dto.film import FilmCreatedResponse, CreateFilmBody
from api.repository.film.mongo import MongoFilmRepository
from api.repository.film.abstractions import FilmRepository
from api.entities.film import Film
from functools import lru_cache
from api.settings import Settings, settings_instance


router = APIRouter(prefix="/api/v1/films", tags=["films"])


@lru_cache
def film_repository(settings: Settings = Depends(settings_instance)):
    """
    Film repository instance to be used as FastAPI dependency
    Args:
        settings:

    Returns:

    """
    return MongoFilmRepository()


@router.post("/", status_code=201, response_model=FilmCreatedResponse)
async def post_create_film(
        film: CreateFilmBody = Body(..., title="film", description="The film details"),
        repo: FilmRepository = Depends(film_repository)
):
    """
    create a film

    Args:
        film:
        repo:

    Returns:

    """

    film_id = str(uuid.uuid4())

    await repo.create(
        film=Film(
            film_id=film_id,
            title=film.title,
            description=film.description,
            release_year=film.release_year,
            watched=film.watched
        )
    )
    return FilmCreatedResponse(id=film_id)
