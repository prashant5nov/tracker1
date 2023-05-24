import typing

import motor.motor_asyncio

from api.entities.film import Film
from api.repository.film.abstractions import FilmRepository, RepositoryException


class MongoFilmRepository(FilmRepository):
    """
        MongoFilmRepository implements the repository pattern for
        our Film entity using MongoDB.


    TODO
    Refer - https://www.mongodb.com/docs/drivers/python/
    Refer - https://motor.readthedocs.io/en/stable/
    Refer - https://pypi.org/project/motor/
    Refer - https://motor.readthedocs.io/en/stable/
    """

    def __init__(self, connection_string: str = "mongodb://localhost:27017",
                 database: str = "film_track_db"):
        # TODO
        # refer -
        # https://motor.readthedocs.io/en/stable/tutorial-asyncio.html#creating-a-client
        self._client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
        self._database = self._client[database]
        # Film collection which holds our film documents.
        # https://motor.readthedocs.io/en/stable/tutorial-asyncio.html#getting-a-collection
        self._films = self._database["films"]

    async def create(self, film: Film):

        # We are using `update_one` function to avoid duplicates
        # `update_one` function performs upsert.
        # TODO
        # refer -
        # https://motor.readthedocs.io/en/stable/tutorial-asyncio.html#updating-documents
        await self._films.update_one(
            {"id": film.id},
            {
                "$set": {
                    "id": film.id,
                    "title": film.title,
                    "description": film.description,
                    "release_year": film.release_year,
                    "watched": film.watched,
                }
            },
            upsert=True,
        )

    async def get_by_id(self, film_id: str) -> typing.Optional[Film]:
        # TODO
        # refer
        # https://motor.readthedocs.io/en/stable/tutorial-asyncio.html#getting-a-single-document-with-find-one
        document = await self._films.find_one({"id": film_id})
        if document:
            return Film(
                film_id=document.get("id"),
                title=document.get("title"),
                description=document.get("description"),
                release_year=document.get("release_year"),
                watched=document.get("watched"),
            )
        return None

    async def get_by_title(
        self, title: str, skip: int = 0, limit: int = 1000
    ) -> typing.List[Film]:
        return_value: typing.List[Film] = []
        # Get cursor from db.
        documents_cursor = self._films.find({"title": title}).skip(skip).limit(limit)
        # Iterate though documents
        async for document in documents_cursor:
            return_value.append(
                Film(
                    film_id=document.get("id"),
                    title=document.get("title"),
                    description=document.get("description"),
                    release_year=document.get("release_year"),
                    watched=document.get("watched"),
                )
            )
        return return_value

    async def update(self, film_id: str, update_parameters: dict):
        if "id" in update_parameters.keys():
            raise RepositoryException("can't update film id.")
        result = await self._films.update_one(
            {"id": film_id}, {"$set": update_parameters}
        )
        if result.modified_count == 0:
            raise RepositoryException(f"film: {film_id} not updated")

    async def delete(self, film_id: str):
        await self._films.delete_one({"id": film_id})