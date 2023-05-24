class Film:
    def __init__(
            self,
            *,
            film_id: str,
            title: str,
            description: str,
            release_year: str,
            watched: bool = False
    ):
        """

        Args:
            film_id: str
                The film UUID represented by a string
            title: str
                The film title
            description: str
                The film description in brief
            release_year: int
                The release year of the film
            watched: bool
                Boolean that indicates if the film has been watched already.
        """

        if film_id is None:
            raise ValueError("film id is required")
        self._id = film_id
        self._title = title
        self._description = description
        self._release_year = release_year
        self._watched = watched

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def release_year(self) -> str:
        return self._release_year

    @property
    def watched(self) -> str:
        return self._watched


if __name__ == "__main__":
    film = Film(
        film_id="random film_id",
        title="random title",
        description="random description",
        release_year="random release_year",
        watched=True
    )
    breakpoint()