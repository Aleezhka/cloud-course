from typing import List
from my_project.auth.service import flight_service
from my_project.auth.controller.general_controller import GeneralController


class FlightController(GeneralController):
    _service = flight_service

    def get_flights_by_airline(self, airline_id: int) -> List[object]:
        return list(map(lambda x: dict(x), self._service.find_by_airline(airline_id)))

    def get_all_flights(self) -> List[object]:
        return list(map(lambda flight: flight.put_into_dto(), self._service.find_all()))

    def find_flight_by_id(self, flight_id):
        flight = self._service.find_by_id(flight_id)
        return flight.put_into_dto() if flight else None
