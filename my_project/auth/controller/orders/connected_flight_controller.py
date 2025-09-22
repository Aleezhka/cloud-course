from typing import List
from my_project.auth.service import connected_flight_service
from my_project.auth.controller.general_controller import GeneralController

class ConnectedFlightController(GeneralController):
    _service = connected_flight_service

    def get_all_connected_flights(self) -> List[object]:
        return list(map(lambda x: x.put_into_dto(), self._service.find_all()))

    def find_connected_flight_by_id(self, connected_flight_id: int) -> object:
        connected_flight = self._service.find_by_id(connected_flight_id)
        return connected_flight.put_into_dto() if connected_flight else None

    def get_connected_flights_for_flight(self, flight_id: int) -> List[object]:
        return list(map(lambda x: x.put_into_dto(), self._service.find_by_flight(flight_id)))
