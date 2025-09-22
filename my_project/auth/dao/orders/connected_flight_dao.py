from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain import ConnectedFlight


class ConnectedFlightDAO(GeneralDAO):
    _domain_type = ConnectedFlight

    def find_all(self) -> List[ConnectedFlight]:
        return self._session.query(ConnectedFlight).all()

    def find_by_id(self, connected_flight_id: int) -> ConnectedFlight:
        return self._session.query(ConnectedFlight).filter(ConnectedFlight.id == connected_flight_id).first()

    def find_by_flight(self, flight_id: int) -> List[ConnectedFlight]:
        return self._session.query(ConnectedFlight).filter(ConnectedFlight.flight_id == flight_id).all()
