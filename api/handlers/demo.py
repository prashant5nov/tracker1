from fastapi import APIRouter, Body, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from api.responses.detail import DetailResponse


class NameIn(BaseModel):
    name: str
    prefix: str = "Mr. "


router = APIRouter()


@router.get("/hello-world", response_model=DetailResponse)
def hello_world():
    return DetailResponse(message="Hello World!!!")


##########################################################
# How to set query parameter for swagger?                #
##########################################################
@router.get("/hello", response_model=DetailResponse)
def send_data_query(name: str = Query(title="Name", description="Some name")):
    return DetailResponse(message=f"Hello {name}!!!")


##########################################################
# How to set Body parameter for swagger?                #
##########################################################
@router.post("/hello/name", response_model=DetailResponse)
def send_data_body(
    name: NameIn = Body(title="Body", description="The body of send data")
):
    """
    Response with `hello name`, where name is user provided from payload

    Args:
        name:

    Returns:

    """

    return DetailResponse(message=f"Hello {name.prefix}{name.name}")


##########################################################
# How to set PATH parameter for swagger?                #
##########################################################
@router.post("/hello/{name}", response_model=DetailResponse)
def send_data_body(name: str = Path(title="Name")):
    """
    TODO - refer
    https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/

    Args:
        name:

    Returns:

    """
    return DetailResponse(message=f"Hello...{name}")


@router.delete("/delete", response_model=DetailResponse)
def delete_data():
    return DetailResponse(message="data deleted")


@router.delete(
    "/delete/{name}",
    response_model=DetailResponse,
    responses={404: {"model": DetailResponse}},
)
def delete_data(name: str):
    if name == "admin":
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                DetailResponse(message="cannot delete admin data")
            ),
        )

    return DetailResponse(message=f"data deleted for {name}")
