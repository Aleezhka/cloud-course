from typing import List
from my_project.auth.dao import flight_dao
from my_project.auth.service.general_service import GeneralService


class FlightService(GeneralService):
    _dao = flight_dao

    def find_by_airline(self, airline_id: int) -> List[object]:
        return self._dao.find_by_airline(airline_id)

    def find_all(self) -> List[object]:
        return self._dao.find_all()

    def find_by_id(self, flight_id: int) -> object:
        return self._dao.find_by_id(flight_id)
