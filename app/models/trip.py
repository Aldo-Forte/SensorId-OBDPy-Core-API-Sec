from models.data_request import DataRequest
from models.trip_repository import TripRepository


class Trip:

    def __init__(self):
        self.__tracks = []

    def get_distance(self, data_request: DataRequest):
        trip_repository = TripRepository()
        trip_data: dict = trip_repository.get_kms_data(data_request)
        trip_data_array: list = self.as_array(trip_data)
        trip_data_split: list = self.split(trip_data_array)
        return self.trip_km()


    def as_array(self, trip_data: dict) -> list:
        data = []

        for element in trip_data:
            km = element["pid"].get("value", -1)
            if km == "":
                km = -1
            data.append(km)

        return data

    def split(self, data: list) -> None:
        track = []
        for i, v in enumerate(data):
            if v != -1:
                track.append(v)
            else:
                self.__tracks.append(track)
                track = []

        return self.__tracks

    def add_track(self, track:list):
        self.__tracks.append(track)

    def trips(self):
        return len(self.__tracks)

    def trip_km(self):
        km = 0.0

        for t in self.__tracks:
            if len(t) <= 1:
                km += 0.0
                continue

            km += t[len(t) - 1] -t[0]

        return km

