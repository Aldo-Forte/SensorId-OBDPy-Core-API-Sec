from pydantic import BaseModel


class DataRequest(BaseModel):
    device: str
    from_timestamp: str
    to_timestamp: str


class PidValueRequest(BaseModel):
    device: str
    pids: list
    from_timestamp: str
    to_timestamp: str