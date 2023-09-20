from app.database.database_mongo import DatabaseMongo
from app.models.data_requests import PidValueRequest


class DeviceRepository:

    def __init__(self):
        pass

    def pids_status(self, device: str):

        db = DatabaseMongo.get_database()
        col = db["devices"]
        data = col.find(
            {
                "device.id": device,
            },
            {"pid": 1, "_id": 0})

        return data


    def pids_values(self, data_request: PidValueRequest) -> dict:

        from_timestamp = datetime.strptime(data_request.from_timestamp, "%Y-%m-%dT%H:%M:%S")
        to_timestamp = datetime.strptime(data_request.to_timestamp, "%Y-%m-%dT%H:%M:%S")

        db = DatabaseMongo.get_database()
        col = db["obd_events"]

        result = []

        for pid in data_request.pids:
            
            data = col.find(
            {
                "device.id": data_request.device,
                "$or": [{"pid.id": int(pid)}],
                "timestamps.server": {"$gte": from_timestamp, "$lte": to_timestamp}
            },
            {"pid": 1, "_id": 0}).sort("timestamps.acquisition", pymongo.ASCENDING)
        
            result.append(data)

        return json.loads(json_util.dumps(result))