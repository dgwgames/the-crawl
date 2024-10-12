from pydantic import BaseModel

class PlayerRegistration(BaseModel):
    name: str
