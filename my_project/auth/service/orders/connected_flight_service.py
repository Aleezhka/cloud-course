from typing import List
from my_project.auth.dao import connected_flight_dao
from my_project.auth.service.general_service import GeneralService


class ConnectedFlightService(GeneralService):
    _dao = connected_flight_dao

    def find_all(self) -> List[object]:
        return self._dao.find_all()

    def find_by_id(self, connected_flight_id: int) -> object:
        return self._dao.find_by_id(connected_flight_id)

    def find_by_flight(self, flight_id: int) -> List[object]:
        return self._dao.find_by_flight(flight_id)
