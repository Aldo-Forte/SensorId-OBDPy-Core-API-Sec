from pydantic import BaseModel


class Device:

    def __init__(self, device_id: str):
        self.device_id = device_id


class PidConfiguration(BaseModel):
        pid_id : str
        enable: int

