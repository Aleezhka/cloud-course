from typing import List
from my_project.auth.service import TicketService
from my_project.auth.controller.general_controller import GeneralController

class TicketController(GeneralController):
    _service = TicketService()

    def get_tickets_by_user_id(self, user_id: int) -> List[dict]:
        tickets = self._service.get_tickets_by_user_id(user_id)
        return [ticket.put_into_dto() for ticket in tickets]

    def get_tickets_by_flight_id(self, flight_id: int) -> List[object]:
        return list(map(lambda x: dict(x), self._service.get_tickets_by_flight_id(flight_id)))

    def get_tickets_by_user_id(self, user_id: int):
        tickets = self._service.get_tickets_by_user(user_id)
        return [ticket.put_into_dto() for ticket in tickets]
