from pydantic import BaseModel


class DetailResponse(BaseModel):
    """
    DetailResponse represents a response with a detailed message
    """

    message: str
