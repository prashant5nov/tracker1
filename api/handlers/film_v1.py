from fastapi import APIRouter, Body
from api.responses.detail import DetailResponse
from api.repository.film.mongo import MongoFilmRepository


router = APIRouter(prefix="/api/v1/films", tags=["films"])


# @router.post("/", status_code=201, response_model=DetailResponse):
# async def post_create_film(
#         film: Body(..., title="Film", description="the film details"),
#         repo: MongoFilmRepository = Depends(film_repository),
# )