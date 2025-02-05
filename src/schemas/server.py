from pydantic import BaseModel, ConfigDict

class ServerBase(BaseModel):
    name: str
    host: str
    port: int
    username: str
    password: str


class ServerCreate(ServerBase):
    pass


class Server(ServerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
