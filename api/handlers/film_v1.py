import uuid
import typing
from fastapi import APIRouter, Body, Query, Path, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from api.responses.detail import DetailResponse
from api.dto.film import (
    FilmCreatedResponse,
    CreateFilmBody,
    FilmResponse,
    FilmUpdateBody
)
from api.repository.film.mongo import MongoFilmRepository, RepositoryException
from api.repository.film.abstractions import FilmRepository
from api.entities.film import Film
from functools import lru_cache
from api.settings import Settings, settings_instance


http_basic = HTTPBasic()


def basic_authentication(
        credentials: HTTPBasicCredentials = Depends(http_basic)
):
    """
    
    # TODO refer
    https://fastapi.tiangolo.com/lo/advanced/security/http-basic-auth/#http-basic-auth
    
    Args:
        credentials: 

    Returns:

    """

    if (
            credentials.username == "prashant"
            and
            credentials.password == "password@321"
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password (bad credentials)"
    )


router = APIRouter(
    prefix="/api/v1/films",
    tags=["films"],
    dependencies=[Depends(basic_authentication)])


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


@router.get(
    "/{film_id}",
    responses={200: {"model": FilmResponse}, 404: {"model": DetailResponse}},
)
async def get_film_by_id(
        film_id: str,
        repo: FilmRepository = Depends(film_repository)
):
    """
    Returns a film if found, None otherwise.

    Args:
        film_id:
        repo:

    Returns:

    """

    film = await repo.get_by_id(film_id=film_id)
    if film is None:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                DetailResponse(message=f"film with id - `{film_id}` not found.")
            ),
        )
    return FilmResponse(
        id=film.id,
        title=film.title,
        description=film.description,
        release_year=film.release_year,
        watched=film.watched,
    )


@router.get(
    "/", response_model=typing.List[FilmResponse]
)
async def get_film_by_title(
        title: str = Query(
            title="Title",
            description="The title of the film",
            min_length=3
        ),
        repo: FilmRepository = Depends(film_repository)
):
    """

    This view/ handler returns films by filtering their titles

    Args:
        title:
        repo:

    Returns:

    """

    films = await repo.get_by_title(title)
    film_return_value = []

    for film in films:
        film_return_value.append(
            FilmResponse(
                id=film.id,
                title=film.title,
                description=film.description,
                release_year=film.release_year,
                watched=film.watched,
            )
        )
    return film_return_value


@router.patch(
    "/{film_id}",
    responses={
        200: {"model": DetailResponse},
        400: {"model": DetailResponse},
    }
)
async def patch_update_film(
        film_id: str = Path(title="Film ID", description="The id of the film"),
        update_parameters: FilmUpdateBody = Body(
            ...,
            title="Update Body",
            description="The parameters of the film to be updated"
        ),
        repo: FilmRepository = Depends(film_repository)
):
    """
    Updates a film record against certain film_id.

    Args:
        film_id:
        update_parameters:
        repo:

    Returns:

    """

    try:
        await repo.update(
            film_id=film_id,
            update_parameters=update_parameters.dict()
        )
        return DetailResponse(message="Film has been updated.")
    except RepositoryException as e:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(DetailResponse(message=str(e)))
        )


@router.delete(
    "/{film_id}",
    status_code=204
)
async def delete_film(
        film_id: str = Path(..., title="Film ID",
                            desription="The ID of the film"),
        repo: FilmRepository = Depends(film_repository)
):

    await repo.delete(film_id=film_id)
    return Response(status_code=204)
