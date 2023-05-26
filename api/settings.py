from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # general settings
    enable_metrics: bool = Field(
        True,
        title="Enable metrics",
        description="Expose prometheus metrics if set to True",
        env="ENABLE_METRICS"
    )

    # MongoDB settings
    mongo_connection_string: str = Field(
        "mongodb://localhost:27017",
        Title="MongoDB films connection string",
        env="MONGODB_CONNECTION_STRING"
    )
    mongo_database_name: str = Field(
        "film_track_db",
        title="MongoDB films database name",
        description="The database name for the mongoDB film database",
        env="MONGODB_DATABASE_NAME"
    )

    def __hash__(self) -> int:
        # NOTE - we are having to override `hash` function because `Settings`
        # class objects are un-hashable (as python core rule)
        return 1


@lru_cache()
def settings_instance():
    """
    NOTE - lru_Cache decoration saves time in IO operation
    lru cache will memorize object returned by the function.

    Returns:
        Settings class object will be used as FastAPI dependency
    """

    return Settings()
