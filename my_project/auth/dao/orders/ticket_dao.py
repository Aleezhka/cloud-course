from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain import Ticket

class TicketDAO(GeneralDAO):
    _domain_type = Ticket

    def find_by_user_id(self, user_id: int) -> List[object]:
        return self._session.query(Ticket).filter(Ticket.user_id == user_id).all()

    def find_by_flight_id(self, flight_id: int) -> List[object]:
        return self._session.query(Ticket).filter(Ticket.flight_id == flight_id).all()
