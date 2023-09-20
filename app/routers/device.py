import json
from bson import json_util
from datetime import datetime
from fastapi import APIRouter, Depends
from dependencies import get_token_header
from database.database_mongo import DatabaseMongo
from models.device import PidConfiguration
import paho.mqtt.client as paho
from idp import OIDCUser, idp
from models.data_request import PidValueRequest
import pymongo
import random


router = APIRouter(
    prefix="/device",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


def pids_data(device: str):
    """

    Parameters
    -------
    device: str
        Device id

    Returns
    -------
        dict

    """

    db = DatabaseMongo.get_database()
    col = db["devices"]
    data = col.find_one(
        {"device": str(device)}, {"_id": 0, "pids_available": 1, "pids_enabled": 1}
    )
    result = json.loads(json_util.dumps(data))
    supported = result["pids_available"]
    enabled = result.get("pids_enabled", "")
    if len(enabled) < len(supported):
        enabled = "0" * len(supported)
    return {"supported": supported, "enabled": enabled}


def pids_status(data: dict) -> list:
    pids_status = []
    for idx, value in enumerate(data["supported"]):
        pid_id = str(hex(idx + 1)).replace("0x", "").rjust(2, "0").upper()
        supported = int(value)
        description = ""
        enabled = int(data["enabled"][idx])
        pid = {"pidId": pid_id, "description": description, "supported": supported, "enabled": enabled}
        pids_status.append(pid)
    return pids_status


def is_supported(pids_supported: str, pid_id: int):
    state = pids_supported[pid_id - 1]
    if state == "1":
        return True
    return False


def replacer(s, newstring, index, nofail=False):
    index = index - 1
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")
    if index < 0:
        return newstring + s
    if index > len(s):
        return s + newstring
    return s[:index] + newstring + s[index + 1:]


def pid_binstring_to_hexstring(binstring: str) -> str:
    result = ""
    chunks = [binstring[i:i+4] for i in range(0, len(binstring), 4)]
    for chunk in chunks:
        result += hex(int(chunk, 2)).replace("0x", "")
    return result


def store_setting(device, configutation):
    db = DatabaseMongo.get_database()
    col = db["devices"]
    col.update_one({"device": device}, {"$set": {"pids_enabled": configutation}}, True)


def publish_setting(device, configutation):
    """
    Pubblica le impostazioni dei pid del device
    :param device:
    :param configutation:
    :return:
    """
    client = paho.Client("obd-mqtt-client")
    client.username_pw_set("sensorid","S3n5or.1D@Mqtt!")
    client.connect("mqtt.sensorid.it", 1883, 60)
    val = random.randint(0, 999)
    val_str = str(val).rjust(3, "0")
    ret = client.publish(f"O/{device}/CNF/P", f"{val_str}|{configutation}", retain=True)


@router.get("/{device}/pid/status")
async def get_pid_status(device: str, user: OIDCUser = Depends(idp.get_current_user())):
    p_data: dict = pids_data(device)
    p_status: list = pids_status(p_data)
    return p_status


@router.put("/{device}/pid/status")
async def put_pid_status(device: str, configuration: list[PidConfiguration], user: OIDCUser = Depends(idp.get_current_user())):
    p_data: dict = pids_data(device)
    p_enabled: str = p_data["enabled"]

    for pid in configuration:
        pid_id = int(f"0x{pid.pid_id}", base=16)
        pid_val = pid.enable

        if not is_supported(p_data["supported"], pid_id):
            return {"risposta": f"The pid {pid.pid_id} is not supported!"}  # TODO: Modificare il messaggio di risposta
        p_enabled = replacer(p_enabled, str(pid_val), pid_id)

    hexstring = pid_binstring_to_hexstring(p_enabled)
    store_setting(device, p_enabled)  # TODO: Da implementare
    publish_setting(device, hexstring)  # TODO: Da implementare
    return {"risposta": hexstring}  # TODO: Modificare il messaggio di risposta



@router.post("/pid/values")
async def get_pid_values(data_request: PidValueRequest, user: OIDCUser = Depends(idp.get_current_user())) -> list:
    db = DatabaseMongo.get_database()

    col = db["obd_events"]
    result = []

    from_timestamp = datetime.strptime(data_request.from_timestamp, "%Y-%m-%dT%H:%M:%S")
    to_timestamp = datetime.strptime(data_request.to_timestamp, "%Y-%m-%dT%H:%M:%S")

    result.append(data_request.device)

    data = col.find({
        "device.id": data_request.device,
        "pid.id": {"$in": data_request.pids},
        "timestamps.acquisition": {"$gte": from_timestamp, "$lte": to_timestamp}
    },
        {"_id": 0, "type": 0, "vehicle": 0, "device": 0, "mqtt": 0, "coordinates": 0}).sort("timestamps.acquisition",
                                                                                            pymongo.ASCENDING)

    result = json.loads(json_util.dumps(data))
    return result
