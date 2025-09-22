from typing import List
from my_project.auth.dao import TicketDAO
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain import Ticket


class TicketService(GeneralService):
    _dao = TicketDAO()

    def get_tickets_by_user_id(self, user_id: int) -> List[Ticket]:
        return self._dao.find_by_user_id(user_id)

    def get_tickets_by_flight_id(self, flight_id: int) -> List[Ticket]:
        return self._dao.find_by_flight_id(flight_id)

    def get_tickets_by_user(self, user_id: int):
        return Ticket.query.filter_by(user_id=user_id).all()

