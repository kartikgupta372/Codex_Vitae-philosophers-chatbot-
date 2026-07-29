from pydantic import BaseModel, Field


class PingRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)


class PingResponse(BaseModel):
    id: str
    message: str
    reply: str
