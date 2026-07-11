from pydantic import BaseModel

class RequestModel(BaseModel):
    type: str
    action: str | None = None
    data: dict | None = None

