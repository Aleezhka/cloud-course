from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain import Flight

class FlightDAO(GeneralDAO):
    _domain_type = Flight

    def find_by_airline(self, airline_id: int) -> List[Flight]:
        return self._session.query(Flight).filter(Flight.airline_id == airline_id).all()

    def find_all(self) -> List[Flight]:
        return self._session.query(Flight).all()

    def find_by_id(self, flight_id: int) -> Flight:
        return self._session.query(Flight).filter(Flight.id == flight_id).first()
