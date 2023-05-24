import typing

from api.entities.film import Film
from api.repository.film.abstractions import FilmRepository, RepositoryException


class MemoryFilmRepository(FilmRepository):
    """
    MemoryFilmRepository implements the repository pattern by using a
    simple in memory database.
    """

    def __init__(self):
        # in-memory database
        self._storage = {}

    async def create(self, film: Film):
        self._storage[film.id] = film

    async def get_by_id(self, film_id: str) -> typing.Optional[Film]:
        return self._storage.get(film_id)

    async def get_by_title(
        self, title: str, skip: int = 0, limit: int = 1000
    ) -> typing.List[Film]:
        return_value = []
        for _, value in self._storage.items():
            if title == value.title:
                return_value.append(value)
        if limit == 0:
            return return_value[skip:]
        return return_value[skip: skip + limit]

    async def update(self, film_id: str, update_parameters: dict):
        film = self._storage.get(film_id)
        if film is None:
            raise RepositoryException(f"film: {film_id} not found")
        for key, value in update_parameters.items():
            if key == "id":
                raise RepositoryException(f"can't update film id.")
            # Check that update_parameters are fields from Film entity.
            if hasattr(film, key):
                # Update the Film entity field.
                setattr(film, f"_{key}", value)

    async def delete(self, film_id: str):
        self._storage.pop(film_id, None)