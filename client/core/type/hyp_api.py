from pydantic import BaseModel



class Response[DataType](BaseModel):
    retcode: int
    message: str
    data: DataType
