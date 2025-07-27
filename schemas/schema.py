from pydantic import BaseModel


class MessageSchema(BaseModel):
    data: str
