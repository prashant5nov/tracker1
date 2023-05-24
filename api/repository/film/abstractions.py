import abc
import typing

from api.entities.film import Film


class RepositoryException(Exception):
    pass


class FilmRepository(abc.ABC):
    async def create(self, film: Film):
        """
        Inserts a film into the database.

        Raises RepositoryException of failure.
        """
        raise NotImplementedError

    async def get_by_id(self, film_id: str) -> typing.Optional[Film]:
        """
        Retrieves a Film by it's ID and if the film is not found it will return None.
        """
        raise NotImplementedError

    async def get_by_title(
        self, title: str, skip: int = 0, limit: int = 1000
    ) -> typing.List[Film]:
        """
        Returns a list of films which share the same title.
        """
        raise NotImplementedError

    async def update(self, film_id: str, update_parameters: dict):
        """
        Update a film by it's id.
        """
        raise NotImplementedError

    async def delete(self, film_id: str):
        """
        Deletes a film by it's id.

        Raises RepositoryException of failure.
        """
        raise NotImplementedError