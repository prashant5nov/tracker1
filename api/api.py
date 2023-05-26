from fastapi import FastAPI
from api.handlers import demo, film_v1


def create_app():
    app = FastAPI(docs_url="/", redoc_url="/docs")
    app.include_router(demo.router)
    app.include_router(film_v1.router)
    return app

