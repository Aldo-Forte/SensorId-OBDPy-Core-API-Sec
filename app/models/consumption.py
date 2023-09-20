from models.consumption_repository import ConsumptionRepository
from models.data_request import DataRequest
from models.trip import Trip
from models.trip_repository import TripRepository


class Consumption:

    def __init__(self):
        self.__tracks = []

    def __sum_array(self, array_data: list) -> float:
        arr_sum = 0.0
        for i in range(0, len(array_data)):
            arr_sum += array_data[i];
        return arr_sum

    def __trip_distance(self, array_data: list) -> float:

        result = 0.0
        print(f"{array_data=}")

        try:
            result = array_data[len(array_data) - 1] - array_data[0]
        except Exception as ex:
            print(f"__trip_distance error: {str(ex)}")
            return result

        print(f"__trip_distance result: {result}")
        return result

    def __trip_consumption(self, trip_distance: float, trip_consumption: float):
        return trip_distance / trip_consumption

    def __mean_array(self, array_data: list):
        s = self.__sum_array(array_data)
        return s / len(array_data)

    def __consumption_calculation(self, trip_data: list, consumption_data: list, debug=False) -> float:
        """

        :param trip_data:
        :param consumption_data:
        :return:
        """

        len_trip = len(trip_data)
        len_cons = len(consumption_data)

        if debug:
            print(f"{trip_data=}")
            print(f"{consumption_data=}")
            print(f"{len_trip=}")
            print(f"{len_cons=}")


        if len_trip != len_cons:
            return 0

        average_consumption_trips = []
        km_trip = []

        for i in range(0, len_cons):

            distance = self.__trip_distance(trip_data[i])

            if debug:
                print(f"{i=}")
                print(f"{distance=}")

            km_trip.append(distance)

            last_consumption_mean = consumption_data[i][-1] if consumption_data[i] != [] else 0.0

            if debug:
                print(f"{last_consumption_mean=}")

            average_consumption_trips.append(distance*last_consumption_mean)

        sum_km_x_cons = self.__sum_array(average_consumption_trips)
        print(f"{sum_km_x_cons=}")
        sum_km = self.__sum_array(km_trip)
        print(f"{sum_km=}")
        result = sum_km_x_cons / sum_km
        print(f"{result=}")

        return result

    def get_consumption(self, data_request: DataRequest):

        consumption_repository = ConsumptionRepository()
        consumption_data: dict = consumption_repository.get_consumption_data(data_request)
        print(f"{consumption_data=}")
        consumption_data_array: list = self.as_array(consumption_data)
        print(f"{consumption_data_array=}")
        splited_consumption_data = self.split(consumption_data_array)
        print(f"{splited_consumption_data=}")

        trip_repository = TripRepository()
        trip_data: dict = trip_repository.get_kms_data(data_request)
        trip = Trip()
        trip_data_array = trip.as_array(trip_data)
        splitted_trip_data = trip.split(trip_data_array)

        result = self.__consumption_calculation(splitted_trip_data, splited_consumption_data, debug=True)
        return result

    def as_array(self, consumptions: dict) -> list:
        data = []

        for element in consumptions:
            print(f"{element=}")
            consumption = element["pid"].get("value", -1)
            if consumption == "":
                consumption = -1
            data.append(consumption)

        return data

    def split(self, data: list) -> list:
        track = []

        for i, v in enumerate(data):
            if v == 0.0:
                continue
            if v == -1:
                self.__tracks.append(track)
                track = []
            else:
                track.append(v)

        print("SPLIT OK")
        return self.__tracks
