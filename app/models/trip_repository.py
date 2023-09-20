import json
from datetime import datetime
import pymongo
from bson import json_util
from database.database_mongo import DatabaseMongo
from models.data_request import DataRequest


class TripRepository:

    def get_kms_data(self, data_request: DataRequest) -> dict:

        from_timestamp = datetime.strptime(data_request.from_timestamp, "%Y-%m-%dT%H:%M:%S")
        to_timestamp = datetime.strptime(data_request.to_timestamp, "%Y-%m-%dT%H:%M:%S")

        db = DatabaseMongo.get_database()



        col = db["obd_events"]
        data = col.find(
            {
                "device.id": data_request.device,
                "$or": [{"pid.id": 241}, {"$and": [{"pid.id": -1}, {"vehicle.status": 0}]}],
                "timestamps.acquisition": {"$gte": from_timestamp, "$lte": to_timestamp}
            },
            {"pid": 1, "_id": 0}).sort("timestamps.acquisition", pymongo.ASCENDING)

        return json.loads(json_util.dumps(data))

    def trip_kms_as_array(self, kms: dict) -> list:
        data = []

        for element in kms:
            km = element["pid"].get("value", -1)
            if km == "":
                km = -1
            data.append(km)

        return data
