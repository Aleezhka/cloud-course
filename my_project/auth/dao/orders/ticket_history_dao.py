from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain import TicketHistory

class TicketHistoryDAO(GeneralDAO):
    _domain_type = TicketHistory

    def find_by_ticket(self, ticket_id: int) -> List[TicketHistory]:
        return self._session.query(TicketHistory).filter(TicketHistory.ticket_id == ticket_id).all()
