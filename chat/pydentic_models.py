from pydantic import BaseModel


class ChannelsMessage(BaseModel):
    event: str
    data: dict
