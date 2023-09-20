import json
from datetime import datetime
import pymongo
from bson import json_util
from database.database_mongo import DatabaseMongo
from models.data_request import DataRequest

class ConsumptionRepository:


    def get_consumption_data(self, data_request: DataRequest) -> dict:

        print("get_consumption_data")
        print(f"{data_request=}")

        from_timestamp = datetime.strptime(data_request.from_timestamp, "%Y-%m-%dT%H:%M:%S")
        to_timestamp = datetime.strptime(data_request.to_timestamp, "%Y-%m-%dT%H:%M:%S")

        db = DatabaseMongo.get_database()
        print(f"{db=}")

        col = db["obd_events"]
        data = col.find(
            {
                "device.id": data_request.device,
                "$or": [{"pid.id": 240}, {"$and": [{"pid.id": -1}, {"vehicle.status": 0}]}],
                "timestamps.acquisition": {"$gte": from_timestamp, "$lte": to_timestamp}
            },
            {"pid": 1, "_id": 0}).sort("timestamps.acquisition", pymongo.ASCENDING)


        data_dumps = json_util.dumps(data)
        print(f"{data_dumps=}")
        data_loads = json.loads(data_dumps)
        print(f"{data_loads=}")
        return data_loads