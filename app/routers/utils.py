from datetime import datetime
import pymongo
import json
from bson import json_util
from fastapi import APIRouter, Depends
from dependencies import get_token_header
from database.database_mongo import DatabaseMongo
from models.data_request import DataRequest

router = APIRouter(
    prefix="/api/v1/utils",
    tags=["Utils"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/device_data")
async def trip(data_request: DataRequest):
    from_timestamp = datetime.strptime(data_request.from_timestamp, "%Y-%m-%dT%H:%M:%S")
    to_timestamp = datetime.strptime(data_request.to_timestamp, "%Y-%m-%dT%H:%M:%S")

    db = DatabaseMongo.get_database()
    col = db["obd_events"]
    data = col.find(
        {
            "device.id": data_request.device,
            "timestamps.acquisition": {"$gte": from_timestamp, "$lte": to_timestamp}
        },
        {"pid": 1, "_id": 1}).sort("timestamps.acquisition", pymongo.ASCENDING)

    return json.loads(json_util.dumps(data))